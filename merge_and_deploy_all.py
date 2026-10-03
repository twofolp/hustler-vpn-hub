#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merge and Deploy Master Pool:
Merges verified general servers with all verified Whitelist servers.
Builds and deploys updated Cloudflare Worker and Telegram Bot.
"""

import os
import sys
import json
import time
import urllib.parse
from typing import List, Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

from build_worker import generate_worker_js, deploy_to_cloudflare

def main():
    # 1. Existing verified servers
    alive_file = os.path.join(DATA_DIR, "alive_servers.json")
    with open(alive_file, "r", encoding="utf-8") as f:
        existing = json.load(f).get("servers", [])

    # 2. Specialized WL servers
    spec_file = os.path.join(DATA_DIR, "specialized_wl_alive.json")
    spec_wl = []
    if os.path.exists(spec_file):
        with open(spec_file, "r", encoding="utf-8") as f:
            spec_wl = json.load(f)

    # 3. Yandex/VK WL servers
    yvk_file = os.path.join(DATA_DIR, "yvk_wl_alive.json")
    yvk_wl = []
    if os.path.exists(yvk_file):
        with open(yvk_file, "r", encoding="utf-8") as f:
            yvk_wl = json.load(f)

    # 4. Newly discovered GitHub WL servers (wlunlocker, hussaroff, etc.)
    new_wl_file = os.path.join(DATA_DIR, "new_alive_whitelists.json")
    new_wl = []
    if os.path.exists(new_wl_file):
        with open(new_wl_file, "r", encoding="utf-8") as f:
            new_wl = json.load(f)

    print(f"[*] Базовый подтвержденный пул: {len(existing)} серверов")
    print(f"[*] Найдено специализированных Whitelist: {len(spec_wl)} серверов")
    print(f"[*] Найдено Yandex/VK Whitelist: {len(yvk_wl)} серверов")
    print(f"[*] Найдено новых GitHub Whitelist (Антиглушилки): {len(new_wl)} серверов")

    # Combine and mark whitelists accurately
    combined = []
    seen = set()

    for s in spec_wl + yvk_wl + new_wl:
        hp = f"{s.get('host')}:{s.get('port')}"
        if hp not in seen:
            seen.add(hp)
            s["is_whitelist"] = True
            sni_l = (s.get("sni") or "").lower()
            if "passport.yandex" in sni_l or "360.yandex" in sni_l or "ya.ru" in sni_l or "dzen" in sni_l:
                s["whitelist_label"] = "🛡️ Яндекс/Дзен"
            elif "vk" in sni_l:
                s["whitelist_label"] = "🛡️ VK"
            elif "google" in sni_l:
                s["whitelist_label"] = "🛡️ Google-DL"
            elif "x5.ru" in sni_l:
                s["whitelist_label"] = "🛡️ X5-Retail"
            elif "gosuslugi" in sni_l:
                s["whitelist_label"] = "🛡️ Госуслуги"
            else:
                s["whitelist_label"] = "🛡️ Whitelist"
            combined.append(s)

    for s in existing:
        hp = f"{s.get('host')}:{s.get('port')}"
        if hp not in seen:
            seen.add(hp)
            combined.append(s)

    # Clean out any ezhik
    combined = [s for s in combined if "ezhik" not in (s.get("host", "") + s.get("sni", "") + s.get("remark", "")).lower()]

    # 4 Strict categories:
    # Cat 1: Foreign General (non-RU, non-whitelist) -> Top of subscription
    foreign_gen = [s for s in combined if s.get("country_code") != "RU" and not s.get("is_whitelist")]
    foreign_gen.sort(key=lambda x: x.get("latency_ms", 9999))

    # Cat 2: Foreign Whitelist (Europe + RU SNI) -> Best of both worlds!
    foreign_wl = [s for s in combined if s.get("country_code") != "RU" and s.get("is_whitelist")]
    foreign_wl.sort(key=lambda x: x.get("latency_ms", 9999))

    # Cat 3: Russian Whitelist (RU node + Whitelist SNI) -> Super strong domestic bypass!
    ru_wl = [s for s in combined if s.get("country_code") == "RU" and s.get("is_whitelist")]
    ru_wl.sort(key=lambda x: x.get("latency_ms", 9999))

    # Cat 4: Russian General
    ru_gen = [s for s in combined if s.get("country_code") == "RU" and not s.get("is_whitelist")]
    ru_gen.sort(key=lambda x: x.get("latency_ms", 9999))

    print("\n" + "=" * 60)
    print(" 📊 ИТОГОВЫЙ ПУЛ СЕРВЕРОВ (РАСШИРЕННЫЙ WHITELIST):")
    print("=" * 60)
    print(f" 1. Зарубежные скоростные (НЕ Россия, Открытый мир): {len(foreign_gen)}")
    for i, s in enumerate(foreign_gen[:5]):
        print(f"    • #{i+1} {s.get('country_flag')} {s.get('country_name')} | {s.get('latency_ms')}ms | {s.get('host')}")

    print(f"\n 2. Зарубежные Whitelist (Амстердам + SNI Яндекс • Обход + Мир): {len(foreign_wl)}")
    for s in foreign_wl:
        print(f"    • {s.get('country_flag')} {s.get('country_name')} | {s.get('whitelist_label')} | SNI: {s.get('sni')} | {s.get('latency_ms')}ms")

    print(f"\n 3. Российские Whitelist (РФ узлы • Обход глушений мобильных сетей): {len(ru_wl)}")
    for s in ru_wl:
        print(f"    • {s.get('country_flag')} {s.get('country_name')} | {s.get('whitelist_label')} | SNI: {s.get('sni')} | {s.get('latency_ms')}ms")

    print(f"\n 4. Российские обычные:                                        {len(ru_gen)}")

    # Ordering:
    # Foreign regular first, Foreign whitelist next, Russian whitelist next, Russian general last
    ordered = foreign_gen + foreign_wl + ru_wl + ru_gen
    print(f"\n [+] ВСЕГО 100% РАБОЧИХ УЗЛОВ (0% N/A): {len(ordered)}")

    # Format remarks cleanly
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

    # Save to disk
    out_payload = {
        "timestamp": time.time(),
        "total": len(ordered),
        "servers": ordered
    }
    with open(alive_file, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, ensure_ascii=False, indent=2)

    with open(os.path.join(DATA_DIR, "alive_servers.txt"), "w", encoding="utf-8") as f:
        for s in ordered:
            f.write(s.get("uri", "") + "\n")

    # Deploy to Cloudflare Workers
    print("\n[*] Деплой на Cloudflare Workers...")
    worker_js = generate_worker_js(ordered)
    deploy_to_cloudflare(worker_js)
    print("\n[+] Деплой успешно завершен!")

if __name__ == "__main__":
    main()
