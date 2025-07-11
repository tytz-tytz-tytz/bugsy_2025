from typing import List
import os
from datetime import datetime


def build_prompt(
    context_chunks: List[str],
    scenario: str,
    use_equivalence_classes: bool = True,
    include_test_types: bool = True,
    include_example: bool = True,
) -> str:
    """
    Собирает полный текст промпта на основе переданных фрагментов документации и описания задачи.
    """

    prompt = "Ты — инженер по тестированию пользовательских интерфейсов.\n"
    prompt += f"\nТвоя задача:\n{scenario.strip()}\n"

    prompt += """\nЦель тестирования: 
Проверить frontend-логику интерфейса, включая:
- отображение данных;
- реакцию на действия пользователя (клики, ввод, переключения);
- валидацию форм;
- поведение при ошибках (некорректные данные, проблемы с сервером);
- взаимодействие с backend (отправка и получение данных);
- сохранение и восстановление состояния компонентов.\n\n"""

    prompt += """Что протестировать: 
Сконцентрируйся на элементах управления, связанных с задачей:
- выпадающие списки;
- чекбоксы;
- поля ввода;
- переключатели;
- логика зависимости между ними.\n\n"""

    if include_test_types:
        prompt += """Требования к тест-кейсам:
- Сгенерируй ровно 20 тест-кейсов — не меньше;
- Используй разнообразные элементы интерфейса, классы эквивалентности, позитивные, негативные и граничные случаи;
- Не включай тесты, связанные с визуальной стилизацией, адаптивностью, кроссбраузерностью и мультиязычностью;
- Включи тесты с граничными значениями, множественным выбором, конфликтами, валидацией, удалением блоков после связывания, отменой настроек, некорректными параметрами и пустыми полями.\n"""

    prompt += """\nФормат описания теста:
1. Тест №: Название теста
2. Предусловия
3. Действия
4. Ожидаемый результат\n"""

    if include_example:
        prompt += """\nПример:
Тест №1: Проверка ошибки при отсутствии обязательного параметра

Предусловия:
1. Интерфейс открыт, пользователь авторизован

Действия:
1. Добавить в рассылку блок с сообщением и weburl-кнопкой, url которой состоит из пробелов
2. Убедиться, что блок участвует в сценарии
3. Запустить рассылку

Ожидаемый результат:
Появляется сообщение об ошибке, запуск невозможен.\n"""

    prompt += "\nО продукте:\nMarketer — интерфейс Maxbot для настройки и запуска клиентских рассылок через мессенджеры и SMS. Интерфейс включает инструменты автоматизации (например, генерация событий, фильтрация по аудитории, настройка сценариев).\n"

    prompt += "\nКонтекст:\nНиже приведены фрагменты документации, описывающие поведение интерфейса. Используй их при генерации тестовых сценариев:\n"

    for i, chunk in enumerate(context_chunks, 1):
        short_title = f"Фрагмент {i}"
        prompt += f"\n{short_title}:\n{chunk.strip()}\n"

    return prompt


def save_prompt_to_file(
    prompt: str,
    scenario_name: str,
    folder: str = "prompts_with_results/prompts"
) -> str:
    """
    Сохраняет промпт в указанный каталог с автоинкрементом имени.
    Возвращает путь к сохраненному файлу.
    """
    import re

    os.makedirs(folder, exist_ok=True)

    # Приводим имя сценария к удобному формату
    base_name = scenario_name.replace(" ", "_").lower()

    # Найдём все существующие файлы с этим именем
    existing_files = [f for f in os.listdir(folder) if f.startswith(base_name) and f.endswith(".txt")]

    # Извлекаем номера, если есть
    numbers = []
    for fname in existing_files:
        match = re.search(rf"{re.escape(base_name)}_(\d+)\.txt", fname)
        if match:
            numbers.append(int(match.group(1)))

    next_num = max(numbers) + 1 if numbers else 1
    filename = f"{base_name}_{next_num}.txt"
    path = os.path.join(folder, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(prompt)

    return path