from dom.extract import extract_toc_layout_fixed as extract_toc_layout
from dom.structure import build_dom_graph
import pandas as pd

# 1. Извлекаем структуру оглавления
toc = extract_toc_layout("data/marketer.pdf")

# 2. Строим граф
G = build_dom_graph(toc)

# 3. Преобразуем в DataFrame
df = pd.DataFrame([
    {
        "node_id": node,
        "title": G.nodes[node]["title"],
        "page": G.nodes[node]["page"],
        "level": G.nodes[node]["level"],
        "depth": G.nodes[node]["depth"],
        "is_leaf": G.nodes[node]["is_leaf"]
    }
    for node in G.nodes
])

# 4. Смотрим результат
print(df.head(30))  # первые 10 строк
# или сохранить
# df.to_csv("dom_structure.csv", index=False)
