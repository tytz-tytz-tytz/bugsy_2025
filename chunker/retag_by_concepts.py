import json
from pathlib import Path

def retag_by_concepts_main():

    # Пути
    CHUNKS_PATH = Path("data/structured_chunks_retagged.json")
    TAGMAP_PATH = Path("data/tag_frequencies_normalized.json")  # если нужно брать оттуда
    OUTPUT_PATH = Path("data/structured_chunks_final_tagged.json")

    # Базовые понятия
    core_concepts = [
        "событ", "макрос", "аргумент", "рассылк", "валидац", "ограничен", "ошибк",
        "интерфейс", "пользователь", "тест", "сценари", "блок", "тип", "состояни",
        "мессенджер", "аудитори", "идентификатор", "тег", "диалог", "настройк", "редактирован"
    ]

    # Загружаем чанки
    print("Загружаем размеченные чанки...")
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # Обновляем теги: заменяем на core_concepts
    for chunk in chunks:
        concept_tags = set()
        for tag in chunk.get("tags", []):
            matched = next((core for core in core_concepts if core in tag), None)
            if matched:
                concept_tags.add(matched)
        chunk["tags"] = sorted(concept_tags)

    # Сохраняем
    print("Сохраняем результат...")
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Готово: теги заменены на базовые понятия → {OUTPUT_PATH}")