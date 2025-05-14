import json
import networkx as nx
from pathlib import Path
from typing import List

GRAPH_PATH = Path("data/concept_graph.json")

def load_concept_graph() -> nx.Graph:
    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        graph_data = json.load(f)

    G = nx.Graph()
    for node in graph_data["nodes"]:
        G.add_node(node["id"], **node)
    for edge in graph_data["edges"]:
        G.add_edge(edge["source"], edge["target"], weight=edge.get("weight", 1))

    return G

def expand_tags(seed_tags: List[str], depth: int = 1) -> List[str]:
    """
    Расширяет теги по графу на N шагов от заданных.
    """
    G = load_concept_graph()
    expanded = set(seed_tags)
    for tag in seed_tags:
        if tag in G:
            neighbors = nx.single_source_shortest_path_length(G, tag, cutoff=depth)
            expanded.update(neighbors.keys())
    return sorted(expanded)
