import json
from typing import List


def load_chunks(path: str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def filter_chunks_by_keywords(chunks: List[dict], keywords: List[str], min_len: int = 100) -> List[dict]:
    """
    Возвращает чанки, в которых ТЕКСТ содержит хотя бы одно ключевое слово
    """
    results = []
    for chunk in chunks:
        text = chunk.get("text", "").lower()
        if len(text) < min_len:
            continue
        if any(keyword.lower() in text for keyword in keywords):
            results.append(chunk)
    return results
