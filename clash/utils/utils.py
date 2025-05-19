import requests
import random
import string
import yaml


def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return ""


def get_random_name(prefix):
    return (
        f"{prefix}-{''.join(random.choices(string.ascii_letters + string.digits, k=5))}"
    )


def generate_clash_config(ss_configs, ssr_configs, vmess_configs, trojan_configs):
    """生成Clash配置文件"""

    # 基础配置
    yaml_config = {
        "port": 7890,
        "socks-port": 7891,
        "allow-lan": True,
        "mode": "Rule",
        "log-level": "info",
        "external-controller": "127.0.0.1:9090",
        "proxies": [],
        "proxy-groups": [
            {
                "name": "自动选择",
                "type": "url-test",
                "url": "https://www.google.com",
                "interval": 300,
                "proxies": [],
            },
            {"name": "节点选择", "type": "select", "proxies": ["自动选择"]},
            {"name": "国外媒体", "type": "select", "proxies": ["节点选择", "自动选择"]},
            {"name": "国内媒体", "type": "select", "proxies": ["DIRECT", "节点选择"]},
        ],
        "rules": [
            "DOMAIN-SUFFIX,facebook.com,节点选择",
            "DOMAIN-SUFFIX,twitter.com,节点选择",
            "DOMAIN-SUFFIX,youtube.com,国外媒体",
            "DOMAIN-SUFFIX,netflix.com,国外媒体",
            "DOMAIN-SUFFIX,bilibili.com,国内媒体",
            "DOMAIN-SUFFIX,iqiyi.com,国内媒体",
            "DOMAIN-SUFFIX,cn,DIRECT",
            "GEOIP,CN,DIRECT",
            "MATCH,节点选择",
        ],
    }

    # 添加节点
    def add_proxys(configs):
        for config in configs:
            # 移除花括号并按逗号分割
            yaml_config["proxies"].append(config)
            yaml_config["proxy-groups"][0]["proxies"].append(config["name"])
            yaml_config["proxy-groups"][1]["proxies"].append(config["name"])

    # 添加所有代理节点
    add_proxys(ss_configs)
    add_proxys(ssr_configs)
    add_proxys(vmess_configs)
    add_proxys(trojan_configs)

    return yaml.dump(yaml_config, allow_unicode=True, sort_keys=False)
