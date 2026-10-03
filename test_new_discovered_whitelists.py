#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test newly discovered GitHub Whitelist Sources:
- wlunlocker (EU & RU cidr)
- hussaroff (lte-universal-checked)
- RKPchannel (whitelist.txt)
- flaafix (AetrisVPN-white-list-lite)
"""

import os
import sys
import json
import time
import socket
import urllib.request
import subprocess
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any

from core.parser import ProxyNode
from core.geoip import COUNTRY_MAP

XRAY_BIN = r"C:\Program Files\INCY\app\resources\bin\xray.exe"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

TARGET_URLS = [
    "https://raw.githubusercontent.com/wlunlocker/vpn-configs/main/whitelist_cidr3_eu.txt",
    "https://raw.githubusercontent.com/wlunlocker/vpn-configs/main/whitelist_cidr1_ru.txt",
    "https://raw.githubusercontent.com/wlunlocker/vpn-configs/main/whitelist_cidr2_ru.txt",
    "https://raw.githubusercontent.com/wlunlocker/vpn-configs/main/whitelist_all.txt",
    "https://raw.githubusercontent.com/hussaroff/lte-universal-checked/main/whitelist.txt",
    "https://raw.githubusercontent.com/RKPchannel/RKP_bypass_configs/main/whitelist.txt",
    "https://raw.githubusercontent.com/flaafix/AetrisVPN-white-list-lite/main/AetrisVPN.txt"
]

def test_probe(args):
    node, worker_id = args
    port = 11700 + worker_id

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

    cfg_file = os.path.join(DATA_DIR, f"temp_newwl_{worker_id}.json")
    with open(cfg_file, "w", encoding="utf-8") as pf:
        json.dump(cfg, pf)

    proc = subprocess.Popen([XRAY_BIN, "run", "-c", cfg_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.35)

    handler = urllib.request.ProxyHandler({"http": f"http://127.0.0.1:{port}"})
    opener = urllib.request.build_opener(handler)
    t0 = time.perf_counter()
    ok = False
    lat = -1

    for u in ["http://cp.cloudflare.com/generate_204", "http://connectivitycheck.gstatic.com/generate_204"]:
        try:
            resp = opener.open(u, timeout=2.2)
            if resp.status in (200, 204):
                lat = int((time.perf_counter() - t0) * 1000)
                ok = True
                break
        except Exception:
            pass

    proc.terminate()
    try:
        proc.wait(timeout=0.4)
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
    print("[*] Сборка конфигов из 7 новых специализированных Whitelist источников...")
    all_raw = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for u in TARGET_URLS:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=7) as resp:
                text = resp.read().decode("utf-8", errors="ignore")
                lines = [l.strip() for l in text.splitlines() if l.strip().startswith("vless://")]
                print(f"  -> {u.split('/')[-1]}: {len(lines)} конфигов")
                all_raw.extend(lines)
        except Exception as e:
            print(f"  [!] {u}: {e}")

    unique = list(set(all_raw))
    print(f"[*] Всего уникальных конфигов: {len(unique)}")

    nodes = []
    seen = set()
    for l in unique:
        n = ProxyNode(l)
        if not n or not n.is_valid:
            continue
        if n.is_cloudflare_cdn_ip():
            continue
        if "ezhik" in (n.host + n.sni + n.remark).lower():
            continue
        key = f"{n.host}:{n.port}"
        if key not in seen:
            seen.add(key)
            nodes.append(n)

    print(f"[*] Валидных кандидатов для проверки: {len(nodes)}")

    concurrency = 30
    args_list = [(n, i % concurrency) for i, n in enumerate(nodes)]
    verified = []
    t0 = time.time()

    print(f"[*] Запуск проверки {len(nodes)} узлов через xray.exe в {concurrency} потоков...")
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        for res in ex.map(test_probe, args_list):
            if res is not None:
                verified.append(res)
                sys.stdout.write(f"\r  [+] Найден живой Whitelist: {len(verified)} ({res.host} • {res.sni} • {res.latency_ms}ms)")
                sys.stdout.flush()

    elapsed = round(time.time() - t0, 1)
    print(f"\n\n[+] Проверка завершена за {elapsed} сек! Найдено живых узлов: {len(verified)}")

    # GeoIP
    results = []
    for node in verified:
        d = node.to_dict()
        d["is_whitelist"] = True
        sni_l = (node.sni or "").lower()
        if "yandex" in sni_l or "dzen" in sni_l:
            d["whitelist_label"] = "🛡️ Яндекс/Дзен"
        elif "vk" in sni_l:
            d["whitelist_label"] = "🛡️ VK"
        elif "tradingview" in sni_l:
            d["whitelist_label"] = "🛡️ TradingView"
        elif "google" in sni_l:
            d["whitelist_label"] = "🛡️ Google-DL"
        else:
            d["whitelist_label"] = "🛡️ Белый список"

        try:
            ip = socket.gethostbyname(d["host"])
        except Exception:
            ip = d["host"]

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

    out_file = os.path.join(DATA_DIR, "new_alive_whitelists.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[+] Сохранено в {out_file}")

if __name__ == "__main__":
    main()
