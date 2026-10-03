#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import subprocess
import time
import urllib.request
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

XRAY_BIN = r"C:\Program Files\INCY\app\resources\bin\xray.exe"

def test_pool():
    with open("data/alive_servers.json", "r", encoding="utf-8") as f:
        servers = json.load(f)["servers"]

    print(f"Testing {len(servers)} servers from pool with REAL Xray HTTP probe...")
    working = []

    for idx, s in enumerate(servers):
        port = 10920 + (idx % 25)

        cfg = {
            "log": {"loglevel": "none"},
            "inbounds": [{"listen": "127.0.0.1", "port": port, "protocol": "http"}],
            "outbounds": [{
                "protocol": "vless",
                "settings": {
                    "vnext": [{
                        "address": s["host"],
                        "port": int(s["port"]),
                        "users": [{"id": s["uuid"], "encryption": "none", "flow": s.get("flow") or ""}]
                    }]
                },
                "streamSettings": {
                    "network": s.get("type") or "tcp",
                    "security": s.get("security") or "none"
                },
                "tag": "proxy"
            }]
        }

        sec = s.get("security")
        if sec == "reality":
            cfg["outbounds"][0]["streamSettings"]["realitySettings"] = {
                "fingerprint": s.get("fp") or "chrome",
                "serverName": s.get("sni") or s["host"],
                "publicKey": s.get("pbk") or "",
                "shortId": s.get("sid") or "",
                "spiderX": ""
            }
        elif sec == "tls":
            cfg["outbounds"][0]["streamSettings"]["tlsSettings"] = {
                "fingerprint": s.get("fp") or "chrome",
                "serverName": s.get("sni") or s["host"],
                "allowInsecure": True
            }

        net = s.get("type")
        if net == "grpc":
            cfg["outbounds"][0]["streamSettings"]["grpcSettings"] = {
                "serviceName": s.get("serviceName") or ""
            }
        elif net == "ws":
            cfg["outbounds"][0]["streamSettings"]["wsSettings"] = {
                "path": s.get("path") or "/",
                "headers": {"Host": s.get("host_header") or s.get("sni") or s["host"]}
            }

        cfg_file = f"probe_{idx}.json"
        with open(cfg_file, "w") as pf:
            json.dump(cfg, pf)

        proc = subprocess.Popen([XRAY_BIN, "run", "-c", cfg_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.35)

        handler = urllib.request.ProxyHandler({"http": f"http://127.0.0.1:{port}"})
        opener = urllib.request.build_opener(handler)
        t0 = time.perf_counter()
        ok = False
        lat = -1
        try:
            resp = opener.open("http://cp.cloudflare.com/generate_204", timeout=2.0)
            if resp.status == 204:
                lat = int((time.perf_counter() - t0) * 1000)
                ok = True
        except Exception:
            pass
        finally:
            proc.terminate()
            try:
                os.remove(cfg_file)
            except Exception:
                pass

        if ok:
            s["latency_ms"] = lat
            working.append(s)
            flag = s.get("country_flag", "")
            cname = s.get("country_name", "")
            cc = s.get("country_code", "")
            print(f"  [{len(working)}] {flag} {cname} ({cc}) {s['host']}:{s['port']} -> {lat}ms")

    print(f"\nTOTAL GUARANTEED WORKING IN INCY: {len(working)} / {len(servers)}")

    with open("data/strictly_verified_servers.json", "w", encoding="utf-8") as wf:
        json.dump({"servers": working, "count": len(working)}, wf, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    test_pool()
