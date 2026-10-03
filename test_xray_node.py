#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import json
import time
import urllib.request
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

XRAY_BIN = r"C:\Program Files\INCY\app\resources\bin\xray.exe"

def test_vless_via_xray(node: dict, port=10855, timeout=4.0):
    cfg = {
        "log": {"loglevel": "none"},
        "inbounds": [
            {
                "listen": "127.0.0.1",
                "port": port,
                "protocol": "http",
                "settings": {"allowTransparent": False}
            }
        ],
        "outbounds": [
            {
                "protocol": "vless",
                "settings": {
                    "vnext": [
                        {
                            "address": node["host"],
                            "port": int(node["port"]),
                            "users": [
                                {
                                    "id": node["uuid"],
                                    "encryption": "none",
                                    "flow": node.get("flow") or ""
                                }
                            ]
                        }
                    ]
                },
                "streamSettings": {
                    "network": node.get("type") or "tcp",
                    "security": node.get("security") or "none"
                },
                "tag": "proxy"
            }
        ]
    }

    sec = node.get("security")
    if sec == "reality":
        cfg["outbounds"][0]["streamSettings"]["realitySettings"] = {
            "fingerprint": node.get("fp") or "chrome",
            "serverName": node.get("sni") or node["host"],
            "publicKey": node.get("pbk") or "",
            "shortId": node.get("sid") or "",
            "spiderX": ""
        }
    elif sec == "tls":
        cfg["outbounds"][0]["streamSettings"]["tlsSettings"] = {
            "fingerprint": node.get("fp") or "chrome",
            "serverName": node.get("sni") or node["host"],
            "allowInsecure": True
        }

    net = node.get("type")
    if net == "grpc":
        cfg["outbounds"][0]["streamSettings"]["grpcSettings"] = {
            "serviceName": node.get("serviceName") or ""
        }
    elif net == "ws":
        cfg["outbounds"][0]["streamSettings"]["wsSettings"] = {
            "path": node.get("path") or "/",
            "headers": {"Host": node.get("host_header") or node.get("sni") or node["host"]}
        }

    cfg_path = os.path.abspath(f"scratch/test_cfg_{port}.json")
    os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

    # Start Xray process
    proc = subprocess.Popen(
        [XRAY_BIN, "run", "-c", cfg_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    time.sleep(0.3)
    t0 = time.perf_counter()
    proxy_handler = urllib.request.ProxyHandler({
        "http": f"http://127.0.0.1:{port}",
        "https": f"http://127.0.0.1:{port}"
    })
    opener = urllib.request.build_opener(proxy_handler)
    req = urllib.request.Request(
        "http://cp.cloudflare.com/generate_204",
        headers={"User-Agent": "Mozilla/5.0"}
    )

    is_ok = False
    latency_ms = -1
    err_msg = ""

    try:
        with opener.open(req, timeout=timeout) as resp:
            if resp.status in (200, 204):
                latency_ms = int((time.perf_counter() - t0) * 1000)
                is_ok = True
    except Exception as e:
        err_msg = str(e)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=1.0)
        except Exception:
            proc.kill()
        try:
            os.remove(cfg_path)
        except Exception:
            pass

    return is_ok, latency_ms, err_msg


if __name__ == "__main__":
    with open("data/alive_servers.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    servers = data["servers"]
    print(f"Testing first 5 servers from current pool using Incy's Xray binary:")
    for idx, s in enumerate(servers[:8]):
        ok, lat, err = test_vless_via_xray(s, port=10850 + idx)
        remark = s.get("remark", "")
        status = f"✅ {lat}ms" if ok else f"❌ N/A ({err[:40]})"
        print(f"[{idx+1}] {remark} -> {status}")
