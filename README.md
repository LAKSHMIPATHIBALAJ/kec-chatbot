# University Admissions Chatbot (RAG System)

## Overview

This project implements an intelligent chatbot designed to answer prospective students' questions about university admissions. It utilizes a Retrieval-Augmented Generation (RAG) system to provide accurate and helpful responses grounded in a curated knowledge base. This approach avoids relying solely on a large language model's general knowledge, which can be prone to inaccuracies.

## Features

*   **RAG-Based Architecture:** Retrieves relevant information from university documents before generating answers.
*   **Comprehensive Knowledge Base:** Supports various document formats, including PDF, DOCX, XLSX, and images (OCR).
*   **User-Friendly Interface:** Accessible through a Streamlit web application.
*   **Persistent Chat History:** Stores and retrieves chat history for improved user experience.

## Technologies Used

*   Python
*   Streamlit
*   Langchain
*   ChromaDB
*   PyMuPDF
*   python-docx
*   openpyxl
*   Pillow (PIL)
*   pytesseract

## Setup Instructions

1.  **Check python version:**

   need python 3.10 0r higher

2.  **Create a virtual environment (recommended):**

    ```sh
    python -m venv venv
    venv\Scripts\activate   # Windows
    # source venv/bin/activate  # macOS/Linux
    ```

3.  **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure Tesseract OCR (if needed):**

    *   If Tesseract is not in your system's PATH, set the `TESSERACT_CMD_PATH` variable in `src/document_processor.py` to the correct path.

5.  **Set up environment variables:**

    *   Create a `.env` file in the project root.
    *   Add any necessary API keys or configuration settings to the `.env` file.

6.  **Run the Streamlit application:**

    ```sh
    streamlit run app.py
    ```

## Usage

1.  Open the Streamlit application in your web browser (usually at `http://localhost:8501`).
2.  Interact with the chatbot by typing your questions in the chat interface.
3.  The chatbot will retrieve relevant information and generate an answer based on the context.

## Data Storage

*   **Chat History:** Stored in a SQLite database (`data/chat_history.db`).
*   **Raw Documents:** Place your university documents (PDF, DOCX, XLSX, images) in the `data/raw_documents/` directory.
*   **Vector Store:** ChromaDB is used to store vector embeddings of the documents in `data/vector_store/chroma_db_data/`.

## Document Processing

The `src/document_processor.py` script handles the extraction of text from various document formats. It uses libraries like PyMuPDF, python-docx, openpyxl, and Pillow (with Tesseract OCR) to process the documents in the `data/raw_documents/` directory.

## Chatbot Logic

The `src/chatbot_logic.py` script contains the core logic for the chatbot, including:

*   Retrieving relevant documents from the vector store.
*   Generating answers using a large language model.
*   Managing the chat history.

