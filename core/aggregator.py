#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sources Aggregator Module
Fetches and merges configs from histeenn/VLESS-PO-GRIBI and upstream mirrors.
"""

import os
import sys
import json
import time
import urllib.request
from typing import List, Tuple, Dict, Any, Optional
from core.parser import ProxyNode, parse_configs_from_text

BASE_REPO_URL = "https://raw.githubusercontent.com/histeenn/VLESS-PO-GRIBI/main/deploy"
MAIN_SUB_URL = f"{BASE_REPO_URL}/sub.txt"

# Priority Russian Whitelist Sources from desktop vpn.txt & sort_needed.txt
EXTRA_WHITELIST_SOURCES = [
    ("https://raw.githubusercontent.com/Sanuyyq/sub-storage1/refs/heads/main/bs.txt", "BS-Storage"),
    ("https://raw.githubusercontent.com/ByeWhiteLists/ByeWhiteLists2/refs/heads/main/ByeWhiteLists2.txt", "ByeWhiteLists"),
    ("https://raw.githubusercontent.com/SilentGhostCodes/WhiteListVpn/refs/heads/main/Whitelist.txt", "SilentGhost-1"),
    ("https://raw.githubusercontent.com/SilentGhostCodes/WhiteListVpn/refs/heads/main/Whitelist%20%E2%84%962.txt", "SilentGhost-2"),
    ("https://raw.githubusercontent.com/zieng2/wl/main/vless_universal.txt", "Zieng-WL"),
    ("https://raw.githubusercontent.com/ewecrow78-gif/whitelist1/main/list.txt", "Ewecrow-WL"),
    ("https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-checked.txt", "Igareck-White"),
    ("https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS_mobile.txt", "Igareck-Mobile"),
    ("https://raw.githubusercontent.com/CidVpn/cid-vpn-config/refs/heads/main/general.txt", "CidVPN-General"),
    ("https://raw.githubusercontent.com/VansFenix/WildVF-/refs/heads/main/VansFenix%231", "VansFenix"),
    ("https://raw.githubusercontent.com/Ai123999/5Frid/refs/heads/main/5Frid_Notorgamers", "5Frid-Gamers"),
    ("https://gitverse.ru/api/repos/cid-uskoritel/cid-white/raw/branch/master/whitelist.txt", "Gitverse-CidWhite"),
    ("https://gitverse.ru/api/repos/flaafix/AetrisVPN/raw/branch/master/AetrisVPN.txt", "Gitverse-Aetris"),
]

PRIORITY_SOURCES = [4, 7, 9, 18, 24]

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


class ConfigAggregator:
    def __init__(self, data_dir: str = DATA_DIR):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.cached_file = os.path.join(self.data_dir, "raw_servers.txt")
        self.meta_file = os.path.join(self.data_dir, "meta.json")

    def fetch_url(self, url: str, timeout: int = 10) -> str:
        """Fetches text content from URL with custom User-Agent."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status == 200:
                    return resp.read().decode("utf-8", errors="ignore")
        except Exception as e:
            pass
        return ""

    def load_cached(self) -> List[ProxyNode]:
        """Loads cached nodes from disk if available."""
        if os.path.exists(self.cached_file):
            try:
                with open(self.cached_file, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                return parse_configs_from_text(content)
            except Exception:
                pass
        return []

    def aggregate(self, fetch_all_sources: bool = True, max_servers: Optional[int] = None) -> List[ProxyNode]:
        """
        Pulls from histeenn/VLESS-PO-GRIBI main sub.txt and all individual subscription sources.
        """
        all_nodes: List[ProxyNode] = []
        seen_keys = set()

        def add_nodes(nodes: List[ProxyNode]):
            for n in nodes:
                key = f"{n.protocol}://{n.uuid}@{n.host}:{n.port}"
                if key not in seen_keys:
                    seen_keys.add(key)
                    all_nodes.append(n)

        # 1. Fetch main sub.txt
        print("[*] Загрузка основного файла sub.txt из VLESS-PO-GRIBI...")
        main_text = self.fetch_url(MAIN_SUB_URL, timeout=12)
        if main_text:
            nodes = parse_configs_from_text(main_text)
            print(f"    -> Загружено {len(nodes)} конфигураций из sub.txt")
            add_nodes(nodes)
        else:
            print("    [!] Не удалось загрузить sub.txt онлайн, проверяем локальный кэш...")
            cached = self.load_cached()
            if cached:
                print(f"    -> Восстановлено {len(cached)} конфигураций из кэша")
                add_nodes(cached)

        # 2. Fetch specific priority whitelist sources from VLESS-PO-GRIBI
        print("[*] Загрузка специализированных Whitelist / Обход источников (4, 7, 9, 18, 24)...")
        for src_id in PRIORITY_SOURCES:
            src_url = f"{BASE_REPO_URL}/subscriptions/{src_id}.txt"
            txt = self.fetch_url(src_url, timeout=8)
            if txt:
                nodes = parse_configs_from_text(txt, default_source_id=src_id)
                print(f"    -> Источник #{src_id}: найдено {len(nodes)} серверов")
                add_nodes(nodes)

        # 3. Fetch extra verified Russian Whitelist sources from desktop
        print("[*] Загрузка дополнительных Whitelist источников из файлов впн.txt и отсортировать надо.txt...")
        for src_url, label in EXTRA_WHITELIST_SOURCES:
            txt = self.fetch_url(src_url, timeout=6)
            if txt:
                nodes = parse_configs_from_text(txt)
                for n in nodes:
                    n.is_whitelist = True
                    if not n.whitelist_label:
                        n.whitelist_label = "🛡️ " + label
                print(f"    -> {label}: получено {len(nodes)} конфигов обхода")
                add_nodes(nodes)
            if max_servers and len(all_nodes) >= max_servers:
                break

        # 3. Optionally fetch remaining sources (1 to 25)
        if fetch_all_sources and (max_servers is None or len(all_nodes) < max_servers):
            print("[*] Проверка дополнительных источников 1..25...")
            for src_id in range(1, 26):
                if src_id in PRIORITY_SOURCES:
                    continue
                src_url = f"{BASE_REPO_URL}/subscriptions/{src_id}.txt"
                txt = self.fetch_url(src_url, timeout=5)
                if txt:
                    nodes = parse_configs_from_text(txt, default_source_id=src_id)
                    add_nodes(nodes)
                if max_servers and len(all_nodes) >= max_servers:
                    break

        # Save to disk cache
        if all_nodes:
            try:
                with open(self.cached_file, "w", encoding="utf-8") as f:
                    f.write("\n".join(n.raw_url for n in all_nodes))
                with open(self.meta_file, "w", encoding="utf-8") as f:
                    json.dump({
                        "total_aggregated": len(all_nodes),
                        "timestamp": time.time(),
                        "time_str": time.strftime("%Y-%m-%d %H:%M:%S")
                    }, f, indent=2)
            except Exception:
                pass

        if max_servers:
            all_nodes = all_nodes[:max_servers]

        print(f"[+] Всего собрано уникальных серверов: {len(all_nodes)}")
        return all_nodes
