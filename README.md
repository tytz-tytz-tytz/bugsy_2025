# Bugsy 2025

**Bugsy 2025** — экспериментальный проект в рамках учебной практики. Система обрабатывает PDF-документацию, разбивает её на логически связанные фрагменты (чанки), выделяет ключевые понятия, нормализует и расширяет теги, а также предоставляет два типа поиска:

* Семантический поиск (на основе эмбеддингов и FAISS)
* Поиск по тегам с расширением по графу понятий

На основе найденных частей документации собирается итоговый промпт. Части документации могут быть выбраны вручную, полуавтоматически или через автоматический поиск по запросу.

---

## Требования

* Python 3.8+

## Установка

1. Клонируйте репозиторий и создайте виртуальное окружение:

```bash
git clone https://github.com/tytz-tytz-tytz/bugsy_2025
cd bugsy_2025
python -m venv myenv
myenv\Scripts\activate  # на Windows
```

2. Установите зависимости:

```bash
pip install -e .
```

---

## Основной пайплайн обработки

```bash
python retag_main.py
```


Этот скрипт выполняет:
1. Извлечение терминов из текста
2. Фильтрацию частотных терминов
3. Теггирование чанков
4. Нормализацию тегов по словарю
5. Сведение тегов к понятийным ядрам

Результат: [`data/structured_chunks_final_tagged.json`](data/structured_chunks_final_tagged.json)

---

## Поиск по документации

1. Семантический поиск (FAISS + Sentence Transformers):

```bash
python search_semantic.py
```

* Запрос лемматизируется, кодируется моделью, ищутся ближайшие чанки

2. Поиск по тегам и графу понятий:

```bash
python tag_graph_search.py
```

* Запрос лемматизируется и расширяется по [`data/concept_graph.json`](data/concept_graph.json)
* Производится пересечение с тегами чанков

---

## Сборка промптов

В директории [`prompts_with_results/`](prompts_with_results) находятся:

* [`prompts/`](prompts_with_results/prompts) — промпты, собранные вручную
* [`results/`](prompts_with_results/results) — результаты генерации с помощью этих промптов
* [`prompt_builder.py`](prompts_with_results/prompt_builder.py) — полуавтоматический сборщик промптов на основе выбранных чанков

Результаты по генерации документированы в:

* [`results_lists_of_cases.md`](results_lists_of_cases.md)
* [`results_test_cases.md`](results_test_cases.md)

---

## Структура проекта

```bash
bugsy_2025/
├── chunker/                   # Обработка документа и теггирование
│   ├── extract_terms.py
│   ├── filter_tag_chunks.py
│   ├── tag_chunks.py
│   ├── normalize_tags.py
│   ├── retag_chunks.py
│   ├── retag_by_concepts.py
├── semantic/                  # Семантический поиск (FAISS)
│   ├── indexer.py
│   ├── search.py
├── graph_search/              # Поиск по понятийной структуре
│   ├── search_engine.py
│   ├── semantic_expander.py
│   ├── build_graph.py
├── prompts_with_results/      # Примеры промптов и результаты генерации
│   ├── prompts/
│   ├── results/
│   ├── prompt_builder.py
├── data/                      # Входные и выходные файлы
│   ├── marketer.pdf
│   ├── structured_chunks_final_tagged.json
│   ├── concept_graph.json
├── search_semantic.py         # Интерфейс семантического поиска
├── tag_graph_search.py        # Интерфейс графового поиска
├── retag_main.py              # Главный pipeline теггирования
├── results_lists_of_cases.md  # Таблица с результатами по кейсам
├── results_test_cases.md      # Таблица с результатами по тестам
├── pyproject.toml
├── requirements.txt
├── README.md
```
---

## Автор

Александра Решетникова
Учебная практика, СПбГУ, весна 2025