import json
import networkx as nx
from pyvis.network import Network
from jinja2 import Template
import pkg_resources
import matplotlib.pyplot as plt

def export_graph_to_json(graph: nx.Graph, path: str) -> None:
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
                "target": v,
                "weight": graph.edges[u, v].get("weight", 1)
            } for u, v in graph.edges
        ]
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def export_graph_to_html(graph: nx.Graph, output_path: str = "graph.html") -> None:
    net = Network(height="1000px", width="100%", directed=False, notebook=False)
    net.barnes_hut()

    try:
        template_path = pkg_resources.resource_filename("pyvis", "templates/template.html")
        with open(template_path, "r", encoding="utf-8") as f:
            net.template = Template(f.read())
    except Exception as e:
        print("Не удалось загрузить шаблон pyvis:", e)
        return

    for node in graph.nodes:
        net.add_node(
            node,
            label=node,
            title=graph.nodes[node].get("title", node),
            level=graph.nodes[node].get("level", 1),
            color="#90EE90" if graph.nodes[node].get("is_leaf") else "#87CEFA"
        )

    for u, v, data in graph.edges(data=True):
        net.add_edge(u, v, value=data.get("weight", 1))

    # 🔧 Критическое исправление: приводим output_path к строке
    net.write_html(str(output_path), notebook=False, open_browser=False)

def visualize_graph(graph: nx.Graph, layout: str = "spring") -> None:
    pos = getattr(nx, f"{layout}_layout")(graph)

    plt.figure(figsize=(16, 12))
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=200,
        font_size=8,
        labels={n: graph.nodes[n].get("title", n)[:30] for n in graph.nodes},
        arrows=True
    )
    plt.title("Граф понятий")
    plt.tight_layout()
    plt.show()