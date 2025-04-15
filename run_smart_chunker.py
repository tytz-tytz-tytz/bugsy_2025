from src.parser.smart_chunker import extract_chunks_with_meta

extract_chunks_with_meta(
    pdf_path="data/docs/marketer.pdf",
    output_path="data/chunks/marketer_chunks_smart.json",
    min_chars=100  # можно уменьшить до 100, если хочется мельче
)
