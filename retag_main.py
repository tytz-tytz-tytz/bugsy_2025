from chunker.extract_terms import extract_terms_main
from chunker.filter_tag_chunks import filter_terms_main
from chunker.tag_chunks import tag_chunks_main
from chunker.normalize_tags import normalize_tags_main
from chunker.retag_chunks import retag_chunks_main
from chunker.retag_by_concepts import retag_by_concepts_main

def main():
    print("Шаг 1: извлечение терминов из чанков")
    extract_terms_main()

    print("Шаг 2: фильтрация терминов")
    filter_terms_main()

    print("Шаг 3: теггирование чанков")
    tag_chunks_main()

    print("Шаг 4: нормализация тегов")
    normalize_tags_main()

    print("Шаг 5: замена тегов на нормализованные")
    retag_chunks_main()

    print("Шаг 6: сведение тегов к базовым понятиям (ядру)")
    retag_by_concepts_main()

    print("\nФинальный файл сохранён: data/structured_chunks_final_tagged.json")

if __name__ == "__main__":
    main()