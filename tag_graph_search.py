import json
from pathlib import Path
from datetime import datetime
import sys

from graph_search.search_engine import normalize_query_to_stems, find_relevant_chunks
from graph_search.semantic_expander import expand_tags

OUTPUT_DIR = Path("search_results_graph")
OUTPUT_DIR.mkdir(exist_ok=True)

def save_results(query: str, tags: list[str], expanded_tags: list[str], chunks: list[dict]) -> None:
    OUTPUT_DIR = Path("search_results_graph")
    OUTPUT_DIR.mkdir(exist_ok=True)

    existing = sorted(OUTPUT_DIR.glob("results_*.json"))
    next_number = len(existing) + 1
    output_path = OUTPUT_DIR / f"results_{next_number:03}.json"

    result = {
        "query": query,
        "stemmed_tags": tags,
        "expanded_tags": expanded_tags,
        "results": chunks
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\nРезультаты сохранены в: {output_path}")

if __name__ == "__main__":
    query = input("Введите запрос: ").strip()

    # 1. Получаем стеммы из запроса
    tags = normalize_query_to_stems(query)

    # 2. Расширяем теги по графу понятий
    expanded_tags = expand_tags(tags, depth=1)

    print(f"\n→ Стеммы запроса: {tags}")
    print(f"→ Расширенные теги: {expanded_tags}")

    # 3. Ищем релевантные чанки
    chunks = find_relevant_chunks(expanded_tags, top_n=5)

    print(f"\nНайдено фрагментов: {len(chunks)}\n")
    for ch in chunks:
        print(f"[{ch['section_id']}] {ch.get('section_title', '')}")
        print(ch["text"][:500].strip().replace("\n", " ") + "...\n---\n")

    # 4. Сохраняем результат
    save_results(query, tags, expanded_tags, chunks)