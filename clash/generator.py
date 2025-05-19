import os
from utils.utils import fetch_url, generate_clash_config
from protocol import vpn_ss, vpn_ssr, vpn_vmess, vpn_trojan


def _find_configs():
    # 来自 app.py 的 URL
    ss_url = (
        "https://gitlab.com/zhifan999/fq/-/wikis/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
    )
    vmess_url = "https://gitlab.com/zhifan999/fq/-/wikis/v2ray%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
    mixin_url = "https://raw.githubusercontent.com/Pawdroid/Free-servers/refs/heads/main/README.md"

    # 获取ss、ssr、vmess、trojan配置
    ss_configs = []
    ssr_configs = []
    ss_page = fetch_url(ss_url)
    ss_configs.extend(vpn_ss.find_ss_link(ss_page, r"ss://[^\\]+"))
    ssr_configs.extend(vpn_ssr.find_ssr_link(ss_page, r"ssr://[^\\]+"))

    vmess_configs = []
    vmess_page = fetch_url(vmess_url)
    vmess_configs.extend(vpn_vmess.find_vmess_link(vmess_page, r"vmess://[^\\]+"))

    trojan_configs = []
    mixin_page = fetch_url(mixin_url)
    ss_configs.extend(vpn_ss.find_ss_link(mixin_page, r"^ss://[^\s\n]+"))
    ssr_configs.extend(vpn_ssr.find_ssr_link(mixin_page, r"^ssr://[^\s\n]+"))
    vmess_configs.extend(vpn_vmess.find_vmess_link(mixin_page, r"^vmess://[^\s\n]+"))
    trojan_configs.extend(
        vpn_trojan.find_trojan_link(mixin_page, r"^trojan://[^\s\n]+")
    )

    return (ss_configs, ssr_configs, vmess_configs, trojan_configs)


def _save_configs(clash_config):
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, "gen_clash_config.yaml")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(clash_config)
    print(f"Clash 配置文件已生成: {output_file}")


def main():
    configs = _find_configs()
    clash_config = generate_clash_config(*configs)
    _save_configs(clash_config)


if __name__ == "__main__":
    main()
