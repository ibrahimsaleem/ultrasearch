#!/usr/bin/env python3
"""
LEANN Core API
"""

import os
import sys
import time
import json
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import numpy as np
from sentence_transformers import SentenceTransformer
import torch

# Add backend paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'leann-backend-hnsw', 'src'))

from leann_backend_hnsw.hnsw_backend import HNSWBuilder, HNSWSearcher

class LeannBuilder:
    """LEANN Index Builder"""
    
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2", 
                 embedding_mode: str = "sentence-transformers",
                 backend_name: str = "hnsw",
                 embedding_function: Optional[callable] = None):
        self.embedding_model = embedding_model
        self.embedding_mode = embedding_mode
        self.backend_name = backend_name
        self.embedding_function = embedding_function
        self.model = None
        self.backend_builder = None
        
    def load_model(self):
        """Load embedding model"""
        if self.model is None:
            if self.embedding_mode == "sentence-transformers":
                self.model = SentenceTransformer(self.embedding_model)
            elif self.embedding_mode == "ollama":
                # Ollama embedding mode
                pass
            elif self.embedding_mode == "gemini":
                # Gemini embedding mode
                pass
        return self.model
    
    def build_index(self, documents: List[str], metadata: List[Dict] = None):
        """Build search index"""
        if not documents:
            return None
            
        # Generate embeddings
        if self.embedding_function:
            embeddings = [self.embedding_function(doc) for doc in documents]
        else:
            model = self.load_model()
            embeddings = model.encode(documents)
        
        # Build backend index
        if self.backend_name == "hnsw":
            self.backend_builder = HNSWBuilder()
            self.backend_builder.build_index(embeddings, documents, metadata)
        
        return self.backend_builder
    
    def save_index(self, path: str):
        """Save index to file"""
        if self.backend_builder:
            self.backend_builder.save_index(path)

class LeannSearcher:
    """LEANN Index Searcher"""
    
    def __init__(self, index_path: str, embedding_model: str = "all-MiniLM-L6-v2",
                 embedding_mode: str = "sentence-transformers",
                 embedding_function: Optional[callable] = None):
        self.index_path = index_path
        self.embedding_model = embedding_model
        self.embedding_mode = embedding_mode
        self.embedding_function = embedding_function
        self.model = None
        self.backend_searcher = None
        
    def load_model(self):
        """Load embedding model"""
        if self.model is None:
            if self.embedding_mode == "sentence-transformers":
                self.model = SentenceTransformer(self.embedding_model)
            elif self.embedding_mode == "ollama":
                # Ollama embedding mode
                pass
            elif self.embedding_mode == "gemini":
                # Gemini embedding mode
                pass
        return self.model
    
    def load_index(self):
        """Load search index"""
        if self.backend_searcher is None:
            self.backend_searcher = HNSWSearcher()
            self.backend_searcher.load_index(self.index_path)
        return self.backend_searcher
    
    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Search index"""
        if not self.backend_searcher:
            self.load_index()
        
        # Generate query embedding
        if self.embedding_function:
            query_embedding = self.embedding_function(query)
        else:
            model = self.load_model()
            query_embedding = model.encode([query])[0]
        
        # Search backend
        results = self.backend_searcher.search(query_embedding, top_k)
        return results

class LeannChat:
    """LEANN Chat Interface"""
    
    def __init__(self, index_path: str, llm_config: Dict[str, Any] = None):
        self.index_path = index_path
        self.llm_config = llm_config or {"type": "ollama", "model": "llama3.2:latest"}
        self.searcher = None
        
    def load_searcher(self):
        """Load search interface"""
        if self.searcher is None:
            self.searcher = LeannSearcher(self.index_path)
        return self.searcher
    
    def chat(self, query: str, context_limit: int = 5) -> str:
        """Chat with RAG"""
        searcher = self.load_searcher()
        
        # Search for relevant context
        results = searcher.search(query, top_k=context_limit)
        
        # Prepare context
        context = "\n".join([result['content'] for result in results])
        
        # Generate response
        if self.llm_config['type'] == 'ollama':
            return self._ollama_chat(query, context)
        elif self.llm_config['type'] == 'gemini':
            return self._gemini_chat(query, context)
        else:
            return f"Found {len(results)} relevant documents for: {query}"
    
    def _ollama_chat(self, query: str, context: str) -> str:
        """Ollama chat response"""
        try:
            import ollama
            
            prompt = f"""Context: {context}

Question: {query}

Answer:"""
            
            response = ollama.generate(
                model=self.llm_config['model'],
                prompt=prompt
            )
            
            return response['response']
        except Exception as e:
            return f"Ollama error: {e}"
    
    def _gemini_chat(self, query: str, context: str) -> str:
        """Gemini chat response"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""Context: {context}

Question: {query}

Answer:"""
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini error: {e}"

def compute_embeddings(texts: List[str], model: str = "all-MiniLM-L6-v2") -> np.ndarray:
    """Compute embeddings for texts"""
    model = SentenceTransformer(model)
    return model.encode(texts)