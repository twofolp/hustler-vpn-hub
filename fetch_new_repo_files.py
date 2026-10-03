#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import re
import json

repos = [
    "RKPchannel/RKP_bypass_configs",
    "VOID-Anonymity/V.O.I.D-VPN_Bypass",
    "rom5n/whitelist-download",
    "wlunlocker/vpn-configs",
    "hussaroff/lte-universal-checked",
    "flaafix/AetrisVPN",
    "flaafix/AetrisVPN-white-list-lite",
    "kudryash0vv/kudryash0vv.YKTFLOW",
    "Amberpiclippers/vpn-configs-for-russia-region",
    "jsxta/whitelist-russia",
    "aviamastersgh/vpn-free-russia"
]

headers = {"User-Agent": "Mozilla/5.0"}
discovered_links = []

for r in repos:
    api_url = f"https://api.github.com/repos/{r}/contents"
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            files = json.loads(resp.read().decode("utf-8"))
            for f in files:
                name = f.get("name", "")
                d_url = f.get("download_url")
                if d_url and (name.endswith(".txt") or name.endswith(".json") or "vless" in name.lower() or "white" in name.lower() or "sub" in name.lower()):
                    print(f"Found source: {r} -> {name}: {d_url}")
                    discovered_links.append(d_url)
    except Exception as e:
        print(f"Error {r}: {e}")

with open("data/new_discovered_raw_links.json", "w", encoding="utf-8") as f:
    json.dump(discovered_links, f, ensure_ascii=False, indent=2)
print(f"Total new raw sources discovered: {len(discovered_links)}")
