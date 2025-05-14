from dom.extract import extract_toc_layout_fixed
from dom.structure import build_dom_graph
from dom.export import export_graph_to_json

toc = extract_toc_layout_fixed("data/marketer.pdf")
graph = build_dom_graph(toc)

export_graph_to_json(graph, "dom_structure.json")