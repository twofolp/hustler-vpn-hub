#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import re

urls = [
    'https://raw.githubusercontent.com/zieng2/wl/main/vless_universal.txt',
    'https://raw.githubusercontent.com/ByeWhiteLists/ByeWhiteLists2/refs/heads/main/ByeWhiteLists2.txt',
    'https://raw.githubusercontent.com/SilentGhostCodes/WhiteListVpn/refs/heads/main/Whitelist.txt',
    'https://raw.githubusercontent.com/SilentGhostCodes/WhiteListVpn/refs/heads/main/Whitelist%20%E2%84%962.txt',
    'https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-checked.txt',
    'https://gitverse.ru/api/repos/cid-uskoritel/cid-white/raw/branch/master/whitelist.txt'
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'curl/7.68.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            text = resp.read().decode('utf-8', errors='ignore')
            vless = re.findall(r'vless://[^\s<>\"\'\n\r]+', text)
            print(u.split('/')[-1], '->', len(vless), 'configs')
            if vless:
                print('  Sample:', vless[0][:110])
    except Exception as e:
        print(u.split('/')[-1], 'ERR:', e)
