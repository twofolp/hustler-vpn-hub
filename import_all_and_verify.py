#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
All-In-One Strict Verification & Cloudflare + Incy Integration Engine
1. Gathers from all sources (sub.txt, desktop files, git repositories)
2. Runs REAL Xray HTTP 204 probes on all nodes (100% genuine traffic check, ZERO N/A)
3. Supports Foreign Whitelists (DE, NL, etc. with VK/Yandex SNI) + Foreign General + RU Whitelist
4. Directly injects the verified subscription and servers into Incy's local database (C:\Users\twofolp\AppData\Local\incy\incy.db)
5. Deploys verified clean pool to Cloudflare Workers and syncs Telegram Bot
"""

import os
import re
import sys
import time
import json
import uuid
import sqlite3
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
XRAY_BIN = r"C:\Program Files\INCY\app\resources\bin\xray.exe"
INCY_DB = r"C:\Users\twofolp\AppData\Local\incy\incy.db"

from core.parser import ProxyParser, ProxyNode
from core.geoip import GeoIPResolver
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

def is_wl(sni: str, remark: str = "") -> bool:
    s = (sni or "").lower() + " " + (remark or "").lower()
    return any(k in s for k in WL_PATTERNS)

WL_PATTERNS = WL_KEYWORDS


def fetch_all_raw_configs() -> List[str]:
    raw_lines = []

    # 1. sub.txt
    sub_path = os.path.join(DATA_DIR, "sub.txt")
    if os.path.exists(sub_path):
        with open(sub_path, "r", encoding="utf-8", errors="ignore") as f:
            for l in f:
                l = l.strip()
                if l.startswith("vless://"):
                    raw_lines.append(l)

    # 2. Desktop files
    desktop = r"C:\Users\twofolp\Desktop"
    if os.path.exists(desktop):
        for fname in os.listdir(desktop):
            if fname.endswith(".txt"):
                fpath = os.path.join(desktop, fname)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                    matches = re.findall(r"vless://[^\s<>\"\'\n]+", text)
                    raw_lines.extend(matches)
                except Exception:
                    pass

    # 3. Sources dir
    sources_dir = os.path.join(BASE_DIR, "sources")
    if os.path.exists(sources_dir):
        for fname in os.listdir(sources_dir):
            if fname.endswith(".txt"):
                fpath = os.path.join(sources_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        for l in f:
                            l = l.strip()
                            if l.startswith("vless://"):
                                raw_lines.append(l)
                except Exception:
                    pass

    return raw_lines


def test_node_xray(args):
    node, worker_id = args
    port = 11200 + worker_id

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

    cfg_file = os.path.join(DATA_DIR, f"xray_worker_{worker_id}.json")
    with open(cfg_file, "w", encoding="utf-8") as f:
        json.dump(cfg, f)

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


def inject_into_incy_db(servers: List[ProxyNode]):
    if not os.path.exists(INCY_DB):
        print(f"[!] Incy DB не найден по пути: {INCY_DB}")
        return

    print("\n[*] Интеграция подписки напрямую в приложение Incy на вашем ПК...")
    con = sqlite3.connect(INCY_DB)
    cur = con.cursor()

    sub_id = "hustler-vpn-subscription-hub"
    sub_name = "🍄 HUSTLER VPN (0% N/A • Проверено)"
    sub_url = "https://vless-hub.danilkaponda.workers.dev/sub/incy"
    now_ms = int(time.time() * 1000)

    # 1. Upsert subscription
    cur.execute("DELETE FROM servers WHERE subscriptionId=?", (sub_id,))
    cur.execute("DELETE FROM subscriptions WHERE id=?", (sub_id,))

    cur.execute("""
        INSERT INTO subscriptions (
            id, name, customName, profileName, routingProfileName, url,
            isEnabled, lastUpdated, updateInterval, serversCount,
            announce, userInfoUpload, userInfoDownload, userInfoTotal, userInfoExpire,
            createdAt, orderIndex
        ) VALUES (?, ?, ?, ?, ?, ?, 1, ?, 3600000, ?, ?, 0, 0, 1073741824000, 0, ?, 0)
    """, (
        sub_id, sub_name, "HUSTLER VPN", "Hustler Hub", "Default", sub_url,
        now_ms, len(servers),
        "🍄 Все серверы проверены через Xray HTTP 204 на вашем ПК!\n⚡ Топ-серверы: без N/A\n🛡️ Whitelist: обход глушений РФ",
        now_ms
    ))

    # 2. Insert servers
    for idx, s in enumerate(servers):
        srv_id = str(uuid.uuid4())
        name = s.get_clean_remark(idx + 1)
        full_cfg = {
            "routing": {
                "domainStrategy": "IPIfNonMatch",
                "rules": [{"protocol": ["bittorrent"], "type": "field", "outboundTag": "direct"}],
                "domainMatcher": "hybrid"
            },
            "outbounds": [
                {
                    "settings": {
                        "vnext": [{
                            "address": s.host,
                            "port": int(s.port),
                            "users": [{"encryption": "none", "id": s.uuid, "flow": s.flow or ""}]
                        }]
                    },
                    "protocol": "vless",
                    "streamSettings": {
                        "network": s.net_type or "tcp",
                        "security": s.security or "none"
                    },
                    "tag": "proxy"
                },
                {"protocol": "freedom", "tag": "direct"},
                {"protocol": "blackhole", "tag": "block"}
            ],
            "meta": {"serverDescription": s.country_name},
            "dns": {"servers": ["1.1.1.1", "1.0.0.1"], "queryStrategy": "UseIP"},
            "inbounds": [
                {"settings": {"udp": True, "auth": "noauth"}, "protocol": "socks", "port": 10808, "tag": "socks", "listen": "127.0.0.1"},
                {"settings": {"allowTransparent": False}, "protocol": "http", "port": 10809, "tag": "http", "listen": "127.0.0.1"}
            ],
            "remarks": name
        }

        if s.security == "reality":
            full_cfg["outbounds"][0]["streamSettings"]["realitySettings"] = {
                "fingerprint": s.fp or "chrome",
                "serverName": s.sni or s.host,
                "publicKey": s.pbk or "",
                "shortId": s.sid or "",
                "spiderX": ""
            }
        elif s.security == "tls":
            full_cfg["outbounds"][0]["streamSettings"]["tlsSettings"] = {
                "fingerprint": s.fp or "chrome",
                "serverName": s.sni or s.host,
                "allowInsecure": True
            }

        if s.net_type == "grpc":
            full_cfg["outbounds"][0]["streamSettings"]["grpcSettings"] = {
                "serviceName": s.params.get("serviceName", "")
            }
        elif s.net_type == "ws":
            full_cfg["outbounds"][0]["streamSettings"]["wsSettings"] = {
                "path": s.path or "/",
                "headers": {"Host": s.host_header or s.sni or s.host}
            }

        cur.execute("""
            INSERT INTO servers (
                id, name, address, port, proxyProtocol, uuid, flow, encryption,
                network, security, sni, fingerprint, publicKey, shortId,
                path, host, serviceName, fullConfigJson, subscriptionId,
                latency, createdAt, orderIndex, customDescription
            ) VALUES (?, ?, ?, ?, 'VLESS', ?, ?, 'none', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            srv_id, name, s.host, s.port, s.uuid, s.flow or "",
            s.net_type or "tcp", s.security or "none", s.sni or s.host,
            s.fp or "chrome", s.pbk or None, s.sid or None,
            s.path or None, s.host_header or None, s.params.get("serviceName"),
            json.dumps(full_cfg, ensure_ascii=False), sub_id,
            s.latency_ms, now_ms, idx, s.country_name
        ))

    con.commit()
    con.close()
    print(f"[+] Подписка успешно обновлена в Incy! Добавлено {len(servers)} серверов с реальным пингом!")


def main():
    print("=" * 65)
    print(" 🚀 ТОЧНАЯ ПРОВЕРКА ЧЕРЕЗ INCY XRAY НА ВАШЕМ ПК")
    print("=" * 65)

    raw_configs = fetch_all_raw_configs()
    print(f"[*] Собрано сырых конфигураций со всех файлов: {len(raw_configs)}")

    parser = ProxyParser()
    candidates = []
    seen = set()

    for line in raw_configs:
        n = parser.parse(line)
        if not n or not n.is_alive:
            continue
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
        candidates.append(n)

    print(f"[*] Валидных VLESS Reality/TLS кандидатов: {len(candidates)}")

    # Test with Incy Xray in parallel
    concurrency = 25
    args_list = [(n, i % concurrency) for i, n in enumerate(candidates[:350])]

    print(f"[*] Запуск проверки реального трафика (HTTP 204) в {concurrency} потоков...")
    t0 = time.time()
    verified: List[ProxyNode] = []
    geoip = GeoIPResolver()

    # Pre-resolve GeoIP
    missing_ips = [n.host for n in candidates]
    geo_map = geoip.resolve_batch_ips(missing_ips)

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        for res in executor.map(test_node_xray, args_list):
            if res is not None:
                # Set GeoIP
                if res.host in geo_map:
                    inf = geo_map[res.host]
                    res.country_code = inf.get("code", "EU")
                    res.country_flag = inf.get("flag", "🇪🇺")
                    res.country_name = inf.get("name_ru", "Европа")
                else:
                    c_info = geoip.detect_from_remark(res.remark)
                    if c_info:
                        res.country_code, res.country_flag, res.country_name = c_info
                    else:
                        res.country_code = "EU"
                        res.country_flag = "🇪🇺"
                        res.country_name = "Европа"

                # Detect Whitelist
                if is_wl(res.sni, res.remark):
                    res.is_whitelist = True
                    lower = (res.sni + " " + res.remark).lower()
                    if "yandex" in lower or "dzen" in lower:
                        res.whitelist_label = "🛡️ Яндекс/Дзен"
                    elif "vk" in lower:
                        res.whitelist_label = "🛡️ VK"
                    elif "gosuslugi" in lower:
                        res.whitelist_label = "🛡️ Госуслуги"
                    else:
                        res.whitelist_label = "🛡️ Whitelist"
                else:
                    res.is_whitelist = False

                verified.append(res)
                sys.stdout.write(f"\r  [+] Найдено рабочих: {len(verified)} ({res.country_flag} {res.country_name} • {res.latency_ms}ms)")
                sys.stdout.flush()

    elapsed = round(time.time() - t0, 1)
    print(f"\n\n[+] Проверка завершена за {elapsed} сек!")
    print(f"    • 100% РАБОЧИХ УЗЛОВ: {len(verified)}")

    if not verified:
        print("[!] Нет подтвержденных рабочих серверов.")
        return

    # Categorize exactly according to user:
    # 1. Foreign general (non-RU, non-whitelist) -> Top of subscription!
    foreign_gen = [n for n in verified if n.country_code != "RU" and not n.is_whitelist]
    foreign_gen.sort(key=lambda x: x.latency_ms)

    # 2. Foreign Whitelist (Зарубежные сервера с SNI под VK / Госуслуги / Яндекс!) -> обходят глушение РФ и дают открытый доступ к миру!
    foreign_wl = [n for n in verified if n.country_code != "RU" and n.is_whitelist]
    foreign_wl.sort(key=lambda x: x.latency_ms)

    # 3. Russian General
    ru_gen = [n for n in verified if n.country_code == "RU" and not n.is_whitelist]
    ru_gen.sort(key=lambda x: x.latency_ms)

    # 4. Russian Whitelist (на самый низ)
    ru_wl = [n for n in verified if n.country_code == "RU" and n.is_whitelist]
    ru_wl.sort(key=lambda x: x.latency_ms)

    print(f"    • Зарубежные скоростные (НЕ Россия):  {len(foreign_gen)}")
    print(f"    • Зарубежные Whitelist (Обход + мир): {len(foreign_wl)}")
    print(f"    • Российские обычные:                 {len(ru_gen)}")
    print(f"    • Российские Whitelist (В самом низу):{len(ru_wl)}")

    # Ordered list
    final_ordered = foreign_gen + foreign_wl + ru_gen + ru_wl

    # Save to JSON
    out_data = {
        "timestamp": time.time(),
        "total": len(final_ordered),
        "servers": [n.to_dict() for n in final_ordered]
    }
    with open(os.path.join(DATA_DIR, "alive_servers.json"), "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)

    # Deploy to Cloudflare Workers
    print("\n[*] Сборка и деплой на Cloudflare Workers...")
    script = generate_worker_js([n.to_dict() for n in final_ordered])
    deploy_to_cloudflare(script)

    # Inject directly into Incy DB
    inject_into_incy_db(final_ordered)

    print("\n" + "=" * 65)
    print(" ✅ ВСЕ СЕРВЕРЫ ПРОВЕРЕНЫ И ИНТЕГРИРОВАНЫ В INCY!")
    print("=" * 65)


if __name__ == "__main__":
    main()
