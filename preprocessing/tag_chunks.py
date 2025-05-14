import json
from pathlib import Path

CHUNKS_PATH = Path("data/structured_chunks.json")
TERMS_PATH = Path("data/candidate_terms_cleaned.json")
OUTPUT_PATH = Path("data/structured_chunks_tagged_cleaned.json")

print("Загружаем термины...")
with open(TERMS_PATH, "r", encoding="utf-8") as f:
    terms_data = json.load(f)
terms = [entry["term"].lower() for entry in terms_data]

print(f"Загружено {len(terms)} терминов.")

print("Загружаем чанки...")
with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Загружено {len(chunks)} чанков.")

print("Присваиваем теги чанкам...")
for chunk in chunks:
    text = chunk.get("text", "").replace("\n", " ").lower()
    tags = [term for term in terms if term in text]
    chunk["tags"] = tags

print("Сохраняем размеченные чанки...")
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print(f"Сохранили размеченные чанки в {OUTPUT_PATH}")
print("Готово")