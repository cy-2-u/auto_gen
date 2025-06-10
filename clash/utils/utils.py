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


def generate_clash_config(nodes):
    """生成Clash配置文件"""
    with open('template.yaml', 'r', encoding='utf-8') as f:
        yaml_config = yaml.safe_load(f)
    for config in nodes:
        yaml_config["proxies"].append(config)
        yaml_config["proxy-groups"][0]["proxies"].append(config["name"])
        yaml_config["proxy-groups"][1]["proxies"].append(config["name"])

    return yaml.dump(yaml_config, allow_unicode=True, sort_keys=False)
