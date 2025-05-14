import json
import networkx as nx
from typing import Union

def export_graph_to_json(graph: nx.DiGraph, path: str) -> None:
    """
    Экспортирует граф в JSON со всеми атрибутами узлов.
    """
    data = {
        "nodes": [
            {
                "id": node,
                **graph.nodes[node]
            } for node in graph.nodes
        ],
        "edges": [
            {
                "source": u,
                "target": v
            } for u, v in graph.edges
        ]
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

import matplotlib.pyplot as plt

def visualize_graph(graph: nx.DiGraph, layout: str = "spring") -> None:
    """
    Быстрая визуализация графа. layout = spring | kamada_kawai | shell
    """
    pos = getattr(nx, f"{layout}_layout")(graph)

    plt.figure(figsize=(16, 12))
    nx.draw(
        graph,
        pos,
        with_labels=True,
        labels={n: graph.nodes[n]["title"][:30] + "..." for n in graph.nodes},
        node_size=200,
        font_size=8,
        arrows=True
    )
    plt.title("DOM-структура документации")
    plt.tight_layout()
    plt.show()

from pyvis.network import Network
import networkx as nx
from jinja2 import Template
import pkg_resources

def export_graph_to_html(graph: nx.DiGraph, output_path: str = "dom_graph.html") -> None:
    """
    Экспортирует граф в интерактивный HTML-файл, обходя баг с template = None.
    """
    net = Network(height="1000px", width="100%", directed=True, notebook=False)
    net.barnes_hut()

    # --- Загружаем шаблон вручную, обход бага ---
    try:
        template_path = pkg_resources.resource_filename("pyvis", "templates/template.html")
        with open(template_path, "r", encoding="utf-8") as f:
            net.template = Template(f.read())
    except Exception as e:
        print("Не удалось загрузить шаблон pyvis:", e)
        return

    # --- Добавляем узлы ---
    for node in graph.nodes:
        title = graph.nodes[node]["title"]
        level = graph.nodes[node]["level"]
        is_leaf = graph.nodes[node]["is_leaf"]

        net.add_node(
            node,
            label=title[:40] + "..." if len(title) > 40 else title,
            title=title,
            level=level,
            color="#90EE90" if is_leaf else "#87CEFA"
        )

    # --- Добавляем рёбра ---
    for source, target in graph.edges:
        net.add_edge(source, target)

    # --- Генерируем HTML без открытия браузера ---
    net.write_html(output_path, notebook=False, open_browser=False)
