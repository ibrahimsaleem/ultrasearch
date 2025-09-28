#!/usr/bin/env python3
"""
LEANN Backend Interfaces
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import numpy as np

class LeannBackendBuilderInterface(ABC):
    """Abstract base class for LEANN backend builders"""
    
    @abstractmethod
    def build_index(self, embeddings: np.ndarray, documents: List[str], 
                   metadata: List[Dict[str, Any]] = None):
        """Build search index from embeddings and documents"""
        pass
    
    @abstractmethod
    def save_index(self, path: str):
        """Save index to file"""
        pass

class LeannBackendSearcherInterface(ABC):
    """Abstract base class for LEANN backend searchers"""
    
    @abstractmethod
    def load_index(self, path: str):
        """Load index from file"""
        pass
    
    @abstractmethod
    def search(self, query_embedding: np.ndarray, top_k: int = 10) -> List[Dict[str, Any]]:
        """Search index with query embedding"""
        pass