import json
import networkx as nx
from itertools import combinations
from collections import defaultdict
from pathlib import Path
import sys

# === Добавляем путь к data/ чтобы импортировать utils_graph ===
sys.path.append(str(Path(__file__).resolve().parent.parent / "data"))

from utils_graph import export_graph_to_json, export_graph_to_html

# === Пути ===
CHUNKS_PATH = Path("data/structured_chunks_final_tagged.json")
GRAPH_OUTPUT_JSON = Path("data/concept_graph.json")
GRAPH_OUTPUT_HTML = Path("data/concept_graph.html")

def build_cooccurrence_graph(chunks_path: Path) -> nx.Graph:
    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    G = nx.Graph()
    cooccurrence = defaultdict(int)

    for chunk in chunks:
        tags = chunk.get("tags", [])
        unique_tags = sorted(set(tags))
        for a, b in combinations(unique_tags, 2):
            key = tuple(sorted((a, b)))
            cooccurrence[key] += 1

    all_tags = set(tag for pair in cooccurrence for tag in pair)
    for tag in all_tags:
        G.add_node(tag, title=tag, level=1, is_leaf=True)

    for (a, b), weight in cooccurrence.items():
        G.add_edge(a, b, weight=weight)

    return G

if __name__ == "__main__":
    print("Строим граф понятий...")
    graph = build_cooccurrence_graph(CHUNKS_PATH)

    print("Экспортируем в JSON...")
    export_graph_to_json(graph, GRAPH_OUTPUT_JSON)

    print("Экспортируем в HTML...")
    export_graph_to_html(graph, GRAPH_OUTPUT_HTML)

    print("Готово: граф сохранён в data/")