import urllib.parse
import re
from utils.utils import get_random_name


def _parse_trojan_link(trojan_link):
    # 去掉 trojan:// 前缀
    link_without_prefix = trojan_link.replace("trojan://", "")
    # 移除注释部分
    if "#" in link_without_prefix:
        link_without_prefix = link_without_prefix.split("#")[0]
    # 分离密码、服务器信息和参数部分
    password_part, server_part = link_without_prefix.split("@", 1)
    # 处理服务器和端口
    server_and_port, params = (
        server_part.split("?", 1)
        if "?" in server_part
        else (server_part, "")
    )
    server, port = server_and_port.split(":")
    # 处理参数部分
    params_dict = {}
    if params:
        param_pairs = params.split("&")
        for pair in param_pairs:
            if "=" in pair:
                key, value = pair.split("=", 1)
                params_dict[key] = urllib.parse.unquote(value)
    return {
        "password": urllib.parse.unquote(password_part),
        "server": server,
        "port": port,
        "params": params_dict,
    }

def _generate_clash(config):
    params_str = ", ".join([f"{k}: {v}" for k, v in config.get("params", {}).items()])
    return {
        "name": get_random_name("Trojan"),
        "type": "trojan",
        "server": config["server"],
        "port": int(config["port"]),
        "password": config["password"],
        "params": params_str,
    }

def convert_trojan_link(trojan_link):
    try:
        config = _parse_trojan_link(trojan_link)
        return _generate_clash(config)
    except Exception as e:
        print(f"解析Trojan链接错误: {trojan_link[:30]}... - {e}")
        return None

def convert_trojan_links(trojan_links):
    results = []
    for link in trojan_links:
        if not link.startswith("trojan://"):
            continue
        print("--------------------------------")
        print("trojan_link: ", link)
        result = convert_trojan_link(link)
        if result:
            print("result: ", result)
            results.append(result)
        else:
            print("error link")
        print("--------------------------------")
    return results

def find_trojan_link(text, regex):
    return re.findall(regex, text, re.MULTILINE)

if __name__ == "__main__":
    trojan_link = "trojan://3d4ad187-b554-4300-bf71-d26c71962504@172.67.138.187:443?security=tls&sni=FFfgtyy.7282728.XYZ&type=ws&host=fffgtyy.7282728.xyz&path=%2FWaHA3RC540rQ8PWqRcOEICAwmfH7&fp=chrome&alpn=http%2F1.1#%E7%BE%8E%E5%9B%BD+CloudFlare%E8%8A%82%E7%82%B9"
    result = convert_trojan_link(trojan_link)
    print(result)
