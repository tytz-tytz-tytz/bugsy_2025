import json
from typing import List


def load_json(path: str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_prompt(
    context_chunks: List[str],
    dom_path: str,
    scenario: str,
    use_equivalence_classes: bool = True,
    include_test_types: bool = True,
) -> str:
    # Загрузка DOM JSON
    dom = load_json(dom_path)

    # Начало промпта
    prompt = "Ты — инженер по тестированию пользовательских интерфейсов.\n\n"

    # 1. Документация
    prompt += "Вот релевантные фрагменты пользовательской документации:\n"
    for i, chunk in enumerate(context_chunks):
        prompt += f"\nФрагмент {i+1}:\n{chunk.strip()}\n"

    # 2. DOM
    prompt += "\nВот структура интерфейса (DOM):\n"
    prompt += json.dumps(dom, indent=2, ensure_ascii=False)

    # 3. Сценарий
    prompt += f"\n\nСценарий:\n{scenario.strip()}\n"

    # 4. Инструкция
    prompt += "\nСгенерируй тест-кейсы по сценарию с учётом документации и DOM."

    if use_equivalence_classes:
        prompt += "\nОбязательно используй классы эквивалентности."

    if include_test_types:
        prompt += "\nДобавь позитивные, негативные и граничные тесты."

    prompt += "\n\nДля каждого теста укажи:\n1. Название теста\n2. Предусловия\n3. Действия\n4. Ожидаемый результат\n"

    return prompt
