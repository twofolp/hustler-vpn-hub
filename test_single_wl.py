#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import time
import subprocess
import urllib.request
from core.parser import ProxyNode

# Sample node from WHITE-CIDR-RU-checked:
# vless://4643976f-85fa-40cf-9e58-ea28b50f253b@37.139.42.225:7448?type=tcp&headerType=none&security=reality&encryption=none&pbk=SB1uC0OEveYjSiS_Nuw9Ld-uVVXWqi794OGnldthY3I&fp=chrome&sni=passport.yandex.ru&sid=51314467140f0c0b&spx=%2F&flow=xtls-rprx-vision#%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F+%23001
url = "vless://4643976f-85fa-40cf-9e58-ea28b50f253b@37.139.42.225:7448?type=tcp&headerType=none&security=reality&encryption=none&pbk=SB1uC0OEveYjSiS_Nuw9Ld-uVVXWqi794OGnldthY3I&fp=chrome&sni=passport.yandex.ru&sid=51314467140f0c0b&spx=%2F&flow=xtls-rprx-vision#%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F+%23001"
node = ProxyNode(url)

port = 11999
cfg = {
    "log": {"loglevel": "debug"},
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
            "security": "reality",
            "realitySettings": {
                "fingerprint": node.fp or "chrome",
                "serverName": node.sni or node.host,
                "publicKey": node.pbk,
                "shortId": node.sid or "",
                "spiderX": "/"
            }
        },
        "tag": "proxy"
    }]
}

with open("data/test_single.json", "w") as f:
    json.dump(cfg, f)

proc = subprocess.Popen([r"C:\Program Files\INCY\app\resources\bin\xray.exe", "run", "-c", "data/test_single.json"])
time.sleep(0.5)

handler = urllib.request.ProxyHandler({"http": f"http://127.0.0.1:{port}"})
opener = urllib.request.build_opener(handler)

for target in ["http://cp.cloudflare.com/generate_204", "http://connectivitycheck.gstatic.com/generate_204", "http://ya.ru"]:
    try:
        t0 = time.time()
        resp = opener.open(target, timeout=3)
        print(f"Target: {target} -> STATUS: {resp.status} in {int((time.time()-t0)*1000)}ms")
    except Exception as e:
        print(f"Target: {target} -> ERR: {e}")

proc.terminate()
