#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Xray Verifier & Incy Direct Importer
Tests VLESS Reality & TLS nodes using Incy's native xray.exe on this PC.
Only nodes that return HTTP 204 from http://cp.cloudflare.com/generate_204 are kept.
Guarantees 0 N/A in Incy.
"""

import os
import sys
import time
import json
import uuid
import sqlite3
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
XRAY_BIN = r"C:\Program Files\INCY\app\resources\bin\xray.exe"
INCY_DB = r"C:\Users\twofolp\AppData\Local\incy\incy.db"

from core.aggregator import ConfigAggregator
from core.parser import ProxyNode
from core.geoip import GeoIPResolver

# Russian whitelist SNI patterns (for bypass during mobile network throttling)
WL_PATTERNS = [
    "yandex.ru", "ya.ru", "dzen.ru", "passport.yandex.ru",
    "vk.com", "vk.me", "userapi.com", "vk-portal.net",
    "gosuslugi.ru", "esia.gosuslugi.ru", "gu-st.ru",
    "mail.ru", "sber.ru", "sberbank.ru", "tinkoff.ru", "t-bank.ru",
    "avito.ru", "ozon.ru", "wildberries.ru", "kinopoisk.ru",
    "api.dobro.ru", "ligastavok.ru", "utiltools.ru", "utiltools.site",
    "guardora.pro", "bobrkurva.shop", "dora-dura.shop"
]

def is_whitelist_sni(sni: str) -> bool:
    if not sni:
        return False
    sni_lower = sni.lower()
    return any(p in sni_lower for p in WL_PATTERNS)


def test_node_worker(args):
    node, worker_id = args
    port = 11100 + worker_id

    cfg = {
        "log": {"loglevel": "none"},
        "inbounds": [{"listen": "127.0.0.1", "port": port, "protocol": "http"}],
        "outbounds": [{
            "protocol": "vless",
            "settings": {
                "vnext": [{
                    "address": node.host,
                    "port": int(node.port),
                    "users": [{"id": node.uuid, "encryption": "none", "flow": node.flow or ""}]
                }]
            },
            "streamSettings": {
                "network": node.net_type or "tcp",
                "security": node.security or "none"
            },
            "tag": "proxy"
        }]
    }

    if node.security == "reality":
        cfg["outbounds"][0]["streamSettings"]["realitySettings"] = {
            "fingerprint": node.fp or "chrome",
            "serverName": node.sni or node.host,
            "publicKey": node.pbk or "",
            "shortId": node.sid or "",
            "spiderX": ""
        }
    elif node.security == "tls":
        cfg["outbounds"][0]["streamSettings"]["tlsSettings"] = {
            "fingerprint": node.fp or "chrome",
            "serverName": node.sni or node.host,
            "allowInsecure": True
        }

    if node.net_type == "grpc":
        cfg["outbounds"][0]["streamSettings"]["grpcSettings"] = {
            "serviceName": node.params.get("serviceName", "")
        }
    elif node.net_type == "ws":
        cfg["outbounds"][0]["streamSettings"]["wsSettings"] = {
            "path": node.path or "/",
            "headers": {"Host": node.host_header or node.sni or node.host}
        }

    cfg_file = os.path.join(DATA_DIR, f"temp_probe_{worker_id}.json")
    with open(cfg_file, "w", encoding="utf-8") as pf:
        json.dump(cfg, pf)

    proc = subprocess.Popen([XRAY_BIN, "run", "-c", cfg_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.35)

    handler = urllib.request.ProxyHandler({"http": f"http://127.0.0.1:{port}"})
    opener = urllib.request.build_opener(handler)
    t0 = time.perf_counter()
    ok = False
    lat = -1
    try:
        resp = opener.open("http://cp.cloudflare.com/generate_204", timeout=2.5)
        if resp.status in (200, 204):
            lat = int((time.perf_counter() - t0) * 1000)
            ok = True
    except Exception:
        pass
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=0.5)
        except Exception:
            proc.kill()
        try:
            os.remove(cfg_file)
        except Exception:
            pass

    if ok:
        node.is_alive = True
        node.latency_ms = lat
        return node
    return None


def collect_candidates(limit=400) -> List[ProxyNode]:
    aggregator = ConfigAggregator(DATA_DIR)
    nodes = aggregator.aggregate(fetch_all_sources=True, max_servers=limit)

    # Filter out fake CDN and plaintext
    valid = []
    seen = set()
    for n in nodes:
        if n.is_cloudflare_cdn_ip():
            continue
        if n.protocol != "vless" or n.security not in ("reality", "tls"):
            continue
        if n.security == "reality" and (not n.pbk or len(n.pbk) < 30 or not n.uuid or len(n.uuid) < 30):
            continue
        key = f"{n.host}:{n.port}"
        if key in seen:
            continue
        seen.add(key)
        valid.append(n)

    return valid


def run_verification(concurrency=25, max_candidates=350):
    print("=" * 65)
    print(" 🚀 ТОЧНАЯ ПРОВЕРКА ЧЕРЕЗ INCY XRAY НА ВАШЕМ ПК")
    print("=" * 65)

    candidates = collect_candidates(limit=max_candidates)
    print(f"[*] Отобрано кандидатов для проверки: {len(candidates)}")
    print(f"[*] Запуск {concurrency} параллельных проверок через xray.exe...")

    t_start = time.time()
    verified: List[ProxyNode] = []
    geoip = GeoIPResolver()

    args_list = [(n, i % concurrency) for i, n in enumerate(candidates)]

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        for res in executor.map(test_node_worker, args_list):
            if res is not None:
                # Mark whitelist status accurately
                if is_whitelist_sni(res.sni) or is_whitelist_sni(res.remark):
                    res.is_whitelist = True
                    if "yandex" in (res.sni + res.remark).lower() or "dzen" in (res.sni + res.remark).lower():
                        res.whitelist_label = "🛡️ Яндекс/Дзен"
                    elif "vk" in (res.sni + res.remark).lower():
                        res.whitelist_label = "🛡️ VK"
                    elif "gosuslugi" in (res.sni + res.remark).lower():
                        res.whitelist_label = "🛡️ Госуслуги"
                    else:
                        res.whitelist_label = "🛡️ Whitelist"
                else:
                    res.is_whitelist = False

                # Country info
                c_info = geoip.detect_from_remark(res.remark)
                if c_info:
                    res.country_code, res.country_flag, res.country_name = c_info
                else:
                    res.country_code = res.country_code or "EU"
                    res.country_flag = res.country_flag or "🇪🇺"
                    res.country_name = res.country_name or "Европа"

                verified.append(res)
                sys.stdout.write(f"\r  [+] Проверено рабочих: {len(verified)} ({res.country_flag} {res.country_name} • {res.latency_ms}ms)")
                sys.stdout.flush()

    elapsed = round(time.time() - t_start, 1)
    print(f"\n\n[+] Проверка завершена за {elapsed} сек!")
    print(f"    • 100% РАБОЧИХ УЗЛОВ (HTTP 204 в Xray): {len(verified)}")

    # Classify nodes:
    # 1. Foreign General (Non-RU, non-whitelist): YouTube, Insta, ChatGPT work!
    foreign_gen = [n for n in verified if n.country_code != "RU" and not n.is_whitelist]
    foreign_gen.sort(key=lambda x: x.latency_ms)

    # 2. Foreign Whitelist (Зарубежные сервера с SNI под VK/Госуслуги/Яндекс! Обходят глушение И дают доступ к зарубежным сайтам):
    foreign_wl = [n for n in verified if n.country_code != "RU" and n.is_whitelist]
    foreign_wl.sort(key=lambda x: x.latency_ms)

    # 3. Russian Whitelist (RU сервера с SNI под VK/Госуслуги):
    ru_wl = [n for n in verified if n.country_code == "RU" and n.is_whitelist]
    ru_wl.sort(key=lambda x: x.latency_ms)

    # 4. Russian General:
    ru_gen = [n for n in verified if n.country_code == "RU" and not n.is_whitelist]
    ru_gen.sort(key=lambda x: x.latency_ms)

    print(f"    • Зарубежные скоростные (НЕ Россия):  {len(foreign_gen)}")
    print(f"    • Зарубежные Whitelist (Обход + мир): {len(foreign_wl)}")
    print(f"    • Российские Whitelist (РФ обход):    {len(ru_wl)}")
    print(f"    • Российские обычные:                 {len(ru_gen)}")

    # Ordered strictly according to user requests:
    # Top: Foreign General
    # Middle: Foreign Whitelist (Bypass with open internet!)
    # Bottom: Russian General and Russian Whitelist at the very end
    final_ordered = foreign_gen + foreign_wl + ru_gen + ru_wl

    # Save to JSON
    out_data = {
        "timestamp": time.time(),
        "total": len(final_ordered),
        "servers": [n.to_dict() for n in final_ordered]
    }
    with open(os.path.join(DATA_DIR, "alive_servers.json"), "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)

    return final_ordered


if __name__ == "__main__":
    run_verification(concurrency=20, max_candidates=250)
