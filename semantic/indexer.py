import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def build_faiss_index(chunk_file="data/structured_chunks.json", model_name='all-MiniLM-L6-v2',
                      index_path="data/faiss_index.index", embeddings_path="data/embeddings.npy"):
    print("Загружаем чанки...")
    with open(chunk_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [chunk["text"] for chunk in chunks]

    print("Строим эмбеддинги с помощью SentenceTransformer...")
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    print(f"Сохраняем эмбеддинги в {embeddings_path}")
    np.save(embeddings_path, embeddings)

    print(f"Строим FAISS-индекс (dim={embeddings.shape[1]})...")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, index_path)
    print(f"Индекс сохранён в {index_path}")