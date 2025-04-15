import fitz  # PyMuPDF
import re
import json
from uuid import uuid4
from pathlib import Path
from typing import List, Dict

# 1. Извлечение структуры оглавления #
def extract_toc_structure(pdf_path: str, toc_start: int = 1, toc_end: int = 5) -> List[Dict]:
    doc = fitz.open(pdf_path)
    headings = []

    def determine_level(x0):
        if x0 <= 58:
            return 1
        elif x0 <= 72:
            return 2
        else:
            return 3

    for page_num in range(toc_start, toc_end):
        page = doc[page_num]
        blocks = page.get_text("blocks")

        for b in blocks:
            x0, y0, x1, y1, text, *_ = b
            text = text.strip()

            if re.search(r'\.{3,}\s*\d+$', text):
                title = re.sub(r'\.{3,}\s*\d+$', '', text).strip()
                page_ref_match = re.findall(r'\d+$', text)
                if not page_ref_match:
                    continue
                page_ref = int(page_ref_match[-1])
                level = determine_level(x0)

                headings.append({
                    "title": title,
                    "level": level,
                    "page_ref": page_ref
                })

    return headings

# 2. Привязка страницы к разделу из оглавления #
def match_section(page_num: int, toc: List[Dict]) -> Dict:
    section = subsection = subsubsection = None

    for h in toc:
        if h["page_ref"] > page_num:
            break
        if h["level"] == 1:
            section = h["title"]
            subsection = None
            subsubsection = None
        elif h["level"] == 2:
            subsection = h["title"]
            subsubsection = None
        elif h["level"] == 3:
            subsubsection = h["title"]

    return {
        "section": section,
        "subsection": subsection,
        "subsubsection": subsubsection
    }

# 3. Основная функция: разметка и сохранение #
def split_pdf_to_chunks(pdf_path: str, output_json_path: str):
    doc = fitz.open(pdf_path)
    toc = extract_toc_structure(pdf_path)
    chunks = []

    START_FROM_PAGE = 6  # Стартуем с 6 страницы (1-based)

    for page_num, page in enumerate(doc):
        if page_num + 1 < START_FROM_PAGE:
            continue  # пропускаем оглавление

        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: (b[1], b[0]))  # сортировка по координатам

        # Привязка к структуре из оглавления
        position = match_section(page_num + 1, toc)

        for b in blocks:
            text = b[4].strip()
            if not text or len(text) < 20:
                continue

            chunk = {
                "chunk_id": str(uuid4()),
                "page": page_num + 1,
                "section": position["section"],
                "subsection": position["subsection"],
                "subsubsection": position["subsubsection"],
                "text": text
            }
            chunks.append(chunk)

    # Сохраняем результат
    Path(output_json_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Сохранено {len(chunks)} фрагментов в {output_json_path}")