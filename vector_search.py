import faiss
import numpy as np
import pandas as pd
from openai import OpenAI
import json
from models_llm import *

# --- Inicializar modelo de embeddings ---
embedding_model = llm_embed


# --- Generar embedding ---
def get_embedding(text: str) -> np.ndarray:
    response = embedding_model(query=text)
    return np.array(response.data[0].embedding, dtype=np.float32)


# --- Cargar índice y metadatos ---
def load_vector_store(index_path: str, metadata_path: str):
    index = faiss.read_index(index_path)
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata


# --- Buscar en el índice ---
def search_similar(query: str, index: faiss.IndexFlatIP, metadata: list, k: int = 10):
    """
    Busca los k resultados más similares en un índice FAISS persistente.
    Retorna una lista de (texto, similitud).
    """
    query_vector = get_embedding(query).reshape(1, -1)
    faiss.normalize_L2(query_vector)
    distances, indices = index.search(query_vector, k)

    results = []
    for i, score in zip(indices[0], distances[0]):
        if 0 <= i < len(metadata):
            results.append({
                "metadata": metadata[i],
                "similarity": float(score)
            })
    return results

