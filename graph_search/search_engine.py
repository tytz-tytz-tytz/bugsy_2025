import json
import re
from pathlib import Path
from typing import List, Dict, Set
import snowballstemmer
from graph_search.semantic_expander import expand_tags

CHUNKS_PATH = Path("data/structured_chunks_final_tagged.json")
stemmer = snowballstemmer.stemmer("russian")


def normalize_query_to_stems(query: str) -> List[str]:
    words = re.findall(r'\w+', query.lower())
    stems = list(set(stemmer.stemWords(words)))
    print(f"Стеммы из запроса: {stems}")
    return stems


def find_graph_chunks(tags: Set[str], min_overlap: int = 1, sort: bool = True) -> List[Dict]:
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    matching = []
    for chunk in chunks:
        chunk_tags = set(chunk.get("tags", []))
        overlap = chunk_tags & tags
        if len(overlap) >= min_overlap:
            chunk["matched_tags"] = list(overlap)
            chunk["overlap_score"] = len(overlap)
            matching.append(chunk)

    if sort:
        matching.sort(key=lambda ch: ch["overlap_score"], reverse=True)

    return matching


def find_graph_chunks(tags: Set[str], sort: bool = True) -> List[Dict]:
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    matching = []
    for chunk in chunks:
        chunk_tags = set(chunk.get("tags", []))
        overlap = chunk_tags & tags
        overlap_count = len(overlap)
        total_tags = len(chunk_tags)

        # Правило: совпадений должно быть либо >= 3, либо совпасть всё, если тегов ≤ 3
        if (total_tags <= 3 and overlap_count == total_tags) or (total_tags > 3 and overlap_count >= 3):
            chunk["matched_tags"] = list(overlap)
            chunk["overlap_score"] = overlap_count
            matching.append(chunk)

    if sort:
        matching.sort(key=lambda ch: ch["overlap_score"], reverse=True)

    return matching

