import json
import numpy as np
import faiss
import re
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import pymorphy2
import inspect
import collections

# --- Monkey-patch для getargspec (для совместимости с Python 3.12) ---
def getargspec(func):
    sig = inspect.signature(func)
    args = [p.name for p in sig.parameters.values()
            if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
    varargs = next((p.name for p in sig.parameters.values()
                    if p.kind == p.VAR_POSITIONAL), None)
    varkw = next((p.name for p in sig.parameters.values()
                  if p.kind == p.VAR_KEYWORD), None)
    defaults = tuple(
        p.default for p in sig.parameters.values()
        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD) and p.default is not p.empty
    ) or None
    return collections.namedtuple('ArgSpec', 'args varargs keywords defaults')(args, varargs, varkw, defaults)

inspect.getargspec = getargspec
# ----------------------------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")
morph = pymorphy2.MorphAnalyzer()


def lemmatize_text(text: str) -> List[str]:
    words = re.findall(r"\w+", text.lower())
    return [morph.parse(w)[0].normal_form for w in words]


def keyword_score(text: str, keywords: List[str]) -> int:
    text_lemmas = set(lemmatize_text(text))
    keyword_lemmas = set(lemmatize_text(" ".join(keywords)))
    return sum(1 for kw in keyword_lemmas if kw in text_lemmas)


def load_data(chunks_path: str, embeddings_path: str, index_path: str):
    chunks = json.load(open(chunks_path, encoding="utf-8"))
    embeddings = np.load(embeddings_path)
    index = faiss.read_index(index_path)
    return chunks, embeddings, index


def search_smart_chunks(query: str, k=10, keywords: List[str] = None) -> List[Dict]:
    """
    Делает semantic search по FAISS, с приоритетом чанков, содержащих ключевые слова.
    Возвращает top-k чанков с полными метаданными.
    """
    chunks_path = "../data/chunks/marketer_chunks_smart.json"
    embeddings_path = "../embeddings/faiss_index/embeddings.npy"
    index_path = "../embeddings/faiss_index/faiss_index.index"

    chunks, embeddings, _ = load_data(chunks_path, embeddings_path, index_path)

    # Шаг 1: фильтрация по keyword_score (по тексту чанков)
    if keywords:
        filtered = [
            (i, ch) for i, ch in enumerate(chunks)
            if keyword_score(ch["text"], keywords) > 0
        ]
    else:
        filtered = list(enumerate(chunks))

    if not filtered:
        print("⚠️ Ничего не найдено по ключевым словам, используем все чанки.")
        filtered = list(enumerate(chunks))

    filtered_ids = [i for i, _ in filtered]
    filtered_chunks = [ch for _, ch in filtered]
    emb_matrix = np.array([embeddings[i] for i in filtered_ids])

    # Шаг 2: семантический поиск
    query_embedding = model.encode([query])
    faiss_index = faiss.IndexFlatL2(emb_matrix.shape[1])
    faiss_index.add(emb_matrix)
    distances, top_i = faiss_index.search(query_embedding, k=50)

    # Шаг 3: комбинированный ранжированный список
    results = []
    for local_idx, distance in zip(top_i[0], distances[0]):
        if local_idx >= len(filtered_chunks):
            continue  # Защита от ошибки
        chunk = filtered_chunks[local_idx]
        score = keyword_score(chunk["text"], keywords or [])
        results.append({
            "chunk": chunk,
            "distance": distance,
            "keyword_score": score
        })

    # Шаг 4: сортировка — приоритет по keyword_score, потом по близости
    results.sort(key=lambda r: (-r["keyword_score"], r["distance"]))

    return [r["chunk"] for r in results[:k]]