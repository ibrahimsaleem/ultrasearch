#!/usr/bin/env python3
"""
Minimal Ollama Demo
"""

import os
import sys
from pathlib import Path

# Add packages to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'packages', 'leann-core', 'src'))

from leann import LeannBuilder, LeannSearcher, LeannChat

def main():
    print("🚀 Minimal Ollama Demo")
    
    # Minimal text chunks
    chunks = [
        "LEANN is a vector database for RAG.",
        "Ollama runs AI models locally.",
        "Together they enable private AI search."
    ]
    
    # Build index
    print("\n🔨 Building index...")
    builder = LeannBuilder(
        embedding_model="all-MiniLM-L6-v2",
        embedding_mode="sentence-transformers",
        backend_name="hnsw"
    )
    
    builder.build_index(chunks)
    builder.save_index("minimal_demo.leann")
    print("✅ Index built!")
    
    # Search
    print("\n🔍 Searching...")
    searcher = LeannSearcher("minimal_demo.leann")
    
    query = "What is LEANN?"
    results = searcher.search(query, top_k=2)
    
    print(f"Query: {query}")
    for i, result in enumerate(results):
        print(f"{i+1}. {result['content']} (Score: {result['score']:.3f})")
    
    # Chat
    print("\n💬 Chat:")
    try:
        chat = LeannChat(
            "minimal_demo.leann",
            llm_config={
                "type": "ollama",
                "model": "llama3.2:1b"
            }
        )
        
        response = chat.chat("Explain LEANN briefly")
        print(f"AI: {response}")
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        print("   Install model: ollama pull llama3.2:1b")
        print("   Start Ollama: ollama serve")

if __name__ == "__main__":
    main()