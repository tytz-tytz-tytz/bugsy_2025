import fitz  # PyMuPDF
import re
import json
from pathlib import Path

def extract_chunks_with_meta(pdf_path: str, output_path: str, min_chars: int = 200, start_page: int = 6):
    """
    Разбивает PDF на логические чанки по заголовкам, начиная с нужной страницы.
    
    Args:
        pdf_path (str): путь к PDF-документу
        output_path (str): путь для сохранения JSON-результата
        min_chars (int): минимальное количество символов в чанке (отсеивает мусор)
        start_page (int): номер страницы, с которой начинать (1-индексация)
    """
    doc = fitz.open(pdf_path)
    chunks = []

    current_section = None

    for i in range(start_page - 1, len(doc)):
        page = doc[i]
        text = page.get_text()
        lines = text.split("\n")

        buffer = []
        for line in lines:
            line = line.strip()

            # Определяем заголовки по шаблону: "1.2 Условия" или "ШАГ 3: ..."
            if re.match(r"^\d{1,2}(\.\d{1,2})?\s+.+", line) or line.isupper():
                # Сохраняем предыдущий буфер перед новым заголовком
                if buffer:
                    chunk_text = " ".join(buffer).strip()
                    if len(chunk_text) >= min_chars:
                        chunks.append({
                            "text": chunk_text,
                            "meta": {
                                "page": i + 1,
                                "section": current_section
                            }
                        })
                    buffer = []
                current_section = line
                continue

            # Добавляем текст в текущий чанк
            if line:
                buffer.append(line)

        # Сохраняем остаток со страницы
        if buffer:
            chunk_text = " ".join(buffer).strip()
            if len(chunk_text) >= min_chars:
                chunks.append({
                    "text": chunk_text,
                    "meta": {
                        "page": i + 1,
                        "section": current_section
                    }
                })

    # Сохраняем результат
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Сохранено {len(chunks)} чанков в {output_path}")