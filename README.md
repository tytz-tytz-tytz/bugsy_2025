Поиск нужных фрагментов документации по пользовательскому запросу.

## Что сделано

### Разметка документации
- Документация разбита на осмысленные фрагменты (чанки):  
  [`data/structured_chunks_final_tagged.json`](data/structured_chunks_final_tagged.json)
- К каждому чанку прикреплены теги — нормализованные термины, извлечённые автоматически.

### Выделение терминов
- Автоматически извлечены многословные термины (N-граммы);
- Очищены, нормализованы, посчитана частота:  
  [`data/tag_frequencies_normalized.json`](data/tag_frequencies_normalized.json)

### Граф понятий
- Построен граф по тегам: узлы — термины, рёбра — совместные появления в одном чанке;
- JSON-граф: [`data/concept_graph.json`](data/concept_graph.json)
- Визуализация: [`data/concept_graph.html`](data/concept_graph.html)

### Граф структуры документа
- Отдельный граф, описывающий структуру всей документации:  
  [`dom_graph.html`](dom_graph.html)
  [`dom_structure.json`](dom_structure.json)

## Поисковый прототип

Скрипт [`scripts/search_chunks.py`](scripts/search_chunks.py):

- Принимает текстовый запрос;
- Делает стемминг слов;
- Расширяет начальные термины через граф понятий;
- Ищет подходящие чанки по тегам;
- Сохраняет результат в [`search_results/`](search_results/)
