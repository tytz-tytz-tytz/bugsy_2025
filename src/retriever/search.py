import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json
from pathlib import Path

# Загружаем модель для эмбеддингов
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_embeddings(file_path="embeddings/faiss_index/embeddings.npy"):
    """Загружает эмбеддинги из numpy файла"""
    return np.load(file_path)

def load_faiss_index(file_path="embeddings/faiss_index/faiss_index.index"):
    """Загружает FAISS индекс"""
    return faiss.read_index(file_path)

def search_faiss(query: str, index: faiss.Index, chunks: list, k: int = 5):
    """Ищет по FAISS индексу"""
    query_embedding = model.encode([query])
    D, I = index.search(query_embedding, k)
    
    results = [chunks[i] for i in I[0]]
    return results

def display_results(results):
    """Печатает результаты поиска"""
    for result in results:
        print(f"Page: {result['page']}, Section: {result['section']}, Text: {result['text']}")

def perform_search(query, k=5):
    """Выполняет поиск по запросу"""
    chunks_path = "data/chunks/marketer_chunks.json"
    embeddings_path = "embeddings/faiss_index/embeddings.npy"
    index_path = "embeddings/faiss_index/faiss_index.index"

    chunks = json.load(open(chunks_path, "r", encoding="utf-8"))
    embeddings = load_embeddings(embeddings_path)
    index = load_faiss_index(index_path)

    results = search_faiss(query, index, chunks, k)
    display_results(results)

def search_similar_chunks(query: str, k: int = 3) -> list:
    chunks_path = "../data/chunks/marketer_chunks.json"
    embeddings_path = "../embeddings/faiss_index/embeddings.npy"
    index_path = "../embeddings/faiss_index/faiss_index.index"

    chunks = json.load(open(chunks_path, "r", encoding="utf-8"))
    embeddings = load_embeddings(embeddings_path)
    index = load_faiss_index(index_path)

    results = search_faiss(query, index, chunks, k)
    return [r["text"] for r in results]
