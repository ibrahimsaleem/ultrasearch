#!/usr/bin/env python3
"""
Document RAG Example
"""

import os
import sys
from pathlib import Path

# Add packages to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'packages', 'leann-core', 'src'))

from leann import LeannBuilder, LeannSearcher, LeannChat

def main():
    print("📚 Document RAG Example")
    
    # Sample documents
    documents = [
        "Python is a high-level programming language.",
        "Machine learning is a subset of artificial intelligence.",
        "Vector databases store high-dimensional vectors.",
        "RAG combines retrieval with generation for better AI responses."
    ]
    
    metadata = [
        {"source": "python_guide.txt", "type": "tutorial"},
        {"source": "ml_basics.txt", "type": "concept"},
        {"source": "vector_db.txt", "type": "technology"},
        {"source": "rag_paper.txt", "type": "research"}
    ]
    
    # Build index
    print("🔨 Building index...")
    builder = LeannBuilder(
        embedding_model="all-MiniLM-L6-v2",
        embedding_mode="sentence-transformers",
        backend_name="hnsw"
    )
    
    builder.build_index(documents, metadata)
    builder.save_index("document_index.leann")
    
    # Search
    print("🔍 Searching...")
    searcher = LeannSearcher("document_index.leann")
    
    query = "What is machine learning?"
    results = searcher.search(query, top_k=2)
    
    print(f"Query: {query}")
    for i, result in enumerate(results):
        print(f"{i+1}. {result['content']} (Score: {result['score']:.3f})")
    
    # Chat
    print("\n💬 Chat example:")
    chat = LeannChat("document_index.leann")
    response = chat.chat("Explain RAG in simple terms")
    print(f"AI: {response}")

if __name__ == "__main__":
    main()