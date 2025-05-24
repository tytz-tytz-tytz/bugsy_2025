import json
import re
from collections import Counter
from pathlib import Path
import nltk
from nltk.corpus import stopwords

def extract_terms_main():
    # Убедись, что стоп-слова загружены
    nltk.download('stopwords')
    stop_words = set(stopwords.words("russian"))

    CHUNKS_PATH = Path("data/structured_chunks.json")
    OUTPUT_PATH = Path("data/candidate_terms.json")

    # Загрузка всех чанков
    print("Загружаем все чанки...")
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Всего чанков: {len(chunks)}")

    # Убираем переносы
    all_texts = [chunk.get("text", "").replace("\n", " ").replace("\r", " ") for chunk in chunks]

    # Сбор слов и биграмм
    all_words = []
    all_bigrams = []

    for text in all_texts:
        words = re.findall(r'\w+', text.lower())
        # Удаляем стоп-слова и короткие слова
        words = [w for w in words if w not in stop_words and len(w) > 2]
        all_words.extend(words)
        all_bigrams.extend([" ".join(pair) for pair in zip(words[:-1], words[1:])])

    # Подсчёт частот
    counts = Counter(all_words + all_bigrams)

    # Отладка: топ 20 терминов
    print("\nТоп 20 терминов:")
    for term, count in counts.most_common(20):
        print(f"{term} — {count}")

    # Фильтрация: биграммы и триграммы без стоп-слов
    filtered = []
    for term, count in counts.items():
        words = term.split()
        if 2 <= len(words) <= 4 and not any(w in stop_words for w in words):
            filtered.append({"term": term, "count": count})

    # Сохраняем результат
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

    print(f"\nСохранили {len(filtered)} терминов в {OUTPUT_PATH}")
    print("Готово")