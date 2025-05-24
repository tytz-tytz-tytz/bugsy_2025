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

# Загружаем модель и морфоанализатор один раз
model = SentenceTransformer("all-MiniLM-L6-v2")
morph = pymorphy2.MorphAnalyzer()


def lemmatize_text(text: str) -> List[str]:
    words = re.findall(r"\w+", text.lower())
    return [morph.parse(w)[0].normal_form for w in words]


def keyword_score(text: str, keywords: List[str]) -> int:
    text_lemmas = set(lemmatize_text(text))
    keyword_lemmas = set(keywords)
    return sum(1 for kw in keyword_lemmas if kw in text_lemmas)


def semantic_search(query: str, top_k: int = 5,
                    index_path: str = "data/faiss_index.index",
                    chunk_path: str = "data/structured_chunks.json",
                    keywords: List[str] = None) -> List[Dict]:
    index = faiss.read_index(index_path)

    with open(chunk_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    query_vector = model.encode([query])
    D, I = index.search(np.array(query_vector), top_k * 2)

    if keywords is None:
        keywords = lemmatize_text(query)

    results = []
    for idx in I[0]:
        chunk = chunks[idx]
        score = keyword_score(chunk["text"], keywords)
        if score > 0:
            results.append((score, chunk))

    results.sort(reverse=True, key=lambda x: x[0])
    return [c for _, c in results[:top_k]]