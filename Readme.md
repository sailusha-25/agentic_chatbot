# Agentic RAG Chatbot for Multi-Format Document Q&A

This project implements an agent-based Retrieval-Augmented Generation (RAG) chatbot as per the coding challenge requirements. It can ingest documents in various formats (PDF, DOCX, PPTX, CSV, TXT), process user queries, and provide answers grounded in the content of those documents.

## 🏛️ Architecture

The system is built on a simple yet effective agentic architecture. The agents are distinct logical components that communicate through a defined messaging standard called the **Model Context Protocol (MCP)**. For this project, the Streamlit `app.py` file acts as the central **Coordinator**, orchestrating the flow of messages between agents.

### Core Components

1.  **IngestionAgent**: This agent's sole responsibility is to handle the initial processing of documents. It receives raw files, uses parsers to extract text content, and splits the text into smaller, manageable chunks suitable for embedding.
2.  **RetrievalAgent**: This agent manages the "memory" of the system. It takes the text chunks from the `IngestionAgent`, generates vector embeddings using Sentence-Transformers, and stores them in a FAISS vector database. When a user asks a question, it retrieves the most relevant chunks of text from this database.
3.  **LLMResponseAgent**: This is the "brains" of the operation. It receives the user's query and the context chunks from the `RetrievalAgent`. It then constructs a precise prompt for the Google Gemini LLM, instructing it to answer the query based *only* on the provided context.

### System Flow & Message Passing (MCP)

The communication follows a clear, sequential path orchestrated by the main application:


1.  **User Uploads Documents**: The user uploads one or more files via the Streamlit UI.
2.  **UI to `IngestionAgent`**: The application triggers the `IngestionAgent` to process these files.
3.  **`IngestionAgent` → `RetrievalAgent`**: The `IngestionAgent` sends an MCP message of type `DOCUMENT_CHUNKS` to the `RetrievalAgent`.
    ```json
    {
      "sender": "IngestionAgent",
      "receiver": "RetrievalAgent",
      "type": "DOCUMENT_CHUNKS",
      "payload": { "chunks": ["...", "...", "..."] }
    }
    ```
4.  **User Asks a Question**: The user types a question into the chat interface.
5.  **UI to `RetrievalAgent`**: The application asks the `RetrievalAgent` to find relevant context for the query.
6.  **`RetrievalAgent` → `LLMResponseAgent`**: The `RetrievalAgent` performs a semantic search and sends the results in an MCP message of type `CONTEXT_RESPONSE`.
    ```json
    {
      "sender": "RetrievalAgent",
      "receiver": "LLMResponseAgent",
      "type": "CONTEXT_RESPONSE",
      "payload": {
        "top_chunks": ["Relevant text 1...", "Relevant text 2..."],
        "query": "What were the Q1 KPIs?"
      }
    }
    ```
7.  **`LLMResponseAgent` → UI**: The `LLMResponseAgent` queries the Gemini model and formats the final answer into an MCP message of type `FINAL_ANSWER`.
    ```json
    {
      "sender": "LLMResponseAgent",
      "receiver": "UI",
      "type": "FINAL_ANSWER",
      "payload": {
        "answer": "The key KPIs tracked in Q1 were...",
        "sources": ["Relevant text 1...", "Relevant text 2..."]
      }
    }
    ```
8.  **Display to User**: The UI displays the answer and provides an expandable section to view the source chunks used to generate it.

## 🛠️ Tech Stack

-   **Backend/Orchestration**: Python
-   **Web Framework (UI)**: Streamlit
-   **LLM**: Google Gemini 1.5 Flash
-   **Embedding Model**: `all-MiniLM-L6-v2` (from Sentence-Transformers / Hugging Face)
-   **Vector Database**: FAISS (Facebook AI Similarity Search) - CPU version
-   **Document Parsers**: `pypdf`, `python-docx`, `python-pptx`, `pandas`

## 🚀 Setup and Installation

Follow these steps to get the application running on your local machine.

### 1. Prerequisites

-   Python 3.8+
-   `pip` and `venv`

### 2. Clone the Repository

```bash
git clone <your-repo-url>
cd agentic-rag-chatbot
```

### 3. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

Install all the required Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5. Configure API Key

You need a Google AI API key to use the Gemini model.

1.  Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Create a file named `.env` in the root directory of the project.
3.  Add your API key to the `.env` file like this:
    ```
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
    ```

## ▶️ How to Run the Application

Once the setup is complete, running the chatbot is simple.

1.  Open your terminal and make sure your virtual environment is activated.
2.  Navigate to the root directory of the project.
3.  Run the following command:

    ```bash
    streamlit run app.py
    ```

4.  Your web browser should automatically open a new tab with the application running.

### Using the Chatbot

1.  **Upload**: Use the sidebar to upload one or more documents. Supported formats are PDF, DOCX, PPTX, TXT, CSV, and MD.
2.  **Process**: Click the **"Process Documents"** button. The application will parse the files, generate embeddings, and create a searchable index. You will see a success message when it's done.
3.  **Chat**: Type your questions into the chat input box at the bottom of the screen and press Enter. The chatbot will use the processed documents to find and generate an answer.

---