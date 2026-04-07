# src/chat_history_manager.py
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Tuple
from pathlib import Path
# Import the database path from utils
from src.utils import CHAT_HISTORY_DB_PATH

class ChatHistoryManager:
    def __init__(self, db_path: Path = CHAT_HISTORY_DB_PATH):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """
        Connects to the SQLite database and creates the 'chat_history' table
        if it does not already exist.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            conn.commit()
            print(f"Chat history database initialized at: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
        finally:
            if conn:
                conn.close()

    def save_message(self, session_id: str, role: str, content: str):
        """
        Saves a single chat message (user or assistant) to the database.

        Args:
            session_id (str): A unique identifier for the conversation session.
            role (str): 'user' or 'assistant'.
            content (str): The content of the message.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            timestamp = datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO chat_history (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
                (session_id, role, content, timestamp)
            )
            conn.commit()
            # print(f"Saved message: [Session: {session_id}, Role: {role}, Content: {content[:50]}...]")
        except sqlite3.Error as e:
            print(f"Error saving message: {e}")
        finally:
            if conn:
                conn.close()

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        """
        Retrieves all chat messages for a given session ID.

        Args:
            session_id (str): The unique identifier for the conversation session.

        Returns:
            List[Dict[str, str]]: A list of dictionaries, each representing a message
                                 (e.g., [{'role': 'user', 'content': 'Hello'}, ...]).
        """
        conn = None
        messages = []
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row # This allows accessing columns by name
            cursor = conn.cursor()
            cursor.execute(
                "SELECT role, content FROM chat_history WHERE session_id = ? ORDER BY timestamp",
                (session_id,)
            )
            rows = cursor.fetchall()
            for row in rows:
                messages.append({"role": row['role'], "content": row['content']})
            print(f"Loaded {len(messages)} messages for session: {session_id}")
        except sqlite3.Error as e:
            print(f"Error loading chat history: {e}")
        finally:
            if conn:
                conn.close()
        return messages

    def clear_history(self, session_id: str):
        """
        Clears all chat messages for a specific session ID.

        Args:
            session_id (str): The unique identifier for the conversation session to clear.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))
            conn.commit()
            print(f"Cleared chat history for session: {session_id}")
        except sqlite3.Error as e:
            print(f"Error clearing chat history: {e}")
        finally:
            if conn:
                conn.close()

# --- For testing the chat_history_manager directly ---
if __name__ == '__main__':
    # For testing, let's use a temporary DB file or the default one
    print("--- Testing ChatHistoryManager ---")
    
    # Initialize the manager
    manager = ChatHistoryManager()

    # Define a session ID for testing
    test_session_id = "test_session_123"
    
    # Clear any previous history for this session to ensure a clean test
    manager.clear_history(test_session_id)

    # Save some messages
    print("\nSaving messages...")
    manager.save_message(test_session_id, "user", "Hello, how do I apply for admissions?")
    manager.save_message(test_session_id, "assistant", "You can apply online via our admissions portal.")
    manager.save_message(test_session_id, "user", "What documents are required?")
    manager.save_message(test_session_id, "assistant", "Transcripts, letters of recommendation, and a personal statement.")

    # Retrieve history
    print(f"\nRetrieving history for session '{test_session_id}':")
    history = manager.get_history(test_session_id)
    for msg in history:
        print(f"  {msg['role'].capitalize()}: {msg['content']}")

    # Test clearing history
    print(f"\nClearing history for session '{test_session_id}'...")
    manager.clear_history(test_session_id)

    # Verify history is cleared
    print(f"\nRetrieving history after clearing for session '{test_session_id}':")
    history_after_clear = manager.get_history(test_session_id)
    if not history_after_clear:
        print("  History successfully cleared. No messages found.")
    else:
        print("  Error: History not cleared.")

    print("\n--- ChatHistoryManager tests complete ---")