import json
import re
from pathlib import Path
from collections import Counter
import snowballstemmer

def normalize_tags_main():
    # Пути к файлам
    INPUT_PATH = Path("data/structured_chunks_tagged_cleaned.json")
    OUTPUT_PATH = Path("data/tag_frequencies_normalized.json")

    # Инициализация стеммера
    stemmer = snowballstemmer.stemmer("russian")

    def normalize_term(term):
        words = re.findall(r'\w+', term.lower())
        stems = stemmer.stemWords(words)
        return " ".join(stems)

    # Загрузка чанков
    print("Загружаем размеченные чанки...")
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # Нормализация тегов
    tag_counter = Counter()
    tag_variants = {}

    for chunk in chunks:
        for tag in chunk.get("tags", []):
            norm = normalize_term(tag)
            tag_counter[norm] += 1
            tag_variants.setdefault(norm, set()).add(tag)

    # Подготовка вывода
    output = [
        {
            "normalized": norm,
            "count": tag_counter[norm],
            "variants": sorted(tag_variants[norm])
        }
        for norm in sorted(tag_counter, key=tag_counter.get, reverse=True)
        if len(norm.split()) > 1  # убираем однословные обрывки
    ]

    # Сохраняем
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Сохранили {len(output)} нормализованных тегов в {OUTPUT_PATH}")