import os
from utils.utils import generate_clash_config, send_markdown_toDing
from utils.fetcher import get_nodes


def _save_configs(clash_config):
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, "gen_clash_config.yaml")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(clash_config)
    print(f"Clash 配置文件已生成: {output_file}")


def _filter_nodes(nodes):
    filtered_nodes = []
    for node in nodes:
        if node.get("type") == "ss" and node.get("cipher") == "ss":
            print(f"过滤节点: {node.get('name')} - 类型和加密方式都为ss")
            continue
        filtered_nodes.append(node)
    return filtered_nodes


if __name__ == "__main__":
    nodes = get_nodes()
    nodes = _filter_nodes(nodes)
    clash_config = generate_clash_config(nodes)
    send_markdown_toDing(nodes)
    _save_configs(clash_config)
    
