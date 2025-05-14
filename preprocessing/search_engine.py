import json
import re
from pathlib import Path
from typing import List, Dict
import snowballstemmer

CHUNKS_PATH = Path("data/structured_chunks_final_tagged.json")

stemmer = snowballstemmer.stemmer("russian")

def normalize_query_to_stems(query: str) -> List[str]:
    words = re.findall(r'\w+', query.lower())
    stems = list(set(stemmer.stemWords(words)))
    print(f"\n[DEBUG] Стеммы из запроса: {stems}")
    return stems

def find_relevant_chunks(stems: List[str], top_n: int = 5) -> List[Dict]:
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    scored = []
    for chunk in chunks:
        tags = chunk.get("tags", [])
        overlap = set(tags) & set(stems)
        if overlap:
            scored.append((len(overlap), overlap, chunk))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [ch for _, _, ch in scored[:top_n]]
