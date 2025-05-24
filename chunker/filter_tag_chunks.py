import json
import re
from collections import Counter
from pathlib import Path
import nltk
from nltk.corpus import stopwords

def filter_terms_main():
    # Убедиться, что стоп-слова есть
    nltk.download('stopwords')
    stop_words = set(stopwords.words("russian"))


    CHUNKS_PATH = Path("data/structured_chunks.json")
    OUTPUT_PATH = Path("data/candidate_terms_cleaned.json")

    # Мусорные фразы, которые часто встречаются в документации
    noise_keywords = {
        "рисунок", "см", "вкладка", "раздел", "страница", "пример", "таблица", "иконка", "рисунке", "нажатие", "нажать"
    }
    print("Загружаем все чанки...")
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Всего чанков: {len(chunks)}")

    # Обработка текста
    all_texts = [chunk.get("text", "").replace("\n", " ").replace("\r", " ") for chunk in chunks]
    all_words = []
    all_bigrams = []

    for text in all_texts:
        words = re.findall(r'\w+', text.lower())
        words = [w for w in words if w not in stop_words and len(w) > 2]
        all_words.extend(words)
        all_bigrams.extend([" ".join(pair) for pair in zip(words[:-1], words[1:])])

    # Объединённый счёт
    counts = Counter(all_words + all_bigrams)

    print("\nТоп 20 терминов до фильтрации:")
    for term, count in counts.most_common(20):
        print(f"{term} — {count}")

    # Фильтрация:
    # - частота >= 3
    # - 2–4 слова
    # - без мусорных ключей
    # - без стоп-слов
    output = []
    for term, count in counts.items():
        words = term.split()
        if count < 3:
            continue
        if not (2 <= len(words) <= 4):
            continue
        if any(w in stop_words for w in words):
            continue
        if any(n in term for n in noise_keywords):
            continue
        output.append({"term": term, "count": count})

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nСохранили {len(output)} очищенных терминов в {OUTPUT_PATH}")
    print("Готово")