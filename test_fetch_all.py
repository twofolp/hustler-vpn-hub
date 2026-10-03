#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-threaded fetcher for ALL 134 sources in:
- Desktop/впн.txt
- Desktop/отсортировать надо.txt
- VLESS-PO-GRIBI main sub.txt
"""

import os
import re
import sys
import time
import base64
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from typing import List, Set, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def get_clean_urls() -> List[str]:
    files = [r"C:\Users\twofolp\Desktop\впн.txt", r"C:\Users\twofolp\Desktop\отсортировать надо.txt"]
    all_urls = set()
    pat = re.compile(r"https?://[^\s<>\"\'\n\r]+")

    for fpath in files:
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            for u in pat.findall(text):
                u = u.rstrip(".,;:)")
                if "translate.yandex" in u or not u:
                    continue
                # Transform github repo URLs to raw or known sub files if applicable
                if "github.com/" in u and "/raw/" not in u and "gist.github.com" not in u and not u.endswith(".txt"):
                    # e.g. https://github.com/AvenCores/goida-vpn-configs
                    repo = u.replace("https://github.com/", "").strip("/")
                    # Try common branch files
                    all_urls.add(f"https://raw.githubusercontent.com/{repo}/main/sub.txt")
                    all_urls.add(f"https://raw.githubusercontent.com/{repo}/master/sub.txt")
                    all_urls.add(f"https://raw.githubusercontent.com/{repo}/main/output/v2ray-base64.txt")
                    all_urls.add(f"https://raw.githubusercontent.com/{repo}/main/output/v2ray.txt")
                    all_urls.add(f"https://raw.githubusercontent.com/{repo}/main/vless.txt")
                else:
                    all_urls.add(u)

    # Also add VLESS-PO-GRIBI main
    all_urls.add("https://raw.githubusercontent.com/histeenn/VLESS-PO-GRIBI/main/deploy/sub.txt")
    return sorted(list(all_urls))

def decode_content(raw_bytes: bytes) -> str:
    # Try utf-8 first
    try:
        text = raw_bytes.decode("utf-8", errors="ignore")
    except Exception:
        text = ""

    # Check if base64 encoded
    clean = text.strip().replace("\r", "").replace("\n", "")
    if clean and not clean.startswith("vless://") and not clean.startswith("vmess://") and not "<html" in clean.lower():
        try:
            pad = len(clean) % 4
            if pad > 0:
                clean += "=" * (4 - pad)
            dec = base64.b64decode(clean).decode("utf-8", errors="ignore")
            if "vless://" in dec or "vmess://" in dec:
                return dec
        except Exception:
            pass
    return text

def fetch_one(url: str) -> Tuple[str, List[str]]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    configs = []
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=7) as resp:
            if resp.status == 200:
                data = resp.read()
                text = decode_content(data)
                # Extract vless configs
                vless_lines = re.findall(r"vless://[^\s<>\"\'\n\r]+", text)
                for v in vless_lines:
                    v_clean = v.strip()
                    if v_clean and "ezhik" not in v_clean.lower():
                        configs.append(v_clean)
    except Exception:
        pass
    return url, configs

def main():
    urls = get_clean_urls()
    print(f"[*] Сформирован список из {len(urls)} целевых URL источников...")
    print(f"[*] Запуск параллельного сбора в 30 потоков...")

    t0 = time.time()
    total_configs = []
    successful_sources = 0

    with ThreadPoolExecutor(max_workers=30) as ex:
        for url, configs in ex.map(fetch_one, urls):
            if configs:
                successful_sources += 1
                total_configs.extend(configs)
                sys.stdout.write(f"\r  [+] Успешно ответил: {successful_sources} источников | Собрано конфигов: {len(total_configs)}")
                sys.stdout.flush()

    elapsed = round(time.time() - t0, 1)
    unique_configs = list(set(total_configs))
    print(f"\n\n[+] Сбор завершен за {elapsed} сек!")
    print(f"    • Ответивших источников: {successful_sources} из {len(urls)}")
    print(f"    • Всего собрано строк vless: {len(total_configs)}")
    print(f"    • Уникальных VLESS конфигураций: {len(unique_configs)}")

if __name__ == "__main__":
    main()
