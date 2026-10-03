#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Specialized Whitelist Sources Scanner:
Pulls directly from the 6 dedicated whitelist repos and tests all nodes.
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

WL_SOURCES = [
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_universal.txt",
    "https://raw.githubusercontent.com/ByeWhiteLists/ByeWhiteLists2/refs/heads/main/ByeWhiteLists2.txt",
    "https://raw.githubusercontent.com/SilentGhostCodes/WhiteListVpn/refs/heads/main/Whitelist.txt",
    "https://raw.githubusercontent.com/SilentGhostCodes/WhiteListVpn/refs/heads/main/Whitelist%20%E2%84%962.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-checked.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS_mobile.txt",
    "https://gitverse.ru/api/repos/cid-uskoritel/cid-white/raw/branch/master/whitelist.txt",
    "https://raw.githubusercontent.com/Sanuyyq/sub-storage1/refs/heads/main/bs.txt",
    "https://raw.githubusercontent.com/ewecrow78-gif/whitelist1/main/list.txt"
]

XRAY_BIN = r"C:\Program Files\INCY\app\resources\bin\xray.exe"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def test_probe(args):
    node, worker_id = args
    port = 11500 + worker_id

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

    cfg_file = os.path.join(DATA_DIR, f"probe_spec_{worker_id}.json")
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
    print("[*] Загрузка 9 специализированных Whitelist источников...")
    all_raw = []
    headers = {"User-Agent": "curl/7.68.0"}

    for s_url in WL_SOURCES:
        try:
            req = urllib.request.Request(s_url, headers=headers)
            with urllib.request.urlopen(req, timeout=7) as resp:
                text = resp.read().decode("utf-8", errors="ignore")
                lines = [l.strip() for l in text.splitlines() if l.strip().startswith("vless://")]
                print(f"  -> {s_url.split('/')[-1]}: {len(lines)} конфигов")
                all_raw.extend(lines)
        except Exception as e:
            print(f"  [!] {s_url.split('/')[-1]}: {e}")

    unique = list(set(all_raw))
    print(f"[*] Всего уникальных конфигов из спец-источников: {len(unique)}")

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

    print(f"[*] Валидных кандидатов для тестирования: {len(nodes)}")

    concurrency = 25
    batch = nodes[:350]
    print(f"[*] Запуск проверки {len(batch)} узлов через xray.exe...")

    args_list = [(n, i % concurrency) for i, n in enumerate(batch)]
    verified = []
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        for res in ex.map(test_probe, args_list):
            if res is not None:
                verified.append(res)
                sys.stdout.write(f"\r  [+] Найдено живых Whitelist: {len(verified)} ({res.host} • {res.latency_ms}ms)")
                sys.stdout.flush()

    elapsed = round(time.time() - t0, 1)
    print(f"\n\n[+] Проверка завершена за {elapsed} сек! Найдено: {len(verified)}")

    # GeoIP
    for v in verified:
        try:
            ip = socket.gethostbyname(v.host)
        except Exception:
            ip = v.host
        try:
            url = f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,city"
            req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
            with urllib.request.urlopen(req, timeout=2.5) as resp:
                g = json.loads(resp.read().decode("utf-8", errors="ignore"))
                if g.get("status") == "success":
                    cc = g.get("countryCode", "EU")
                    v.country_code = cc
                    if cc in COUNTRY_MAP:
                        v.country_flag = COUNTRY_MAP[cc]["flag"]
                        v.country_name = COUNTRY_MAP[cc]["name_ru"]
                    else:
                        v.country_flag = "🌐"
                        v.country_name = g.get("country", "Зарубежный")
        except Exception:
            pass
        time.sleep(0.04)

    # Save
    out_file = os.path.join(DATA_DIR, "specialized_wl_alive.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump([n.to_dict() for n in verified], f, ensure_ascii=False, indent=2)
    print(f"[+] Сохранено {len(verified)} узлов в data/specialized_wl_alive.json")

if __name__ == "__main__":
    main()
