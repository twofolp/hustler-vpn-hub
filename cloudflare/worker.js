/**
 * 🍄 HUSTLER VPN • Cloudflare Smart Hub & Telegram Bot
 * Features:
 * - Telegram WebApp Mini App (/app)
 * - Personalized User Subscriptions (/sub/u/:userId)
 * - 1-Click "Добавить в Incy" & "Добавить в Happ"
 * - 100% Clean Server Names (Flag + Country Name + Tag + Ping)
 * - Auto-Failover per country
 */

const BOT_TOKEN = "8869884346:AAGZ0zL0_znst6qZo27fdYMKBeZGleOZAEg";
const SYNC_SECRET = "hustler_secret_2026";

// Verified server pool with clean remarks
let CACHED_SERVERS = [{"protocol": "vless", "host": "199.232.78.143", "port": 443, "uuid": "60cfd7f1-c24a-4ef0-97a3-1fb66437de13", "security": "tls", "sni": "edge.microsoft.com", "pbk": "", "sid": "", "flow": "", "type": "xhttp", "remark": "🇺🇸 США [🎮 Игровой] • 82ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "US", "country_flag": "🇺🇸", "country_name": "США", "latency_ms": 82, "is_alive": true, "source_id": null, "uri": "vless://60cfd7f1-c24a-4ef0-97a3-1fb66437de13@199.232.78.143:443?mode=auto&pcs=cd6e838b9bfe31cab8b3d5c858b0d6223fe84ece236c1fdb281be93c302e1e6e&path=%2F&security=tls&alpn=h2&encryption=none&insecure=0&host=Napalexp.global.ssl.fastly.net&fp=edge&type=xhttp&allowInsecure=0&sni=edge.microsoft.com#%F0%9F%87%BA%F0%9F%87%B8%20%D0%A1%D0%A8%D0%90%20%5B%F0%9F%8E%AE%20%D0%98%D0%B3%D1%80%D0%BE%D0%B2%D0%BE%D0%B9%5D%20%E2%80%A2%2082ms"}, {"protocol": "vless", "host": "104.254.140.62", "port": 443, "uuid": "926bc4cd-709e-4e90-8aa7-78db75fbe86b", "security": "tls", "sni": "gbs-MiTiVPN--MiTiVPN--MiTiVPN---MiTiVPN--MiTiVPN--MiTiVPN.KinGNetWork.iR", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇺🇸 США • 88ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "US", "country_flag": "🇺🇸", "country_name": "США", "latency_ms": 88, "is_alive": true, "source_id": null, "uri": "vless://926bc4cd-709e-4e90-8aa7-78db75fbe86b@104.254.140.62:443?encryption=none&type=ws&security=tls&path=%2F---%40MiTiVPN---%40MiTiVPN%2F---%40MiTiVPN---%40MiTiVPN%2F---%40MiTiVPN---%40MiTiVPN%2Fgb---%40MiTiVPN---%40MiTiVPN%2F---%40MiTiVPN---%40MiTiVPN%2F---%40MiTiVPN---%40MiTiVPN&host=gbbs-MiTiVPN--MiTiVPN--MiTiVPN---MiTiVPN--MiTiVPN--MiTiVPN.KinGNetWork.iR&sni=gbs-MiTiVPN--MiTiVPN--MiTiVPN---MiTiVPN--MiTiVPN--MiTiVPN.KinGNetWork.iR&alpn=h2%2Chttp%2F1.1&fp=chrome#%F0%9F%87%BA%F0%9F%87%B8%20%D0%A1%D0%A8%D0%90%20%E2%80%A2%2088ms"}, {"protocol": "vless", "host": "45.80.111.7", "port": 443, "uuid": "926bc4cd-709e-4e90-8aa7-78db75fbe86b", "security": "tls", "sni": "2--ldej--MiTiVPN---MiTiVPN-o.KingNetwork.ir", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇩🇪 Германия • 89ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "DE", "country_flag": "🇩🇪", "country_name": "Германия", "latency_ms": 89, "is_alive": true, "source_id": null, "uri": "vless://926bc4cd-709e-4e90-8aa7-78db75fbe86b@45.80.111.7:443?encryption=none&type=ws&security=tls&path=%2F---%40MiTiVPN---%40MiTiVPN%2F---%40MiTiVPN---%40MiTiVPN%2F---%40MiTiVPN---%40MiTiVPN%2Fde2---%40MiTiVPN---%40MiTiVPN%2F---%40MiTiVPN---%40MiTiVPN%2F---%40MiTiVPN---%40MiTiVPN&host=De2-MiTiVPN--MiTiVPN--MiTiVPN---MiTiVPN--MiTiVPN--MiTiVPN.KinGNetWork.iR&sni=2--ldej--MiTiVPN---MiTiVPN-o.KingNetwork.ir&alpn=h2%2Chttp%2F1.1&fp=chrome#%F0%9F%87%A9%F0%9F%87%AA%20%D0%93%D0%B5%D1%80%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F%20%E2%80%A2%2089ms"}, {"protocol": "vless", "host": "45.130.125.207", "port": 443, "uuid": "926bc4cd-709e-4e90-8aa7-78db75fbe86b", "security": "tls", "sni": "1111--MiTiVPN---MiTiVPN-o.KinGNetWork.iR", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🌐 Seychelles • 99ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "SC", "country_flag": "🌐", "country_name": "Seychelles", "latency_ms": 99, "is_alive": true, "source_id": null, "uri": "vless://926bc4cd-709e-4e90-8aa7-78db75fbe86b@45.130.125.207:443?encryption=none&type=ws&security=tls&path=%2F---%40MiTiVPN---%40MiTiVPN%2F---%40MiTiVPN---%40MiTiVPN%2F---%40MiTiVPN---%40MiTiVPN%2Fdde---%40MiTiVPN---%40MiTiVPN%2F---%40MiTiVPN---%40MiTiVPN%2F---%40MiTiVPN---%40MiTiVPN&host=De1-MiTiVPN--MiTiVPN--MiTiVPN---MiTiVPN--MiTiVPN--MiTiVPN.KinGNetWork.iR&sni=1111--MiTiVPN---MiTiVPN-o.KinGNetWork.iR&alpn=h2%2Chttp%2F1.1&fp=chrome#%F0%9F%8C%90%20Seychelles%20%E2%80%A2%2099ms"}, {"protocol": "vless", "host": "69.46.46.10", "port": 443, "uuid": "b1abaebf-41e9-0617-fa54-901793b4188e", "security": "tls", "sni": "rvg-production-6cac.up.railway.app", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇺🇸 США • 142ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "US", "country_flag": "🇺🇸", "country_name": "США", "latency_ms": 142, "is_alive": true, "source_id": null, "uri": "vless://b1abaebf-41e9-0617-fa54-901793b4188e@69.46.46.10:443?path=%2Fws%2Fb1abaebf-41e9-0617-fa54-901793b4188e&security=tls&alpn=http%2F1.1&encryption=none&host=rvg-production-6cac.up.railway.app&fp=ios&type=ws&sni=rvg-production-6cac.up.railway.app#%F0%9F%87%BA%F0%9F%87%B8%20%D0%A1%D0%A8%D0%90%20%E2%80%A2%20142ms"}, {"protocol": "vless", "host": "69.46.46.40", "port": 443, "uuid": "14e941de-82a6-802c-b0f3-c31697d9692b", "security": "tls", "sni": "rvg-production-471c.up.railway.app", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇺🇸 США • 156ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "US", "country_flag": "🇺🇸", "country_name": "США", "latency_ms": 156, "is_alive": true, "source_id": null, "uri": "vless://14e941de-82a6-802c-b0f3-c31697d9692b@69.46.46.40:443?path=%2Fws%2F14e941de-82a6-802c-b0f3-c31697d9692b&security=tls&alpn=http%2F1.1&encryption=none&insecure=0&host=rvg-production-471c.up.railway.app&fp=ios&type=ws&allowInsecure=0&sni=rvg-production-471c.up.railway.app#%F0%9F%87%BA%F0%9F%87%B8%20%D0%A1%D0%A8%D0%90%20%E2%80%A2%20156ms"}, {"protocol": "vless", "host": "159.195.40.19", "port": 443, "uuid": "8033102198", "security": "tls", "sni": "de7.fast-connect-service.site", "pbk": "", "sid": "", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇩🇪 Германия • 157ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "DE", "country_flag": "🇩🇪", "country_name": "Германия", "latency_ms": 157, "is_alive": true, "source_id": null, "uri": "vless://8033102198@159.195.40.19:443?security=tls&alpn=http%2F1.1&encryption=none&insecure=0&headerType=none&fp=firefox&type=tcp&allowInsecure=0&flow=xtls-rprx-vision&sni=de7.fast-connect-service.site#%F0%9F%87%A9%F0%9F%87%AA%20%D0%93%D0%B5%D1%80%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F%20%E2%80%A2%20157ms"}, {"protocol": "vless", "host": "94.140.0.1", "port": 443, "uuid": "3a3de813-bfaa-4355-bc47-05c7245431d2", "security": "tls", "sni": "Australia.havray2025.ir", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇦🇪 ОАЭ • 160ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "AE", "country_flag": "🇦🇪", "country_name": "ОАЭ", "latency_ms": 160, "is_alive": true, "source_id": null, "uri": "vless://3a3de813-bfaa-4355-bc47-05c7245431d2@94.140.0.1:443?encryption=none&type=ws&security=tls&path=%2F%3Fed%3D2560&host=Australia.havray2025.ir&sni=Australia.havray2025.ir&alpn=h3%2Ch2%2Chttp%2F1.1&fp=chrome&insecure=0&allowInsecure=0#%F0%9F%87%A6%F0%9F%87%AA%20%D0%9E%D0%90%D0%AD%20%E2%80%A2%20160ms"}, {"protocol": "vless", "host": "94.183.154.216", "port": 2003, "uuid": "a955a742-71de-4d5c-a65e-63eb290a8a10", "security": "reality", "sni": "www.filimo.com", "pbk": "oxVeOPOnhOnMvPA-pZ2z_OAbXsf2oCp9YRt7TcmdjBo", "sid": "2c4a61e923dd21e2", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🌐 Iran • 176ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "IR", "country_flag": "🌐", "country_name": "Iran", "latency_ms": 176, "is_alive": true, "source_id": null, "uri": "vless://a955a742-71de-4d5c-a65e-63eb290a8a10@94.183.154.216:2003?security=reality&encryption=mlkem768x25519plus.native.0rtt.100-111-1111.75-0-111.50-0-3333.156NRkt21U_2b3dQK0MprNGqLivKRysedHYJNmESJVY&pbk=oxVeOPOnhOnMvPA-pZ2z_OAbXsf2oCp9YRt7TcmdjBo&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=www.filimo.com&sid=2c4a61e923dd21e2#%F0%9F%8C%90%20Iran%20%E2%80%A2%20176ms"}, {"protocol": "vless", "host": "87.121.162.154", "port": 49001, "uuid": "e35296cf-ba7d-4fac-a67e-313d98a4f648", "security": "reality", "sni": "al.allmoon.fun", "pbk": "dG4t9_JHKdqd-mAMZMUreWFRpHTR2bGyuZBW29HKe3U", "sid": "", "flow": "", "type": "grpc", "remark": "🌐 Albania • 179ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "AL", "country_flag": "🌐", "country_name": "Albania", "latency_ms": 179, "is_alive": true, "source_id": null, "uri": "vless://e35296cf-ba7d-4fac-a67e-313d98a4f648@87.121.162.154:49001?mode=gun&security=reality&encryption=none&pbk=dG4t9_JHKdqd-mAMZMUreWFRpHTR2bGyuZBW29HKe3U&fp=qq&type=grpc&serviceName=grpc&sni=al.allmoon.fun#%F0%9F%8C%90%20Albania%20%E2%80%A2%20179ms"}, {"protocol": "vless", "host": "auto.gsupport.support", "port": 443, "uuid": "348b1b7d-fe7b-43f9-84b5-a2917925c8a8", "security": "reality", "sni": "en1.freehiliters.com", "pbk": "hyOYRfDSIYyqALQt3N2H0RjK8gbV1JvPTkNACC4PJF8", "sid": "8718c58d3d51db59", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇪🇺 Европа • 185ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EU", "country_flag": "🇪🇺", "country_name": "Европа", "latency_ms": 185, "is_alive": true, "source_id": null, "uri": "vless://348b1b7d-fe7b-43f9-84b5-a2917925c8a8@auto.gsupport.support:443?type=tcp&security=reality&fp=firefox&sni=en1.freehiliters.com&pbk=hyOYRfDSIYyqALQt3N2H0RjK8gbV1JvPTkNACC4PJF8&sid=8718c58d3d51db59&flow=xtls-rprx-vision#%F0%9F%87%AA%F0%9F%87%BA%20%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%20%E2%80%A2%20185ms"}, {"protocol": "vless", "host": "109.69.218.164", "port": 443, "uuid": "c28ee61d-0d43-4e69-8e6a-6397ed0ffc03", "security": "reality", "sni": "zealous-vortex.cdn.cachefleet.com", "pbk": "cv_KJnMzQUZruACPbH-BCgLWrYqPm2dbUymg-gW_sVc", "sid": "", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🌐 Belgium • 192ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "BE", "country_flag": "🌐", "country_name": "Belgium", "latency_ms": 192, "is_alive": true, "source_id": null, "uri": "vless://c28ee61d-0d43-4e69-8e6a-6397ed0ffc03@109.69.218.164:443?security=reality&encryption=none&pbk=cv_KJnMzQUZruACPbH-BCgLWrYqPm2dbUymg-gW_sVc&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=zealous-vortex.cdn.cachefleet.com#%F0%9F%8C%90%20Belgium%20%E2%80%A2%20192ms"}, {"protocol": "vless", "host": "94.183.154.216", "port": 2002, "uuid": "a955a742-71de-4d5c-a65e-63eb290a8a10", "security": "reality", "sni": "www.filimo.com", "pbk": "FDFM2nFrAKssmyFrYwvcB7BFTWBXtPjsucXPzd9BDFU", "sid": "0396fed66be8f2ca", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🌐 Iran • 193ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "IR", "country_flag": "🌐", "country_name": "Iran", "latency_ms": 193, "is_alive": true, "source_id": null, "uri": "vless://a955a742-71de-4d5c-a65e-63eb290a8a10@94.183.154.216:2002?security=reality&encryption=mlkem768x25519plus.native.0rtt.100-111-1111.75-0-111.50-0-3333.wlYOgfylfwe7Ls_csmDJ1ELXXg84s6mn37-bP9kvmGk&pbk=FDFM2nFrAKssmyFrYwvcB7BFTWBXtPjsucXPzd9BDFU&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=www.filimo.com&sid=0396fed66be8f2ca#%F0%9F%8C%90%20Iran%20%E2%80%A2%20193ms"}, {"protocol": "vless", "host": "31.76.119.17", "port": 443, "uuid": "454431fc-71e2-42b1-b375-5b55dd06666a", "security": "reality", "sni": "example.org", "pbk": "aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU", "sid": "", "flow": "", "type": "tcp", "remark": "🇩🇪 Германия • 220ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "DE", "country_flag": "🇩🇪", "country_name": "Германия", "latency_ms": 220, "is_alive": true, "source_id": null, "uri": "vless://454431fc-71e2-42b1-b375-5b55dd06666a@31.76.119.17:443?encryption=none&fp=firefox&pbk=aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU&security=reality&sni=example.org&type=tcp#%F0%9F%87%A9%F0%9F%87%AA%20%D0%93%D0%B5%D1%80%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F%20%E2%80%A2%20220ms"}, {"protocol": "vless", "host": "94.183.154.216", "port": 1002, "uuid": "a955a742-71de-4d5c-a65e-63eb290a8a10", "security": "reality", "sni": "www.filimo.com", "pbk": "OInX6PLOlHUx9CkvaGJNxuXhrA0bym6PnGcW5qpI8hk", "sid": "d2830ef9f5bdeb2b", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🌐 Iran • 224ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "IR", "country_flag": "🌐", "country_name": "Iran", "latency_ms": 224, "is_alive": true, "source_id": null, "uri": "vless://a955a742-71de-4d5c-a65e-63eb290a8a10@94.183.154.216:1002?security=reality&encryption=mlkem768x25519plus.native.0rtt.100-111-1111.75-0-111.50-0-3333.Mwkrd83bm5m80iu6CgKLEwH-UEIQnr8SvunV6wOd4Tk&pbk=OInX6PLOlHUx9CkvaGJNxuXhrA0bym6PnGcW5qpI8hk&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=www.filimo.com&sid=d2830ef9f5bdeb2b#%F0%9F%8C%90%20Iran%20%E2%80%A2%20224ms"}, {"protocol": "vless", "host": "45.132.176.161", "port": 9882, "uuid": "5d16ac22-6eea-426f-b778-6f4c2961faef", "security": "reality", "sni": "dl.google.com", "pbk": "bnRIb3Er1i-K6NGGByCO9UbGfOvu43ZoiK7ulPd1SzU", "sid": "", "flow": "", "type": "grpc", "remark": "🇨🇭 Швейцария • 235ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "CH", "country_flag": "🇨🇭", "country_name": "Швейцария", "latency_ms": 235, "is_alive": true, "source_id": null, "uri": "vless://5d16ac22-6eea-426f-b778-6f4c2961faef@45.132.176.161:9882?encryption=none&security=reality&sni=dl.google.com&pbk=bnRIb3Er1i-K6NGGByCO9UbGfOvu43ZoiK7ulPd1SzU&type=grpc&serviceName=grpc-tunnel&fp=android#%F0%9F%87%A8%F0%9F%87%AD%20%D0%A8%D0%B2%D0%B5%D0%B9%D1%86%D0%B0%D1%80%D0%B8%D1%8F%20%E2%80%A2%20235ms"}, {"protocol": "vless", "host": "94.183.154.216", "port": 1001, "uuid": "a955a742-71de-4d5c-a65e-63eb290a8a10", "security": "reality", "sni": "www.filimo.com", "pbk": "KX755gv-2X6CXLfWm33OmTc3zHKHcNQK7nPZ06nki1U", "sid": "429e38fcd14a06a8", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🌐 Iran • 242ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "IR", "country_flag": "🌐", "country_name": "Iran", "latency_ms": 242, "is_alive": true, "source_id": null, "uri": "vless://a955a742-71de-4d5c-a65e-63eb290a8a10@94.183.154.216:1001?security=reality&encryption=mlkem768x25519plus.native.0rtt.100-111-1111.75-0-111.50-0-3333.ejm35mx3XTS_gTck_ChVg_HHP4H9Msde_q2NDk-EtWc&pbk=KX755gv-2X6CXLfWm33OmTc3zHKHcNQK7nPZ06nki1U&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=www.filimo.com&sid=429e38fcd14a06a8#%F0%9F%8C%90%20Iran%20%E2%80%A2%20242ms"}, {"protocol": "vless", "host": "46.28.71.154", "port": 443, "uuid": "4bdeee92-97e8-414d-bef6-ec1d5e2ab73b", "security": "reality", "sni": "spanish67.kovsh.lol", "pbk": "bZpzmeWiEJyJQy0W2hHc34Nr6BuFXj1UDd80Cbwh1Fk", "sid": "ff776ff77be48b88", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇪🇸 Испания • 287ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "ES", "country_flag": "🇪🇸", "country_name": "Испания", "latency_ms": 287, "is_alive": true, "source_id": null, "uri": "vless://4bdeee92-97e8-414d-bef6-ec1d5e2ab73b@46.28.71.154:443?encryption=none&security=reality&type=tcp&sni=spanish67.kovsh.lol&flow=xtls-rprx-vision&fp=chrome&pbk=bZpzmeWiEJyJQy0W2hHc34Nr6BuFXj1UDd80Cbwh1Fk&sid=ff776ff77be48b88#%F0%9F%87%AA%F0%9F%87%B8%20%D0%98%D1%81%D0%BF%D0%B0%D0%BD%D0%B8%D1%8F%20%E2%80%A2%20287ms"}, {"protocol": "vless", "host": "130.94.1.177", "port": 443, "uuid": "b1c31d36-c6b5-414b-88d2-9e24e7bfcca3", "security": "tls", "sni": "www.nihaoyun.top", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇹🇷 Турция • 289ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "TR", "country_flag": "🇹🇷", "country_name": "Турция", "latency_ms": 289, "is_alive": true, "source_id": null, "uri": "vless://b1c31d36-c6b5-414b-88d2-9e24e7bfcca3@130.94.1.177:443?encryption=none&fp=firefox&host=www.nihaoyun.top&security=tls&sni=www.nihaoyun.top&type=ws#%F0%9F%87%B9%F0%9F%87%B7%20%D0%A2%D1%83%D1%80%D1%86%D0%B8%D1%8F%20%E2%80%A2%20289ms"}, {"protocol": "vless", "host": "188.132.192.145", "port": 2087, "uuid": "b1c31d36-c6b5-414b-88d2-9e24e7bfcca3", "security": "tls", "sni": "www.nihaoyun.top", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇹🇷 Турция • 290ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "TR", "country_flag": "🇹🇷", "country_name": "Турция", "latency_ms": 290, "is_alive": true, "source_id": null, "uri": "vless://b1c31d36-c6b5-414b-88d2-9e24e7bfcca3@188.132.192.145:2087?security=tls&fp=chrome&sni=www.nihaoyun.top&type=ws&headerType=none&host=www.nihaoyun.top&path=%2F#%F0%9F%87%B9%F0%9F%87%B7%20%D0%A2%D1%83%D1%80%D1%86%D0%B8%D1%8F%20%E2%80%A2%20290ms"}, {"protocol": "vless", "host": "site.check-looks.space", "port": 2083, "uuid": "ca608afb-55ff-4f36-9d00-606fedbb30e1", "security": "tls", "sni": "site.check-looks.space", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇪🇺 Европа • 310ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EU", "country_flag": "🇪🇺", "country_name": "Европа", "latency_ms": 310, "is_alive": true, "source_id": null, "uri": "vless://ca608afb-55ff-4f36-9d00-606fedbb30e1@site.check-looks.space:2083?fp=chrome&security=tls&sni=site.check-looks.space&type=ws#%F0%9F%87%AA%F0%9F%87%BA%20%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%20%E2%80%A2%20310ms"}, {"protocol": "vless", "host": "finl11.ali-bard.online", "port": 443, "uuid": "4643976f-85fa-40cf-9e58-ea28b50f253b", "security": "reality", "sni": "finl11.ali-bard.online", "pbk": "SB1uC0OEveYjSiS_Nuw9Ld-uVVXWqi794OGnldthY3I", "sid": "", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇪🇺 Европа • 323ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EU", "country_flag": "🇪🇺", "country_name": "Европа", "latency_ms": 323, "is_alive": true, "source_id": null, "uri": "vless://4643976f-85fa-40cf-9e58-ea28b50f253b@finl11.ali-bard.online:443?type=tcp&security=reality&flow=xtls-rprx-vision&fp=qq&pbk=SB1uC0OEveYjSiS_Nuw9Ld-uVVXWqi794OGnldthY3I&sni=finl11.ali-bard.online#%F0%9F%87%AA%F0%9F%87%BA%20%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%20%E2%80%A2%20323ms"}, {"protocol": "vless", "host": "spanish67.kovsh.lol", "port": 443, "uuid": "4bdeee92-97e8-414d-bef6-ec1d5e2ab73b", "security": "reality", "sni": "spanish67.kovsh.lol", "pbk": "bZpzmeWiEJyJQy0W2hHc34Nr6BuFXj1UDd80Cbwh1Fk", "sid": "ff776ff77be48b88", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇪🇺 Европа • 324ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EU", "country_flag": "🇪🇺", "country_name": "Европа", "latency_ms": 324, "is_alive": true, "source_id": null, "uri": "vless://4bdeee92-97e8-414d-bef6-ec1d5e2ab73b@spanish67.kovsh.lol:443?security=reality&encryption=none&pbk=bZpzmeWiEJyJQy0W2hHc34Nr6BuFXj1UDd80Cbwh1Fk&headerType=none&fp=chrome&spx=%2F&type=tcp&flow=xtls-rprx-vision&sni=spanish67.kovsh.lol&sid=ff776ff77be48b88#%F0%9F%87%AA%F0%9F%87%BA%20%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%20%E2%80%A2%20324ms"}, {"protocol": "vless", "host": "103.31.4.127", "port": 443, "uuid": "b1c31d36-c6b5-414b-88d2-9e24e7bfcca3", "security": "tls", "sni": "www.nihaoyun.top", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇺🇸 США • 347ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "US", "country_flag": "🇺🇸", "country_name": "США", "latency_ms": 347, "is_alive": true, "source_id": null, "uri": "vless://b1c31d36-c6b5-414b-88d2-9e24e7bfcca3@103.31.4.127:443?security=tls&fp=chrome&sni=www.nihaoyun.top&type=ws&headerType=none&host=www.nihaoyun.top&path=%2F#%F0%9F%87%BA%F0%9F%87%B8%20%D0%A1%D0%A8%D0%90%20%E2%80%A2%20347ms"}, {"protocol": "vless", "host": "109.172.8.48", "port": 8443, "uuid": "b1c31d36-c6b5-414b-88d2-9e24e7bfcca3", "security": "tls", "sni": "www.nihaoyun.top", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇨🇿 Чехия • 348ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "CZ", "country_flag": "🇨🇿", "country_name": "Чехия", "latency_ms": 348, "is_alive": true, "source_id": null, "uri": "vless://b1c31d36-c6b5-414b-88d2-9e24e7bfcca3@109.172.8.48:8443?security=tls&fp=chrome&sni=www.nihaoyun.top&type=ws&headerType=none&host=www.nihaoyun.top&path=%2F#%F0%9F%87%A8%F0%9F%87%BF%20%D0%A7%D0%B5%D1%85%D0%B8%D1%8F%20%E2%80%A2%20348ms"}, {"protocol": "vless", "host": "200.165.231.209", "port": 443, "uuid": "ff0b6ba8-bed0-4c4d-bbc9-23af47582615", "security": "tls", "sni": "wstg.datasynctrue.online", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇫🇮 Финляндия • 355ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "FI", "country_flag": "🇫🇮", "country_name": "Финляндия", "latency_ms": 355, "is_alive": true, "source_id": null, "uri": "vless://ff0b6ba8-bed0-4c4d-bbc9-23af47582615@200.165.231.209:443?encryption=none&host=wstg.datasynctrue.online&path=%2Fapi%2Fconnect&security=tls&sni=wstg.datasynctrue.online&type=ws#%F0%9F%87%AB%F0%9F%87%AE%20%D0%A4%D0%B8%D0%BD%D0%BB%D1%8F%D0%BD%D0%B4%D0%B8%D1%8F%20%E2%80%A2%20355ms"}, {"protocol": "vless", "host": "yaruss.stopingiphatered.shop", "port": 443, "uuid": "4bdeee92-97e8-414d-bef6-ec1d5e2ab73b", "security": "reality", "sni": "yaruss.stopingiphatered.shop", "pbk": "bZpzmeWiEJyJQy0W2hHc34Nr6BuFXj1UDd80Cbwh1Fk", "sid": "ff776ff77be48b88", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇺🇸 США • 389ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "US", "country_flag": "🇺🇸", "country_name": "США", "latency_ms": 389, "is_alive": true, "source_id": null, "uri": "vless://4bdeee92-97e8-414d-bef6-ec1d5e2ab73b@yaruss.stopingiphatered.shop:443?encryption=none&security=reality&type=tcp&sni=yaruss.stopingiphatered.shop&flow=xtls-rprx-vision&fp=chrome&pbk=bZpzmeWiEJyJQy0W2hHc34Nr6BuFXj1UDd80Cbwh1Fk&sid=ff776ff77be48b88#%F0%9F%87%BA%F0%9F%87%B8%20%D0%A1%D0%A8%D0%90%20%E2%80%A2%20389ms"}, {"protocol": "vless", "host": "103.31.4.189", "port": 443, "uuid": "b1c31d36-c6b5-414b-88d2-9e24e7bfcca3", "security": "tls", "sni": "www.nihaoyun.top", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇺🇸 США • 395ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "US", "country_flag": "🇺🇸", "country_name": "США", "latency_ms": 395, "is_alive": true, "source_id": null, "uri": "vless://b1c31d36-c6b5-414b-88d2-9e24e7bfcca3@103.31.4.189:443?security=tls&fp=chrome&sni=www.nihaoyun.top&type=ws&headerType=none&host=www.nihaoyun.top&path=%2F#%F0%9F%87%BA%F0%9F%87%B8%20%D0%A1%D0%A8%D0%90%20%E2%80%A2%20395ms"}, {"protocol": "vless", "host": "80.47.6.12", "port": 443, "uuid": "4bdeee92-97e8-414d-bef6-ec1d5e2ab73b", "security": "reality", "sni": "polkakurvich.hohoterz.beer", "pbk": "X6gBZNZSv_k1pyvLmQaDD4LsYk7jIA1SObRR5r-4Ynk", "sid": "fcfd621a2f36e3b6", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇬🇧 Великобритания • 405ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "GB", "country_flag": "🇬🇧", "country_name": "Великобритания", "latency_ms": 405, "is_alive": true, "source_id": null, "uri": "vless://4bdeee92-97e8-414d-bef6-ec1d5e2ab73b@80.47.6.12:443?security=reality&encryption=none&pbk=X6gBZNZSv_k1pyvLmQaDD4LsYk7jIA1SObRR5r-4Ynk&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=polkakurvich.hohoterz.beer&sid=fcfd621a2f36e3b6#%F0%9F%87%AC%F0%9F%87%A7%20%D0%92%D0%B5%D0%BB%D0%B8%D0%BA%D0%BE%D0%B1%D1%80%D0%B8%D1%82%D0%B0%D0%BD%D0%B8%D1%8F%20%E2%80%A2%20405ms"}, {"protocol": "vless", "host": "144.31.219.97", "port": 443, "uuid": "454431fc-71e2-42b1-b375-5b55dd06666a", "security": "reality", "sni": "example.org", "pbk": "aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU", "sid": "", "flow": "", "type": "tcp", "remark": "🇩🇪 Германия • 415ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "DE", "country_flag": "🇩🇪", "country_name": "Германия", "latency_ms": 415, "is_alive": true, "source_id": null, "uri": "vless://454431fc-71e2-42b1-b375-5b55dd06666a@144.31.219.97:443?encryption=none&fp=firefox&pbk=aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU&security=reality&sni=example.org&type=tcp#%F0%9F%87%A9%F0%9F%87%AA%20%D0%93%D0%B5%D1%80%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F%20%E2%80%A2%20415ms"}, {"protocol": "vless", "host": "www.lianchuang123.com", "port": 443, "uuid": "2c473bc0-484c-49d5-8cf3-c89d26b724fe", "security": "tls", "sni": "sni.mmadcoffee.info", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇪🇺 Европа • 449ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EU", "country_flag": "🇪🇺", "country_name": "Европа", "latency_ms": 449, "is_alive": true, "source_id": null, "uri": "vless://2c473bc0-484c-49d5-8cf3-c89d26b724fe@www.lianchuang123.com:443?type=ws&encryption=none&host=smtp.mmadcoffee.info&path=%2F16838%2Fc89d26b724fe%2F&security=tls&sni=sni.mmadcoffee.info&fp=chrome#%F0%9F%87%AA%F0%9F%87%BA%20%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%20%E2%80%A2%20449ms"}, {"protocol": "vless", "host": "82.41.30.112", "port": 443, "uuid": "454431fc-71e2-42b1-b375-5b55dd06666a", "security": "reality", "sni": "example.com", "pbk": "2AKBmK0PMf2zUMhRo1Ad-WNf_XoRk3AN-SGo6ZdhxA4", "sid": "ecca56e9a9963ed7", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇰🇿 Казахстан • 459ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "KZ", "country_flag": "🇰🇿", "country_name": "Казахстан", "latency_ms": 459, "is_alive": true, "source_id": null, "uri": "vless://454431fc-71e2-42b1-b375-5b55dd06666a@82.41.30.112:443?type=tcp&security=reality&flow=xtls-rprx-vision&fp=firefox&pbk=2AKBmK0PMf2zUMhRo1Ad-WNf_XoRk3AN-SGo6ZdhxA4&sid=ecca56e9a9963ed7&sni=example.com#%F0%9F%87%B0%F0%9F%87%BF%20%D0%9A%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D1%82%D0%B0%D0%BD%20%E2%80%A2%20459ms"}, {"protocol": "vless", "host": "2.58.66.198", "port": 443, "uuid": "454431fc-71e2-42b1-b375-5b55dd06666a", "security": "reality", "sni": "example.org", "pbk": "aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU", "sid": "", "flow": "", "type": "tcp", "remark": "🇩🇪 Германия • 479ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "DE", "country_flag": "🇩🇪", "country_name": "Германия", "latency_ms": 479, "is_alive": true, "source_id": null, "uri": "vless://454431fc-71e2-42b1-b375-5b55dd06666a@2.58.66.198:443?encryption=none&fp=firefox&pbk=aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU&security=reality&sni=example.org&type=tcp#%F0%9F%87%A9%F0%9F%87%AA%20%D0%93%D0%B5%D1%80%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F%20%E2%80%A2%20479ms"}, {"protocol": "vless", "host": "ware.tunnelgate.org", "port": 443, "uuid": "4deb9957-e037-4ae2-8892-da357cc6f99f", "security": "tls", "sni": "ware.tunnelgate.org", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇪🇺 Европа • 522ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EU", "country_flag": "🇪🇺", "country_name": "Европа", "latency_ms": 522, "is_alive": true, "source_id": null, "uri": "vless://4deb9957-e037-4ae2-8892-da357cc6f99f@ware.tunnelgate.org:443?path=%2Fws%2Fv1%2Fru&security=tls&alpn=http%2F1.1&encryption=mlkem768x25519plus.native.0rtt.fsGtiqlb1xuwUZF-iPrG-9aedIIVJyMnPCNu9EiNrMKVfwcDmvBNvhRpcaxvSMuhMjDI1qh0W1wI1rRzA3OB_TKFqNomhKW841Na5qKCCFYAGRENYXCVY0qqLaU1a9gqdak6T2LG9aUtXLdY_sY1jxI5JOhcNtc6lQGIj6NVHPOa5Zd3FhdRGUo8aFopsJJUaCePlkWN4UxrzUA5geFtM1g7WcVNiFpuV_vOEQKPgHQNgwAdWYGZWfVIp6TJTfk3HYvChZgjbUkeU9y6t8A9H2Ut9QiTqjA-z1IV8CgUUNa7PvuHYOUgsLipX9BeFYOf4VSpwsmMtWtywIN2LyBU69wjyhMPmEwGOdGWdvGyVJWQ4xULffWEpvlCBBCRSJAQGyIMHPVdYuU7ALzE5dgM_Aodphek1LLAcAx3ZWIAdtowSvKD9GwuPIotC-TFNaa60qCHbsW1YFQS1CJDGxDIUCYbwKGgIqM4__BYhtDIrGtmltQKyjxJJrI3ndKrHaJb4tjDc2dJ1yO_Lom8K8mZfpVM9qg0xIE3aqeBaSFIxiueWzVf4uy0FISgxip0pzw7E4tjepIXkXbI1ZkMG2VtPmwr0wR4fWddPPV-rdklaeNzonguCspC9-JEwTjFQ3nG5yXPrLm5LcovgjIHPylwDqsQiqN2J8ESI9xOQcKJ-JVrSzZwnEhO8iZ4wVhm_Ga7qIk-TDK23JDHRRJAkvy7WYWtCluPIlXK_upU_gN-BAUrC3V81AvHQqWnBeopVaGppFo7QZd9JpoXB_RqqpXGRfXGHptsPhGUR0h-7dYnEFR_MCIV_jNLCwy2U2UDd2TBBODKF5fEPisCoYMiXQrKhhhacZqL5Io5UpWYB9lmH9VFyHwTBFfJuAuYrhcKx_Ag5kNJoBJDRTiMDifBS7MewSSrzeWCoIuiK2Q5BGodsSZAdcbGs5mySwsmQBwQWCqgDObMYzeHMxu-IksLlLKMCVQET5smRdRTkgtJclAvsuB9l4rDkPcVsKCCH8ktxGO6aSPLS4ib2Hc32qNgKASVRZYfyGM6GoN5c9hsa_QVtfa4ANqaqMzJmbJaxcA2FmsHXhaG6UXGqDd32hofLjt1NyUH8DjAIksdA2Ycy5xz3yRZCIIeKHaUR5s9uoQWfZYYMYJfl6o6ohmEXrScGGN_BYgb1GSkX5OcODGDKBVdPEd20IQ62je4pYUJzjtw66MkZUuS2_VRlni1aqNz4JB3sKpAtDyMqYApa-x2v5YU1tdH1BQkYmty16pqE1w4akVZ-rJOQwnJlrY6-1gz2PtjWHQoWju_31E92WYYwoMBSPkEhgCcbTys0FAD6sxu6Mh2UrSh0AZIX3mdXWk2IlmSd7QuoFuNEClwRCiNpokoclMkyvOe7oEFa6xIGvGMGnc2RzkmCyXBjyZgIgussYtl8ZplgcOAiAZzf-sM7-XItKlWAABWituyNyOiL_FtLkGgrpYw4NjJ_iZtoJaVpkGcALwtnrSWv1M9yvMV4wFlkDiyOyaWERidV5s75sA0l_ADPKpMd0_DPh_PN_2luzFs4QMrudBp2KJEE8Jn5Ob0_dk&insecure=0&host=ware.tunnelgate.org&fp=qq&type=ws&allowInsecure=0&sni=ware.tunnelgate.org#%F0%9F%87%AA%F0%9F%87%BA%20%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%20%E2%80%A2%20522ms"}, {"protocol": "vless", "host": "5.45.107.150", "port": 8443, "uuid": "b1c31d36-c6b5-414b-88d2-9e24e7bfcca3", "security": "tls", "sni": "www.nihaoyun.top", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇩🇪 Германия • 528ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "DE", "country_flag": "🇩🇪", "country_name": "Германия", "latency_ms": 528, "is_alive": true, "source_id": null, "uri": "vless://b1c31d36-c6b5-414b-88d2-9e24e7bfcca3@5.45.107.150:8443?security=tls&fp=chrome&sni=www.nihaoyun.top&type=ws&headerType=none&host=www.nihaoyun.top&path=%2F#%F0%9F%87%A9%F0%9F%87%AA%20%D0%93%D0%B5%D1%80%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F%20%E2%80%A2%20528ms"}, {"protocol": "vless", "host": "217.19.122.200", "port": 443, "uuid": "bc5ec86c-3e65-4272-994c-59a924c72a68", "security": "tls", "sni": "fbsv6.guardora.pro", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇳🇱 Нидерланды • 593ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "NL", "country_flag": "🇳🇱", "country_name": "Нидерланды", "latency_ms": 593, "is_alive": true, "source_id": null, "uri": "vless://bc5ec86c-3e65-4272-994c-59a924c72a68@217.19.122.200:443?type=ws&security=tls&encryption=none&path=%2Fws&host=fbsv6.guardora.pro&sni=fbsv6.guardora.pro&fp=firefox&alpn=http%2F1.1&headerType=none#%F0%9F%87%B3%F0%9F%87%B1%20%D0%9D%D0%B8%D0%B4%D0%B5%D1%80%D0%BB%D0%B0%D0%BD%D0%B4%D1%8B%20%E2%80%A2%20593ms"}, {"protocol": "vless", "host": "ziro.skin", "port": 443, "uuid": "f028a8c0-6763-4558-aee3-2563db9d7825", "security": "tls", "sni": "", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇺🇸 США • 593ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "US", "country_flag": "🇺🇸", "country_name": "США", "latency_ms": 593, "is_alive": true, "source_id": null, "uri": "vless://f028a8c0-6763-4558-aee3-2563db9d7825@ziro.skin:443?type=ws&headerType=none&security=tls&encryption=none&fp=qq&path=%2Fxxvclws#%F0%9F%87%BA%F0%9F%87%B8%20%D0%A1%D0%A8%D0%90%20%E2%80%A2%20593ms"}, {"protocol": "vless", "host": "185.146.234.242", "port": 443, "uuid": "b1c31d36-c6b5-414b-88d2-9e24e7bfcca3", "security": "tls", "sni": "www.nihaoyun.top", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇬🇧 Великобритания • 611ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "GB", "country_flag": "🇬🇧", "country_name": "Великобритания", "latency_ms": 611, "is_alive": true, "source_id": null, "uri": "vless://b1c31d36-c6b5-414b-88d2-9e24e7bfcca3@185.146.234.242:443?security=tls&fp=chrome&sni=www.nihaoyun.top&type=ws&headerType=none&host=www.nihaoyun.top&path=%2F#%F0%9F%87%AC%F0%9F%87%A7%20%D0%92%D0%B5%D0%BB%D0%B8%D0%BA%D0%BE%D0%B1%D1%80%D0%B8%D1%82%D0%B0%D0%BD%D0%B8%D1%8F%20%E2%80%A2%20611ms"}, {"protocol": "vless", "host": "de.monkora.org", "port": 443, "uuid": "454431fc-71e2-42b1-b375-5b55dd06666a", "security": "reality", "sni": "example.org", "pbk": "aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU", "sid": "", "flow": "", "type": "tcp", "remark": "🇪🇺 Европа • 621ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EU", "country_flag": "🇪🇺", "country_name": "Европа", "latency_ms": 621, "is_alive": true, "source_id": null, "uri": "vless://454431fc-71e2-42b1-b375-5b55dd06666a@de.monkora.org:443?encryption=none&security=reality&sni=example.org&fp=firefox&pbk=aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU&type=tcp&headerType=none#%F0%9F%87%AA%F0%9F%87%BA%20%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%20%E2%80%A2%20621ms"}, {"protocol": "vless", "host": "45.154.206.88", "port": 443, "uuid": "454431fc-71e2-42b1-b375-5b55dd06666a", "security": "reality", "sni": "es.monkeyisland.xyz", "pbk": "2AKBmK0PMf2zUMhRo1Ad-WNf_XoRk3AN-SGo6ZdhxA4", "sid": "ecca56e9a9963ed7", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇪🇸 Испания • 673ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "ES", "country_flag": "🇪🇸", "country_name": "Испания", "latency_ms": 673, "is_alive": true, "source_id": null, "uri": "vless://454431fc-71e2-42b1-b375-5b55dd06666a@45.154.206.88:443?type=tcp&security=reality&flow=xtls-rprx-vision&fp=firefox&pbk=2AKBmK0PMf2zUMhRo1Ad-WNf_XoRk3AN-SGo6ZdhxA4&sid=ecca56e9a9963ed7&sni=es.monkeyisland.xyz#%F0%9F%87%AA%F0%9F%87%B8%20%D0%98%D1%81%D0%BF%D0%B0%D0%BD%D0%B8%D1%8F%20%E2%80%A2%20673ms"}, {"protocol": "vless", "host": "161.35.192.122", "port": 443, "uuid": "b1c31d36-c6b5-414b-88d2-9e24e7bfcca3", "security": "tls", "sni": "www.nihaoyun.top", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇩🇪 Германия • 704ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "DE", "country_flag": "🇩🇪", "country_name": "Германия", "latency_ms": 704, "is_alive": true, "source_id": null, "uri": "vless://b1c31d36-c6b5-414b-88d2-9e24e7bfcca3@161.35.192.122:443?security=tls&fp=chrome&sni=www.nihaoyun.top&type=ws&headerType=none&host=www.nihaoyun.top&path=%2F#%F0%9F%87%A9%F0%9F%87%AA%20%D0%93%D0%B5%D1%80%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F%20%E2%80%A2%20704ms"}, {"protocol": "vless", "host": "polkakurvich.hohoterz.beer", "port": 443, "uuid": "4bdeee92-97e8-414d-bef6-ec1d5e2ab73b", "security": "reality", "sni": "polkakurvich.hohoterz.beer", "pbk": "X6gBZNZSv_k1pyvLmQaDD4LsYk7jIA1SObRR5r-4Ynk", "sid": "fcfd621a2f36e3b6", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇪🇺 Европа • 710ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EU", "country_flag": "🇪🇺", "country_name": "Европа", "latency_ms": 710, "is_alive": true, "source_id": null, "uri": "vless://4bdeee92-97e8-414d-bef6-ec1d5e2ab73b@polkakurvich.hohoterz.beer:443?security=reality&encryption=none&pbk=X6gBZNZSv_k1pyvLmQaDD4LsYk7jIA1SObRR5r-4Ynk&headerType=none&fp=firefox&spx=%2F&type=tcp&flow=xtls-rprx-vision&sni=polkakurvich.hohoterz.beer&sid=fcfd621a2f36e3b6#%F0%9F%87%AA%F0%9F%87%BA%20%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%20%E2%80%A2%20710ms"}, {"protocol": "vless", "host": "se.monkora.org", "port": 443, "uuid": "454431fc-71e2-42b1-b375-5b55dd06666a", "security": "reality", "sni": "example.org", "pbk": "aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU", "sid": "", "flow": "", "type": "tcp", "remark": "🇪🇺 Европа • 763ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EU", "country_flag": "🇪🇺", "country_name": "Европа", "latency_ms": 763, "is_alive": true, "source_id": null, "uri": "vless://454431fc-71e2-42b1-b375-5b55dd06666a@se.monkora.org:443?encryption=none&security=reality&sni=example.org&fp=firefox&pbk=aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU&type=tcp&headerType=none#%F0%9F%87%AA%F0%9F%87%BA%20%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%20%E2%80%A2%20763ms"}, {"protocol": "vless", "host": "2.26.148.145", "port": 443, "uuid": "4643976f-85fa-40cf-9e58-ea28b50f253b", "security": "reality", "sni": "polo.ali-bard.online", "pbk": "SB1uC0OEveYjSiS_Nuw9Ld-uVVXWqi794OGnldthY3I", "sid": "", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇵🇱 Польша • 817ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "PL", "country_flag": "🇵🇱", "country_name": "Польша", "latency_ms": 817, "is_alive": true, "source_id": null, "uri": "vless://4643976f-85fa-40cf-9e58-ea28b50f253b@2.26.148.145:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=SB1uC0OEveYjSiS_Nuw9Ld-uVVXWqi794OGnldthY3I&security=reality&sni=polo.ali-bard.online&type=tcp#%F0%9F%87%B5%F0%9F%87%B1%20%D0%9F%D0%BE%D0%BB%D1%8C%D1%88%D0%B0%20%E2%80%A2%20817ms"}, {"protocol": "vless", "host": "be.monkora.org", "port": 443, "uuid": "454431fc-71e2-42b1-b375-5b55dd06666a", "security": "reality", "sni": "example.org", "pbk": "aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU", "sid": "", "flow": "", "type": "tcp", "remark": "🇪🇺 Европа • 837ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EU", "country_flag": "🇪🇺", "country_name": "Европа", "latency_ms": 837, "is_alive": true, "source_id": null, "uri": "vless://454431fc-71e2-42b1-b375-5b55dd06666a@be.monkora.org:443?encryption=none&security=reality&sni=example.org&fp=firefox&pbk=aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU&type=tcp&headerType=none#%F0%9F%87%AA%F0%9F%87%BA%20%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%20%E2%80%A2%20837ms"}, {"protocol": "vless", "host": "ulet-bm-s1700.reverseenge.sbs", "port": 8443, "uuid": "8674df07-56b3-43ea-b687-aef2b1a20137", "security": "reality", "sni": "ulet-bm-s1700.reverseenge.sbs", "pbk": "p_vxl_ONmhWrvQu6338enahTy_ZmxJ4bJ9OF5fzqphw", "sid": "", "flow": "", "type": "grpc", "remark": "🇪🇺 Европа • 868ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EU", "country_flag": "🇪🇺", "country_name": "Европа", "latency_ms": 868, "is_alive": true, "source_id": null, "uri": "vless://8674df07-56b3-43ea-b687-aef2b1a20137@ulet-bm-s1700.reverseenge.sbs:8443?type=grpc&security=reality&fp=firefox&pbk=p_vxl_ONmhWrvQu6338enahTy_ZmxJ4bJ9OF5fzqphw&sni=ulet-bm-s1700.reverseenge.sbs#%F0%9F%87%AA%F0%9F%87%BA%20%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%20%E2%80%A2%20868ms"}, {"protocol": "vless", "host": "176.123.165.25", "port": 9881, "uuid": "5d16ac22-6eea-426f-b778-6f4c2961faef", "security": "reality", "sni": "dl.google.com", "pbk": "Dfgu8Ey0M8Hz4gXGZAwQ3H9jLt2HByVsjAOTWiuKDB0", "sid": "aabbccdd", "flow": "", "type": "grpc", "remark": "🇸🇪 Швеция • 892ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "SE", "country_flag": "🇸🇪", "country_name": "Швеция", "latency_ms": 892, "is_alive": true, "source_id": null, "uri": "vless://5d16ac22-6eea-426f-b778-6f4c2961faef@176.123.165.25:9881?encryption=none&security=reality&sni=dl.google.com&pbk=Dfgu8Ey0M8Hz4gXGZAwQ3H9jLt2HByVsjAOTWiuKDB0&sid=aabbccdd&type=grpc&serviceName=grpc-tunnel&fp=ios#%F0%9F%87%B8%F0%9F%87%AA%20%D0%A8%D0%B2%D0%B5%D1%86%D0%B8%D1%8F%20%E2%80%A2%20892ms"}, {"protocol": "vless", "host": "108.156.39.79", "port": 443, "uuid": "720043a3-d5fb-4a94-883c-13e4b628253c", "security": "tls", "sni": "lon-rem-2.vip107.cfd", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇬🇧 Великобритания • 901ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "GB", "country_flag": "🇬🇧", "country_name": "Великобритания", "latency_ms": 901, "is_alive": true, "source_id": null, "uri": "vless://720043a3-d5fb-4a94-883c-13e4b628253c@108.156.39.79:443?type=ws&security=tls&encryption=none&sni=lon-rem-2.vip107.cfd&path=%2F&host=lon-rem-2.vip107.cfd&alpn=http%2F1.1&fp=chrome#%F0%9F%87%AC%F0%9F%87%A7%20%D0%92%D0%B5%D0%BB%D0%B8%D0%BA%D0%BE%D0%B1%D1%80%D0%B8%D1%82%D0%B0%D0%BD%D0%B8%D1%8F%20%E2%80%A2%20901ms"}, {"protocol": "vless", "host": "31.76.119.123", "port": 443, "uuid": "454431fc-71e2-42b1-b375-5b55dd06666a", "security": "reality", "sni": "example.org", "pbk": "aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU", "sid": "", "flow": "", "type": "tcp", "remark": "🇩🇪 Германия • 902ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "DE", "country_flag": "🇩🇪", "country_name": "Германия", "latency_ms": 902, "is_alive": true, "source_id": null, "uri": "vless://454431fc-71e2-42b1-b375-5b55dd06666a@31.76.119.123:443?type=tcp&headerType=none&security=reality&encryption=none&sni=example.org&fp=firefox&pbk=aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU#%F0%9F%87%A9%F0%9F%87%AA%20%D0%93%D0%B5%D1%80%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F%20%E2%80%A2%20902ms"}, {"protocol": "vless", "host": "90.156.218.163", "port": 443, "uuid": "adc11f30-e4cb-4985-bf5e-f9ded69c019f", "security": "reality", "sni": "eh.vk.ru", "pbk": "fNfokzklCF4l_c8k8PciOCjm5ecNoF_sNLjEtaO-xzI", "sid": "db04ce8bdb8900f1", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇵🇱 Польша • 917ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "PL", "country_flag": "🇵🇱", "country_name": "Польша", "latency_ms": 917, "is_alive": true, "source_id": null, "uri": "vless://adc11f30-e4cb-4985-bf5e-f9ded69c019f@90.156.218.163:443?type=tcp&security=reality&host=%3FTELEGRAM--MARAMBASHI--MARAMBASHI&sni=eh.vk.ru&pbk=fNfokzklCF4l_c8k8PciOCjm5ecNoF_sNLjEtaO-xzI&sid=db04ce8bdb8900f1&flow=xtls-rprx-vision&fp=ios#%F0%9F%87%B5%F0%9F%87%B1%20%D0%9F%D0%BE%D0%BB%D1%8C%D1%88%D0%B0%20%E2%80%A2%20917ms"}, {"protocol": "vless", "host": "109.172.8.73", "port": 443, "uuid": "b1c31d36-c6b5-414b-88d2-9e24e7bfcca3", "security": "tls", "sni": "www.nihaoyun.top", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇨🇿 Чехия • 972ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "CZ", "country_flag": "🇨🇿", "country_name": "Чехия", "latency_ms": 972, "is_alive": true, "source_id": null, "uri": "vless://b1c31d36-c6b5-414b-88d2-9e24e7bfcca3@109.172.8.73:443?security=tls&fp=chrome&sni=www.nihaoyun.top&type=ws&headerType=none&host=www.nihaoyun.top&path=%2F#%F0%9F%87%A8%F0%9F%87%BF%20%D0%A7%D0%B5%D1%85%D0%B8%D1%8F%20%E2%80%A2%20972ms"}, {"protocol": "vless", "host": "170.168.4.52", "port": 443, "uuid": "4643976f-85fa-40cf-9e58-ea28b50f253b", "security": "reality", "sni": "finl11.ali-bard.online", "pbk": "SB1uC0OEveYjSiS_Nuw9Ld-uVVXWqi794OGnldthY3I", "sid": "", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇫🇮 Финляндия • 993ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "FI", "country_flag": "🇫🇮", "country_name": "Финляндия", "latency_ms": 993, "is_alive": true, "source_id": null, "uri": "vless://4643976f-85fa-40cf-9e58-ea28b50f253b@170.168.4.52:443?encryption=none&flow=xtls-rprx-vision&fp=firefox&pbk=SB1uC0OEveYjSiS_Nuw9Ld-uVVXWqi794OGnldthY3I&security=reality&sni=finl11.ali-bard.online&type=tcp#%F0%9F%87%AB%F0%9F%87%AE%20%D0%A4%D0%B8%D0%BD%D0%BB%D1%8F%D0%BD%D0%B4%D0%B8%D1%8F%20%E2%80%A2%20993ms"}, {"protocol": "vless", "host": "78.159.250.214", "port": 443, "uuid": "4054fdc2-ee80-4419-8a8e-d937df4719e2", "security": "reality", "sni": "qq.utiltools.site", "pbk": "drY21DHNOr6ezJLA2B10mzTExeJ9-gVBfTBNLwVBtWI", "sid": "", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇪🇪 Эстония • 1069ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EE", "country_flag": "🇪🇪", "country_name": "Эстония", "latency_ms": 1069, "is_alive": true, "source_id": null, "uri": "vless://4054fdc2-ee80-4419-8a8e-d937df4719e2@78.159.250.214:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=qq.utiltools.site&fp=random&pbk=drY21DHNOr6ezJLA2B10mzTExeJ9-gVBfTBNLwVBtWI&spx=%2F&type=tcp#%F0%9F%87%AA%F0%9F%87%AA%20%D0%AD%D1%81%D1%82%D0%BE%D0%BD%D0%B8%D1%8F%20%E2%80%A2%201069ms"}, {"protocol": "vless", "host": "qq.utiltools.site", "port": 443, "uuid": "4054fdc2-ee80-4419-8a8e-d937df4719e2", "security": "reality", "sni": "qq.utiltools.site", "pbk": "drY21DHNOr6ezJLA2B10mzTExeJ9-gVBfTBNLwVBtWI", "sid": "", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇪🇺 Европа • 1078ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EU", "country_flag": "🇪🇺", "country_name": "Европа", "latency_ms": 1078, "is_alive": true, "source_id": null, "uri": "vless://4054fdc2-ee80-4419-8a8e-d937df4719e2@qq.utiltools.site:443?Telegram=Cfox_Server---Cfox_Server---Cfox_Server---Cfox_Server---Cfox_Server---Cfox_Server---Cfox_Server---Cfox_Server---Cfox_Server---Cfox_Server---Cfox_Server---Cfox_Server---Cfox_Server---Cfox_Server---Cfox_Server---Cfox_Server&security=reality&encryption=none&pbk=drY21DHNOr6ezJLA2B10mzTExeJ9-gVBfTBNLwVBtWI&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=qq.utiltools.site#%F0%9F%87%AA%F0%9F%87%BA%20%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%20%E2%80%A2%201078ms"}, {"protocol": "vless", "host": "nl.monkora.org", "port": 443, "uuid": "454431fc-71e2-42b1-b375-5b55dd06666a", "security": "reality", "sni": "example.org", "pbk": "aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU", "sid": "", "flow": "", "type": "tcp", "remark": "🇪🇺 Европа • 1085ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EU", "country_flag": "🇪🇺", "country_name": "Европа", "latency_ms": 1085, "is_alive": true, "source_id": null, "uri": "vless://454431fc-71e2-42b1-b375-5b55dd06666a@nl.monkora.org:443?encryption=none&security=reality&sni=example.org&fp=firefox&pbk=aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU&type=tcp&headerType=none#%F0%9F%87%AA%F0%9F%87%BA%20%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%20%E2%80%A2%201085ms"}, {"protocol": "vless", "host": "islam.konus.buzz", "port": 443, "uuid": "8f6e49e6-7f03-4f10-9da9-1716158d80ed", "security": "reality", "sni": "islam.konus.buzz", "pbk": "RAO2mBIVFV-jEUhUsnszqPDJDbn0rzdh25q4Kf4wPzA", "sid": "f9f79c884e393c6c", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇪🇺 Европа • 1167ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EU", "country_flag": "🇪🇺", "country_name": "Европа", "latency_ms": 1167, "is_alive": true, "source_id": null, "uri": "vless://8f6e49e6-7f03-4f10-9da9-1716158d80ed@islam.konus.buzz:443?type=tcp&headerType=none&security=reality&encryption=none&sni=islam.konus.buzz&fp=random&pbk=RAO2mBIVFV-jEUhUsnszqPDJDbn0rzdh25q4Kf4wPzA&sid=f9f79c884e393c6c&flow=xtls-rprx-vision#%F0%9F%87%AA%F0%9F%87%BA%20%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%20%E2%80%A2%201167ms"}, {"protocol": "vless", "host": "api.mediapriboy.cc", "port": 443, "uuid": "97561873-a59e-4a91-bb7e-56e869ca3328", "security": "reality", "sni": "api.mediapriboy.cc", "pbk": "r5WB5FnSCt4eeBC1FJMfkWHbzsMuabo0Rc6wuAhlZUs", "sid": "a8", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇳🇱 Нидерланды • 1239ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "NL", "country_flag": "🇳🇱", "country_name": "Нидерланды", "latency_ms": 1239, "is_alive": true, "source_id": null, "uri": "vless://97561873-a59e-4a91-bb7e-56e869ca3328@api.mediapriboy.cc:443?encryption=none&flow=xtls-rprx-vision&type=tcp&security=reality&sni=api.mediapriboy.cc&pbk=r5WB5FnSCt4eeBC1FJMfkWHbzsMuabo0Rc6wuAhlZUs&sid=a8&fp=firefox#%F0%9F%87%B3%F0%9F%87%B1%20%D0%9D%D0%B8%D0%B4%D0%B5%D1%80%D0%BB%D0%B0%D0%BD%D0%B4%D1%8B%20%E2%80%A2%201239ms"}, {"protocol": "vless", "host": "cz.monkora.org", "port": 443, "uuid": "454431fc-71e2-42b1-b375-5b55dd06666a", "security": "reality", "sni": "example.org", "pbk": "aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU", "sid": "", "flow": "", "type": "tcp", "remark": "🇪🇺 Европа • 1413ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EU", "country_flag": "🇪🇺", "country_name": "Европа", "latency_ms": 1413, "is_alive": true, "source_id": null, "uri": "vless://454431fc-71e2-42b1-b375-5b55dd06666a@cz.monkora.org:443?encryption=none&security=reality&sni=example.org&fp=firefox&pbk=aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU&type=tcp&headerType=none#%F0%9F%87%AA%F0%9F%87%BA%20%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%20%E2%80%A2%201413ms"}, {"protocol": "vless", "host": "86.54.82.184", "port": 443, "uuid": "454431fc-71e2-42b1-b375-5b55dd06666a", "security": "reality", "sni": "example.org", "pbk": "aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU", "sid": "", "flow": "", "type": "tcp", "remark": "🇨🇿 Чехия • 1492ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "CZ", "country_flag": "🇨🇿", "country_name": "Чехия", "latency_ms": 1492, "is_alive": true, "source_id": null, "uri": "vless://454431fc-71e2-42b1-b375-5b55dd06666a@86.54.82.184:443?encryption=none&fp=firefox&pbk=aUdvs6o4PHN6jmdkIKBA2rHsN_7l8W2SaDfNgzn-BwU&security=reality&sni=example.org&type=tcp#%F0%9F%87%A8%F0%9F%87%BF%20%D0%A7%D0%B5%D1%85%D0%B8%D1%8F%20%E2%80%A2%201492ms"}, {"protocol": "vless", "host": "qq.utiltools.ru", "port": 443, "uuid": "eb78e1f0-d921-4ca9-a889-261fcc5a0547", "security": "reality", "sni": "qq.utiltools.ru", "pbk": "drY21DHNOr6ezJLA2B10mzTExeJ9-gVBfTBNLwVBtWI", "sid": "", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇷🇺 Россия [🎮 Игровой] • 65ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 65, "is_alive": true, "source_id": null, "uri": "vless://eb78e1f0-d921-4ca9-a889-261fcc5a0547@qq.utiltools.ru:443?encryption=none&type=tcp&security=reality&headerType=none&host=%2F%3FBIA_TELEGRAM%40ShadowProxy66&sni=qq.utiltools.ru&fp=qq&insecure=1&allowInsecure=1&pbk=drY21DHNOr6ezJLA2B10mzTExeJ9-gVBfTBNLwVBtWI&flow=xtls-rprx-vision#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%5B%F0%9F%8E%AE%20%D0%98%D0%B3%D1%80%D0%BE%D0%B2%D0%BE%D0%B9%5D%20%E2%80%A2%2065ms"}, {"protocol": "vless", "host": "81.94.148.214", "port": 443, "uuid": "bc5ec86c-3e65-4272-994c-59a924c72a68", "security": "tls", "sni": "fbsv6.guardora.pro", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇷🇺 Россия • 218ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 218, "is_alive": true, "source_id": null, "uri": "vless://bc5ec86c-3e65-4272-994c-59a924c72a68@81.94.148.214:443?encryption=none&fp=chrome&path=%2Fws&security=tls&sni=fbsv6.guardora.pro&type=ws#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%E2%80%A2%20218ms"}, {"protocol": "vless", "host": "87.228.101.179", "port": 443, "uuid": "407294c6-c298-49bb-8ff4-82be35c17da5", "security": "reality", "sni": "ads.x5.ru", "pbk": "0EsjnmPXqgmtnYhWNvjM93k6Lso3M9biZRiA4Z7sKUc", "sid": "00000000", "flow": "", "type": "grpc", "remark": "🇷🇺 Россия • 693ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 693, "is_alive": true, "source_id": null, "uri": "vless://407294c6-c298-49bb-8ff4-82be35c17da5@87.228.101.179:443?mode=gun&security=reality&encryption=none&pbk=0EsjnmPXqgmtnYhWNvjM93k6Lso3M9biZRiA4Z7sKUc&fp=edge&type=grpc&sni=ads.x5.ru&sid=00000000#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%E2%80%A2%20693ms"}, {"protocol": "vless", "host": "84.201.180.177", "port": 7443, "uuid": "b4370239-e25b-4396-8d67-2c6f2f6c8655", "security": "reality", "sni": "api.dobro.ru", "pbk": "8qUiIosG5-OQWo0tD29BQCbxb50neUg8BynxdAvDzB4", "sid": "132142", "flow": "xtls-rprx-vision", "type": "raw", "remark": "🇷🇺 Россия • 884ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 884, "is_alive": true, "source_id": null, "uri": "vless://b4370239-e25b-4396-8d67-2c6f2f6c8655@84.201.180.177:7443?type=raw&security=reality&flow=xtls-rprx-vision&fp=firefox&pbk=8qUiIosG5-OQWo0tD29BQCbxb50neUg8BynxdAvDzB4&sid=132142&sni=api.dobro.ru#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%E2%80%A2%20884ms"}, {"protocol": "vless", "host": "2.26.104.40", "port": 443, "uuid": "f4d71fd6-1c25-4748-836b-1dbda9268039", "security": "reality", "sni": "s5.mangateka.top", "pbk": "GLb7RkOVWgSiZ7oZ6MfeByW284NpBy2FrOtgEPXbuic", "sid": "d343252c9207a130", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇷🇺 Россия • 975ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 975, "is_alive": true, "source_id": null, "uri": "vless://f4d71fd6-1c25-4748-836b-1dbda9268039@2.26.104.40:443?type=tcp&security=reality&flow=xtls-rprx-vision&fp=firefox&pbk=GLb7RkOVWgSiZ7oZ6MfeByW284NpBy2FrOtgEPXbuic&sid=d343252c9207a130&sni=s5.mangateka.top#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%E2%80%A2%20975ms"}, {"protocol": "vless", "host": "185.147.26.210", "port": 443, "uuid": "1c5ed2e1-56da-41ab-9a78-159d9892ec17", "security": "reality", "sni": "example.com", "pbk": "9rdvkUGJyNbRvsB0Pp06h1URq9AHDPRtH9-wmNB1-j4", "sid": "e4aa362b5f9d07d7", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇷🇺 Россия • 1116ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 1116, "is_alive": true, "source_id": null, "uri": "vless://1c5ed2e1-56da-41ab-9a78-159d9892ec17@185.147.26.210:443?security=reality&encryption=none&pbk=9rdvkUGJyNbRvsB0Pp06h1URq9AHDPRtH9-wmNB1-j4&host=%2F%3FTELEGRAM--MARAMBASHI--MARAMBASHI&headerType=none&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=example.com&sid=e4aa362b5f9d07d7#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%E2%80%A2%201116ms"}, {"protocol": "vless", "host": "46.243.232.125", "port": 443, "uuid": "bc5ec86c-3e65-4272-994c-59a924c72a68", "security": "tls", "sni": "fbsv6.guardora.pro", "pbk": "", "sid": "", "flow": "", "type": "ws", "remark": "🇷🇺 Россия [🛡️ Белый список] • 352ms", "is_whitelist": true, "whitelist_label": "🛡️ Белый список", "whitelist_category": "Keyword-Bypass", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 352, "is_alive": true, "source_id": null, "uri": "vless://bc5ec86c-3e65-4272-994c-59a924c72a68@46.243.232.125:443?encryption=none&fp=firefox&path=%2Fws&security=tls&sni=fbsv6.guardora.pro&type=ws#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%5B%F0%9F%9B%A1%EF%B8%8F%20%D0%91%D0%B5%D0%BB%D1%8B%D0%B9%20%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA%5D%20%E2%80%A2%20352ms"}, {"protocol": "vless", "host": "nw.shadownet.pro", "port": 8443, "uuid": "03e6c071-d34b-4236-9d06-a57cc364bede", "security": "reality", "sni": "yandex.ru", "pbk": "RDoffndyw7wskux1uVqjlPPe_ikh3cisVEoyleiRlR4", "sid": "", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇷🇺 Россия [🛡️ Яндекс/Дзен] • 375ms", "is_whitelist": true, "whitelist_label": "🛡️ Яндекс/Дзен", "whitelist_category": "Yandex-Dzen", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 375, "is_alive": true, "source_id": null, "uri": "vless://03e6c071-d34b-4236-9d06-a57cc364bede@nw.shadownet.pro:8443?type=tcp&headerType=none&security=reality&encryption=none&sni=yandex.ru&fp=qq&pbk=RDoffndyw7wskux1uVqjlPPe_ikh3cisVEoyleiRlR4&flow=xtls-rprx-vision#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%5B%F0%9F%9B%A1%EF%B8%8F%20%D0%AF%D0%BD%D0%B4%D0%B5%D0%BA%D1%81/%D0%94%D0%B7%D0%B5%D0%BD%5D%20%E2%80%A2%20375ms"}, {"protocol": "vless", "host": "81.94.148.120", "port": 7449, "uuid": "2690c11f-7258-43fe-aeb9-d90f93a3c317", "security": "reality", "sni": "passport.yandex.ru", "pbk": "blW-TdkBvKRn4-lkM64Cn2QgfOqjCRYRQ9upE6RPt3c", "sid": "c0c41dc21cf7c18e", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇳🇱 Нидерланды [🛡️ Яндекс/Дзен] • 673ms", "is_whitelist": true, "whitelist_label": "🛡️ Яндекс/Дзен", "whitelist_category": "Yandex-Dzen", "country_code": "NL", "country_flag": "🇳🇱", "country_name": "Нидерланды", "latency_ms": 673, "is_alive": true, "source_id": null, "uri": "vless://2690c11f-7258-43fe-aeb9-d90f93a3c317@81.94.148.120:7449?encryption=none&flow=xtls-rprx-vision&security=reality&sni=passport.yandex.ru&fp=random&pbk=blW-TdkBvKRn4-lkM64Cn2QgfOqjCRYRQ9upE6RPt3c&sid=c0c41dc21cf7c18e&type=tcp#%F0%9F%87%B3%F0%9F%87%B1%20%D0%9D%D0%B8%D0%B4%D0%B5%D1%80%D0%BB%D0%B0%D0%BD%D0%B4%D1%8B%20%5B%F0%9F%9B%A1%EF%B8%8F%20%D0%AF%D0%BD%D0%B4%D0%B5%D0%BA%D1%81/%D0%94%D0%B7%D0%B5%D0%BD%5D%20%E2%80%A2%20673ms"}, {"protocol": "vless", "host": "185.229.9.176", "port": 46018, "uuid": "d01e89b1-e260-4d30-a363-4a46ff3f9627", "security": "reality", "sni": "ligastavok.ru", "pbk": "een4U3X5mnY1gH2swiakXS9BJ8P4omf8Qp_s8sTp_3Y", "sid": "68ae5e7c11f80af5", "flow": "", "type": "grpc", "remark": "🇷🇺 Россия [🛡️ Обход-СМИ] • 1097ms", "is_whitelist": true, "whitelist_label": "🛡️ Обход-СМИ", "whitelist_category": "Bypass-Media", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 1097, "is_alive": true, "source_id": null, "uri": "vless://d01e89b1-e260-4d30-a363-4a46ff3f9627@185.229.9.176:46018?mode=gun&security=reality&encryption=none&pbk=een4U3X5mnY1gH2swiakXS9BJ8P4omf8Qp_s8sTp_3Y&fp=firefox&spx=%2F&type=grpc&sni=ligastavok.ru&sid=68ae5e7c11f80af5#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%5B%F0%9F%9B%A1%EF%B8%8F%20%D0%9E%D0%B1%D1%85%D0%BE%D0%B4-%D0%A1%D0%9C%D0%98%5D%20%E2%80%A2%201097ms"}];

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const url = new URL(request.url);
  const path = url.pathname.replace(/\/+$/, '') || '/';
  const origin = url.origin;

  // 1. Telegram Webhook
  if (path === '/webhook/telegram' && request.method === 'POST') {
    return handleTelegramWebhook(request, origin);
  }

  // 2. Telegram WebApp Mini App (Opens directly inside Telegram)
  if (path === '/app') {
    return serveMiniApp(request, origin);
  }

  // 3. Dynamic Data Sync API (for automated background checker)
  if (path === '/api/sync' && request.method === 'POST') {
    return handleSync(request);
  }

  // 4. Setup Telegram Webhook & Menu Button
  if (path === '/setup-telegram') {
    return setupTelegramWebhook(origin);
  }

  // 5. API Stats
  if (path === '/api/stats') {
    return new Response(JSON.stringify(getStats()), {
      headers: { 'Content-Type': 'application/json; charset=utf-8', 'Access-Control-Allow-Origin': '*' }
    });
  }

  // 6. Personal User Subscriptions (/sub/u/:userId)
  if (path.startsWith('/sub/u/')) {
    const userId = path.replace('/sub/u/', '').split('/')[0] || 'default';
    return servePersonalSub(userId, 'Incy');
  }

  // 7. General Subscriptions (Foreign first, RU middle, Whitelist at bottom)
  if (path === '/sub' || path === '/sub/all' || path === '/sub/incy') {
    return serveBase64Sub(getOrderedServers(), 'Incy-Universal');
  }
  if (path === '/sub/happ') {
    return serveBase64Sub(getOrderedServers(), 'Happ-Universal');
  }
  if (path === '/sub/whitelist') {
    const wl = CACHED_SERVERS.filter(s => s.is_whitelist);
    return serveBase64Sub(wl.length > 0 ? wl : CACHED_SERVERS, 'Whitelist-Обход');
  }
  if (path === '/sub/gaming') {
    const gaming = CACHED_SERVERS.filter(s => !s.is_whitelist && s.country_code !== 'RU' && s.latency_ms > 0 && s.latency_ms <= 85);
    return serveBase64Sub(gaming.length > 0 ? gaming : CACHED_SERVERS.slice(0, 30), 'Gaming-LowPing');
  }
  if (path === '/sub/top3') {
    const top3 = getTop3PerCountry();
    return serveBase64Sub(top3, 'Top3-Country');
  }
  if (path.startsWith('/sub/country/')) {
    const cc = path.replace('/sub/country/', '').toUpperCase();
    const cServers = CACHED_SERVERS.filter(s => s.country_code === cc);
    return serveBase64Sub(cServers, `Country-${cc}`);
  }

  // 8. Direct 1-Click Keys
  // ⚡ Самый первый: Лучший зарубежный сервер (Обязательно НЕ Россия!)
  if (path === '/best') {
    const best = getBestForeignServer();
    return new Response(best ? best.uri : 'No servers available', { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
  }
  if (path === '/best-whitelist') {
    const bestWl = getBestWhitelistServer();
    return new Response(bestWl ? bestWl.uri : 'No servers available', { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
  }
  if (path === '/best-gaming') {
    const bestGame = getBestGamingServer();
    return new Response(bestGame ? bestGame.uri : 'No servers available', { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
  }

  // 9. Clash Meta & Singbox
  if (path === '/clash') {
    return serveClashMeta();
  }
  if (path === '/singbox') {
    return serveSingbox();
  }

  // 10. Default Dashboard
  return serveDashboard(origin);
}

// =========================================================================
// Subscription Delivery & 3-Tier Ordering
// =========================================================================
function getOrderedServers() {
  const foreign = CACHED_SERVERS.filter(s => !s.is_whitelist && s.country_code !== 'RU').sort((a,b) => (a.latency_ms||999) - (b.latency_ms||999));
  const ru = CACHED_SERVERS.filter(s => !s.is_whitelist && s.country_code === 'RU').sort((a,b) => (a.latency_ms||999) - (b.latency_ms||999));
  const wl = CACHED_SERVERS.filter(s => s.is_whitelist).sort((a,b) => (a.latency_ms||999) - (b.latency_ms||999));
  return [...foreign, ...ru, ...wl];
}

function getBestForeignServer() {
  return CACHED_SERVERS.find(s => !s.is_whitelist && s.country_code !== 'RU') || CACHED_SERVERS[0];
}

function getBestGamingServer() {
  return CACHED_SERVERS.find(s => !s.is_whitelist && s.country_code !== 'RU' && s.latency_ms > 0 && s.latency_ms <= 85) || getBestForeignServer();
}

function getBestWhitelistServer() {
  return CACHED_SERVERS.find(s => s.is_whitelist) || CACHED_SERVERS[0];
}

function servePersonalSub(userId, clientName) {
  // Get top 3 per country (ordered: Foreign first, RU middle, Whitelist bottom)
  const servers = getTop3PerCountry();
  const uris = servers.map((s, idx) => {
    const flag = s.country_flag || '🌐';
    const cName = s.country_name || s.country_code || 'VPN';
    const tag = s.is_whitelist ? ` [${s.whitelist_label || '🛡️ Обход'}]` : (s.latency_ms <= 85 ? ' [🎮 Игровой]' : '');
    const ping = s.latency_ms > 0 ? ` • ${s.latency_ms}ms` : '';
    const cleanRemark = `${flag} ${cName}${tag} #${idx+1}${ping}`;

    const baseUri = s.uri.split('#')[0];
    return `${baseUri}#${encodeURIComponent(cleanRemark)}`;
  }).filter(Boolean);

  const plainText = uris.join('\n');
  const base64Text = btoa(unescape(encodeURIComponent(plainText)));

  return new Response(base64Text, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
      'Subscription-Userinfo': 'upload=0; download=0; total=1073741824000; expire=0',
      'profile-update-interval': '6',
      'Content-Disposition': `inline; filename="sub_user_${userId}.txt"`
    }
  });
}

function serveBase64Sub(servers, label) {
  const uris = servers.map((s, idx) => {
    const flag = s.country_flag || '🌐';
    const cName = s.country_name || s.country_code || 'VPN';
    const tag = s.is_whitelist ? ` [${s.whitelist_label || '🛡️ Обход'}]` : (s.latency_ms <= 85 ? ' [🎮 Игровой]' : '');
    const ping = s.latency_ms > 0 ? ` • ${s.latency_ms}ms` : '';
    const cleanRemark = `${flag} ${cName}${tag} #${idx+1}${ping}`;
    const baseUri = s.uri.split('#')[0];
    return `${baseUri}#${encodeURIComponent(cleanRemark)}`;
  }).filter(Boolean);

  const plainText = uris.join('\n');
  const base64Text = btoa(unescape(encodeURIComponent(plainText)));

  return new Response(base64Text, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
      'Subscription-Userinfo': 'upload=0; download=0; total=1073741824000; expire=0',
      'profile-update-interval': '6',
      'Content-Disposition': `inline; filename="sub_${encodeURIComponent(label)}.txt"`
    }
  });
}

function getTop3PerCountry() {
  const ordered = getOrderedServers();
  const byCountry = {};
  const result = [];
  for (const s of ordered) {
    const cc = s.country_code || 'OTHER';
    if (!byCountry[cc]) byCountry[cc] = 0;
    if (byCountry[cc] < 3) {
      byCountry[cc]++;
      result.push(s);
    }
  }
  return result;
}

function getStats() {
  const total = CACHED_SERVERS.length;
  const wlCount = CACHED_SERVERS.filter(s => s.is_whitelist).length;
  const gamingCount = CACHED_SERVERS.filter(s => !s.is_whitelist && s.country_code !== 'RU' && s.latency_ms > 0 && s.latency_ms <= 85).length;
  const pings = CACHED_SERVERS.map(s => s.latency_ms).filter(p => p > 0);
  const avgPing = pings.length > 0 ? Math.round(pings.reduce((a, b) => a + b, 0) / pings.length) : 0;
  const countries = [...new Set(CACHED_SERVERS.map(s => s.country_code).filter(c => c && c !== 'OTHER'))];

  return {
    total,
    alive_count: total,
    whitelist_count: wlCount,
    gaming_count: gamingCount,
    avg_ping: avgPing,
    countries_count: countries.length,
    countries,
    best_server: getBestForeignServer(),
    best_whitelist: getBestWhitelistServer(),
    best_gaming: getBestGamingServer()
  };
}

// =========================================================================
// Telegram Bot Webhook & Mini App
// =========================================================================
async function setupTelegramWebhook(origin) {
  const hookUrl = `${origin}/webhook/telegram`;
  const tgRes = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/setWebhook?url=${encodeURIComponent(hookUrl)}&drop_pending_updates=true`);
  const tgData = await tgRes.json();

  // Set native menu button to open WebApp
  await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/setChatMenuButton`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      menu_button: {
        type: 'web_app',
        text: '🍄 VPN Hub',
        web_app: { url: `${origin}/app` }
      }
    })
  });

  return new Response(JSON.stringify({ status: 'ok', webhook: hookUrl, telegram: tgData }), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' }
  });
}

async function handleTelegramWebhook(request, origin) {
  try {
    const update = await request.json();
    if (update.message) {
      await handleMessage(update.message, origin);
    } else if (update.callback_query) {
      await handleCallback(update.callback_query, origin);
    }
  } catch (e) {
    console.error('Telegram webhook error:', e);
  }
  return new Response('OK');
}

async function sendTelegram(method, payload) {
  const url = `https://api.telegram.org/bot${BOT_TOKEN}/${method}`;
  return fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
}

async function handleMessage(msg, origin) {
  const chatId = msg.chat.id;
  const userId = msg.from.id;
  const firstName = msg.from.first_name || 'Друг';
  const text = msg.text || '';

  if (text.startsWith('/start') || text.startsWith('/help')) {
    const personalSubUrl = `${origin}/sub/u/${userId}`;
    const appUrl = `${origin}/app?u=${userId}`;

    const welcome = `🍄 <b>HUSTLER VPN • Персональный Hub</b>\n\n` +
      `Привет, <b>${firstName}</b>! Для вас сгенерирована <b>личная подписка</b> без нерабочих узлов и без рекламы.\n\n` +
      `⚡ <b>Поддержка клиентов:</b> Incy (в приоритете) и Happ\n` +
      `🛡️ <b>Белые списки РФ:</b> VK, Госуслуги, Яндекс (обход глушений)\n` +
      `🎮 <b>Игровые узлы:</b> с минимальным пингом (&lt;65ms)\n\n` +
      `Нажмите <b>«🚀 Открыть VPN Hub»</b> ниже для удобного управления:`;

    const keyboard = {
      inline_keyboard: [
        [
          { text: '🚀 Открыть VPN Hub (Incy / Happ)', web_app: { url: appUrl } }
        ],
        [
          { text: '⚡ Лучший зарубежный сервер (Мин. пинг)', callback_data: 'best_server' }
        ],
        [
          { text: '📱 Добавить в Incy (1 клик)', callback_data: `sub_incy_${userId}` },
          { text: '🚀 Добавить в Happ', callback_data: `sub_happ_${userId}` }
        ],
        [
          { text: '🎮 Игровой сервер (<65ms)', callback_data: 'best_game' },
          { text: '🌍 Топ-3 по странам', callback_data: `sub_top3_${userId}` }
        ],
        [
          { text: '🛡️ Белые списки РФ (VK / Госуслуги / СМИ)', callback_data: 'best_wl' }
        ]
      ]
    };

    await sendTelegram('sendMessage', {
      chat_id: chatId,
      text: welcome,
      parse_mode: 'HTML',
      reply_markup: keyboard
    });
  }
}

async function handleCallback(cb, origin) {
  const chatId = cb.message.chat.id;
  const data = cb.data;

  if (data.startsWith('sub_incy')) {
    const userId = data.replace('sub_incy_', '') || cb.from.id;
    const subUrl = `${origin}/sub/u/${userId}`;
    const text = `📱 <b>Ваша личная подписка для Incy:</b>\n\n` +
      `1. Скопируйте ссылку подписки (нажмите на неё):\n` +
      `<code>${subUrl}</code>\n\n` +
      `2. Откройте приложение <b>Incy</b>\n` +
      `3. Нажмите <b>«+»</b> в правом верхнем углу → <b>«Импорт из буфера обмена»</b>\n` +
      `4. Нажмите большую кнопку подключения!\n\n` +
      `<i>Все сервера гарантированно рабочие (проверены TLS handshake), с названиями стран и флагами.</i>`;

    await sendTelegram('sendMessage', { chat_id: chatId, text, parse_mode: 'HTML' });
  } else if (data.startsWith('sub_happ')) {
    const userId = data.replace('sub_happ_', '') || cb.from.id;
    const subUrl = `${origin}/sub/u/${userId}`;
    const text = `🚀 <b>Ваша личная подписка для Happ:</b>\n\n` +
      `Скопируйте ссылку и вставьте в Happ:\n` +
      `<code>${subUrl}</code>`;
    await sendTelegram('sendMessage', { chat_id: chatId, text, parse_mode: 'HTML' });
  } else if (data === 'best_server') {
    const best = getBestForeignServer();
    if (best) {
      const text = `⚡ <b>Лучший зарубежный сервер (Минимальный пинг):</b>\n\n` +
        `<b>Локация:</b> ${best.country_flag} ${best.country_name} (${best.country_code})\n` +
        `<b>Пинг:</b> <code>${best.latency_ms} ms</code>\n` +
        `<i>(Зарубежный сервер для свободного доступа: YouTube, Instagram, ChatGPT)</i>\n\n` +
        `Нажмите на ключ ниже, чтобы скопировать в Incy:\n` +
        `<code>${best.uri}</code>`;
      await sendTelegram('sendMessage', { chat_id: chatId, text, parse_mode: 'HTML' });
    }
  } else if (data === 'best_game') {
    const bestGame = getBestGamingServer();
    if (bestGame) {
      const text = `🎮 <b>Игровой зарубежный сервер с ультранизкой задержкой:</b>\n\n` +
        `<b>Локация:</b> ${bestGame.country_flag} ${bestGame.country_name}\n` +
        `<b>Пинг:</b> <code>${bestGame.latency_ms} ms</code> (Brawl Stars, Discord, Онлайн-игры)\n\n` +
        `Нажмите для копирования:\n` +
        `<code>${bestGame.uri}</code>`;
      await sendTelegram('sendMessage', { chat_id: chatId, text, parse_mode: 'HTML' });
    }
  } else if (data === 'best_wl') {
    const bestWl = getBestWhitelistServer();
    if (bestWl) {
      const text = `🛡️ <b>Сервер белого списка (Обход глушений РФ):</b>\n\n` +
        `<b>Сервис:</b> ${bestWl.whitelist_label || 'Белый список'}\n` +
        `<b>Маскировка:</b> <code>${bestWl.sni || 'vk.com'}</code>\n` +
        `<b>Локация:</b> ${bestWl.country_flag} ${bestWl.country_name}\n` +
        `<b>Пинг:</b> <code>${bestWl.latency_ms} ms</code>\n\n` +
        `Нажмите на ключ для копирования:\n` +
        `<code>${bestWl.uri}</code>`;
      await sendTelegram('sendMessage', { chat_id: chatId, text, parse_mode: 'HTML' });
    }
  } else if (data.startsWith('sub_top3')) {
    const userId = data.replace('sub_top3_', '') || cb.from.id;
    const subUrl = `${origin}/sub/top3`;
    const text = `🌍 <b>Подписка «Топ-3 по каждой стране»:</b>\n\n` +
      `Включает по 3 лучших сервера на каждую локацию:\n` +
      `<code>${subUrl}</code>`;
    await sendTelegram('sendMessage', { chat_id: chatId, text, parse_mode: 'HTML' });
  }

  await sendTelegram('answerCallbackQuery', { callback_query_id: cb.id });
}

// =========================================================================
// Telegram WebApp Mini App (/app)
// =========================================================================
function serveMiniApp(request, origin) {
  const url = new URL(request.url);
  const userId = url.searchParams.get('u') || 'user';
  const personalSubUrl = `${origin}/sub/u/${userId}`;
  const stats = getStats();

  const html = `<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>🍄 HUSTLER VPN Mini App</title>
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #090d16;
      --card: rgba(18, 24, 38, 0.85);
      --border: rgba(255, 255, 255, 0.08);
      --cyan: #06b6d4;
      --emerald: #10b981;
      --purple: #8b5cf6;
      --text: #f8fafc;
      --text-sec: #94a3b8;
    }
    * { margin:0; padding:0; box-sizing:border-box; -webkit-tap-highlight-color: transparent; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', sans-serif;
      padding: 16px;
      line-height: 1.4;
      min-height: 100vh;
    }
    .header {
      display: flex; align-items: center; justify-content: space-between;
      padding-bottom: 14px; border-bottom: 1px solid var(--border); margin-bottom: 16px;
    }
    .user-pill {
      font-size: 11px; background: rgba(255,255,255,0.06); padding: 4px 10px;
      border-radius: 99px; border: 1px solid var(--border); font-family: 'JetBrains Mono', monospace;
    }
    .big-actions { display: flex; flex-direction: column; gap: 12px; margin-bottom: 18px; }
    .btn-main {
      display: flex; align-items: center; justify-content: center; gap: 10px;
      width: 100%; padding: 15px; border-radius: 14px; font-weight: 800; font-size: 15px;
      border: none; cursor: pointer; transition: all 0.2s; text-decoration: none;
    }
    .btn-incy {
      background: linear-gradient(135deg, var(--cyan), #0284c7); color: #fff;
      box-shadow: 0 4px 16px rgba(6,182,212,0.3);
    }
    .btn-happ {
      background: linear-gradient(135deg, var(--purple), #6366f1); color: #fff;
      box-shadow: 0 4px 16px rgba(139,92,246,0.3);
    }
    .btn-main:active { transform: scale(0.98); }

    .quick-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 18px; }
    .btn-quick {
      background: var(--card); border: 1px solid var(--border); border-radius: 12px;
      padding: 12px 10px; text-align: center; cursor: pointer; color: var(--text);
      font-size: 13px; font-weight: 700; display: flex; flex-direction: column; align-items: center; gap: 4px;
    }
    .btn-quick:active { background: rgba(255,255,255,0.1); }
    .btn-quick span { font-size: 11px; color: var(--text-sec); font-weight: 500; }

    .sub-box {
      background: var(--card); border: 1px solid var(--border); border-radius: 14px;
      padding: 14px; margin-bottom: 16px;
    }
    .sub-input {
      width: 100%; background: rgba(0,0,0,0.4); border: 1px solid var(--border);
      border-radius: 8px; padding: 10px; color: #fff; font-family: monospace; font-size: 12px;
      margin: 8px 0; outline: none;
    }

    .modal-overlay {
      position: fixed; inset: 0; background: rgba(0,0,0,0.8); backdrop-filter: blur(8px);
      display: none; align-items: center; justify-content: center; z-index: 100; padding: 20px;
    }
    .modal-card {
      background: #121826; border: 1px solid var(--cyan); border-radius: 18px;
      padding: 20px; width: 100%; max-width: 360px; text-align: center;
    }
    .toast {
      position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
      background: #1e293b; border: 1px solid var(--cyan); color: #fff; padding: 10px 18px;
      border-radius: 99px; font-weight: 700; font-size: 13px; display: none; z-index: 200;
    }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <h2 style="font-size:18px; font-weight:800;">🍄 HUSTLER VPN</h2>
      <p style="font-size:11px; color:var(--text-sec);">Сервера проверены • Без N/A</p>
    </div>
    <div class="user-pill" id="user-display">ID: ${userId}</div>
  </div>

  <!-- 1. Top Action: Best Foreign Server (Guaranteed Non-RU) -->
  <div style="background: linear-gradient(135deg, rgba(6,182,212,0.18), rgba(16,185,129,0.18)); border: 1.5px solid var(--cyan); border-radius: 16px; padding: 16px; margin-bottom: 16px; cursor: pointer;" onclick="copyDirectKey('${origin}/best', '⚡ Лучший зарубежный сервер скопирован!')">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="font-size:11px; color:var(--cyan); font-weight:800; text-transform:uppercase; letter-spacing:0.5px;">⚡ САМЫЙ БЫСТРЫЙ СЕРВЕР (НЕ РОССИЯ)</div>
        <div style="font-size:15px; font-weight:800; margin-top:2px;">${stats.best_server ? `${stats.best_server.country_flag} ${stats.best_server.country_name} • ${stats.best_server.latency_ms}ms` : '⚡ Зарубежный узел'}</div>
        <div style="font-size:11px; color:var(--text-sec); margin-top:2px;">YouTube, Instagram, ChatGPT без блокировок</div>
      </div>
      <button class="btn-main" style="width:auto; padding:10px 16px; font-size:12px; background:var(--cyan); color:#000; border-radius:10px;">Скопировать</button>
    </div>
  </div>

  <!-- 2. Primary Incy & Happ Buttons -->
  <div class="big-actions">
    <button class="btn-main btn-incy" onclick="installSub('Incy')">
      📱 Добавить подписку в Incy (1 клик)
    </button>
    <button class="btn-main btn-happ" onclick="installSub('Happ')">
      🚀 Добавить подписку в Happ
    </button>
  </div>

  <!-- 3. Quick foreign server picks -->
  <div style="font-size:12px; font-weight:700; color:var(--text-sec); text-transform:uppercase; margin-bottom:8px;">Быстрый выбор:</div>
  <div class="quick-grid">
    <div class="btn-quick" onclick="copyDirectKey('${origin}/best-gaming', '🎮 Игровой сервер скопирован!')">
      🎮 Игровой сервер
      <span>Низкий пинг (&lt;85ms)</span>
    </div>
    <div class="btn-quick" onclick="copyDirectKey('${origin}/sub/top3', '🌍 Топ-3 по странам скопировано!')">
      🌍 Топ-3 по странам
      <span>По 3 узла на страну</span>
    </div>
  </div>

  <!-- 4. Personal link box -->
  <div class="sub-box">
    <div style="display:flex; justify-content:space-between; font-size:12px; font-weight:700;">
      <span>🔗 Ваша персональная ссылка:</span>
      <span style="color:var(--emerald);">1 TB • Без лимитов</span>
    </div>
    <input type="text" readonly value="${personalSubUrl}" id="sub-url-input" class="sub-input">
    <button class="btn-main" style="background:rgba(255,255,255,0.08); padding:8px; font-size:12px;" onclick="copyInput()">
      Копировать ссылку подписки
    </button>
  </div>

  <!-- 5. Bottom Section: Russian Whitelist Bypass -->
  <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 14px; margin-top: 14px; margin-bottom: 16px;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="font-size:11px; color:var(--emerald); font-weight:800; text-transform:uppercase;">🛡️ Сервера обхода белых списков РФ</div>
        <div style="font-size:13px; font-weight:700; margin-top:2px;">Маскировка: VK, Госуслуги, Яндекс, СМИ</div>
        <div style="font-size:11px; color:var(--text-sec);">Использовать при изолировании мобильной сети</div>
      </div>
      <button class="btn-main" style="width:auto; padding:8px 12px; font-size:11px; background:rgba(16,185,129,0.2); color:var(--emerald); border: 1px solid var(--emerald); border-radius:10px;" onclick="copyDirectKey('${origin}/best-whitelist', '🛡️ Whitelist сервер скопирован!')">Скопировать</button>
    </div>
  </div>

  <div id="toast" class="toast">Скопировано!</div>

  <!-- Instruction Modal -->
  <div class="modal-overlay" id="modal-inst">
    <div class="modal-card">
      <div style="font-size:36px; margin-bottom:10px;">✅</div>
      <h3 style="font-size:17px; margin-bottom:8px;">Подписка скопирована!</h3>
      <p style="font-size:13px; color:var(--text-sec); text-align:left; margin-bottom:16px;">
        1. Откройте приложение <b id="modal-app-name" style="color:var(--cyan);">Incy</b>.<br>
        2. Нажмите <b>«+»</b> в правом верхнем углу.<br>
        3. Выберите <b>«Импорт из буфера обмена»</b>.<br>
        4. Нажмите большую кнопку подключения!
      </p>
      <button class="btn-main btn-incy" onclick="closeModal()">Понятно, открыть Incy</button>
    </div>
  </div>

  <script>
    const tg = window.Telegram?.WebApp;
    if (tg) {
      tg.ready();
      tg.expand();
      if (tg.initDataUnsafe?.user) {
        document.getElementById('user-display').textContent = tg.initDataUnsafe.user.first_name || 'ID: ${userId}';
      }
    }

    const subUrl = "${personalSubUrl}";

    function installSub(appName) {
      navigator.clipboard.writeText(subUrl);
      if (tg?.HapticFeedback) tg.HapticFeedback.notificationOccurred('success');
      showToast('Ссылка скопирована!');

      document.getElementById('modal-app-name').textContent = appName;
      document.getElementById('modal-inst').style.display = 'flex';

      // Deep link attempt
      if (appName === 'Incy') {
        window.location.href = "incy://install-sub?url=" + encodeURIComponent(subUrl);
      } else if (appName === 'Happ') {
        window.location.href = "happ://install-sub?url=" + encodeURIComponent(subUrl);
      }
    }

    function copyInput() {
      navigator.clipboard.writeText(subUrl);
      if (tg?.HapticFeedback) tg.HapticFeedback.notificationOccurred('success');
      showToast('Подписка скопирована!');
    }

    async function copyDirectKey(url, msg) {
      const res = await fetch(url);
      const text = await res.text();
      navigator.clipboard.writeText(text);
      if (tg?.HapticFeedback) tg.HapticFeedback.notificationOccurred('success');
      showToast(msg);
    }

    function closeModal() {
      document.getElementById('modal-inst').style.display = 'none';
      if (tg?.close) tg.close();
    }

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.style.display = 'block';
      setTimeout(() => t.style.display = 'none', 2200);
    }
  </script>
</body>
</html>`;

  return new Response(html, {
    headers: { 'Content-Type': 'text/html; charset=utf-8' }
  });
}

// =========================================================================
// Data Sync API
// =========================================================================
async function handleSync(request) {
  try {
    const body = await request.json();
    if (body.secret !== SYNC_SECRET) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), { status: 401 });
    }
    if (Array.isArray(body.servers) && body.servers.length > 0) {
      CACHED_SERVERS = body.servers;
      return new Response(JSON.stringify({ status: 'synced', count: CACHED_SERVERS.length }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { status: 400 });
  }
  return new Response(JSON.stringify({ error: 'Invalid data' }), { status: 400 });
}

// =========================================================================
// Clash Meta & Singbox
// =========================================================================
function serveClashMeta() {
  const proxies = CACHED_SERVERS.slice(0, 80).map((s, idx) => {
    const name = `${s.country_flag} ${s.country_name || s.country_code} #${idx+1} • ${s.latency_ms}ms`;
    return `  - name: "${name}"
    type: vless
    server: ${s.host}
    port: ${s.port}
    uuid: ${s.uuid}
    network: ${s.type || 'tcp'}
    tls: ${s.security === 'reality' || s.security === 'tls'}
    flow: ${s.flow || ''}
    servername: ${s.sni || s.host}
    client-fingerprint: chrome
    reality-opts:
      public-key: ${s.pbk || ''}
      short-id: "${s.sid || ''}"
    udp: true`;
  }).join('\n');

  const names = CACHED_SERVERS.slice(0, 80).map((s, idx) => `      - "${s.country_flag} ${s.country_name || s.country_code} #${idx+1} • ${s.latency_ms}ms"`).join('\n');

  const yaml = `# Generated by HUSTLER VPN Hub
port: 7890
socks-port: 7891
mode: rule
proxies:
${proxies}

proxy-groups:
  - name: "⚡ Авто-выбор (Лучший пинг)"
    type: url-test
    url: http://cp.cloudflare.com/generate_204
    interval: 60
    proxies:
${names}
  - name: "🚀 PROXY"
    type: select
    proxies:
      - "⚡ Авто-выбор (Лучший пинг)"
${names}

rules:
  - GEOIP,RU,DIRECT
  - MATCH,🚀 PROXY
`;
  return new Response(yaml, {
    headers: { 'Content-Type': 'application/yaml; charset=utf-8', 'Content-Disposition': 'inline; filename="clash.yaml"' }
  });
}

function serveSingbox() {
  const outbounds = CACHED_SERVERS.slice(0, 50).map((s, idx) => ({
    type: 'vless',
    tag: `${s.country_flag} ${s.country_name || s.country_code} #${idx+1} • ${s.latency_ms}ms`,
    server: s.host,
    server_port: s.port,
    uuid: s.uuid,
    tls: { enabled: true, server_name: s.sni || s.host }
  }));

  const tags = outbounds.map(o => o.tag);
  const config = {
    version: 1,
    outbounds: [
      { type: 'selector', tag: 'select', outbounds: ['urltest', ...tags] },
      { type: 'urltest', tag: 'urltest', outbounds: tags, url: 'https://www.gstatic.com/generate_204' },
      ...outbounds
    ]
  };
  return new Response(JSON.stringify(config, null, 2), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' }
  });
}

// =========================================================================
// HTML Dashboard
// =========================================================================
function serveDashboard(origin) {
  const stats = getStats();
  const html = `<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🍄 HUSTLER VPN • Cloudflare Hub</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #090d16;
      --card: rgba(18, 24, 38, 0.75);
      --border: rgba(255, 255, 255, 0.08);
      --cyan: #06b6d4;
      --emerald: #10b981;
      --purple: #8b5cf6;
      --amber: #f59e0b;
      --text: #f8fafc;
      --text-sec: #94a3b8;
    }
    * { margin:0; padding:0; box-sizing:border-box; }
    body {
      background: var(--bg); color: var(--text); font-family: 'Plus Jakarta Sans', sans-serif;
      min-height: 100vh; padding: 24px; line-height: 1.5;
    }
    .container { max-width: 1200px; margin: 0 auto; }
    .header {
      display: flex; justify-content: space-between; align-items: center; padding-bottom: 24px;
      border-bottom: 1px solid var(--border); margin-bottom: 24px; flex-wrap: wrap; gap: 16px;
    }
    .brand { display: flex; align-items: center; gap: 14px; }
    .brand h1 { font-size: 24px; font-weight: 800; }
    .badge { font-size: 11px; background: linear-gradient(135deg, var(--cyan), var(--purple)); padding: 3px 8px; border-radius: 99px; }
    .stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 14px; margin-bottom: 24px; }
    .stat-card { background: var(--card); border: 1px solid var(--border); padding: 16px; border-radius: 14px; backdrop-filter: blur(10px); }
    .stat-num { font-size: 24px; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: var(--cyan); }
    .stat-label { font-size: 12px; color: var(--text-sec); text-transform: uppercase; font-weight: 600; }
    
    .quick-actions {
      background: linear-gradient(135deg, rgba(6, 182, 212, 0.08), rgba(16, 185, 129, 0.08));
      border: 1px solid rgba(6, 182, 212, 0.3); padding: 20px; border-radius: 16px; margin-bottom: 24px;
    }
    .actions-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px; margin-top: 14px; }
    .btn {
      display: inline-flex; align-items: center; justify-content: center; gap: 8px;
      padding: 12px 18px; border-radius: 10px; font-weight: 700; font-size: 14px;
      border: none; cursor: pointer; transition: all 0.2s; text-decoration: none;
    }
    .btn-cyan { background: var(--cyan); color: #000; }
    .btn-emerald { background: var(--emerald); color: #000; }
    .btn-purple { background: var(--purple); color: #fff; }
    .btn-outline { background: rgba(255,255,255,0.06); color: #fff; border: 1px solid var(--border); }
    
    .cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; margin-bottom: 24px; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 20px; display: flex; flex-direction: column; }
    .card h3 { font-size: 16px; margin-bottom: 8px; }
    .card p { font-size: 13px; color: var(--text-sec); margin-bottom: 16px; flex-grow: 1; }
    .input-box { display: flex; gap: 8px; }
    .input-box input { flex: 1; background: rgba(0,0,0,0.4); border: 1px solid var(--border); border-radius: 8px; padding: 8px 12px; color: #fff; font-family: monospace; font-size: 12px; }

    .toast {
      position: fixed; bottom: 20px; right: 20px; background: #1e293b; border: 1px solid var(--cyan);
      color: #fff; padding: 12px 20px; border-radius: 10px; font-weight: 600; display: none; z-index: 1000;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="brand">
        <span style="font-size:32px;">🍄</span>
        <div>
          <h1>HUSTLER VPN • Cloudflare Hub <span class="badge">ONLINE</span></h1>
          <p style="color:var(--text-sec); font-size:13px;">Подписки для Incy &amp; Happ • Whitelist обходы • Telegram Bot @hustler_vpn_robot</p>
        </div>
      </div>
      <div>
        <a href="https://t.me/hustler_vpn_robot" target="_blank" class="btn btn-purple">🤖 Открыть Telegram Бота</a>
      </div>
    </div>

    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-label">Рабочих серверов</div>
        <div class="stat-num">${stats.total}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Белые списки (Обход)</div>
        <div class="stat-num" style="color:var(--emerald);">${stats.whitelist_count}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Игровые узлы (&lt;85ms)</div>
        <div class="stat-num" style="color:var(--purple);">${stats.gaming_count}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Средний пинг</div>
        <div class="stat-num">${stats.avg_ping} ms</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Стран в базе</div>
        <div class="stat-num">${stats.countries_count}</div>
      </div>
    </div>

    <!-- Quick action buttons -->
    <div class="quick-actions">
      <h2 style="font-size:18px;">⚡ Быстрое подключение в 1 клик:</h2>
      <p style="font-size:13px; color:var(--text-sec);">Нажмите на кнопку — ключ скопируется в буфер для мгновенной вставки в Incy или Happ!</p>
      <div class="actions-grid">
        <button class="btn btn-cyan" onclick="copyUrl('${origin}/best', 'Лучший сервер скопирован!')">⚡ Скопировать лучший сервер (Мин. пинг)</button>
        <button class="btn btn-emerald" onclick="copyUrl('${origin}/best-whitelist', 'Лучший обход (Whitelist) скопирован!')">🛡️ Скопировать лучший обход (Whitelist)</button>
        <button class="btn btn-purple" onclick="copyUrl('${origin}/best-gaming', 'Игровой сервер скопирован!')">🎮 Скопировать игровой сервер</button>
      </div>
    </div>

    <!-- Subscriptions grid -->
    <div class="cards-grid">
      <div class="card" style="border-color:rgba(6,182,212,0.4);">
        <div style="font-size:11px; color:var(--cyan); font-weight:700; margin-bottom:4px;">ПРИОРИТЕТ ДЛЯ INCY</div>
        <h3>📱 Подписка для Incy</h3>
        <p>Все протестированные рабочие сервера. Нажмите «+» → «Импорт из буфера» в приложении Incy.</p>
        <div class="input-box">
          <input type="text" readonly value="${origin}/sub/incy" id="inp-incy">
          <button class="btn btn-cyan" style="padding:8px 14px;" onclick="copyInput('inp-incy')">Копировать</button>
        </div>
      </div>

      <div class="card" style="border-color:rgba(16,185,129,0.4);">
        <div style="font-size:11px; color:var(--emerald); font-weight:700; margin-bottom:4px;">ОБХОД ГЛУШЕНИЙ РФ</div>
        <h3>🛡️ Подписка Whitelist (Белые списки)</h3>
        <p>Сервера с маскировкой под VK, Госуслуги, Яндекс. Работают при жестких блокировках!</p>
        <div class="input-box">
          <input type="text" readonly value="${origin}/sub/whitelist" id="inp-wl">
          <button class="btn btn-emerald" style="padding:8px 14px;" onclick="copyInput('inp-wl')">Копировать</button>
        </div>
      </div>

      <div class="card">
        <div style="font-size:11px; color:var(--purple); font-weight:700; margin-bottom:4px;">ПО 3 НА СТРАНУ</div>
        <h3>🌍 Топ-3 по каждой стране</h3>
        <p>Компактная подписка, содержащая ровно по 3 лучших сервера на каждую страну с наименьшим пингом.</p>
        <div class="input-box">
          <input type="text" readonly value="${origin}/sub/top3" id="inp-top3">
          <button class="btn btn-purple" style="padding:8px 14px;" onclick="copyInput('inp-top3')">Копировать</button>
        </div>
      </div>

      <div class="card">
        <div style="font-size:11px; color:var(--amber); font-weight:700; margin-bottom:4px;">HAPP КЛИЕНТ</div>
        <h3>🚀 Подписка для Happ</h3>
        <p>Оптимизированная база проверенных серверов для клиента Happ.</p>
        <div class="input-box">
          <input type="text" readonly value="${origin}/sub/happ" id="inp-happ">
          <button class="btn btn-outline" style="padding:8px 14px;" onclick="copyInput('inp-happ')">Копировать</button>
        </div>
      </div>
    </div>
  </div>

  <div id="toast" class="toast">Ссылка скопирована!</div>

  <script>
    function copyInput(id) {
      const el = document.getElementById(id);
      navigator.clipboard.writeText(el.value);
      showToast('Подписка скопирована в буфер обмена!');
    }
    async function copyUrl(url, msg) {
      const res = await fetch(url);
      const text = await res.text();
      navigator.clipboard.writeText(text);
      showToast(msg);
    }
    function showToast(msg) {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.style.display = 'block';
      setTimeout(() => t.style.display = 'none', 2500);
    }
  </script>
</body>
</html>`;

  return new Response(html, {
    headers: { 'Content-Type': 'text/html; charset=utf-8' }
  });
}
