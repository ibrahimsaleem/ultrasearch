#!/usr/bin/env python3
"""
HNSW Backend Implementation
"""

import os
import pickle
import numpy as np
from typing import List, Dict, Any, Optional
import faiss

class HNSWBuilder:
    """HNSW Index Builder"""
    
    def __init__(self, dimension: int = 384, m: int = 16, ef_construction: int = 200):
        self.dimension = dimension
        self.m = m
        self.ef_construction = ef_construction
        self.index = None
        self.documents = []
        self.metadata = []
        
    def build_index(self, embeddings: np.ndarray, documents: List[str], 
                   metadata: List[Dict[str, Any]] = None):
        """Build HNSW index"""
        self.documents = documents
        self.metadata = metadata or []
        
        # Create FAISS HNSW index
        self.index = faiss.IndexHNSWFlat(self.dimension, self.m)
        self.index.hnsw.efConstruction = self.ef_construction
        
        # Add embeddings to index
        self.index.add(embeddings.astype('float32'))
        
    def save_index(self, path: str):
        """Save index to file"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, path + '.faiss')
        
        # Save documents and metadata
        with open(path + '.pkl', 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'metadata': self.metadata
            }, f)

class HNSWSearcher:
    """HNSW Index Searcher"""
    
    def __init__(self):
        self.index = None
        self.documents = []
        self.metadata = []
        
    def load_index(self, path: str):
        """Load HNSW index"""
        # Load FAISS index
        self.index = faiss.read_index(path + '.faiss')
        
        # Load documents and metadata
        with open(path + '.pkl', 'rb') as f:
            data = pickle.load(f)
            self.documents = data['documents']
            self.metadata = data['metadata']
    
    def search(self, query_embedding: np.ndarray, top_k: int = 10) -> List[Dict[str, Any]]:
        """Search HNSW index"""
        if self.index is None:
            return []
        
        # Set search parameters
        self.index.hnsw.efSearch = max(50, top_k * 2)
        
        # Search
        scores, indices = self.index.search(query_embedding.reshape(1, -1).astype('float32'), top_k)
        
        # Format results
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(self.documents):
                result = {
                    'content': self.documents[idx],
                    'score': float(score),
                    'index': int(idx)
                }
                
                # Add metadata if available
                if idx < len(self.metadata):
                    result.update(self.metadata[idx])
                
                results.append(result)
        
        return results