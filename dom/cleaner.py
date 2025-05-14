from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLineHorizontal
from typing import List
import re

def extract_clean_page_texts(pdf_path: str) -> List[str]:
    """
    Чисто извлекает текст из PDF постранично:
    - удаляет номера страниц (например, '12')
    - удаляет строки с 'страница ...'
    - оставляет рисунки, заголовки, основной текст
    """
    pages = []
    for page_layout in extract_pages(pdf_path):
        lines = []
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for line in element:
                    if isinstance(line, LTTextLineHorizontal):
                        text = line.get_text().strip()

                        # Удаляем одиночные номера страниц
                        if re.fullmatch(r"\d{1,3}", text):
                            continue

                        # Удаляем строки вроде "Страница 5 из 98"
                        if "страница" in text.lower():
                            continue

                        # Пропускаем пустое
                        if not text:
                            continue

                        lines.append(text)

        page_text = "\n".join(lines)
        pages.append(page_text.strip())

    return pages
