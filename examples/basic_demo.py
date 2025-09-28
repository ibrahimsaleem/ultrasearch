#!/usr/bin/env python3
"""
Basic LEANN Demo
"""

import os
import sys
from pathlib import Path

# Add packages to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'packages', 'leann-core', 'src'))

from leann import LeannBuilder, LeannSearcher, LeannChat

def main():
    print("🚀 LEANN Basic Demo")
    
    # Sample text chunks
    chunks = [
        "LEANN is a low-storage vector index for RAG systems.",
        "It uses graph-based selective recomputation for efficiency.",
        "The system provides 97% less storage than traditional solutions.",
        "LEANN supports multiple backends including HNSW and DiskANN.",
        "It's optimized for personal AI applications and laptop-wide search."
    ]
    
    # Build index
    print("\n🔨 Building index...")
    builder = LeannBuilder(
        embedding_model="all-MiniLM-L6-v2",
        embedding_mode="sentence-transformers",
        backend_name="hnsw"
    )
    
    builder.build_index(chunks)
    builder.save_index("demo_knowledge.leann")
    print("✅ Index built successfully!")
    
    # Search
    print("\n🔍 Searching...")
    searcher = LeannSearcher("demo_knowledge.leann")
    
    queries = [
        "What is LEANN?",
        "How does it save storage?",
        "What backends are supported?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        results = searcher.search(query, top_k=2)
        
        for i, result in enumerate(results):
            print(f"{i+1}. {result['content']} (Score: {result['score']:.3f})")
    
    # Chat
    print("\n💬 Interactive chat demo:")
    print("(Note: Requires Ollama or Gemini for full functionality)")
    
    try:
        chat = LeannChat("demo_knowledge.leann")
        response = chat.chat("Tell me about LEANN's storage efficiency")
        print(f"AI: {response}")
    except Exception as e:
        print(f"Chat not available: {e}")
        print("To enable chat, install Ollama or set up Gemini API")

if __name__ == "__main__":
    main()