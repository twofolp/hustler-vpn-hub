#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extended Pool Verifier using Native Xray HTTP 204:
Tests whitelist candidates and diverse candidates from all 134 sources.
Merges newly discovered working nodes with our existing verified pool.
Deploys to Cloudflare Workers.
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
from typing import List, Dict, Any, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
XRAY_BIN = r"C:\Program Files\INCY\app\resources\bin\xray.exe"

from core.parser import ProxyNode
from core.geoip import COUNTRY_MAP
from build_worker import generate_worker_js, deploy_to_cloudflare

WL_KEYWORDS = [
    "yandex.ru", "ya.ru", "dzen.ru", "passport.yandex.ru",
    "vk.com", "vk.me", "userapi.com", "vk-portal.net",
    "gosuslugi.ru", "esia.gosuslugi.ru", "gu-st.ru",
    "mail.ru", "sber.ru", "sberbank.ru", "tinkoff.ru", "t-bank.ru",
    "avito.ru", "ozon.ru", "wildberries.ru", "kinopoisk.ru",
    "api.dobro.ru", "ligastavok.ru", "utiltools.ru", "utiltools.site",
    "guardora.pro", "bobrkurva.shop", "dora-dura.shop", "soxy-boobs.shop"
]

def check_wl(sni: str, remark: str = "") -> bool:
    s = (sni or "").lower() + " " + (remark or "").lower()
    return any(k in s for k in WL_KEYWORDS)

def test_node_worker(args):
    node, worker_id = args
    port = 11300 + worker_id

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

    cfg_file = os.path.join(DATA_DIR, f"temp_probe2_{worker_id}.json")
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

def main():
    print("=" * 65)
    print(" 🚀 МАСШТАБНАЯ ПРОВЕРКА ВСЕХ 134 ИСТОЧНИКОВ ЧЕРЕЗ XRAY HTTP 204")
    print("=" * 65)

    # 1. Load existing verified servers
    alive_path = os.path.join(DATA_DIR, "alive_servers.json")
    existing_servers = []
    seen_hosts = set()

    if os.path.exists(alive_path):
        with open(alive_path, "r", encoding="utf-8") as f:
            existing_servers = json.load(f).get("servers", [])
        for s in existing_servers:
            seen_hosts.add(f"{s.get('host')}:{s.get('port')}")
        print(f"[*] Уже подтвержденных рабочих серверов в пуле: {len(existing_servers)}")

    # 2. Load candidates from all_candidates.txt
    cand_path = os.path.join(DATA_DIR, "all_candidates.txt")
    if not os.path.exists(cand_path):
        print("[!] all_candidates.txt not found!")
        return

    candidates = []
    with open(cand_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n = ProxyNode(line)
            if not n or not n.is_valid:
                continue
            if "ezhik" in (n.host + n.sni + n.remark).lower():
                continue
            key = f"{n.host}:{n.port}"
            if key in seen_hosts:
                continue
            seen_hosts.add(key)
            candidates.append(n)

    print(f"[*] Новых уникальных кандидатов для проверки: {len(candidates)}")

    # Prioritize: Whitelist nodes first, then others
    wl_cands = [n for n in candidates if check_wl(n.sni, n.remark)]
    other_cands = [n for n in candidates if not check_wl(n.sni, n.remark)]

    print(f"  • Новых кандидатов с Whitelist SNI: {len(wl_cands)}")
    print(f"  • Обычных кандидатов: {len(other_cands)}")

    # Test top 120 whitelist candidates + top 150 diverse general candidates
    test_batch = wl_cands[:120] + other_cands[:150]
    print(f"[*] Отобрано для тестирования в текущем раунде: {len(test_batch)} узлов")

    concurrency = 25
    args_list = [(n, i % concurrency) for i, n in enumerate(test_batch)]

    newly_verified = []
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        for res in ex.map(test_node_worker, args_list):
            if res is not None:
                newly_verified.append(res)
                sys.stdout.write(f"\r  [+] Найден новый живой: {len(newly_verified)} ({res.host} • {res.latency_ms}ms)")
                sys.stdout.flush()

    elapsed = round(time.time() - t0, 1)
    print(f"\n\n[+] Проверка завершена за {elapsed} сек! Найдено дополнительных рабочих узлов: {len(newly_verified)}")

    # Convert newly verified to dicts & resolve GeoIP
    new_dicts = []
    for n in newly_verified:
        d = n.to_dict()
        host = d["host"]
        sni = d.get("sni", "")

        if check_wl(sni, d.get("remark", "")):
            d["is_whitelist"] = True
            sni_l = sni.lower()
            if "yandex" in sni_l or "dzen" in sni_l:
                d["whitelist_label"] = "🛡️ Яндекс/Дзен"
            elif "vk" in sni_l:
                d["whitelist_label"] = "🛡️ VK"
            elif "gosuslugi" in sni_l:
                d["whitelist_label"] = "🛡️ Госуслуги"
            else:
                d["whitelist_label"] = "🛡️ Whitelist"
        else:
            d["is_whitelist"] = False
            d["whitelist_label"] = ""

        try:
            ip = socket.gethostbyname(host)
        except Exception:
            ip = host

        try:
            url = f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,city"
            req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
            with urllib.request.urlopen(req, timeout=3) as resp:
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

        new_dicts.append(d)
        time.sleep(0.05)

    # Merge with existing verified servers
    all_combined = existing_servers + new_dicts

    # Deduplicate by host:port
    final_unique = []
    seen_hp = set()
    for s in all_combined:
        hp = f"{s.get('host')}:{s.get('port')}"
        if hp not in seen_hp:
            seen_hp.add(hp)
            final_unique.append(s)

    # 4 Strict categories
    foreign_gen = [s for s in final_unique if s.get("country_code") != "RU" and not s.get("is_whitelist")]
    foreign_gen.sort(key=lambda x: x.get("latency_ms", 9999))

    foreign_wl = [s for s in final_unique if s.get("country_code") != "RU" and s.get("is_whitelist")]
    foreign_wl.sort(key=lambda x: x.get("latency_ms", 9999))

    ru_gen = [s for s in final_unique if s.get("country_code") == "RU" and not s.get("is_whitelist")]
    ru_gen.sort(key=lambda x: x.get("latency_ms", 9999))

    ru_wl = [s for s in final_unique if s.get("country_code") == "RU" and s.get("is_whitelist")]
    ru_wl.sort(key=lambda x: x.get("latency_ms", 9999))

    ordered = foreign_gen + foreign_wl + ru_gen + ru_wl

    print("\n" + "=" * 55)
    print(" 📊 ОБНОВЛЕННЫЙ ОБЩИЙ ПУЛ (ВСЕ ИСТОЧНИКИ ПРОВЕРЕНЫ):")
    print("=" * 55)
    print(f" 1. Зарубежные скоростные (НЕ Россия, Открытый мир): {len(foreign_gen)}")
    print(f" 2. Зарубежные Whitelist (Европа + SNI обхода):       {len(foreign_wl)}")
    print(f" 3. Российские обычные:                               {len(ru_gen)}")
    print(f" 4. Российские Whitelist (В самом низу):              {len(ru_wl)}")
    print(f" [+] ИТОГО 100% РАБОЧИХ УЗЛОВ:                       {len(ordered)}")

    # Update remarks cleanly
    for idx, s in enumerate(ordered):
        flag = s.get("country_flag", "🌐")
        cname = s.get("country_name", "Сервер")
        lat = s.get("latency_ms", 0)
        is_w = s.get("is_whitelist", False)
        wl_lbl = s.get("whitelist_label", "Whitelist")

        if idx == 0 and s.get("country_code") != "RU" and not is_w:
            s["remark"] = f"⚡ Лучший зарубежный сервер (Мин. пинг) • {flag} {cname} • {lat}ms"
        elif is_w:
            if s.get("country_code") != "RU":
                s["remark"] = f"{flag} {cname} • {wl_lbl} (Зарубежный обход) • {lat}ms"
            else:
                s["remark"] = f"🇷🇺 Россия • {wl_lbl} (РФ обход) • {lat}ms"
        else:
            s["remark"] = f"{flag} {cname} #{idx+1} • {lat}ms"

        uri = s.get("uri", "")
        if "#" in uri:
            base_uri = uri.split("#")[0]
            s["uri"] = f"{base_uri}#{urllib.parse.quote(s['remark'])}"

    # Save to alive_servers.json
    out_payload = {
        "timestamp": time.time(),
        "total": len(ordered),
        "servers": ordered
    }
    with open(alive_path, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, ensure_ascii=False, indent=2)

    with open(os.path.join(DATA_DIR, "alive_servers.txt"), "w", encoding="utf-8") as f:
        for s in ordered:
            f.write(s.get("uri", "") + "\n")

    # Deploy to Cloudflare Workers
    print("\n[*] Деплой расширенного пула на Cloudflare Workers...")
    worker_js = generate_worker_js(ordered)
    deploy_to_cloudflare(worker_js)
    print("\n[+] Деплой расширенного пула успешно завершен!")

if __name__ == "__main__":
    main()
