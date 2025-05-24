import networkx as nx
import re
from typing import List, Dict
import json

def load_dom_graph(graph_path):
    with open(graph_path, 'r', encoding='utf-8') as f:
        graph = json.load(f)
    return graph

def build_dom_graph(toc_entries: List[Dict]) -> nx.DiGraph:
    """
    Строит DOM-граф из заголовков документации с учётом вложенности.
    """
    G = nx.DiGraph()
    G.add_node("root", title="Документация Marketer", page=0, level=-1)
    stack = []

    for idx, entry in enumerate(toc_entries):

        # Генерируем читаемый node_id: <номер>_<слаг-заголовок>
        slug = re.sub(r'\W+', '_', entry["title"].lower()).strip('_')
        node_id = f"{idx}_{slug}"

        # Добавляем вершину с метаинформацией
        G.add_node(node_id, **entry)

        # Ищем родителя по уровню вложенности
        while stack and stack[-1][1] >= entry["level"]:
            stack.pop()

        if stack:
            parent_id = stack[-1][0]
            G.add_edge(parent_id, node_id)
        else:
            G.add_edge("root", node_id)

        stack.append((node_id, entry["level"]))

    # Добавляем глубину и is_leaf-флаг
    def mark_depths(node, depth=0):
        G.nodes[node]["depth"] = depth
        for child in G.successors(node):
            mark_depths(child, depth + 1)

    roots = [n for n, d in G.in_degree() if d == 0]
    for root in roots:
        mark_depths(root)

    for node in G.nodes:
        G.nodes[node]["is_leaf"] = G.out_degree(node) == 0

    return G