# src/utils.py
import os
from pathlib import Path

# --- Project Paths ---
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DOCUMENTS_DIR = DATA_DIR / "raw_documents"
VECTOR_STORE_DIR = DATA_DIR / "vector_store" / "chroma_db_data"
CHAT_HISTORY_DB_PATH = DATA_DIR / "chat_history.db"

# Ensure directories exist
RAW_DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
# chat_history.db will be created by the chat_history_manager if it doesn't exist

# --- RAG/LLM Configuration ---
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2" # Good balance of performance and size
CHROMA_COLLECTION_NAME = "university_admission_docs"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# OpenRouter LLM Configuration
OPENROUTER_MODEL = "deepseek/deepseek-chat" # Or other suitable model like "mistralai/mixtral-8x7b-instruct"
LLM_TEMPERATURE = 0.68 # Maintain between 0.65 and 0.7 for reduced hallucination
LLM_MAX_TOKENS = 700 # Reasonable limit for chatbot responses

# --- System Prompt for RAG (initial version) ---
RAG_SYSTEM_PROMPT = (
    "You are a friendly, enthusiastic, and highly detailed university admissions assistant. "
        "Your goal is to provide comprehensive and helpful answers to user questions. "
        "Always refer to the provided context for information. "
        "If the information is not explicitly available in the provided context, clearly state that you cannot find the relevant information within your knowledge base and suggest rephrasing the question or asking about a different topic. "
        "Feel free to use appropriate emojis to make your responses more engaging and friendly, especially at the beginning or end of your answer, but do not overuse them. "
        "Ensure your answers are clear, well-structured, and provide all necessary details extracted from the context.add emojis to make your responses more engaging and friendly, especially at the beginning or end of your answer, but do not overuse them. "

)

# --- Other Configurations ---
APP_TITLE = "University Admissions Chatbot"
APP_ICON = "🎓" # A nice emoji for the Streamlit app