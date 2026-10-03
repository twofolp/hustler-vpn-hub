#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloud 24/7 Automated VLESS Checker & Cloudflare Deployer
Runs anywhere: on Linux (GitHub Actions / Cloud VPS) or Windows.
1. Downloads Xray automatically if not installed.
2. Aggregates configs from 134+ online sources + local sources.
3. Tests candidates in 35 parallel workers using real Xray HTTP 204 requests.
4. Resolves GeoIP and strictly categorizes (Foreign Fast, Foreign Whitelist, Russian Whitelist).
5. Deploys fresh pool to Cloudflare Workers API without requiring any local PC.
"""

import os
import re
import sys
import json
import time
import socket
import base64
import platform
import subprocess
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
SOURCES_DIR = os.path.join(BASE_DIR, "sources")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SOURCES_DIR, exist_ok=True)

from core.parser import ProxyNode
from core.geoip import COUNTRY_MAP
from build_worker import generate_worker_js, deploy_to_cloudflare

# Load environment variables from .env if present
_env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(_env_path):
    with open(_env_path, "r", encoding="utf-8") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

# Cloudflare & Telegram Credentials (supports environment variables for CI/CD)
CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID", "0cce12c9f195e5f0bfe609e85d1a810e")
CF_API_TOKEN = os.getenv("CF_API_TOKEN", "")
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "8869884346:AAGZ0zL0_znst6qZo27fdYMKBeZGleOZAEg")

# Specialized Whitelist Upstreams
WHITELIST_SOURCES = [
    "https://raw.githubusercontent.com/wlunlocker/vpn-configs/main/whitelist_cidr3_eu.txt",
    "https://raw.githubusercontent.com/wlunlocker/vpn-configs/main/whitelist_cidr1_ru.txt",
    "https://raw.githubusercontent.com/wlunlocker/vpn-configs/main/whitelist_cidr2_ru.txt",
    "https://raw.githubusercontent.com/wlunlocker/vpn-configs/main/whitelist_all.txt",
    "https://raw.githubusercontent.com/hussaroff/lte-universal-checked/main/whitelist.txt",
    "https://raw.githubusercontent.com/RKPchannel/RKP_bypass_configs/main/whitelist.txt",
    "https://raw.githubusercontent.com/flaafix/AetrisVPN-white-list-lite/main/AetrisVPN.txt",
    "https://raw.githubusercontent.com/Sanuyyq/sub-storage1/refs/heads/main/bs.txt",
    "https://raw.githubusercontent.com/SilentGhostCodes/WhiteListVpn/refs/heads/main/Whitelist.txt",
    "https://raw.githubusercontent.com/SilentGhostCodes/WhiteListVpn/refs/heads/main/Whitelist%20%E2%84%962.txt",
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_universal.txt",
    "https://raw.githubusercontent.com/ByeWhiteLists/ByeWhiteLists2/refs/heads/main/ByeWhiteLists2.txt",
    "https://raw.githubusercontent.com/histeenn/VLESS-PO-GRIBI/main/deploy/sub.txt"
]

WL_KEYWORDS = [
    "yandex.ru", "ya.ru", "dzen.ru", "passport.yandex.ru", "360.yandex.ru",
    "vk.com", "vk.me", "userapi.com", "vk-portal.net", "vk.ru",
    "gosuslugi.ru", "esia.gosuslugi.ru", "gu-st.ru",
    "mail.ru", "sber.ru", "sberbank.ru", "tinkoff.ru", "t-bank.ru",
    "avito.ru", "ozon.ru", "wildberries.ru", "kinopoisk.ru",
    "api.dobro.ru", "ligastavok.ru", "utiltools.ru", "utiltools.site",
    "guardora.pro", "bobrkurva.shop", "dora-dura.shop", "soxy-boobs.shop",
    "drom-buy.help", "support-pay-api.help", "ads.x5.ru", "dl.google.com"
]

def find_or_download_xray() -> str:
    """Finds Xray executable or downloads it on Linux."""
    # 1. Custom path
    custom = os.getenv("XRAY_PATH")
    if custom and os.path.exists(custom):
        return custom

    # 2. Windows Incy path
    if platform.system() == "Windows":
        candidates = [
            r"C:\Program Files\INCY\app\resources\bin\xray.exe",
            os.path.join(BASE_DIR, "xray.exe")
        ]
        for c in candidates:
            if os.path.exists(c):
                return c

    # 3. Linux / Path
    if shutil_which := subprocess.run(["which", "xray"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True).stdout.strip():
        if os.path.exists(shutil_which):
            return shutil_which

    local_bin = os.path.join(BASE_DIR, "xray")
    if os.path.exists(local_bin):
        return local_bin

    # 4. Download on Linux
    if platform.system() == "Linux":
        print("[*] Скачивание Xray Core для Linux...")
        url = "https://github.com/XTLS/Xray-core/releases/download/v26.7.28/Xray-linux-64.zip"
        zip_path = os.path.join(BASE_DIR, "xray.zip")
        try:
            urllib.request.urlretrieve(url, zip_path)
            import zipfile
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extract('xray', BASE_DIR)
            os.chmod(local_bin, 0o755)
            if os.path.exists(zip_path):
                os.remove(zip_path)
            print("[+] Xray Core успешно установлен!")
            return local_bin
        except Exception as e:
            print(f"[!] Не удалось скачать Xray: {e}")

    return "xray"


TOXIC_SNIS = [
    "speed.cloudflare.com", "yahoo.com", "speedtest.net", "aws.amazon.com", "amazon.com"
]

def is_toxic_sni(sni: str) -> bool:
    s = (sni or "").lower()
    return any(t in s for t in TOXIC_SNIS)

def is_wl(sni: str, remark: str = "") -> bool:
    s = (sni or "").lower() + " " + (remark or "").lower()
    return any(p in s for p in WL_KEYWORDS)

def get_wl_label(sni: str, remark: str = "") -> str:
    s = (sni or "").lower() + " " + (remark or "").lower()
    if "passport.yandex" in s or "360.yandex" in s or "ya.ru" in s or "yandex" in s or "dzen" in s:
        return "🛡️ Яндекс/Дзен"
    if "vk" in s or "userapi" in s:
        return "🛡️ VK"
    if "google" in s:
        return "🛡️ Google-DL"
    if "x5.ru" in s:
        return "🛡️ X5-Retail"
    if "gosuslugi" in s or "gu-st" in s:
        return "🛡️ Госуслуги"
    if "sber" in s or "tinkoff" in s:
        return "🛡️ Банки"
    return "🛡️ Whitelist"


def fetch_one_source(url: str) -> List[str]:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    configs = []
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read()
            text = data.decode("utf-8", errors="ignore")
            # If base64
            clean = text.strip().replace("\r", "").replace("\n", "")
            if clean and not clean.startswith("vless://") and not "<html" in clean.lower():
                try:
                    pad = len(clean) % 4
                    if pad > 0:
                        clean += "=" * (4 - pad)
                    dec = base64.b64decode(clean).decode("utf-8", errors="ignore")
                    if "vless://" in dec:
                        text = dec
                except Exception:
                    pass
            for line in re.findall(r"vless://[^\s<>\"\'\n\r]+", text):
                line = line.strip()
                if line and "ezhik" not in line.lower():
                    configs.append(line)
    except Exception:
        pass
    return configs


def collect_all_candidates() -> List[ProxyNode]:
    print("[*] Сбор конфигураций со всех источников (Whitelist + Все файлы подписок)...")
    sources_to_fetch = set(WHITELIST_SOURCES)

    # Local sources files
    for fname in ["vpn.txt", "sort_needed.txt"]:
        fpath = os.path.join(SOURCES_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("http"):
                        sources_to_fetch.add(line.rstrip(".,;)"))

    print(f"[*] Всего опрашиваемых URL источников: {len(sources_to_fetch)}")
    all_raw = []
    with ThreadPoolExecutor(max_workers=30) as ex:
        for cfgs in ex.map(fetch_one_source, list(sources_to_fetch)):
            all_raw.extend(cfgs)

    unique_raw = list(set(all_raw))
    print(f"[+] Собрано уникальных VLESS строк: {len(unique_raw)}")

    nodes = []
    seen = set()
    for raw in unique_raw:
        n = ProxyNode(raw)
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

    print(f"[+] Валидных уникальных узлов (без CDN): {len(nodes)}")
    return nodes


def test_node_probe(args):
    node, worker_id, xray_bin = args
    port = 12000 + (worker_id % 200)

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

    cfg_file = os.path.join(DATA_DIR, f"cprobe_{worker_id}.json")
    with open(cfg_file, "w", encoding="utf-8") as pf:
        json.dump(cfg, pf)

    proc = subprocess.Popen([xray_bin, "run", "-c", cfg_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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


def run_full_check():
    print("=" * 65)
    print(" 🚀 АВТОМАТИЧЕСКИЙ ОБЛАЧНЫЙ ЧЕКЕР VLESS HUB (24/7/365)")
    print("=" * 65)

    xray_bin = find_or_download_xray()
    print(f"[*] Используемый бинарник Xray: {xray_bin}")

    # 1. Load existing pool
    alive_file = os.path.join(DATA_DIR, "alive_servers.json")
    existing_servers = []
    seen_keys = set()

    if os.path.exists(alive_file):
        try:
            with open(alive_file, "r", encoding="utf-8") as f:
                existing_servers = json.load(f).get("servers", [])
        except Exception:
            existing_servers = []

    print(f"[*] Текущий базовый пул: {len(existing_servers)} серверов")

    # 2. Re-test existing servers to prune dead ones and measure fresh latency
    concurrency = 50
    surviving_nodes = []
    if existing_servers:
        print("[*] Экспресс-проверка текущего пула (проверка живых серверов)...")
        existing_proxy_nodes = []
        for s in existing_servers:
            uri = s.get("uri") or f"vless://{s.get('uuid')}@{s.get('host')}:{s.get('port')}?type={s.get('type')}&security={s.get('security')}&sni={s.get('sni')}"
            n = ProxyNode(uri)
            if n and n.is_valid:
                # restore metadata
                n.country_code = s.get("country_code", "OTHER")
                n.country_flag = s.get("country_flag", "🌐")
                n.country_name = s.get("country_name", "Зарубежный")
                n.is_whitelist = s.get("is_whitelist", False)
                n.whitelist_label = s.get("whitelist_label", "")
                existing_proxy_nodes.append(n)
                seen_keys.add(f"{n.host}:{n.port}")

        args_ex = [(n, i, xray_bin) for i, n in enumerate(existing_proxy_nodes)]
        with ThreadPoolExecutor(max_workers=concurrency) as ex:
            for res in ex.map(test_node_probe, args_ex):
                if res is not None:
                    surviving_nodes.append(res)

        print(f"[+] Из текущего пула подтверждено живых: {len(surviving_nodes)} из {len(existing_servers)}")

    # 3. Collect candidates to replenish pool
    candidates = collect_all_candidates()

    new_candidates = [n for n in candidates if f"{n.host}:{n.port}" not in seen_keys]
    wl_nodes = [n for n in new_candidates if is_wl(n.sni, n.remark)]
    gen_nodes = [n for n in new_candidates if not is_wl(n.sni, n.remark) and not is_toxic_sni(n.sni)]

    print(f"  • Свежих кандидатов с Whitelist SNI: {len(wl_nodes)}")
    print(f"  • Свежих обычных кандидатов (без токсичных SNI): {len(gen_nodes)}")

    # Test large fresh batch: up to 800 whitelist + 800 general candidates
    batch = wl_nodes[:800] + gen_nodes[:800]
    args_list = [(n, i + len(surviving_nodes), xray_bin) for i, n in enumerate(batch)]

    print(f"[*] Проверка {len(batch)} новых кандидатов для пополнения пула...")
    t0 = time.time()
    newly_verified: List[ProxyNode] = []

    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        for res in ex.map(test_node_probe, args_list):
            if res is not None:
                newly_verified.append(res)
                sys.stdout.write(f"\r  [+] Добавлен новый рабочий: {len(newly_verified)} ({res.host} • {res.latency_ms}ms)")
                sys.stdout.flush()

    elapsed = round(time.time() - t0, 1)
    print(f"\n\n[+] Проверка новых кандидатов завершена за {elapsed} сек! Найдено: {len(newly_verified)}")

    verified = surviving_nodes + newly_verified
    print(f"[+] Всего подтвержденных серверов в пуле: {len(verified)}")

    if not verified:
        print("[!] Нет живых узлов, откат.")
        return

    # GeoIP resolution
    print("[*] Определение геолокации и стран для рабочих узлов...")
    results = []
    for node in verified:
        d = node.to_dict()
        if is_wl(node.sni, node.remark):
            d["is_whitelist"] = True
            d["whitelist_label"] = get_wl_label(node.sni, node.remark)
        else:
            d["is_whitelist"] = False
            d["whitelist_label"] = ""

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
        time.sleep(0.03)

    # 4 Strict categories:
    foreign_gen = [s for s in results if s.get("country_code") != "RU" and not s.get("is_whitelist")]
    foreign_gen.sort(key=lambda x: x.get("latency_ms", 9999))

    foreign_wl = [s for s in results if s.get("country_code") != "RU" and s.get("is_whitelist")]
    foreign_wl.sort(key=lambda x: x.get("latency_ms", 9999))

    ru_wl = [s for s in results if s.get("country_code") == "RU" and s.get("is_whitelist")]
    ru_wl.sort(key=lambda x: x.get("latency_ms", 9999))

    ru_gen = [s for s in results if s.get("country_code") == "RU" and not s.get("is_whitelist")]
    ru_gen.sort(key=lambda x: x.get("latency_ms", 9999))

    ordered = foreign_gen + foreign_wl + ru_wl + ru_gen

    print("\n" + "=" * 60)
    print(" 📊 ИТОГОВАЯ СТАТИСТИКА ПРОВЕРКИ:")
    print("=" * 60)
    print(f" • Зарубежные скоростные (НЕ Россия, Открытый мир): {len(foreign_gen)}")
    print(f" • Зарубежные Whitelist (Европа + SNI РФ • Обход):  {len(foreign_wl)}")
    print(f" • Российские Whitelist (РФ узлы • Антиглушилки):    {len(ru_wl)}")
    print(f" • Российские обычные:                                {len(ru_gen)}")
    print(f" [+] ИТОГО 100% РАБОЧИХ УЗЛОВ:                        {len(ordered)}")

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
    with open(os.path.join(DATA_DIR, "alive_servers.json"), "w", encoding="utf-8") as f:
        json.dump(out_payload, f, ensure_ascii=False, indent=2)

    with open(os.path.join(DATA_DIR, "alive_servers.txt"), "w", encoding="utf-8") as f:
        for s in ordered:
            f.write(s.get("uri", "") + "\n")

    # Deploy to Cloudflare Workers
    print("\n[*] Деплой на Cloudflare Workers...")
    worker_js = generate_worker_js(ordered)
    deploy_to_cloudflare(worker_js)
    print("\n[+] Деплой на Cloudflare успешно завершен!")


if __name__ == "__main__":
    run_full_check()
