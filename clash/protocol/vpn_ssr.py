import base64
import urllib.parse
import re
from utils.utils import get_random_name


def _parse_ssr_link(ssr_link):
    # 去掉 ssr:// 前缀
    encoded_part = ssr_link.replace("ssr://", "")
    # 去除URL中可能包含的非法字符
    encoded_part = encoded_part.split("#")[0]  # 移除注释部分
    # 处理Base64填充
    missing_padding = len(encoded_part) % 4
    if missing_padding:
        encoded_part += "=" * (4 - missing_padding)
    # 尝试解码 base64 部分
    decoded = base64.b64decode(encoded_part).decode("utf-8")
    # 分离基本信息和参数部分
    basic_info, param_str = decoded.split("/", 1)
    server, port, protocol, cipher, obfs, password_encoded = basic_info.split(":")
    # 解码密码
    missing_padding = len(password_encoded) % 4
    if missing_padding:
        password_encoded += "=" * (4 - missing_padding)
    try:
        password_bytes = base64.b64decode(password_encoded)
        password = password_bytes.decode("utf-8")
    except:
        password = password_encoded  # 如果解码失败，使用原始值
    # 解析参数
    params = urllib.parse.parse_qs(param_str.lstrip("?"))
    result = {
        "server": server,
        "port": int(port),
        "protocol": protocol,
        "cipher": cipher,
        "obfs": obfs,
        "password": password,
    }
    for key, value in params.items():
        result[key] = value[0]
    return result

def _generate_clash(config):
    return {
        "name": get_random_name("SSR"),
        "type": "ssr",
        "server": config["server"],
        "port": config["port"],
        "obfs": config["obfs"],
        "protocol": config["protocol"],
        "cipher": config["cipher"],
        "password": config["password"],
    }

def convert_ssr_link(ssr_link):
    try:
        config = _parse_ssr_link(ssr_link)
        return _generate_clash(config)
    except Exception as e:
        print(f"解析SSR链接错误: {ssr_link} - {e}")
        return None

def convert_ssr_links(ssr_links):
    results = []
    for link in ssr_links:
        if "ssr://" not in link:
            continue
        print("--------------------------------")
        print("ssr_link: ", link)
        result = convert_ssr_link(link)
        if result:
            print("result: ", result)
            results.append(result)
        else:
            print("error link")
        print("--------------------------------")
    return results

def find_ssr_link(text, regex):
    return re.findall(regex, text, re.MULTILINE)

if __name__ == "__main__":
    ssr_link = "ssr://ZG9uZ3RhaXdhbmc1LmNvbTozMjAwMDphdXRoX2NoYWluX2E6Y2hhY2hhMjAtaWV0Zjp0bHMxLjJfdGlja2V0X2F1dGg6Wkc5dVozUmhhWGRoYm1jdVkyOXQvP29iZnNwYXJhbT0mcmVtYXJrcz1aRzl1WjNSaGFYZGhibWN1WTI5dDZJcUM1NEs1"
    result = convert_ssr_link(ssr_link)
    print(result)
