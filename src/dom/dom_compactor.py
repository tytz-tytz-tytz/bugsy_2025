# src/dom/dom_compactor.py

import json
from pathlib import Path
from collections import defaultdict

def clean_text(text: str):
    """Очищает текст от мусора и символов-иконок"""
    if not text:
        return None
    text = text.strip().replace("\n", " ")
    if all(c in "" for c in text.strip()):
        return None
    if len(text.strip()) < 2:
        return None
    return text.strip()

def compact_and_group_dom(input_path: str, output_path: str):
    """Группирует DOM по смысловым категориям"""
    with open(input_path, encoding="utf-8") as f:
        dom = json.load(f)

    elements = dom.get("elements", [])
    grouped = defaultdict(list)

    for el in elements:
        tag = el.get("tag")
        text = clean_text(el.get("aria_label") or el.get("placeholder") or el.get("text"))
        role = el.get("role")

        if not text:
            continue

        t_lower = text.lower()

        # Группировка по смыслу
        if any(w in t_lower for w in ["email", "аудитория", "файл", "тег"]):
            grouped["targeting_fields"].append(text)

        elif "ограничивать время" in t_lower or "времени" in t_lower or "дней" in t_lower:
            grouped["scheduling_options"].append(text)

        elif "рассылк" in t_lower or "отправлять" in t_lower or "сообщени" in t_lower:
            grouped["delivery_settings"].append(text)

        elif tag == "button" or "сохранить" in t_lower or "запустить" in t_lower:
            grouped["action_buttons"].append(text)

        else:
            grouped["other_ui_elements"].append(text)

    # Удаляем дубли, сортируем
    final_dom = {k: sorted(set(v)) for k, v in grouped.items()}

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_dom, f, indent=2, ensure_ascii=False)

    print(f"DOM сохранён в {output_path}")
