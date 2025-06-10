from utils.utils import fetch_url
from protocol import vpn_ss, vpn_ssr, vpn_vmess, vpn_trojan

def _find_from_github_fq():
    nodes = []
    content = fetch_url(
        "https://gitlab.com/zhifan999/fq/-/wikis/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
    )
    nodes.extend(vpn_ss.find_ss_link(content, r"ss://[^\\]+"))
    nodes.extend(vpn_ssr.find_ssr_link(content, r"ssr://[^\\]+"))
    content = fetch_url(
        "https://gitlab.com/zhifan999/fq/-/wikis/v2ray%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
    )
    nodes.extend(vpn_vmess.find_vmess_link(content, r"vmess://[^\\]+"))
    print(f"Github Wiki 解析节点数: {len(nodes)}")
    return nodes

def _find_from_github_text():
    nodes = []
    urls = [
        "https://raw.githubusercontent.com/ermaozi/get_subscribe/refs/heads/main/subscribe/v2ray.txt",
        "https://raw.githubusercontent.com/aiboboxx/v2rayfree/refs/heads/main/README.md",
        "https://raw.githubusercontent.com/Pawdroid/Free-servers/refs/heads/main/README.md",
    ]
    for url in urls:
        content = fetch_url(url)
        nodes.extend(vpn_ss.find_ss_link(content, r"^ss://[^\s\n]+"))
        nodes.extend(vpn_ssr.find_ssr_link(content, r"^ssr://[^\s\n]+"))
        nodes.extend(vpn_vmess.find_vmess_link(content, r"^vmess://[^\s\n]+"))
        nodes.extend(vpn_trojan.find_trojan_link(content, r"^trojan://[^\s\n]+"))
    print(f"Github Text 解析节点数: {len(nodes)}") 
    return nodes

def _search_nodes():
    nodes = []
    nodes.extend(_find_from_github_text())
    nodes.extend(_find_from_github_fq())
    return set(nodes)

def get_nodes():
    result = []
    nodes = _search_nodes()
    result.extend(vpn_ss.convert_ss_links(nodes))
    result.extend(vpn_ssr.convert_ssr_links(nodes))
    result.extend(vpn_vmess.convert_vmess_links(nodes))
    result.extend(vpn_trojan.convert_trojan_links(nodes))
    return result
    
