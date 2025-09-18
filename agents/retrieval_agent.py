# agents/retrieval_agent.py

from core.mcp import create_mcp_message

class RetrievalAgent:
    """
    Agent responsible for managing the vector store and retrieving context.
    """
    def __init__(self, vector_store_manager):
        self.name = "RetrievalAgent"
        self.vector_store = vector_store_manager

    def handle_ingestion(self, mcp_message):
        """
        Receives document chunks and builds the vector store index.

        Args:
            mcp_message (dict): The MCP message from the IngestionAgent.
        """
        if mcp_message["type"] == "DOCUMENT_CHUNKS":
            chunks = mcp_message["payload"]["chunks"]
            print(f"[{self.name}]: Received {len(chunks)} chunks for indexing.")
            self.vector_store.build_index(chunks)
            print(f"[{self.name}]: Indexing complete.")

    def retrieve_context(self, user_query):
        """
        Retrieves relevant context from the vector store for a given query.

        Args:
            user_query (str): The user's question.

        Returns:
            dict: An MCP message containing the retrieved context.
        """
        print(f"[{self.name}]: Searching for context for query: '{user_query}'")
        relevant_chunks = self.vector_store.search(user_query, k=5)
        
        # Create an MCP message to send context to the LLMResponseAgent
        message = create_mcp_message(
            sender=self.name,
            receiver="LLMResponseAgent",
            msg_type="CONTEXT_RESPONSE",
            payload={
                "top_chunks": relevant_chunks,
                "query": user_query
            }
        )
        return message