from bs4 import BeautifulSoup
import json
from pathlib import Path

def is_meaningful(el):
    """Оставляем только элементы, содержащие полезный смысл"""
    return (
        el.name in ["input", "textarea", "select", "button"]
        or el.get("aria-label")
        or el.get("placeholder")
        or el.get("role") in ["listbox", "combobox", "tab"]
        or (el.text and not all(c in "" for c in el.text.strip()))
    )

def extract_useful_info(el):
    return {
        "tag": el.name,
        "type": el.get("type"),
        "name": el.get("name"),
        "id": el.get("id"),
        "role": el.get("role"),
        "aria_label": el.get("aria-label"),
        "placeholder": el.get("placeholder"),
        "text": el.get_text(strip=True)[:100]
    }

def extract_compact_dom(html_path: str, output_path: str):
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    all_elements = soup.find_all(["input", "select", "textarea", "button", "a", "label", "div", "span"])

    # Применяем фильтр
    relevant_elements = [extract_useful_info(el) for el in all_elements if is_meaningful(el)]

    dom_json = {
        "elements": relevant_elements
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dom_json, f, indent=2, ensure_ascii=False)

    print(f"Упрощённый DOM сохранён в: {output_path}")
