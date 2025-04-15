from src.parser.pdf_splitter import split_pdf_to_chunks

if __name__ == "__main__":
    split_pdf_to_chunks(
        pdf_path="data/docs/marketer.pdf",
        output_json_path="data/chunks/marketer_chunks.json"
    )
