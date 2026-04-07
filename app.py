import streamlit as st
import time
st.markdown("""
<style>
/* Background */
body {
    background-color: #0e1117;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    border-radius: 15px;
    padding: 10px;
    margin-bottom: 10px;
}

/* User message */
[data-testid="stChatMessage"][data-role="user"] {
    background-color: #1f77b4;
    color: white;
}

/* Assistant message */
[data-testid="stChatMessage"][data-role="assistant"] {
    background-color: #262730;
    color: white;
}

/* Input box */
textarea {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)
from pathlib import Path

from src.utils import APP_TITLE, APP_ICON, RAW_DOCUMENTS_DIR
# from src.chat_history_manager import ChatHistoryManager
# from src.document_processor import process_documents
from src.chatbot_logic import get_rag_response


# -------------------------------------------------
# Streamlit Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Initialize Session State
# -------------------------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = "default_user_session"

# if "chat_history_manager" not in st.session_state:
    # st.session_state.chat_history_manager = ChatHistoryManager()
    # st.session_state.chat_history_manager._initialize_db()

# -------------------------------------------------
# Initialize RAG & Index Documents (RUN ONLY ONCE)
# -------------------------------------------------
# @st.cache_resource
# def initialize_rag_components_and_index_docs():
#     """
#     Initializes ChromaDB collection and indexes documents
#     ONLY if the collection is empty.
#     """
#     try:
#         collection = get_chroma_collection()

#         # ✅ IMPORTANT FIX:
#         # Index documents ONLY if collection is empty
#         if collection.count() == 0:
#             all_processed_docs = process_documents(RAW_DOCUMENTS_DIR)
#             if all_processed_docs:
#                 index_documents_to_chromadb(all_processed_docs)
#                 print(f"Indexed {len(all_processed_docs)} documents into ChromaDB.")
#             else:
#                 print("No documents found to index.")
#         else:
#             print("ChromaDB already initialized. Skipping re-indexing.")

#         return True

#     except Exception as e:
#         st.error(f"Error initializing knowledge base: {e}")
#         print(f"Initialization error: {e}")
#         return False

# -------------------------------------------------
# Main App UI
# -------------------------------------------------
st.markdown("## 🤖 KEC AI Chatbot")
st.caption("Ask anything about Kuppam Engineering College 🎓")
st.divider()

# Initialize RAG pipeline once
if not st.session_state.get("rag_pipeline_and_indexing_done", False):
    with st.spinner("Initializing knowledge base..."):
        st.session_state.rag_pipeline_and_indexing_done = (
            # initialize_rag_components_and_index_docs()
        )

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.title("🎓 KEC AI Assistant")
st.sidebar.caption("Smart Chatbot")
st.sidebar.header("📚 Knowledge Base")
st.sidebar.write("Documents are loaded from `data/raw_documents`.")

st.sidebar.markdown("---")
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
# -------------------------------------------------
# Chat History Initialization
# -------------------------------------------------
if "messages" not in st.session_state:
    greeting = (
        "👋 Hi! I'm your KEC Assistant.\n\n"
        "Ask me about admissions, courses, fees, hostel, placements and more! 🎓"
    )

    st.session_state.messages = [
        {"role": "assistant", "content": greeting}
    ]
# -------------------------------------------------
# Display Chat Messages
# -------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------------------------
# User Input
# -------------------------------------------------
if user_query := st.chat_input("Ask a question about university admissions..."):

    # Save and display user message
    st.session_state.messages.append(
        {"role": "user", "content": user_query}
    )
    # st.session_state.chat_history_manager.save_message(
    #     st.session_state.session_id, "user", user_query
    # )

    with st.chat_message("user"):
        st.markdown(user_query)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking... Please wait"):
            try:
                bot_response = get_rag_response(user_query)
            except Exception as e:
                bot_response = (
                    f"An error occurred while generating the response: {e}"
                )

            bot_response = str(bot_response)  # safety conversion
            st.markdown(bot_response)

            # Save assistant message
            st.session_state.messages.append(
                {"role": "assistant", "content": bot_response}
            )
            # st.session_state.chat_history_manager.save_message(
            #     st.session_state.session_id, "assistant", bot_response
            # )

# -------------------------------------------------
# Footer / Debug Info
# -------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("App Info")
st.sidebar.write(f"Session ID: `{st.session_state.session_id}`")
# st.sidebar.write(f"Knowledge Base Docs: `{get_chroma_collection().count()}`")
# st.sidebar.write(f"Chat History DB: `{CHAT_HISTORY_DB_PATH.name}`")
st.sidebar.write(f"Data Directory: `{RAW_DOCUMENTS_DIR.name}`")

st.sidebar.markdown("---")
st.sidebar.info(
    "This chatbot uses Retrieval-Augmented Generation (RAG) "
    "with OpenRouter LLMs. Chat history is persistent for the session. ✨"
)
