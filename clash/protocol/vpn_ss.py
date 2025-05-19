import base64
import re
from utils.utils import get_random_name


def _parse_ss_link(ss_link):
    try:
        # 去掉 ss:// 前缀
        encoded_part = ss_link.replace("ss://", "")
        # 去除可能存在的注释部分
        if "#" in encoded_part:
            encoded_part = encoded_part.split("#")[0]

        # 分离出 base64 编码部分和服务器信息部分
        if "@" in encoded_part:
            try:
                base64_part, server_info = encoded_part.split("@")
                # 处理Base64填充
                missing_padding = len(base64_part) % 4
                if missing_padding:
                    base64_part += "=" * (4 - missing_padding)
                # 解码 base64 部分
                decoded = base64.b64decode(base64_part).decode("utf-8")
                cipher, password = decoded.split(":")
                # 分离服务器地址和端口
                server, port = server_info.split(":")
                return {
                    "cipher": cipher,
                    "password": password,
                    "server": server,
                    "port": port,
                }
            except Exception as e:
                raise ValueError(f"Failed to parse SS link: {e}")
        else:
            raise ValueError("Invalid SS link format: missing @")
    except Exception as e:
        raise ValueError(f"Error parsing SS link: {e}")


def _generate_clash(config):
    return {
        "name": get_random_name("SS"),
        "type": "ss",
        "server": config["server"],
        "port": int(config["port"]),
        "cipher": config["cipher"],
        "password": config["password"],
    }


def _convert_ss_link(ss_link):
    try:
        config = _parse_ss_link(ss_link)
        return _generate_clash(config)
    except Exception as e:
        print(f"解析SS链接错误: {ss_link} - {e}")
        return None


def find_ss_link(text, regex):
    links = list(set(re.findall(regex, text, re.MULTILINE)))
    results = []
    for link in links:
        print("--------------------------------")
        print("ss_link: ", link)
        result = _convert_ss_link(link)
        if result:
            print("result: ", result)
            results.append(result)
        print("--------------------------------")
    return results


if __name__ == "__main__":
    ss_link = "ss://YWVzLTI1Ni1nY206ZG9uZ3RhaXdhbmcuY29t@92.118.205.110:11111#dongtaiwang.com%E8%8A%82%E7%82%B9ss"
    result = _convert_ss_link(ss_link)
    print(result)
