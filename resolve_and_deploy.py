#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resolve GeoIP, strictly classify servers, and deploy to Cloudflare Workers.
Ensures zero interaction with Ezhik VPN.
"""

import os
import sys
import json
import time
import socket
import urllib.request
import urllib.parse
from typing import List, Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

from core.geoip import COUNTRY_MAP
from build_worker import generate_worker_js, deploy_to_cloudflare

WL_KEYWORDS = [
    "yandex.ru", "ya.ru", "dzen.ru", "passport.yandex.ru",
    "vk.com", "vk.me", "userapi.com", "vk-portal.net",
    "gosuslugi.ru", "esia.gosuslugi.ru", "gu-st.ru",
    "mail.ru", "sber.ru", "sberbank.ru", "tinkoff.ru", "t-bank.ru",
    "avito.ru", "ozon.ru", "wildberries.ru", "kinopoisk.ru",
    "api.dobro.ru", "ligastavok.ru", "utiltools.ru", "utiltools.site",
    "guardora.pro", "bobrkurva.shop", "dora-dura.shop", "soxy-boobs.shop",
    "drom-buy.help", "support-pay-api.help"
]

def check_wl(sni: str, remark: str = "") -> bool:
    s = (sni or "").lower() + " " + (remark or "").lower()
    return any(k in s for k in WL_KEYWORDS)

def main():
    alive_path = os.path.join(DATA_DIR, "alive_servers.json")
    if not os.path.exists(alive_path):
        print(f"[!] {alive_path} not found!")
        return

    with open(alive_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    raw_servers = data.get("servers", [])
    print(f"[*] Исходно проверенных серверов (Xray HTTP 204): {len(raw_servers)}")

    # 1. Strict filter: EXCLUDE any Ezhik VPN configs
    clean_servers = []
    for s in raw_servers:
        comb = (s.get("host", "") + s.get("sni", "") + s.get("remark", "")).lower()
        if "ezhik" in comb:
            print(f"[-] Пропуск стороннего хоста: {s.get('host')}")
            continue
        clean_servers.append(s)

    print(f"[*] Серверов НАШЕГО VPN (после фильтра сторонних): {len(clean_servers)}")

    # 2. GeoIP resolution for all servers
    print("[*] Определение геолокации и стран для каждого узла...")
    for idx, s in enumerate(clean_servers):
        host = s.get("host", "")
        sni = s.get("sni", "")

        # Detect whitelist
        if check_wl(sni, s.get("remark", "")):
            s["is_whitelist"] = True
            sni_l = sni.lower()
            if "yandex" in sni_l or "dzen" in sni_l:
                s["whitelist_label"] = "🛡️ Яндекс/Дзен"
            elif "vk" in sni_l:
                s["whitelist_label"] = "🛡️ VK"
            elif "gosuslugi" in sni_l:
                s["whitelist_label"] = "🛡️ Госуслуги"
            else:
                s["whitelist_label"] = "🛡️ Whitelist"
        else:
            s["is_whitelist"] = False
            s["whitelist_label"] = ""

        # Resolve IP
        try:
            ip = socket.gethostbyname(host)
        except Exception:
            ip = host

        # Get country
        try:
            url = f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,city"
            req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                g = json.loads(resp.read().decode("utf-8", errors="ignore"))
                if g.get("status") == "success":
                    cc = g.get("countryCode", "EU")
                    s["country_code"] = cc
                    if cc in COUNTRY_MAP:
                        s["country_flag"] = COUNTRY_MAP[cc]["flag"]
                        s["country_name"] = COUNTRY_MAP[cc]["name_ru"]
                    else:
                        s["country_flag"] = "🌐"
                        s["country_name"] = g.get("country", "Зарубежный")
        except Exception as e:
            if s.get("country_code") in COUNTRY_MAP:
                s["country_flag"] = COUNTRY_MAP[s["country_code"]]["flag"]
                s["country_name"] = COUNTRY_MAP[s["country_code"]]["name_ru"]
            else:
                s["country_flag"] = "🇪🇺"
                s["country_name"] = "Европа"

        time.sleep(0.08)

    # 3. Categorization into 4 strict groups
    foreign_gen = [s for s in clean_servers if s.get("country_code") != "RU" and not s.get("is_whitelist")]
    foreign_gen.sort(key=lambda x: x.get("latency_ms", 9999))

    foreign_wl = [s for s in clean_servers if s.get("country_code") != "RU" and s.get("is_whitelist")]
    foreign_wl.sort(key=lambda x: x.get("latency_ms", 9999))

    ru_gen = [s for s in clean_servers if s.get("country_code") == "RU" and not s.get("is_whitelist")]
    ru_gen.sort(key=lambda x: x.get("latency_ms", 9999))

    ru_wl = [s for s in clean_servers if s.get("country_code") == "RU" and s.get("is_whitelist")]
    ru_wl.sort(key=lambda x: x.get("latency_ms", 9999))

    print("\n" + "=" * 55)
    print(" 📊 ИТОГОВАЯ КАТЕГОРИЗАЦИЯ НАШЕГО VPN:")
    print("=" * 55)
    print(f" 1. Зарубежные скоростные (НЕ Россия, Открытый мир): {len(foreign_gen)}")
    for i, s in enumerate(foreign_gen[:5]):
        print(f"    • #{i+1} {s.get('country_flag')} {s.get('country_name')} | {s.get('latency_ms')}ms | {s.get('host')}")

    print(f"\n 2. Зарубежные Whitelist (Европа + SNI обхода):       {len(foreign_wl)}")
    for s in foreign_wl:
        print(f"    • {s.get('country_flag')} {s.get('country_name')} | {s.get('whitelist_label')} | SNI: {s.get('sni')} | {s.get('latency_ms')}ms")

    print(f"\n 3. Российские обычные:                               {len(ru_gen)}")
    for s in ru_gen:
        print(f"    • {s.get('country_flag')} {s.get('country_name')} | {s.get('latency_ms')}ms | {s.get('host')}")

    print(f"\n 4. Российские Whitelist (В самом низу):              {len(ru_wl)}")
    for s in ru_wl:
        print(f"    • {s.get('country_flag')} {s.get('country_name')} | {s.get('whitelist_label')} | {s.get('latency_ms')}ms")

    # Combine in exact order:
    ordered = foreign_gen + foreign_wl + ru_gen + ru_wl

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

        # Re-build URI with new remark
        # Extract base URI without hash
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

    # Save alive_servers.txt for quick text view
    with open(os.path.join(DATA_DIR, "alive_servers.txt"), "w", encoding="utf-8") as f:
        for s in ordered:
            f.write(s.get("uri", "") + "\n")

    print("\n[+] Обновлен локальный файл data/alive_servers.json")

    # 4. Deploy to Cloudflare Workers
    print("\n[*] Сборка и деплой на Cloudflare Workers...")
    worker_js = generate_worker_js(ordered)
    deploy_to_cloudflare(worker_js)

    print("\n" + "=" * 55)
    print(" ✅ ДЕПЛОЙ НАШЕГО VPN УСПЕШНО ЗАВЕРШЕН!")
    print("=" * 55)

if __name__ == "__main__":
    main()
