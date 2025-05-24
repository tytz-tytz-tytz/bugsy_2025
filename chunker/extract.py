from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLine
from typing import List, Dict
import re

def extract_toc_layout_fixed(pdf_path: str, max_pages: int = 5) -> List[Dict]:
    """
    Извлекает оглавление из PDF, корректно объединяя строки, если они относятся к одному заголовку.
    """
    toc_entries = []
    page_counter = 0

    for page_layout in extract_pages(pdf_path):
        if page_counter >= max_pages:
            break
        page_counter += 1

        lines = []
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for line in element:
                    if isinstance(line, LTTextLine):
                        text = line.get_text().strip()
                        if text and text.lower() != "содержание":
                            x0 = round(line.x0)
                            lines.append((x0, text))

        i = 0
        while i < len(lines):
            x0, line_text = lines[i]
            full_text = line_text
            page_number = None

            # Проверяем: есть ли номер страницы в этой строке?
            match = re.match(r"^(.*?)(?:\.{2,}|[\s\-–—]+)(\d{1,3})$", line_text)
            if match:
                raw_title = match.group(1).strip()
                page_number = int(match.group(2).strip())
                full_text = raw_title
                i += 1

            else:
                # Пытаемся склеить с следующей строкой, если та содержит номер страницы
                if i + 1 < len(lines):
                    next_x0, next_text = lines[i + 1]
                    if next_x0 == x0:
                        combined = f"{line_text} {next_text}"
                        match = re.match(r"^(.*?)(?:\.{2,}|[\s\-–—]+)(\d{1,3})$", combined)
                        if match:
                            raw_title = match.group(1).strip()
                            page_number = int(match.group(2).strip())
                            full_text = raw_title
                            i += 2
                            toc_entries.append({
                                "title": re.sub(r'\.{2,}', '', full_text).strip(),
                                "page": page_number,
                                "x0": x0
                            })
                            continue
                i += 1
                continue  # если не удалось склеить — пропускаем

            toc_entries.append({
                "title": re.sub(r'\.{2,}', '', full_text).strip(),
                "page": page_number,
                "x0": x0
            })

    # Преобразуем x0 в уровни вложенности
    unique_x = sorted(set(entry["x0"] for entry in toc_entries))
    x_to_level = {x: i for i, x in enumerate(unique_x)}

    for entry in toc_entries:
        entry["level"] = x_to_level[entry["x0"]]

    return [
        {"title": e["title"], "page": e["page"], "level": e["level"]}
        for e in toc_entries
    ]