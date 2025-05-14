import json
from pathlib import Path

# Пути к файлам
CHUNKS_PATH = Path("data/structured_chunks_tagged_cleaned.json")
NORMALIZED_TAGS_PATH = Path("data/tag_frequencies_normalized.json")
OUTPUT_PATH = Path("data/structured_chunks_retagged.json")

print("Загружаем нормализованные теги...")
with open(NORMALIZED_TAGS_PATH, "r", encoding="utf-8") as f:
    normalized_data = json.load(f)

# Мап: вариант → нормализованный тег
variant_to_normalized = {}
for entry in normalized_data:
    for variant in entry["variants"]:
        variant_to_normalized[variant] = entry["normalized"]

print("Загружаем чанки...")
with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print("Заменяем теги...")
for chunk in chunks:
    original_tags = chunk.get("tags", [])
    new_tags = set()
    for tag in original_tags:
        normalized = variant_to_normalized.get(tag)
        if normalized:
            new_tags.add(normalized)
    chunk["tags"] = sorted(new_tags)

print("Сохраняем результат...")
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print(f"Готово: теги обновлены и сохранены в {OUTPUT_PATH}")