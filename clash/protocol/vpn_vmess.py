import base64
import json
import re
from utils.utils import get_random_name


def _parse_vmess_link(vmess_link):
    """解析vmess协议链接"""
    # 提取base64部分
    encoded_str = vmess_link.replace("vmess://", "")
    # 处理Base64填充
    missing_padding = len(encoded_str) % 4
    if missing_padding:
        encoded_str += "=" * (4 - missing_padding)
    decoded_str = base64.urlsafe_b64decode(encoded_str).decode("utf-8")
    # 解析配置参数
    config = json.loads(decoded_str)
    # 提取关键字段
    required_fields = [
        "add",
        "port",
        "id",
        "aid",
        "scy",
        "net",
        "type",
        "host",
        "path",
        "tls",
    ]
    return {field: config.get(field, "N/A") for field in required_fields}

def _generate_clash(config):
    protocol = config["net"]
    return {
        "name": get_random_name("VMESS"),
        "type": "vmess",
        "server": config["add"],
        "port": int(config["port"]),
        "uuid": config["id"],
        "alterId": int(config["aid"]),
        "cipher": config["scy"] if config["scy"] != "N/A" else "none",
        "tls": bool(config["tls"]),
        "network": protocol,
        f"{protocol}-opts": {
            "path": config["path"],
            "headers": {"Host": config["host"]},
        },
    }

def convert_vmess_link(vmess_link):
    try:
        config = _parse_vmess_link(vmess_link)
        return _generate_clash(config)
    except Exception as e:
        print(f"解析VMess链接错误: {vmess_link[:30]}... - {e}")
        return None

def convert_vmess_links(vmess_links):
    results = []
    for link in vmess_links:
        if not link.startswith("vmess://"):
            continue
        print("--------------------------------")
        print("vmess_link: ", link)
        result = convert_vmess_link(link)
        if result:
            print("result: ", result)
            results.append(result)
        else:
            print("error link")
        print("--------------------------------")
    return results

def find_vmess_link(text, regex):
    return re.findall(regex, text, re.MULTILINE)

if __name__ == "__main__":
    # 单元测试
    test_link = "vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogImRvbmd0YWl3YW5nLmNvbVx1ODI4Mlx1NzBCOTEiLA0KICAiYWRkIjogIjIwOC4xMTUuMjQ5Ljk4IiwNCiAgInBvcnQiOiAiNjE1NzgiLA0KICAiaWQiOiAiN2I3MGIyMzMtOWQ4Yy00NWJhLTg1ZmUtNTIzZDM2YmVkNjAwIiwNCiAgImFpZCI6ICIwIiwNCiAgInNjeSI6ICJhdXRvIiwNCiAgIm5ldCI6ICJ3cyIsDQogICJ0eXBlIjogIm5vbmUiLA0KICAiaG9zdCI6ICJ3d3cuYmluZy5jb20iLA0KICAicGF0aCI6ICJnaXRodWIuY29tL0FsdmluOTk5OSIsDQogICJ0bHMiOiAiIiwNCiAgInNuaSI6ICIiLA0KICAiYWxwbiI6ICIiLA0KICAiZnAiOiAiIg0KfQ=="
    result = convert_vmess_link(test_link)
    print(result)
