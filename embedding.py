from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import streamlit as st

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

def embed_texts(texts):
    embeddings = model.encode(texts)
    return np.array(embeddings)

def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def search_similar(index, query_embedding, k=3):
    distances, indices = index.search(query_embedding, k)
    return indices[0], distances[0]

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))