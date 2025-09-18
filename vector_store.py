# core/vector_store.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorStoreManager:
    """
    Manages the vector store, including embedding generation and retrieval.
    """
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # Initialize the embedding model
        self.embedding_model = SentenceTransformer(model_name)
        self.dimension = self.embedding_model.get_sentence_embedding_dimension()
        
        # Initialize an empty FAISS index
        self.index = None
        self.chunks_with_metadata = []

    def build_index(self, chunks):
        """
        Builds the FAISS index from a list of text chunks.

        Args:
            chunks (list[str]): A list of text chunks to be indexed.
        """
        if not chunks:
            return

        # Store chunks for later retrieval
        self.chunks_with_metadata = chunks
        
        # Generate embeddings for all chunks
        embeddings = self.embedding_model.encode(chunks, convert_to_tensor=False)
        
        # Create a FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        print("✅ FAISS index built successfully.")

    def search(self, query, k=5):
        """
        Searches the index for the most relevant chunks to a query.

        Args:
            query (str): The user's query.
            k (int): The number of relevant chunks to retrieve.

        Returns:
            list[str]: A list of the top k relevant text chunks.
        """
        if self.index is None:
            return []

        # Generate embedding for the query
        query_embedding = self.embedding_model.encode([query], convert_to_tensor=False)
        
        # Perform the search
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), k)
        
        # Retrieve the corresponding chunks
        relevant_chunks = [self.chunks_with_metadata[i] for i in indices[0]]
        return relevant_chunks