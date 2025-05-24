from semantic.search import semantic_search
from pathlib import Path
import json

def save_semantic_results(query: str, results: list[dict]):
    output_dir = Path("search_results_semantic")
    output_dir.mkdir(exist_ok=True)

    existing = sorted(output_dir.glob("results_*.json"))
    next_number = len(existing) + 1
    output_path = output_dir / f"results_{next_number:03}.json"

    output = {
        "query": query,
        "results": results
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nРезультаты сохранены в: {output_path}")

def main():
    query = input("Введите запрос для поиска по документации:\n> ")
    results = semantic_search(query, top_k=5)

    print("\nТоп релевантных чанков:\n")
    for i, chunk in enumerate(results, 1):
        print(f"--- [{i}] {chunk['section_title']} (стр. {chunk['page_start']}) ---")
        print(chunk['text'][:500] + "\n...")

    save_semantic_results(query, results)

if __name__ == "__main__":
    main()