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
let CACHED_SERVERS = [{"protocol": "vless", "host": "172.235.43.210", "port": 53957, "uuid": "7ab29f89-6eef-4171-b232-fc4f580ad31b", "security": "reality", "sni": "www.nvidia.com", "pbk": "XUHlbk5VH5z4E2wxZBhlpLZ33qevyQgqU7dheRDgoGQ", "sid": "44e82fd7b97b14", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇺🇸 США #337 • 207ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "US", "country_flag": "🇺🇸", "country_name": "США", "latency_ms": 207, "is_alive": true, "source_id": null, "uri": "vless://7ab29f89-6eef-4171-b232-fc4f580ad31b@172.235.43.210:53957?flow=xtls-rprx-vision&fp=random&pbk=XUHlbk5VH5z4E2wxZBhlpLZ33qevyQgqU7dheRDgoGQ&security=reality&sid=44e82fd7b97b14&sni=www.nvidia.com&type=tcp#%F0%9F%87%BA%F0%9F%87%B8%20%D0%A1%D0%A8%D0%90%20%23337%20%E2%80%A2%20207ms"}, {"protocol": "vless", "host": "51.81.203.63", "port": 443, "uuid": "cb2dbb6a-a1ea-4023-9ace-6466cee57241", "security": "reality", "sni": "www.icloud.com", "pbk": "nqwCf6oW49tEtmQ0EzxigZ0uu1pg0E30CS54G40Iti0", "sid": "4477382ff6d3d41c", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇺🇸 США #342 • 229ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "US", "country_flag": "🇺🇸", "country_name": "США", "latency_ms": 229, "is_alive": true, "source_id": null, "uri": "vless://cb2dbb6a-a1ea-4023-9ace-6466cee57241@51.81.203.63:443?flow=xtls-rprx-vision&fp=chrome&pbk=nqwCf6oW49tEtmQ0EzxigZ0uu1pg0E30CS54G40Iti0&security=reality&sid=4477382ff6d3d41c&sni=www.icloud.com&type=tcp#%F0%9F%87%BA%F0%9F%87%B8%20%D0%A1%D0%A8%D0%90%20%23342%20%E2%80%A2%20229ms"}, {"protocol": "vless", "host": "137.175.82.40", "port": 30556, "uuid": "949d278e-6d98-4014-84e9-59f1c6c93e0e", "security": "reality", "sni": "www.lovelive-anime.jp", "pbk": "EcmNQqZxyW4GCEQF-7nH54w3qgBkLzsfqFSgafGjB0E", "sid": "d082f567", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇺🇸 США #343 • 230ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "US", "country_flag": "🇺🇸", "country_name": "США", "latency_ms": 230, "is_alive": true, "source_id": null, "uri": "vless://949d278e-6d98-4014-84e9-59f1c6c93e0e@137.175.82.40:30556?flow=xtls-rprx-vision&fp=ios&pbk=EcmNQqZxyW4GCEQF-7nH54w3qgBkLzsfqFSgafGjB0E&security=reality&sid=d082f567&sni=www.lovelive-anime.jp&type=tcp#%F0%9F%87%BA%F0%9F%87%B8%20%D0%A1%D0%A8%D0%90%20%23343%20%E2%80%A2%20230ms"}, {"protocol": "vless", "host": "185.86.13.98", "port": 443, "uuid": "5bd9a692-be8f-11f1-bba4-3aa621cc36ab", "security": "reality", "sni": "ulet-bm-s1700.reverseenge.sbs", "pbk": "97DqdgDD5u_2o2RApPAvm_6cYGpphY8uqz23nsGhF1I", "sid": "", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇳🇱 Нидерланды #350 • 266ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "NL", "country_flag": "🇳🇱", "country_name": "Нидерланды", "latency_ms": 266, "is_alive": true, "source_id": null, "uri": "vless://5bd9a692-be8f-11f1-bba4-3aa621cc36ab@185.86.13.98:443?type=tcp&security=reality&flow=xtls-rprx-vision&fp=firefox&pbk=97DqdgDD5u_2o2RApPAvm_6cYGpphY8uqz23nsGhF1I&sni=ulet-bm-s1700.reverseenge.sbs#%F0%9F%87%B3%F0%9F%87%B1%20%D0%9D%D0%B8%D0%B4%D0%B5%D1%80%D0%BB%D0%B0%D0%BD%D0%B4%D1%8B%20%23350%20%E2%80%A2%20266ms"}, {"protocol": "vless", "host": "34.3.101.206", "port": 443, "uuid": "c64a5cfa-0fd6-4978-b062-6e89da013260", "security": "reality", "sni": "gateway.icloud.com", "pbk": "C4ky4RduL1cfjZ3okHXDkpD2Ns4DViMkB-mDlisBrzc", "sid": "8a17287288cf25e5", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇺🇸 США #351 • 297ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "US", "country_flag": "🇺🇸", "country_name": "США", "latency_ms": 297, "is_alive": true, "source_id": null, "uri": "vless://c64a5cfa-0fd6-4978-b062-6e89da013260@34.3.101.206:443?flow=xtls-rprx-vision&fp=firefox&pbk=C4ky4RduL1cfjZ3okHXDkpD2Ns4DViMkB-mDlisBrzc&security=reality&sid=8a17287288cf25e5&sni=gateway.icloud.com&type=tcp#%F0%9F%87%BA%F0%9F%87%B8%20%D0%A1%D0%A8%D0%90%20%23351%20%E2%80%A2%20297ms"}, {"protocol": "vless", "host": "162.35.242.252", "port": 443, "uuid": "e3e9805a-6c8b-4edd-8ee8-621df79806eb", "security": "reality", "sni": "nl.aksay.pro", "pbk": "ClG6fvriBTK8donGsTlKusJ0dwRCgVDDTAGzAtZzJDY", "sid": "82c2b7d5e70ff000", "flow": "", "type": "tcp", "remark": "🇳🇱 Нидерланды #352 • 300ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "NL", "country_flag": "🇳🇱", "country_name": "Нидерланды", "latency_ms": 300, "is_alive": true, "source_id": null, "uri": "vless://e3e9805a-6c8b-4edd-8ee8-621df79806eb@162.35.242.252:443?fp=firefox&pbk=ClG6fvriBTK8donGsTlKusJ0dwRCgVDDTAGzAtZzJDY&security=reality&sid=82c2b7d5e70ff000&sni=nl.aksay.pro&spx=%2F&type=tcp#%F0%9F%87%B3%F0%9F%87%B1%20%D0%9D%D0%B8%D0%B4%D0%B5%D1%80%D0%BB%D0%B0%D0%BD%D0%B4%D1%8B%20%23352%20%E2%80%A2%20300ms"}, {"protocol": "vless", "host": "177.1.186.44", "port": 443, "uuid": "55ccbeb5-0bf4-4e4d-afcb-23c038e73e00", "security": "reality", "sni": "mcde.67resserv67.info", "pbk": "4hvjCaGIMlFeWxMYoAWTNHQOaZkGvGQREOjB3Unn7iE", "sid": "29455a3a790acbd0", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇩🇪 Германия #353 • 301ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "DE", "country_flag": "🇩🇪", "country_name": "Германия", "latency_ms": 301, "is_alive": true, "source_id": null, "uri": "vless://55ccbeb5-0bf4-4e4d-afcb-23c038e73e00@177.1.186.44:443?security=reality&encryption=none&pbk=4hvjCaGIMlFeWxMYoAWTNHQOaZkGvGQREOjB3Unn7iE&headerType=none&fp=chrome&spx=%2F&type=tcp&flow=xtls-rprx-vision&sni=mcde.67resserv67.info&sid=29455a3a790acbd0#%F0%9F%87%A9%F0%9F%87%AA%20%D0%93%D0%B5%D1%80%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F%20%23353%20%E2%80%A2%20301ms"}, {"protocol": "vless", "host": "163.245.52.91", "port": 443, "uuid": "87fd990d-ca93-440a-bbd4-e8281c4a0910", "security": "reality", "sni": "d3-ee1.cloud-cdn.xyz", "pbk": "g36Z7YIqJMJP-uv3DBr72X5jvfjyW1qIAxa8TkWmpmQ", "sid": "ad6e08b22389abd2", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇪🇪 Эстония #354 • 309ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "EE", "country_flag": "🇪🇪", "country_name": "Эстония", "latency_ms": 309, "is_alive": true, "source_id": null, "uri": "vless://87fd990d-ca93-440a-bbd4-e8281c4a0910@163.245.52.91:443?flow=xtls-rprx-vision&fp=edge&pbk=g36Z7YIqJMJP-uv3DBr72X5jvfjyW1qIAxa8TkWmpmQ&security=reality&sid=ad6e08b22389abd2&sni=d3-ee1.cloud-cdn.xyz&spx=%2F&type=tcp#%F0%9F%87%AA%F0%9F%87%AA%20%D0%AD%D1%81%D1%82%D0%BE%D0%BD%D0%B8%D1%8F%20%23354%20%E2%80%A2%20309ms"}, {"protocol": "vless", "host": "51.81.203.63", "port": 443, "uuid": "cb2dbb6a-a1ea-4023-9ace-6466cee57241", "security": "reality", "sni": "www.icloud.com", "pbk": "nqwCf6oW49tEtmQ0EzxigZ0uu1pg0E30CS54G40Iti0", "sid": "4477382ff6d3d41c", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇺🇸 США #357 • 327ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "US", "country_flag": "🇺🇸", "country_name": "США", "latency_ms": 327, "is_alive": true, "source_id": null, "uri": "vless://cb2dbb6a-a1ea-4023-9ace-6466cee57241@51.81.203.63:443?flow=xtls-rprx-vision&fp=chrome&pbk=nqwCf6oW49tEtmQ0EzxigZ0uu1pg0E30CS54G40Iti0&security=reality&sid=4477382ff6d3d41c&sni=www.icloud.com&type=tcp#%F0%9F%87%BA%F0%9F%87%B8%20%D0%A1%D0%A8%D0%90%20%23357%20%E2%80%A2%20327ms"}, {"protocol": "vless", "host": "185.171.202.105", "port": 443, "uuid": "4bdeee92-97e8-414d-bef6-ec1d5e2ab73b", "security": "reality", "sni": "fra.loozerp.wiki", "pbk": "bZpzmeWiEJyJQy0W2hHc34Nr6BuFXj1UDd80Cbwh1Fk", "sid": "ff776ff77be48b88", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇫🇷 Франция #359 • 355ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "FR", "country_flag": "🇫🇷", "country_name": "Франция", "latency_ms": 355, "is_alive": true, "source_id": null, "uri": "vless://4bdeee92-97e8-414d-bef6-ec1d5e2ab73b@185.171.202.105:443?security=reality&encryption=none&pbk=bZpzmeWiEJyJQy0W2hHc34Nr6BuFXj1UDd80Cbwh1Fk&headerType=none&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=fra.loozerp.wiki&sid=ff776ff77be48b88#%F0%9F%87%AB%F0%9F%87%B7%20%D0%A4%D1%80%D0%B0%D0%BD%D1%86%D0%B8%D1%8F%20%23359%20%E2%80%A2%20355ms"}, {"protocol": "vless", "host": "2.27.249.133", "port": 443, "uuid": "0f4081e7-612b-425f-8def-eebf144aedba", "security": "reality", "sni": "vault.connectiux.com", "pbk": "ITd6cmCxudmTvGcwnAzpd0VRe8jS9KJAQ1tmtVN3mCM", "sid": "9e15546f267baa64", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇳🇱 Нидерланды #363 • 394ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "NL", "country_flag": "🇳🇱", "country_name": "Нидерланды", "latency_ms": 394, "is_alive": true, "source_id": null, "uri": "vless://0f4081e7-612b-425f-8def-eebf144aedba@2.27.249.133:443?security=reality&encryption=none&pbk=ITd6cmCxudmTvGcwnAzpd0VRe8jS9KJAQ1tmtVN3mCM&headerType=none&fp=safari&type=tcp&flow=xtls-rprx-vision&sni=vault.connectiux.com&sid=9e15546f267baa64#%F0%9F%87%B3%F0%9F%87%B1%20%D0%9D%D0%B8%D0%B4%D0%B5%D1%80%D0%BB%D0%B0%D0%BD%D0%B4%D1%8B%20%23363%20%E2%80%A2%20394ms"}, {"protocol": "vless", "host": "95.85.224.51", "port": 443, "uuid": "342ab7e4-5a89-0001-8809-304120d4aa83", "security": "reality", "sni": "max.ru", "pbk": "WWeAHWUVD-phmnjNJ823cer0c4CMIbEs08AhsuEZmDc", "sid": "a696de84963656de", "flow": "xtls-rprx-vision", "type": "raw", "remark": "🇪🇪 Эстония #364 • 441ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "Bypass-Media", "country_code": "EE", "country_flag": "🇪🇪", "country_name": "Эстония", "latency_ms": 441, "is_alive": true, "source_id": null, "uri": "vless://342ab7e4-5a89-0001-8809-304120d4aa83@95.85.224.51:443?security=reality&type=raw&packetEncoding=xudp&sni=max.ru&fp=qq&flow=xtls-rprx-vision&sid=a696de84963656de&pbk=WWeAHWUVD-phmnjNJ823cer0c4CMIbEs08AhsuEZmDc#%F0%9F%87%AA%F0%9F%87%AA%20%D0%AD%D1%81%D1%82%D0%BE%D0%BD%D0%B8%D1%8F%20%23364%20%E2%80%A2%20441ms"}, {"protocol": "vless", "host": "45.9.156.24", "port": 443, "uuid": "2f35965a-9a9b-45fd-ba32-987296dfb6be", "security": "reality", "sni": "bg2.univesalsrv.com", "pbk": "0f0dh_FUju5cHgQcIwUjHvxQb9aIZ00p0kZRHeE7Ey4", "sid": "501ab3325b77e1ca", "flow": "", "type": "grpc", "remark": "🇧🇬 Болгария #368 • 491ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "BG", "country_flag": "🇧🇬", "country_name": "Болгария", "latency_ms": 491, "is_alive": true, "source_id": null, "uri": "vless://2f35965a-9a9b-45fd-ba32-987296dfb6be@45.9.156.24:443?mode=gun&security=reality&encryption=none&authority=%2F%3FTELEGRAM%40MARAMBASHI_MARAMBASHI&pbk=0f0dh_FUju5cHgQcIwUjHvxQb9aIZ00p0kZRHeE7Ey4&fp=firefox&type=grpc&serviceName=api.v2.PushService&sni=bg2.univesalsrv.com&sid=501ab3325b77e1ca#%F0%9F%87%A7%F0%9F%87%AC%20%D0%91%D0%BE%D0%BB%D0%B3%D0%B0%D1%80%D0%B8%D1%8F%20%23368%20%E2%80%A2%20491ms"}, {"protocol": "vless", "host": "150.241.101.17", "port": 8443, "uuid": "47d9b534-8a0a-4bd2-90f1-1d6ade14427e", "security": "reality", "sni": "yandex.net", "pbk": "SbVKOEMjK0sIlbwg4akyBg5mL5KZwwB-ed4eEE7YnRc", "sid": "6ba85179e30d4fc2", "flow": "xtls-rprx-vision", "type": "raw", "remark": "🇩🇪 Германия #369 • 496ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "Yandex-Dzen", "country_code": "DE", "country_flag": "🇩🇪", "country_name": "Германия", "latency_ms": 496, "is_alive": true, "source_id": null, "uri": "vless://47d9b534-8a0a-4bd2-90f1-1d6ade14427e@150.241.101.17:8443?encryption=none&flow=xtls-rprx-vision&type=raw&headerType=none&security=reality&fp=safari&pbk=SbVKOEMjK0sIlbwg4akyBg5mL5KZwwB-ed4eEE7YnRc&sni=yandex.net&sid=6ba85179e30d4fc2#%F0%9F%87%A9%F0%9F%87%AA%20%D0%93%D0%B5%D1%80%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F%20%23369%20%E2%80%A2%20496ms"}, {"protocol": "vless", "host": "bg3.univesalsrv.com", "port": 443, "uuid": "2f35965a-9a9b-45fd-ba32-987296dfb6be", "security": "reality", "sni": "bg3.univesalsrv.com", "pbk": "XBfCioniAKXgKYBUVnvBXu80AIaIa4SpAB3w8qeF7Gk", "sid": "1be1bd931c98c84a", "flow": "", "type": "grpc", "remark": "🇧🇬 Болгария #373 • 593ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "BG", "country_flag": "🇧🇬", "country_name": "Болгария", "latency_ms": 593, "is_alive": true, "source_id": null, "uri": "vless://2f35965a-9a9b-45fd-ba32-987296dfb6be@bg3.univesalsrv.com:443?mode=gun&security=reality&encryption=none&pbk=XBfCioniAKXgKYBUVnvBXu80AIaIa4SpAB3w8qeF7Gk&fp=chrome&type=grpc&serviceName=home.v1.ApiService&sni=bg3.univesalsrv.com&sid=1be1bd931c98c84a#%F0%9F%87%A7%F0%9F%87%AC%20%D0%91%D0%BE%D0%BB%D0%B3%D0%B0%D1%80%D0%B8%D1%8F%20%23373%20%E2%80%A2%20593ms"}, {"protocol": "vless", "host": "bg4.univesalsrv.com", "port": 443, "uuid": "2f35965a-9a9b-45fd-ba32-987296dfb6be", "security": "reality", "sni": "bg4.univesalsrv.com", "pbk": "k-vH6pkyAv26L1_dXKOFhp0Kesur9-FCUDoj-IIpVhc", "sid": "51f45d4fd58cc319", "flow": "", "type": "grpc", "remark": "🇧🇬 Болгария #375 • 614ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "BG", "country_flag": "🇧🇬", "country_name": "Болгария", "latency_ms": 614, "is_alive": true, "source_id": null, "uri": "vless://2f35965a-9a9b-45fd-ba32-987296dfb6be@bg4.univesalsrv.com:443?encryption=none&security=reality&sni=bg4.univesalsrv.com&fp=firefox&pbk=k-vH6pkyAv26L1_dXKOFhp0Kesur9-FCUDoj-IIpVhc&sid=51f45d4fd58cc319&type=grpc&authority=MTMVPN&serviceName=cloud.v1.RelayService&mode=gun#%F0%9F%87%A7%F0%9F%87%AC%20%D0%91%D0%BE%D0%BB%D0%B3%D0%B0%D1%80%D0%B8%D1%8F%20%23375%20%E2%80%A2%20614ms"}, {"protocol": "vless", "host": "18.183.215.124", "port": 28573, "uuid": "871bfce7-8440-4394-8d82-56b51f20fdad", "security": "reality", "sni": "www.sony.com", "pbk": "1DJr9toke7FRuSXjibBVuNvRnLnJnN5kXwUBG6Romzg", "sid": "03653bc03be10c97", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇯🇵 Япония #377 • 729ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "JP", "country_flag": "🇯🇵", "country_name": "Япония", "latency_ms": 729, "is_alive": true, "source_id": null, "uri": "vless://871bfce7-8440-4394-8d82-56b51f20fdad@18.183.215.124:28573?flow=xtls-rprx-vision&fp=firefox&host=v2raynplus--v2raynplus--v2raynplus--&pbk=1DJr9toke7FRuSXjibBVuNvRnLnJnN5kXwUBG6Romzg&security=reality&sid=03653bc03be10c97&sni=www.sony.com&type=tcp#%F0%9F%87%AF%F0%9F%87%B5%20%D0%AF%D0%BF%D0%BE%D0%BD%D0%B8%D1%8F%20%23377%20%E2%80%A2%20729ms"}, {"protocol": "vless", "host": "54.169.200.246", "port": 41688, "uuid": "49c0aac1-5e05-4f04-b624-248fc59e03c4", "security": "reality", "sni": "www.intel.com", "pbk": "srwIElIGTPs0kshpN1vvPsn4wixV_pLd56y_v9m0sTk", "sid": "7f342137c20387", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇸🇬 Сингапур #378 • 750ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "SG", "country_flag": "🇸🇬", "country_name": "Сингапур", "latency_ms": 750, "is_alive": true, "source_id": null, "uri": "vless://49c0aac1-5e05-4f04-b624-248fc59e03c4@54.169.200.246:41688?flow=xtls-rprx-vision&fp=edge&pbk=srwIElIGTPs0kshpN1vvPsn4wixV_pLd56y_v9m0sTk&security=reality&sid=7f342137c20387&sni=www.intel.com&type=tcp#%F0%9F%87%B8%F0%9F%87%AC%20%D0%A1%D0%B8%D0%BD%D0%B3%D0%B0%D0%BF%D1%83%D1%80%20%23378%20%E2%80%A2%20750ms"}, {"protocol": "vless", "host": "hinet1.2yly.com", "port": 24215, "uuid": "19d5a678-8396-4e3b-93da-ece618d0e83a", "security": "reality", "sni": "addons.mozilla.org", "pbk": "mdWKUPMVTtTbDqK10BPb89OcqBC2-Lx-4NOYtqc1GWE", "sid": "", "flow": "", "type": "tcp", "remark": "🌐 Taiwan #379 • 767ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "TW", "country_flag": "🌐", "country_name": "Taiwan", "latency_ms": 767, "is_alive": true, "source_id": null, "uri": "vless://19d5a678-8396-4e3b-93da-ece618d0e83a@hinet1.2yly.com:24215?security=reality&encryption=none&pbk=mdWKUPMVTtTbDqK10BPb89OcqBC2-Lx-4NOYtqc1GWE&headerType=none&fp=chrome&type=tcp&sni=addons.mozilla.org#%F0%9F%8C%90%20Taiwan%20%23379%20%E2%80%A2%20767ms"}, {"protocol": "vless", "host": "46.137.202.178", "port": 12512, "uuid": "2a6c617d-98e4-49c3-95ab-76f02fcf0150", "security": "reality", "sni": "www.intel.com", "pbk": "sO0RBMr_l8TLtZaYBX8n3NdI9AtaugUqJpCR1szNsyA", "sid": "e692a8250d2e2fd0", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇸🇬 Сингапур #381 • 779ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "SG", "country_flag": "🇸🇬", "country_name": "Сингапур", "latency_ms": 779, "is_alive": true, "source_id": null, "uri": "vless://2a6c617d-98e4-49c3-95ab-76f02fcf0150@46.137.202.178:12512?flow=xtls-rprx-vision&fp=qq&host=www.intel.com&path=%2F&pbk=sO0RBMr_l8TLtZaYBX8n3NdI9AtaugUqJpCR1szNsyA&security=reality&sid=e692a8250d2e2fd0&sni=www.intel.com&type=tcp#%F0%9F%87%B8%F0%9F%87%AC%20%D0%A1%D0%B8%D0%BD%D0%B3%D0%B0%D0%BF%D1%83%D1%80%20%23381%20%E2%80%A2%20779ms"}, {"protocol": "vless", "host": "13.231.19.51", "port": 11690, "uuid": "e2b8b217-cffb-4d66-9b8b-eca6e4334032", "security": "reality", "sni": "www.tesla.com", "pbk": "Bv3z0_uFRabB9C4CFpNfqepZUyeO4YTh1duJdMBNLkg", "sid": "034885e346fd30", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇯🇵 Япония #383 • 865ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "JP", "country_flag": "🇯🇵", "country_name": "Япония", "latency_ms": 865, "is_alive": true, "source_id": null, "uri": "vless://e2b8b217-cffb-4d66-9b8b-eca6e4334032@13.231.19.51:11690?flow=xtls-rprx-vision&fp=edge&pbk=Bv3z0_uFRabB9C4CFpNfqepZUyeO4YTh1duJdMBNLkg&security=reality&sid=034885e346fd30&sni=www.tesla.com&type=tcp#%F0%9F%87%AF%F0%9F%87%B5%20%D0%AF%D0%BF%D0%BE%D0%BD%D0%B8%D1%8F%20%23383%20%E2%80%A2%20865ms"}, {"protocol": "vless", "host": "greeeeeek.pumpkinpie.study", "port": 443, "uuid": "8f6e49e6-7f03-4f10-9da9-1716158d80ed", "security": "reality", "sni": "greeeeeek.pumpkinpie.study", "pbk": "lza1anie-lqVSKrFdfSzq4XLd8Ge2qyCDkgZb1xr1k0", "sid": "9fa5c0092361b848", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🌐 Greece #385 • 988ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "GR", "country_flag": "🌐", "country_name": "Greece", "latency_ms": 988, "is_alive": true, "source_id": null, "uri": "vless://8f6e49e6-7f03-4f10-9da9-1716158d80ed@greeeeeek.pumpkinpie.study:443?type=tcp&headerType=none&security=reality&encryption=none&sni=greeeeeek.pumpkinpie.study&fp=random&pbk=lza1anie-lqVSKrFdfSzq4XLd8Ge2qyCDkgZb1xr1k0&sid=9fa5c0092361b848&flow=xtls-rprx-vision#%F0%9F%8C%90%20Greece%20%23385%20%E2%80%A2%20988ms"}, {"protocol": "vless", "host": "95.85.254.153", "port": 443, "uuid": "4bdeee92-97e8-414d-bef6-ec1d5e2ab73b", "security": "reality", "sni": "polka.stopingiphatered.shop", "pbk": "bZpzmeWiEJyJQy0W2hHc34Nr6BuFXj1UDd80Cbwh1Fk", "sid": "ff776ff77be48b88", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇵🇱 Польша #386 • 1194ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "PL", "country_flag": "🇵🇱", "country_name": "Польша", "latency_ms": 1194, "is_alive": true, "source_id": null, "uri": "vless://4bdeee92-97e8-414d-bef6-ec1d5e2ab73b@95.85.254.153:443?security=reality&encryption=none&pbk=bZpzmeWiEJyJQy0W2hHc34Nr6BuFXj1UDd80Cbwh1Fk&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=polka.stopingiphatered.shop&sid=ff776ff77be48b88#%F0%9F%87%B5%F0%9F%87%B1%20%D0%9F%D0%BE%D0%BB%D1%8C%D1%88%D0%B0%20%23386%20%E2%80%A2%201194ms"}, {"protocol": "vless", "host": "91.108.249.201", "port": 705, "uuid": "87fd990d-ca93-440a-bbd4-e8281c4a0910", "security": "reality", "sni": "www.kayak.com", "pbk": "nn7zao7trQrkZv5IjiOPmeWPe-Qtj3tFi14Eon9RHC4", "sid": "", "flow": "", "type": "grpc", "remark": "🇵🇱 Польша #387 • 1374ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "PL", "country_flag": "🇵🇱", "country_name": "Польша", "latency_ms": 1374, "is_alive": true, "source_id": null, "uri": "vless://87fd990d-ca93-440a-bbd4-e8281c4a0910@91.108.249.201:705?mode=gun&security=reality&encryption=none&authority=PLANB_NET---PLANB_NET---PLANB_NET---PLANB_NET---PLANB_NET&pbk=nn7zao7trQrkZv5IjiOPmeWPe-Qtj3tFi14Eon9RHC4&fp=chrome&spx=%2F&type=grpc&sni=www.kayak.com#%F0%9F%87%B5%F0%9F%87%B1%20%D0%9F%D0%BE%D0%BB%D1%8C%D1%88%D0%B0%20%23387%20%E2%80%A2%201374ms"}, {"protocol": "vless", "host": "144.31.215.227", "port": 443, "uuid": "91d734be-a3d0-4d50-83ab-74cf7b6966fa", "security": "reality", "sni": "cdn-de.bulkavpn.top", "pbk": "LEoyslGYLVf2XWq9Bkq8Hod-EsB3ZoTlvR5AKK3rciQ", "sid": "c885e8f8", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇩🇪 Германия #388 • 1429ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "DE", "country_flag": "🇩🇪", "country_name": "Германия", "latency_ms": 1429, "is_alive": true, "source_id": null, "uri": "vless://91d734be-a3d0-4d50-83ab-74cf7b6966fa@144.31.215.227:443?security=reality&encryption=none&pbk=LEoyslGYLVf2XWq9Bkq8Hod-EsB3ZoTlvR5AKK3rciQ&host=%2F%3FTelegram---PLANB_NET---PLANB_NET---PLANB_NET---PLANB_NET&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=cdn-de.bulkavpn.top&sid=c885e8f8#%F0%9F%87%A9%F0%9F%87%AA%20%D0%93%D0%B5%D1%80%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F%20%23388%20%E2%80%A2%201429ms"}, {"protocol": "vless", "host": "103.27.157.120", "port": 443, "uuid": "025a80fb-233b-4714-b02d-f4384c653d58", "security": "reality", "sni": "download.amd.com", "pbk": "k0883nIGfstbzb8hES-dQ1yPcBwbUbnsyg4w-UA5gkA", "sid": "68aaa5222092bbea", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇩🇪 Германия #390 • 1545ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "DE", "country_flag": "🇩🇪", "country_name": "Германия", "latency_ms": 1545, "is_alive": true, "source_id": null, "uri": "vless://025a80fb-233b-4714-b02d-f4384c653d58@103.27.157.120:443?security=reality&encryption=none&pbk=k0883nIGfstbzb8hES-dQ1yPcBwbUbnsyg4w-UA5gkA&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=download.amd.com&sid=68aaa5222092bbea#%F0%9F%87%A9%F0%9F%87%AA%20%D0%93%D0%B5%D1%80%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F%20%23390%20%E2%80%A2%201545ms"}, {"protocol": "vless", "host": "137.74.16.237", "port": 443, "uuid": "aaec4e42-a095-44b6-a239-f16d234a0798", "security": "reality", "sni": "www.icloud.com", "pbk": "7LSzvilTVKGMtBDuKGeMrLtlhY7tQf5YcG566dEgO0I", "sid": "b390e0a721d242b0", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇫🇷 Франция #391 • 2018ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "FR", "country_flag": "🇫🇷", "country_name": "Франция", "latency_ms": 2018, "is_alive": true, "source_id": null, "uri": "vless://aaec4e42-a095-44b6-a239-f16d234a0798@137.74.16.237:443?security=reality&encryption=none&pbk=7LSzvilTVKGMtBDuKGeMrLtlhY7tQf5YcG566dEgO0I&headerType=none&fp=chrome&spx=%2F&type=tcp&flow=xtls-rprx-vision&sni=www.icloud.com&sid=b390e0a721d242b0#%F0%9F%87%AB%F0%9F%87%B7%20%D0%A4%D1%80%D0%B0%D0%BD%D1%86%D0%B8%D1%8F%20%23391%20%E2%80%A2%202018ms"}, {"protocol": "vless", "host": "201.34.137.215", "port": 443, "uuid": "f811a2e8-08ed-4b30-b44c-449a7cab54d8", "security": "reality", "sni": "max.ru", "pbk": "G-v5THUO0-dAiT_dxTXsLwT-Rm4K4ucQX0VHHNBR0Uw", "sid": "", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇷🇺 Россия #412 • 425ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "Bypass-Media", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 425, "is_alive": true, "source_id": null, "uri": "vless://f811a2e8-08ed-4b30-b44c-449a7cab54d8@201.34.137.215:443?type=tcp&security=reality&flow=xtls-rprx-vision&fp=random&pbk=G-v5THUO0-dAiT_dxTXsLwT-Rm4K4ucQX0VHHNBR0Uw&sni=max.ru#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%23412%20%E2%80%A2%20425ms"}, {"protocol": "vless", "host": "31.76.34.216", "port": 443, "uuid": "94def50e-5f3c-4e4c-9719-3325f42d2131", "security": "reality", "sni": "ru-c-1.minzt.su", "pbk": "XrgbY2hKJQG8QOZO2J1pGmZsbvjSsSWoM9iULIMGK00", "sid": "", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇷🇺 Россия #413 • 470ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 470, "is_alive": true, "source_id": null, "uri": "vless://94def50e-5f3c-4e4c-9719-3325f42d2131@31.76.34.216:443?security=reality&encryption=none&pbk=XrgbY2hKJQG8QOZO2J1pGmZsbvjSsSWoM9iULIMGK00&headerType=none&fp=chrome&spx=/&type=tcp&flow=xtls-rprx-vision&sni=ru-c-1.minzt.su#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%23413%20%E2%80%A2%20470ms"}, {"protocol": "vless", "host": "195.133.73.65", "port": 443, "uuid": "ebd1c0d6-7ff4-4b9f-8692-237517a27a64", "security": "reality", "sni": "anyfile2file.com", "pbk": "mza5Hn1aolSz65qu-UwvBP3oesxMe25r11o4nxvikF0", "sid": "64c1fe36c7846400", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇷🇺 Россия #414 • 479ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 479, "is_alive": true, "source_id": null, "uri": "vless://ebd1c0d6-7ff4-4b9f-8692-237517a27a64@195.133.73.65:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=anyfile2file.com&fp=random&pbk=mza5Hn1aolSz65qu-UwvBP3oesxMe25r11o4nxvikF0&sid=64c1fe36c7846400&type=tcp#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%23414%20%E2%80%A2%20479ms"}, {"protocol": "vless", "host": "tgfree.rush-server.com", "port": 443, "uuid": "ebd1c0d6-7ff4-4b9f-8692-237517a27a64", "security": "reality", "sni": "anyfile2file.com", "pbk": "mza5Hn1aolSz65qu-UwvBP3oesxMe25r11o4nxvikF0", "sid": "64c1fe36c7846400", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇷🇺 Россия #415 • 510ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 510, "is_alive": true, "source_id": null, "uri": "vless://ebd1c0d6-7ff4-4b9f-8692-237517a27a64@tgfree.rush-server.com:443?flow=xtls-rprx-vision&encryption=none&security=reality&sni=anyfile2file.com&fp=chrome&pbk=mza5Hn1aolSz65qu-UwvBP3oesxMe25r11o4nxvikF0&sid=64c1fe36c7846400&allowinsecure=0&type=tcp&headerType=none#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%23415%20%E2%80%A2%20510ms"}, {"protocol": "vless", "host": "5.42.99.64", "port": 8443, "uuid": "c53ea5e9-ed8b-4990-805d-7f1d6451426c", "security": "reality", "sni": "du-rov.secureservice.top", "pbk": "fSVfR9NB-6J6smrZlavi0GWd8JfDh0aXuEkKbtuFzUI", "sid": "3cbc3d737fb9c4af", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇷🇺 Россия #416 • 536ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 536, "is_alive": true, "source_id": null, "uri": "vless://c53ea5e9-ed8b-4990-805d-7f1d6451426c@5.42.99.64:8443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=du-rov.secureservice.top&fp=random&pbk=fSVfR9NB-6J6smrZlavi0GWd8JfDh0aXuEkKbtuFzUI&sid=3cbc3d737fb9c4af&type=tcp#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%23416%20%E2%80%A2%20536ms"}, {"protocol": "vless", "host": "85.117.235.50", "port": 443, "uuid": "f4d71fd6-1c25-4748-836b-1dbda9268039", "security": "reality", "sni": "cz1.animeteka.info", "pbk": "PmdZ2ETkHc0zjYcs22xT_wyZk5fEpX7mg7RP396HBBc", "sid": "232b1b09e45325a4", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇷🇺 Россия #417 • 579ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 579, "is_alive": true, "source_id": null, "uri": "vless://f4d71fd6-1c25-4748-836b-1dbda9268039@85.117.235.50:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=cz1.animeteka.info&fp=random&pbk=PmdZ2ETkHc0zjYcs22xT_wyZk5fEpX7mg7RP396HBBc&sid=232b1b09e45325a4&type=tcp#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%23417%20%E2%80%A2%20579ms"}, {"protocol": "vless", "host": "tgfree.rush-server.com", "port": 443, "uuid": "ebd1c0d6-7ff4-4b9f-8692-237517a27a64", "security": "reality", "sni": "anyfile2file.com", "pbk": "mza5Hn1aolSz65qu-UwvBP3oesxMe25r11o4nxvikF0", "sid": "64c1fe36c7846400", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇷🇺 Россия #418 • 835ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 835, "is_alive": true, "source_id": null, "uri": "vless://ebd1c0d6-7ff4-4b9f-8692-237517a27a64@tgfree.rush-server.com:443?security=reality&encryption=none&pbk=mza5Hn1aolSz65qu-UwvBP3oesxMe25r11o4nxvikF0&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=anyfile2file.com&sid=64c1fe36c7846400#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%23418%20%E2%80%A2%20835ms"}, {"protocol": "vless", "host": "85.117.235.50", "port": 443, "uuid": "f4d71fd6-1c25-4748-836b-1dbda9268039", "security": "reality", "sni": "cz1.animeteka.info", "pbk": "PmdZ2ETkHc0zjYcs22xT_wyZk5fEpX7mg7RP396HBBc", "sid": "232b1b09e45325a4", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇷🇺 Россия #419 • 1614ms", "is_whitelist": false, "whitelist_label": "", "whitelist_category": "", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 1614, "is_alive": true, "source_id": null, "uri": "vless://f4d71fd6-1c25-4748-836b-1dbda9268039@85.117.235.50:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=cz1.animeteka.info&fp=random&pbk=PmdZ2ETkHc0zjYcs22xT_wyZk5fEpX7mg7RP396HBBc&sid=232b1b09e45325a4&type=tcp#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%23419%20%E2%80%A2%201614ms"}, {"protocol": "vless", "host": "83.168.71.216", "port": 443, "uuid": "a18f7c2d-9e45-4b8a-af3c-1d5e7f9c8b2a", "security": "reality", "sni": "ads.x5.ru", "pbk": "8h8t5eBWL9oERK7xWHQLFJE5j6sZdgNDQAs3EGnNbho", "sid": "2f49bccf11150ef2", "flow": "", "type": "tcp", "remark": "🇵🇱 Польша • 🛡️ X5-Retail (Зарубежный обход) • 449ms", "is_whitelist": true, "whitelist_label": "🛡️ X5-Retail", "whitelist_category": "", "country_code": "PL", "country_flag": "🇵🇱", "country_name": "Польша", "latency_ms": 449, "is_alive": true, "source_id": null, "uri": "vless://a18f7c2d-9e45-4b8a-af3c-1d5e7f9c8b2a@83.168.71.216:443?Telegram=@GozargahAzad,@GozargahAzad,@GozargahAzad,@GozargahAzad,@GozargahAzad,@GozargahAzad,@GozargahAzad&security=reality&encryption=none&pbk=8h8t5eBWL9oERK7xWHQLFJE5j6sZdgNDQAs3EGnNbho&host=mmad&headerType=none&fp=chrome&type=tcp&sni=ads.x5.ru&sid=2f49bccf11150ef2#%F0%9F%87%B5%F0%9F%87%B1%20%D0%9F%D0%BE%D0%BB%D1%8C%D1%88%D0%B0%20%E2%80%A2%20%F0%9F%9B%A1%EF%B8%8F%20X5-Retail%20%28%D0%97%D0%B0%D1%80%D1%83%D0%B1%D0%B5%D0%B6%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%29%20%E2%80%A2%20449ms"}, {"protocol": "vless", "host": "83.168.71.216", "port": 443, "uuid": "a18f7c2d-9e45-4b8a-af3c-1d5e7f9c8b2a", "security": "reality", "sni": "ads.x5.ru", "pbk": "8h8t5eBWL9oERK7xWHQLFJE5j6sZdgNDQAs3EGnNbho", "sid": "2f49bccf11150ef2", "flow": "", "type": "tcp", "remark": "🇵🇱 Польша • 🛡️ X5-Retail (Зарубежный обход) • 461ms", "is_whitelist": true, "whitelist_label": "🛡️ X5-Retail", "whitelist_category": "Keyword-Bypass", "country_code": "PL", "country_flag": "🇵🇱", "country_name": "Польша", "latency_ms": 461, "is_alive": true, "source_id": null, "uri": "vless://a18f7c2d-9e45-4b8a-af3c-1d5e7f9c8b2a@83.168.71.216:443?security=reality&encryption=none&pbk=8h8t5eBWL9oERK7xWHQLFJE5j6sZdgNDQAs3EGnNbho&host=%2F&headerType=none&fp=chrome&type=tcp&sni=ads.x5.ru&sid=2f49bccf11150ef2#%F0%9F%87%B5%F0%9F%87%B1%20%D0%9F%D0%BE%D0%BB%D1%8C%D1%88%D0%B0%20%E2%80%A2%20%F0%9F%9B%A1%EF%B8%8F%20X5-Retail%20%28%D0%97%D0%B0%D1%80%D1%83%D0%B1%D0%B5%D0%B6%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%29%20%E2%80%A2%20461ms"}, {"protocol": "vless", "host": "tg.riotvpn.eu", "port": 443, "uuid": "a18f7c2d-9e45-4b8a-af3c-1d5e7f9c8b2a", "security": "reality", "sni": "ads.x5.ru", "pbk": "8h8t5eBWL9oERK7xWHQLFJE5j6sZdgNDQAs3EGnNbho", "sid": "2f49bccf11150ef2", "flow": "", "type": "tcp", "remark": "🇵🇱 Польша • 🛡️ X5-Retail (Зарубежный обход) • 701ms", "is_whitelist": true, "whitelist_label": "🛡️ X5-Retail", "whitelist_category": "Keyword-Bypass", "country_code": "PL", "country_flag": "🇵🇱", "country_name": "Польша", "latency_ms": 701, "is_alive": true, "source_id": null, "uri": "vless://a18f7c2d-9e45-4b8a-af3c-1d5e7f9c8b2a@tg.riotvpn.eu:443?type=tcp&encryption=none&flow=&sni=ads.x5.ru&alpn=channel%40VPNine1-channel%40VPNine1-channel%40VPNine1-channel%40VPNine1-channel%40VPNine1-channel%40VPNine1-channel%40VPNine1-channel%40VPNine1%D0%A9%D2%96&fp=chrome&security=reality&pbk=8h8t5eBWL9oERK7xWHQLFJE5j6sZdgNDQAs3EGnNbho&sid=2f49bccf11150ef2#%F0%9F%87%B5%F0%9F%87%B1%20%D0%9F%D0%BE%D0%BB%D1%8C%D1%88%D0%B0%20%E2%80%A2%20%F0%9F%9B%A1%EF%B8%8F%20X5-Retail%20%28%D0%97%D0%B0%D1%80%D1%83%D0%B1%D0%B5%D0%B6%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%29%20%E2%80%A2%20701ms"}, {"protocol": "vless", "host": "193.163.203.253", "port": 443, "uuid": "441afe11-a180-4516-bb80-80a8a6b38705", "security": "reality", "sni": "yandex.ru", "pbk": "gE8LUmGFXik94SoDXNiAG5KprGyhjoRwDuhGebgAVWk", "sid": "5ee019e02e6ed99a", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇷🇺 Россия • 🛡️ Яндекс/Дзен (РФ обход) • 815ms", "is_whitelist": true, "whitelist_label": "🛡️ Яндекс/Дзен", "whitelist_category": "Yandex-Dzen", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 815, "is_alive": true, "source_id": null, "uri": "vless://441afe11-a180-4516-bb80-80a8a6b38705@193.163.203.253:443?type=tcp&security=reality&sni=yandex.ru&fp=chrome&flow=xtls-rprx-vision&pbk=gE8LUmGFXik94SoDXNiAG5KprGyhjoRwDuhGebgAVWk&sid=5ee019e02e6ed99a#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%E2%80%A2%20%F0%9F%9B%A1%EF%B8%8F%20%D0%AF%D0%BD%D0%B4%D0%B5%D0%BA%D1%81/%D0%94%D0%B7%D0%B5%D0%BD%20%28%D0%A0%D0%A4%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%29%20%E2%80%A2%20815ms"}, {"protocol": "vless", "host": "bl3fk52.sysopnova.art", "port": 443, "uuid": "441afe11-a180-4516-bb80-80a8a6b38705", "security": "reality", "sni": "yandex.ru", "pbk": "gE8LUmGFXik94SoDXNiAG5KprGyhjoRwDuhGebgAVWk", "sid": "5ee019e02e6ed99a", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇷🇺 Россия • 🛡️ Яндекс/Дзен (РФ обход) • 915ms", "is_whitelist": true, "whitelist_label": "🛡️ Яндекс/Дзен", "whitelist_category": "Yandex-Dzen", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 915, "is_alive": true, "source_id": null, "uri": "vless://441afe11-a180-4516-bb80-80a8a6b38705@bl3fk52.sysopnova.art:443?encryption=none&flow=xtls-rprx-vision&fp=&pbk=gE8LUmGFXik94SoDXNiAG5KprGyhjoRwDuhGebgAVWk&security=reality&sid=5ee019e02e6ed99a&sni=yandex.ru&type=tcp#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%E2%80%A2%20%F0%9F%9B%A1%EF%B8%8F%20%D0%AF%D0%BD%D0%B4%D0%B5%D0%BA%D1%81/%D0%94%D0%B7%D0%B5%D0%BD%20%28%D0%A0%D0%A4%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%29%20%E2%80%A2%20915ms"}, {"protocol": "vless", "host": "qq.utiltools.site", "port": 443, "uuid": "4054fdc2-ee80-4419-8a8e-d937df4719e2", "security": "reality", "sni": "qq.utiltools.site", "pbk": "drY21DHNOr6ezJLA2B10mzTExeJ9-gVBfTBNLwVBtWI", "sid": "", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇳🇱 Нидерланды • 🛡️ Whitelist (Зарубежный обход) • 926ms", "is_whitelist": true, "whitelist_label": "🛡️ Whitelist", "whitelist_category": "Keyword-Bypass", "country_code": "NL", "country_flag": "🇳🇱", "country_name": "Нидерланды", "latency_ms": 926, "is_alive": true, "source_id": null, "uri": "vless://4054fdc2-ee80-4419-8a8e-d937df4719e2@qq.utiltools.site:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=qq.utiltools.site&fp=random&pbk=drY21DHNOr6ezJLA2B10mzTExeJ9-gVBfTBNLwVBtWI&type=tcp&packetEncoding=xudp#%F0%9F%87%B3%F0%9F%87%B1%20%D0%9D%D0%B8%D0%B4%D0%B5%D1%80%D0%BB%D0%B0%D0%BD%D0%B4%D1%8B%20%E2%80%A2%20%F0%9F%9B%A1%EF%B8%8F%20Whitelist%20%28%D0%97%D0%B0%D1%80%D1%83%D0%B1%D0%B5%D0%B6%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%29%20%E2%80%A2%20926ms"}, {"protocol": "vless", "host": "qq.utiltools.site", "port": 443, "uuid": "4054fdc2-ee80-4419-8a8e-d937df4719e2", "security": "reality", "sni": "qq.utiltools.site", "pbk": "drY21DHNOr6ezJLA2B10mzTExeJ9-gVBfTBNLwVBtWI", "sid": "", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇳🇱 Нидерланды • 🛡️ Whitelist (Зарубежный обход) • 927ms", "is_whitelist": true, "whitelist_label": "🛡️ Whitelist", "whitelist_category": "", "country_code": "NL", "country_flag": "🇳🇱", "country_name": "Нидерланды", "latency_ms": 927, "is_alive": true, "source_id": null, "uri": "vless://4054fdc2-ee80-4419-8a8e-d937df4719e2@qq.utiltools.site:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=qq.utiltools.site&fp=random&pbk=drY21DHNOr6ezJLA2B10mzTExeJ9-gVBfTBNLwVBtWI&type=tcp&packetEncoding=xudp#%F0%9F%87%B3%F0%9F%87%B1%20%D0%9D%D0%B8%D0%B4%D0%B5%D1%80%D0%BB%D0%B0%D0%BD%D0%B4%D1%8B%20%E2%80%A2%20%F0%9F%9B%A1%EF%B8%8F%20Whitelist%20%28%D0%97%D0%B0%D1%80%D1%83%D0%B1%D0%B5%D0%B6%D0%BD%D1%8B%D0%B9%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%29%20%E2%80%A2%20927ms"}, {"protocol": "vless", "host": "bl3fk52.sysopnova.art", "port": 443, "uuid": "441afe11-a180-4516-bb80-80a8a6b38705", "security": "reality", "sni": "yandex.ru", "pbk": "gE8LUmGFXik94SoDXNiAG5KprGyhjoRwDuhGebgAVWk", "sid": "5ee019e02e6ed99a", "flow": "xtls-rprx-vision", "type": "raw", "remark": "🇷🇺 Россия • 🛡️ Яндекс/Дзен (РФ обход) • 942ms", "is_whitelist": true, "whitelist_label": "🛡️ Яндекс/Дзен", "whitelist_category": "Yandex-Dzen", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 942, "is_alive": true, "source_id": null, "uri": "vless://441afe11-a180-4516-bb80-80a8a6b38705@bl3fk52.sysopnova.art:443?security=reality&type=raw&packetEncoding=xudp&sni=yandex.ru&fp=chrome&flow=xtls-rprx-vision&sid=5ee019e02e6ed99a&pbk=gE8LUmGFXik94SoDXNiAG5KprGyhjoRwDuhGebgAVWk&encryption=none#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%E2%80%A2%20%F0%9F%9B%A1%EF%B8%8F%20%D0%AF%D0%BD%D0%B4%D0%B5%D0%BA%D1%81/%D0%94%D0%B7%D0%B5%D0%BD%20%28%D0%A0%D0%A4%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%29%20%E2%80%A2%20942ms"}, {"protocol": "vless", "host": "193.163.203.170", "port": 443, "uuid": "11aabba0-5fd1-4f15-8068-74c1a466cefc", "security": "reality", "sni": "yandex.ru", "pbk": "GCCZ1ZZjB_nj7yxqFi22bIIWWr_G6rnWUzDcssN_40o", "sid": "b28db60d77c50b4f", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇷🇺 Россия • 🛡️ Яндекс/Дзен (РФ обход) • 1236ms", "is_whitelist": true, "whitelist_label": "🛡️ Яндекс/Дзен", "whitelist_category": "Yandex-Dzen", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 1236, "is_alive": true, "source_id": null, "uri": "vless://11aabba0-5fd1-4f15-8068-74c1a466cefc@193.163.203.170:443?type=tcp&security=reality&flow=xtls-rprx-vision&fp=firefox&pbk=GCCZ1ZZjB_nj7yxqFi22bIIWWr_G6rnWUzDcssN_40o&sid=b28db60d77c50b4f&sni=yandex.ru#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%E2%80%A2%20%F0%9F%9B%A1%EF%B8%8F%20%D0%AF%D0%BD%D0%B4%D0%B5%D0%BA%D1%81/%D0%94%D0%B7%D0%B5%D0%BD%20%28%D0%A0%D0%A4%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%29%20%E2%80%A2%201236ms"}, {"protocol": "vless", "host": "prep.wwwinternetvideo.click", "port": 443, "uuid": "1c332eae-7e02-4acd-996d-4eb3e652401c", "security": "reality", "sni": "yandex.ru", "pbk": "uitO4Z8t9TplwwYaqwLqh5rfxDh_X8bOBiNuPbzvaEM", "sid": "bbe46bd8f6b96839", "flow": "xtls-rprx-vision", "type": "tcp", "remark": "🇷🇺 Россия • 🛡️ Яндекс/Дзен (РФ обход) • 1391ms", "is_whitelist": true, "whitelist_label": "🛡️ Яндекс/Дзен", "whitelist_category": "Yandex-Dzen", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 1391, "is_alive": true, "source_id": null, "uri": "vless://1c332eae-7e02-4acd-996d-4eb3e652401c@prep.wwwinternetvideo.click:443?security=reality&encryption=none&pbk=uitO4Z8t9TplwwYaqwLqh5rfxDh_X8bOBiNuPbzvaEM&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=yandex.ru&sid=bbe46bd8f6b96839#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%E2%80%A2%20%F0%9F%9B%A1%EF%B8%8F%20%D0%AF%D0%BD%D0%B4%D0%B5%D0%BA%D1%81/%D0%94%D0%B7%D0%B5%D0%BD%20%28%D0%A0%D0%A4%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%29%20%E2%80%A2%201391ms"}, {"protocol": "vless", "host": "45.12.75.242", "port": 26424, "uuid": "633f424e-2b11-48da-a6b3-a849dd71456f", "security": "reality", "sni": "ya.ru", "pbk": "l8AubqcxQO-HRFJy4pZL1vbLOo-eXit69s-XulSELE0", "sid": "23103e1e", "flow": "", "type": "raw", "remark": "🇷🇺 Россия • 🛡️ Яндекс/Дзен (РФ обход) • 1731ms", "is_whitelist": true, "whitelist_label": "🛡️ Яндекс/Дзен", "whitelist_category": "Yandex-Dzen", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 1731, "is_alive": true, "source_id": null, "uri": "vless://633f424e-2b11-48da-a6b3-a849dd71456f@45.12.75.242:26424?encryption=none&pbk=l8AubqcxQO-HRFJy4pZL1vbLOo-eXit69s-XulSELE0&security=reality&sid=23103e1e&sni=ya.ru&type=raw#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%E2%80%A2%20%F0%9F%9B%A1%EF%B8%8F%20%D0%AF%D0%BD%D0%B4%D0%B5%D0%BA%D1%81/%D0%94%D0%B7%D0%B5%D0%BD%20%28%D0%A0%D0%A4%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%29%20%E2%80%A2%201731ms"}, {"protocol": "vless", "host": "45.12.75.242", "port": 26424, "uuid": "633f424e-2b11-48da-a6b3-a849dd71456f", "security": "reality", "sni": "ya.ru", "pbk": "l8AubqcxQO-HRFJy4pZL1vbLOo-eXit69s-XulSELE0", "sid": "23103e1e", "flow": "", "type": "raw", "remark": "🇷🇺 Россия • 🛡️ Яндекс/Дзен (РФ обход) • 2108ms", "is_whitelist": true, "whitelist_label": "🛡️ Яндекс/Дзен", "whitelist_category": "Yandex-Dzen", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 2108, "is_alive": true, "source_id": null, "uri": "vless://633f424e-2b11-48da-a6b3-a849dd71456f@45.12.75.242:26424?encryption=none&fp=qq&pbk=l8AubqcxQO-HRFJy4pZL1vbLOo-eXit69s-XulSELE0&security=reality&sid=23103e1e&sni=ya.ru&type=raw#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%E2%80%A2%20%F0%9F%9B%A1%EF%B8%8F%20%D0%AF%D0%BD%D0%B4%D0%B5%D0%BA%D1%81/%D0%94%D0%B7%D0%B5%D0%BD%20%28%D0%A0%D0%A4%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%29%20%E2%80%A2%202108ms"}, {"protocol": "vless", "host": "62.152.58.90", "port": 443, "uuid": "1bb2af63-4472-44ed-9c70-8f316258b68b", "security": "reality", "sni": "360.yandex.ru", "pbk": "JBKJlzuJH1YzDHAoz28wEKbzWTGpDpKjgtSq0oT0a0k", "sid": "27e53bbcab7593d7", "flow": "", "type": "grpc", "remark": "🇷🇺 Россия • 🛡️ Яндекс/Дзен (РФ обход) • 2409ms", "is_whitelist": true, "whitelist_label": "🛡️ Яндекс/Дзен", "whitelist_category": "Yandex-Dzen", "country_code": "RU", "country_flag": "🇷🇺", "country_name": "Россия", "latency_ms": 2409, "is_alive": true, "source_id": null, "uri": "vless://1bb2af63-4472-44ed-9c70-8f316258b68b@62.152.58.90:443?encryption=none&mode=gun&pbk=JBKJlzuJH1YzDHAoz28wEKbzWTGpDpKjgtSq0oT0a0k&security=reality&sid=27e53bbcab7593d7&sni=360.yandex.ru&spx=%2F&type=grpc&fp=edge#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%E2%80%A2%20%F0%9F%9B%A1%EF%B8%8F%20%D0%AF%D0%BD%D0%B4%D0%B5%D0%BA%D1%81/%D0%94%D0%B7%D0%B5%D0%BD%20%28%D0%A0%D0%A4%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%29%20%E2%80%A2%202409ms"}];

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
  const foreignWl = CACHED_SERVERS.filter(s => s.is_whitelist && s.country_code !== 'RU').sort((a,b) => (a.latency_ms||999) - (b.latency_ms||999));
  const ru = CACHED_SERVERS.filter(s => !s.is_whitelist && s.country_code === 'RU').sort((a,b) => (a.latency_ms||999) - (b.latency_ms||999));
  const ruWl = CACHED_SERVERS.filter(s => s.is_whitelist && s.country_code === 'RU').sort((a,b) => (a.latency_ms||999) - (b.latency_ms||999));
  return [...foreign, ...foreignWl, ...ru, ...ruWl];
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
  const servers = getTop3PerCountry();
  const uris = servers.map((s, idx) => {
    let cleanRemark = "";
    if (idx === 0 && !s.is_whitelist && s.country_code !== 'RU') {
      cleanRemark = `⚡ Лучший зарубежный сервер (Мин. пинг) • ${s.country_flag || '🌐'} ${s.country_name || ''} • ${s.latency_ms}ms`;
    } else {
      const flag = s.country_flag || '🌐';
      const cName = s.country_name || s.country_code || 'VPN';
      let tag = "";
      if (s.is_whitelist) {
        tag = s.country_code !== 'RU' ? ` [${s.whitelist_label || '🛡️ Обход'} • Зарубежный]` : ` [${s.whitelist_label || '🛡️ Обход'} • РФ]`;
      } else if (s.latency_ms <= 85 && s.latency_ms > 0) {
        tag = ' [🎮 Игровой]';
      }
      const ping = s.latency_ms > 0 ? ` • ${s.latency_ms}ms` : '';
      cleanRemark = `${flag} ${cName}${tag} #${idx+1}${ping}`;
    }
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
    let cleanRemark = "";
    if (idx === 0 && !s.is_whitelist && s.country_code !== 'RU') {
      cleanRemark = `⚡ Лучший зарубежный сервер (Мин. пинг) • ${s.country_flag || '🌐'} ${s.country_name || ''} • ${s.latency_ms}ms`;
    } else {
      const flag = s.country_flag || '🌐';
      const cName = s.country_name || s.country_code || 'VPN';
      let tag = "";
      if (s.is_whitelist) {
        tag = s.country_code !== 'RU' ? ` [${s.whitelist_label || '🛡️ Обход'} • Зарубежный]` : ` [${s.whitelist_label || '🛡️ Обход'} • РФ]`;
      } else if (s.latency_ms <= 85 && s.latency_ms > 0) {
        tag = ' [🎮 Игровой]';
      }
      const ping = s.latency_ms > 0 ? ` • ${s.latency_ms}ms` : '';
      cleanRemark = `${flag} ${cName}${tag} #${idx+1}${ping}`;
    }
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
          { text: '🛡️ Лучший белый список (Мин. пинг)', callback_data: 'best_wl' }
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
    const foreignWl = CACHED_SERVERS.find(s => s.is_whitelist && s.country_code !== 'RU');
    if (bestWl) {
      let text = `🛡️ <b>Лучший белый список (Минимальный пинг):</b>\n\n` +
        `<b>Локация:</b> ${bestWl.country_flag} ${bestWl.country_name}\n` +
        `<b>Сервис маскировки:</b> ${bestWl.whitelist_label || 'Белый список'} (<code>${bestWl.sni || 'yandex.ru'}</code>)\n` +
        `<b>Пинг:</b> <code>${bestWl.latency_ms} ms</code>\n` +
        `<i>(Работает на мобильном интернете при любых глушениях операторов)</i>\n\n` +
        `Нажмите на ключ ниже, чтобы скопировать в Incy:\n` +
        `<code>${bestWl.uri}</code>`;

      if (foreignWl && foreignWl.host !== bestWl.host) {
        text += `\n\n🌐 <b>Зарубежный Whitelist (Обход + весь мировой интернет):</b>\n` +
          `${foreignWl.country_flag} ${foreignWl.country_name} • ${foreignWl.whitelist_label} • ${foreignWl.latency_ms}ms\n` +
          `<code>${foreignWl.uri}</code>`;
      }

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
  <div style="background: linear-gradient(135deg, rgba(6,182,212,0.18), rgba(16,185,129,0.18)); border: 1.5px solid var(--cyan); border-radius: 16px; padding: 16px; margin-bottom: 12px; cursor: pointer;" onclick="copyDirectKey('${origin}/best', '⚡ Лучший зарубежный сервер скопирован!')">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="font-size:11px; color:var(--cyan); font-weight:800; text-transform:uppercase; letter-spacing:0.5px;">⚡ САМЫЙ БЫСТРЫЙ СЕРВЕР (НЕ РОССИЯ)</div>
        <div style="font-size:15px; font-weight:800; margin-top:2px;">${stats.best_server ? `${stats.best_server.country_flag} ${stats.best_server.country_name} • ${stats.best_server.latency_ms}ms` : '⚡ Зарубежный узел'}</div>
        <div style="font-size:11px; color:var(--text-sec); margin-top:2px;">YouTube, Instagram, ChatGPT без блокировок</div>
      </div>
      <button class="btn-main" style="width:auto; padding:10px 16px; font-size:12px; background:var(--cyan); color:#000; border-radius:10px;">Скопировать</button>
    </div>
  </div>

  <!-- 1b. Best Whitelist Server (Minimum Ping) -->
  <div style="background: linear-gradient(135deg, rgba(16,185,129,0.18), rgba(6,182,212,0.18)); border: 1.5px solid var(--emerald); border-radius: 16px; padding: 16px; margin-bottom: 16px; cursor: pointer;" onclick="copyDirectKey('${origin}/best-whitelist', '🛡️ Лучший белый список скопирован!')">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="font-size:11px; color:var(--emerald); font-weight:800; text-transform:uppercase; letter-spacing:0.5px;">🛡️ ЛУЧШИЙ БЕЛЫЙ СПИСОК (МИН. ПИНГ)</div>
        <div style="font-size:15px; font-weight:800; margin-top:2px;">${stats.best_whitelist ? `${stats.best_whitelist.country_flag} ${stats.best_whitelist.country_name} • ${stats.best_whitelist.whitelist_label || 'Обход'} • ${stats.best_whitelist.latency_ms}ms` : '🛡️ Белый список'}</div>
        <div style="font-size:11px; color:var(--text-sec); margin-top:2px;">Работает на мобильном интернете при любых глушениях операторов</div>
      </div>
      <button class="btn-main" style="width:auto; padding:10px 16px; font-size:12px; background:var(--emerald); color:#000; border-radius:10px;">Скопировать</button>
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
