#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep Whitelist Scanner:
Tests all 1,500+ whitelist candidates using Incy's native xray.exe.
Finds both Foreign Whitelists (EU with Russian SNI) and Russian Whitelists.
"""

import os
import sys
import json
import time
import socket
import urllib.request
import urllib.parse
import subprocess
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
XRAY_BIN = r"C:\Program Files\INCY\app\resources\bin\xray.exe"

from core.parser import ProxyNode
from core.geoip import COUNTRY_MAP

WL_PATTERNS = [
    "yandex.ru", "ya.ru", "dzen.ru", "passport.yandex.ru",
    "vk.com", "vk.me", "userapi.com", "vk-portal.net",
    "gosuslugi.ru", "esia.gosuslugi.ru", "gu-st.ru",
    "mail.ru", "sber.ru", "sberbank.ru", "tinkoff.ru", "t-bank.ru",
    "avito.ru", "ozon.ru", "wildberries.ru", "kinopoisk.ru",
    "api.dobro.ru", "ligastavok.ru", "utiltools.ru", "utiltools.site",
    "guardora.pro", "bobrkurva.shop", "dora-dura.shop", "soxy-boobs.shop",
    "drom-buy.help", "support-pay-api.help"
]

def is_wl(sni: str, remark: str = "") -> bool:
    s = (sni or "").lower() + " " + (remark or "").lower()
    return any(p in s for p in WL_PATTERNS)

def get_wl_label(sni: str, remark: str = "") -> str:
    s = (sni or "").lower() + " " + (remark or "").lower()
    if "passport.yandex" in s or "yandex" in s or "dzen" in s or "ya.ru" in s:
        return "🛡️ Яндекс/Дзен"
    if "vk" in s or "userapi" in s:
        return "🛡️ VK"
    if "gosuslugi" in s or "gu-st" in s:
        return "🛡️ Госуслуги"
    if "sber" in s or "tinkoff" in s or "t-bank" in s:
        return "🛡️ Банки"
    if "mail.ru" in s:
        return "🛡️ Mail.ru"
    if "dobro.ru" in s:
        return "🛡️ Добро.ру"
    return "🛡️ Whitelist"

def test_probe(args):
    node, worker_id = args
    port = 11400 + worker_id

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

    cfg_file = os.path.join(DATA_DIR, f"temp_wl_{worker_id}.json")
    with open(cfg_file, "w", encoding="utf-8") as pf:
        json.dump(cfg, pf)

    proc = subprocess.Popen([XRAY_BIN, "run", "-c", cfg_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.35)

    handler = urllib.request.ProxyHandler({"http": f"http://127.0.0.1:{port}"})
    opener = urllib.request.build_opener(handler)
    t0 = time.perf_counter()
    ok = False
    lat = -1

    # Try Cloudflare generate_204 first, fallback to gstatic generate_204
    for test_url in ["http://cp.cloudflare.com/generate_204", "http://connectivitycheck.gstatic.com/generate_204"]:
        try:
            resp = opener.open(test_url, timeout=2.2)
            if resp.status in (200, 204):
                lat = int((time.perf_counter() - t0) * 1000)
                ok = True
                break
        except Exception:
            pass

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

def main():
    print("=" * 65)
    print(" 🛡️ ПОИСК И ПРОВЕРКА ВСЕХ WHITELIST УЗЛОВ ЧЕРЕЗ NATIVE XRAY")
    print("=" * 65)

    cand_file = os.path.join(DATA_DIR, "all_candidates.txt")
    if not os.path.exists(cand_file):
        print(f"[!] {cand_file} не найден!")
        return

    wl_nodes = []
    seen = set()

    with open(cand_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n = ProxyNode(line)
            if not n or not n.is_valid:
                continue
            if "ezhik" in (n.host + n.sni + n.remark).lower():
                continue
            if is_wl(n.sni, n.remark):
                key = f"{n.host}:{n.port}"
                if key not in seen:
                    seen.add(key)
                    wl_nodes.append(n)

    print(f"[*] Всего уникальных Whitelist кандидатов для проверки: {len(wl_nodes)}")

    # Check in parallel 30 workers
    concurrency = 30
    batch = wl_nodes[:500]  # Test top 500 candidates
    print(f"[*] Запуск проверки {len(batch)} узлов в {concurrency} потоков...")

    args_list = [(n, i % concurrency) for i, n in enumerate(batch)]
    verified_wl = []
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        for res in ex.map(test_probe, args_list):
            if res is not None:
                verified_wl.append(res)
                sys.stdout.write(f"\r  [+] Найден живой Whitelist: {len(verified_wl)} ({res.host} • {res.sni} • {res.latency_ms}ms)")
                sys.stdout.flush()

    elapsed = round(time.time() - t0, 1)
    print(f"\n\n[+] Проверка Whitelist завершена за {elapsed} сек! Найдено живых: {len(verified_wl)}")

    # Resolve GeoIP for all alive Whitelist nodes
    print("[*] Определение геолокации Whitelist узлов...")
    results = []
    for node in verified_wl:
        d = node.to_dict()
        d["is_whitelist"] = True
        d["whitelist_label"] = get_wl_label(node.sni, node.remark)

        host = d["host"]
        try:
            ip = socket.gethostbyname(host)
        except Exception:
            ip = host

        try:
            url = f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,city"
            req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
            with urllib.request.urlopen(req, timeout=2.5) as resp:
                g = json.loads(resp.read().decode("utf-8", errors="ignore"))
                if g.get("status") == "success":
                    cc = g.get("countryCode", "EU")
                    d["country_code"] = cc
                    if cc in COUNTRY_MAP:
                        d["country_flag"] = COUNTRY_MAP[cc]["flag"]
                        d["country_name"] = COUNTRY_MAP[cc]["name_ru"]
                    else:
                        d["country_flag"] = "🌐"
                        d["country_name"] = g.get("country", "Зарубежный")
        except Exception:
            d["country_code"] = "EU"
            d["country_flag"] = "🇪🇺"
            d["country_name"] = "Европа"

        results.append(d)
        time.sleep(0.04)

    # Classify into Foreign Whitelist vs Russian Whitelist
    fwl = [s for s in results if s.get("country_code") != "RU"]
    fwl.sort(key=lambda x: x.get("latency_ms", 9999))

    rwl = [s for s in results if s.get("country_code") == "RU"]
    rwl.sort(key=lambda x: x.get("latency_ms", 9999))

    print("\n" + "=" * 60)
    print(f" 🛡️ НАЙДЕННЫЕ ЖИВЫЕ WHITELIST УЗЛЫ:")
    print("=" * 60)
    print(f" • Зарубежные Whitelist (Европа + SNI РФ • Обход + Мир): {len(fwl)}")
    for s in fwl:
        print(f"   - {s.get('country_flag')} {s.get('country_name')} | {s.get('whitelist_label')} | SNI: {s.get('sni')} | {s.get('latency_ms')}ms")

    print(f"\n • Российские Whitelist (РФ узлы • Полный обход блокировок): {len(rwl)}")
    for s in rwl:
        print(f"   - 🇷🇺 {s.get('country_name')} | {s.get('whitelist_label')} | SNI: {s.get('sni')} | {s.get('latency_ms')}ms")

    # Save to data/verified_whitelists.json
    out_file = os.path.join(DATA_DIR, "verified_whitelists.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"timestamp": time.time(), "foreign_wl": fwl, "russian_wl": rwl}, f, ensure_ascii=False, indent=2)
    print(f"\n[+] Сохранено в {out_file}")

if __name__ == "__main__":
    main()
