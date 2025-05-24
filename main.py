import json
from chunker.extract import extract_toc_layout_fixed
from chunker.structure import build_dom_graph
from chunker.chunker import build_chunks_with_toc_analysis

def main():
    pdf_path = "data/marketer.pdf"
    graph_path = "data/dom_structure.json"
    output_path = "data/structured_chunks.json"

    # 1. Извлекаем оглавление из первых страниц PDF
    toc_entries = extract_toc_layout_fixed(pdf_path)

    # Добавляем уровни вложенности по отступам (чем больше x0 — тем глубже)
    for entry in toc_entries:
        entry["level"] = 0  # если есть x0: entry["level"] = entry.get("x0", 0) // 30

    # 2. Строим граф структуры
    graph = build_dom_graph(toc_entries)

    # 3. Сохраняем DOM-структуру
    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump({
            "nodes": [
                {"id": node, **graph.nodes[node]}
                for node in graph.nodes if node != "root"
            ]
        }, f, ensure_ascii=False, indent=2)

    print("DOM-структура сохранена")

    # 4. Делим PDF на чанки
    build_chunks_with_toc_analysis(pdf_path, graph_path, output_path)

    print(f"Чанки сохранены в {output_path}")

if __name__ == "__main__":
    main()