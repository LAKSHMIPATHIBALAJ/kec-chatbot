import os
import json
import uuid
import requests
# import chromadb
from pathlib import Path
from typing import List, Dict, Tuple
from dotenv import load_dotenv
# from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()

# -------------------------------------------------
# Configuration
# -------------------------------------------------
VECTOR_STORE_DIR = Path(os.getenv("VECTOR_STORE_DIR", "data/vector_store/chroma_db_data"))
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "university_admission_docs")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "mistralai/mistral-7b-instruct")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# Global Cached Objects
# -------------------------------------------------
# _chroma_client = None
# _chroma_collection = None
# _embedding_function = None

# # -------------------------------------------------
# # ChromaDB Helpers
# # -------------------------------------------------
# def get_chroma_client():
#     global _chroma_client
#     if _chroma_client is None:
#         _chroma_client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
#     return _chroma_client
def get_rag_response(query: str) -> str:
    return f"You asked: {query}\n\n⚠️ Knowledge base is temporarily disabled for deployment."

def get_embedding_function():
    global _embedding_function
    if _embedding_function is None:
        _embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
    return _embedding_function


def get_chroma_collection():
    global _chroma_collection
    if _chroma_collection is None:
        client = get_chroma_client()
        embedding_func = get_embedding_function()
        _chroma_collection = client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME,
            embedding_function=embedding_func
        )
    return _chroma_collection

# -------------------------------------------------
# Index Documents into ChromaDB
# -------------------------------------------------
def index_documents_to_chromadb(processed_documents: List[Tuple[str, Dict]]):
    collection = get_chroma_collection()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len
    )

    documents, metadatas, ids = [], [], []

    for text_content, original_metadata in processed_documents:
        chunks = splitter.split_text(text_content)

        for chunk in chunks:
            chunk_id = str(uuid.uuid4())  # ✅ UNIQUE ID FIX
            documents.append(chunk)
            metadatas.append(original_metadata)
            ids.append(chunk_id)

    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

# -------------------------------------------------
# Retrieve Relevant Chunks
# -------------------------------------------------
def retrieve_relevant_chunks(query: str, n_results: int = 5) -> List[Dict]:
    collection = get_chroma_collection()

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []
    if results and results["documents"]:
        for i in range(len(results["documents"][0])):
            chunks.append({
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })
    return chunks

# -------------------------------------------------
# Call OpenRouter LLM
# -------------------------------------------------
def get_llm_response(prompt: str) -> str:
    if not OPENROUTER_API_KEY:
        return "❌ OPENROUTER_API_KEY is missing."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": LLM_MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,   # ✅ STABLE OUTPUT
        "max_tokens": 500
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error contacting LLM: {e}"

# -------------------------------------------------
# Main RAG Function
# -------------------------------------------------
def get_rag_response(query: str) -> str:
    chunks = retrieve_relevant_chunks(query)

    if not chunks:
        return (
            "❌ Sorry, I couldn't find this in my knowledge base. Please ask about KEC admissions, courses, fees, etc."
        )

    context = "\n\n".join(chunk["content"] for chunk in chunks)

    system_prompt = (
        "You are a smart and friendly university assistant chatbot for Kuppam Engineering College.\n\n"
    
    "Answer in a clear, structured, and engaging way like ChatGPT.\n\n"
    
    "Follow this format:\n"
    "1. Start with a short introduction\n"
    "2. Use bullet points for key details\n"
    "3. Keep it simple and easy to understand\n"
    "4. Add emojis where appropriate\n"
    "5. End with a helpful summary\n\n"
    
    "Only use the provided context. Do not make up information.\n"
    )

    full_prompt = (
        f"{system_prompt}\n\n"
        f"Context:\n{context}\n\n"
        f"User Question: {query}\n\n"
        "Answer:"
    )

    return get_llm_response(full_prompt)

# -------------------------------------------------
# Local Testing
# -------------------------------------------------
if __name__ == "__main__":
    print("Chatbot logic loaded successfully.")
