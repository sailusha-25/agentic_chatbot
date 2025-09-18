# app.py

import streamlit as st
from dotenv import load_dotenv

from core.vector_store import VectorStoreManager
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.response_agent import LLMResponseAgent

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Agentic RAG Chatbot 🤖", layout="wide")

st.title("Agentic RAG Chatbot for Multi-Format Documents")
st.write("Upload your documents (PDF, DOCX, PPTX, TXT, CSV) and ask questions!")

# --- Agent and Core Component Initialization ---
# This is done once and stored in the session state to persist across reruns.

if "vector_store_manager" not in st.session_state:
    st.session_state.vector_store_manager = VectorStoreManager()

if "ingestion_agent" not in st.session_state:
    st.session_state.ingestion_agent = IngestionAgent()

if "retrieval_agent" not in st.session_state:
    st.session_state.retrieval_agent = RetrievalAgent(st.session_state.vector_store_manager)

if "response_agent" not in st.session_state:
    st.session_state.response_agent = LLMResponseAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "processed" not in st.session_state:
    st.session_state.processed = False

# --- UI Sidebar for Document Upload ---

with st.sidebar:
    st.header("1. Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose files",
        accept_multiple_files=True,
        type=['pdf', 'docx', 'pptx', 'txt', 'csv', 'md']
    )

    if st.button("Process Documents") and uploaded_files:
        with st.spinner("Processing documents... This may take a moment."):
            # Step 1: IngestionAgent processes files and creates an MCP message
            ingestion_mcp = st.session_state.ingestion_agent.process_files(uploaded_files)
            
            # Step 2: RetrievalAgent receives the message and builds the vector store
            st.session_state.retrieval_agent.handle_ingestion(ingestion_mcp)
            
            st.session_state.processed = True
            st.success("✅ Documents processed and indexed successfully!")

    st.header("2. Ask Questions")
    st.info("Once documents are processed, you can ask questions in the chat window.")

# --- Main Chat Interface ---

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Show sources if they exist in the assistant's message
        if "sources" in message:
            with st.expander("View Sources"):
                for source in message["sources"]:
                    st.info(source)

# Handle new chat input
if user_query := st.chat_input("What would you like to know?"):
    if not st.session_state.processed:
        st.warning("Please upload and process documents before asking questions.")
    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # --- Agentic Workflow Execution ---
        with st.spinner("Thinking..."):
            # Step 3: RetrievalAgent gets relevant context for the query
            retrieval_mcp = st.session_state.retrieval_agent.retrieve_context(user_query)
            
            # Step 4: LLMResponseAgent generates the final answer
            final_mcp = st.session_state.response_agent.generate_response(retrieval_mcp)
            
            response_payload = final_mcp["payload"]
            answer = response_payload["answer"]
            sources = response_payload["sources"]

            # Display assistant's response
            with st.chat_message("assistant"):
                st.markdown(answer)
                if sources:
                    with st.expander("View Sources"):
                        for source in sources:
                            st.info(source)
            
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })