# agents/response_agent.py

import os
import google.generativeai as genai
from core.mcp import create_mcp_message

class LLMResponseAgent:
    """
    Agent responsible for generating a final answer using the LLM.
    """
    def __init__(self):
        self.name = "LLMResponseAgent"
        # Configure the Gemini model
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_response(self, mcp_message):
        """
        Generates a response using the retrieved context and the user query.

        Args:
            mcp_message (dict): The MCP message from the RetrievalAgent.

        Returns:
            dict: An MCP message containing the final answer and source chunks.
        """
        if mcp_message["type"] != "CONTEXT_RESPONSE":
            return create_mcp_message(self.name, "Coordinator", "ERROR", {"error": "Invalid message type"})

        context_chunks = mcp_message["payload"]["top_chunks"]
        query = mcp_message["payload"]["query"]

        print(f"[{self.name}]: Generating response for query: '{query}'")

        if not context_chunks:
            final_answer = "I could not find any relevant information in the uploaded documents to answer your question."
        else:
            context_str = "\n---\n".join(context_chunks)
            
            prompt = f"""
            You are a helpful assistant. Answer the user's question based *only* on the provided context.
            If the answer is not found in the context, say "I could not find the answer in the provided documents."

            CONTEXT:
            {context_str}

            QUESTION:
            {query}

            ANSWER:
            """

            try:
                response = self.model.generate_content(prompt)
                final_answer = response.text
            except Exception as e:
                print(f"[{self.name}]: Error calling Gemini API: {e}")
                final_answer = "Sorry, I encountered an error while generating the response."
        
        # Create the final message
        final_message = create_mcp_message(
            sender=self.name,
            receiver="UI",
            msg_type="FINAL_ANSWER",
            payload={
                "answer": final_answer,
                "sources": context_chunks
            }
        )
        return final_message