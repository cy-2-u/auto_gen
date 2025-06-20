import requests
import random
import string
import yaml
import os


def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return ""


def get_random_name(prefix):
    data_set = string.ascii_letters + string.digits
    random_value = "".join(random.choices(data_set, k=5))
    return f"{prefix}-{random_value}"


def generate_clash_config(nodes):
    """生成Clash配置文件"""
    with open("template.yaml", "r", encoding="utf-8") as f:
        yaml_config = yaml.safe_load(f)
    for config in nodes:
        yaml_config["proxies"].append(config)
        yaml_config["proxy-groups"][0]["proxies"].append(config["name"])
    return yaml.dump(yaml_config, allow_unicode=True, sort_keys=False)


def send_markdown_toDing(nodes):
    base_url = "https://proxy.v2gh.com/https://raw.githubusercontent.com/YangLang116/auto_gen/master/clash"
    response = requests.request(
        "POST",
        "https://oapi.dingtalk.com/robot/send",
        json={
            "msgtype": "markdown",
            "markdown": {
                "title": "VPN",
                "text": f"- 更新节点数: {len(nodes)}\n- 订阅地址: {base_url}/gen_clash_config.yaml\n![QR]({base_url}/qr/v2gh.png)",
            },
        },
        params={"access_token": os.environ["CLASH_DING_TOKEN"]},
    )
    print(f"send result: {response.text}")
