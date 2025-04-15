import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import json
from pathlib import Path

# Загрузка модели для эмбеддингов
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(chunks_path: str):
    """Загружает фрагменты и генерирует эмбеддинги"""
    with open(chunks_path, 'r', encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [chunk['text'] for chunk in chunks]
    embeddings = model.encode(texts, convert_to_tensor=True)

    return embeddings, chunks

def save_embeddings(embeddings, file_path="embeddings/faiss_index/embeddings.npy"):
    """Сохраняет эмбеддинги в numpy файл"""
    np.save(file_path, embeddings)

def create_faiss_index(embeddings):
    """Создаёт FAISS индекс и сохраняет его"""
    embeddings = embeddings.cpu().detach().numpy()
    d = embeddings.shape[1]  # Размерность эмбеддинга
    index = faiss.IndexFlatL2(d)  # Индекс с использованием L2 расстояния
    index.add(embeddings)
    return index

def save_faiss_index(index, file_path="embeddings/faiss_index/faiss_index.index"):
    """Сохраняет FAISS индекс"""
    faiss.write_index(index, file_path)

# Основная логика
def process_pdf_and_create_index(pdf_path="data/chunks/marketer_chunks.json"):
    embeddings, chunks = create_embeddings(pdf_path)
    save_embeddings(embeddings)
    index = create_faiss_index(embeddings)
    save_faiss_index(index)

    print(f"Индекс FAISS и эмбеддинги успешно сохранены!")

if __name__ == "__main__":
    process_pdf_and_create_index()
