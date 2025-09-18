# agents/ingestion_agent.py

from core.file_handler import parse_document, get_text_chunks
from core.mcp import create_mcp_message

class IngestionAgent:
    """
    Agent responsible for parsing and preprocessing documents.
    """
    def __init__(self):
        self.name = "IngestionAgent"

    def process_files(self, files):
        """
        Parses uploaded files, splits them into chunks, and sends them for processing.

        Args:
            files (list): A list of uploaded file objects.

        Returns:
            dict: An MCP message containing the document chunks.
        """
        print(f"[{self.name}]: Starting file processing...")
        all_chunks = []
        for file in files:
            print(f"[{self.name}]: Parsing {file.name}...")
            text = parse_document(file)
            chunks = get_text_chunks(text)
            all_chunks.extend(chunks)
        
        print(f"[{self.name}]: Generated {len(all_chunks)} chunks.")
        
        # Create an MCP message to send the chunks to the RetrievalAgent
        message = create_mcp_message(
            sender=self.name,
            receiver="RetrievalAgent",
            msg_type="DOCUMENT_CHUNKS",
            payload={"chunks": all_chunks}
        )
        return message