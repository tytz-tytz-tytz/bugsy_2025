import json
import networkx as nx
from pathlib import Path
from typing import List, Set

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

def expand_tags(stems: List[str], limit_per_stem: int = 3) -> Set[str]:
    with open("data/concept_graph.json", "r", encoding="utf-8") as f:
        graph = json.load(f)

    expanded = set()
    for stem in stems:
        neighbors = graph.get(stem, [])
        expanded.update(neighbors[:limit_per_stem])
    return expanded