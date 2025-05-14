import json
import re
from typing import List, Dict
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLine
from dom.structure import load_dom_graph


def normalize_title(title: str) -> str:
    return re.sub(r"[^а-яА-Яa-zA-Z0-9]+", " ", title.strip().lower())


def extract_text_by_page(pdf_path: str) -> Dict[int, str]:
    pages = {}
    for i, page_layout in enumerate(extract_pages(pdf_path)):
        texts = []
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for line in element:
                    if isinstance(line, LTTextLine):
                        text = line.get_text().strip()
                        if text:
                            texts.append(text)
        pages[i + 1] = "\n".join(texts)
    return pages


def collect_headings_from_toc(graph: Dict) -> List[Dict]:
    return [
        {
            "id": node["id"],
            "title": node["title"],
            "level": node["level"],
            "page": node["page"]
        }
        for node in graph["nodes"]
        if isinstance(node, dict) and node.get("title") and node.get("level") >= 0
    ]


def build_chunks_with_toc_analysis(pdf_path: str, graph_path: str, output_path: str) -> List[Dict]:
    graph = load_dom_graph(graph_path)
    all_text = extract_text_by_page(pdf_path)
    headings = collect_headings_from_toc(graph)
    chunks = []

    # Order headings as in TOC using their IDs
    id_order = [node["id"] for node in graph["nodes"] if isinstance(node, dict)]
    sorted_headings = sorted(headings, key=lambda h: id_order.index(h["id"]))
    all_text_str = {p: all_text.get(p, '') for p in range(1, max(all_text.keys()) + 1)}

    for i, heading in enumerate(sorted_headings):
        current_page = heading["page"]
        start_title = heading["title"]
        start_id = heading["id"]
        level = heading["level"]

        next_heading = None
        for j in range(i + 1, len(sorted_headings)):
            if sorted_headings[j]["level"] <= level:
                next_heading = sorted_headings[j]
                break

        page_range = range(current_page, (next_heading["page"] if next_heading else max(all_text.keys()) + 1) + 1)
        text_range = "\n".join(all_text_str.get(p, '') for p in page_range)

        start_match = re.search(re.escape(start_title), text_range)
        start_idx = start_match.start() if start_match else 0

        end_idx = len(text_range)
        if next_heading:
            next_match = re.search(re.escape(next_heading["title"]), text_range[start_idx + len(start_title):])
            if next_match:
                end_idx = start_idx + len(start_title) + next_match.start()

        content = text_range[start_idx:end_idx].strip()

        page_end = current_page
        for p in reversed(page_range):
            if all_text_str.get(p) and all_text_str[p] in content:
                page_end = p
                break

        chunks.append({
            "section_id": start_id,
            "section_title": start_title,
            "level": level,
            "page_start": current_page,
            "page_end": page_end,
            "text": content
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    return chunks
