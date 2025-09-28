#!/usr/bin/env python3
"""
Fast Ollama Demo for Slower Systems
"""

import os
import sys
from pathlib import Path

# Add packages to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'packages', 'leann-core', 'src'))

from leann import LeannBuilder, LeannSearcher, LeannChat

def main():
    print("🚀 Fast Ollama Demo (Optimized for Slower Systems)")
    print("   Using smaller, faster models")
    
    # Sample text chunks
    chunks = [
        "This demo uses smaller models for faster performance.",
        "llama3.2:1b is a 1 billion parameter model that's very fast.",
        "It's perfect for slower systems and quick testing.",
        "The model still provides good quality responses.",
        "You can upgrade to larger models when needed.",
        "Local AI ensures privacy and no internet required.",
        "Smaller models use less RAM and CPU.",
        "Perfect for development and experimentation."
    ]
    
    # Build index
    print("\n🔨 Building index...")
    builder = LeannBuilder(
        embedding_model="all-MiniLM-L6-v2", # Fast embedding model
        embedding_mode="sentence-transformers",
        backend_name="hnsw",
    )
    
    builder.build_index(chunks)
    builder.save_index("fast_demo.leann")
    print("✅ Index built!")
    
    # Search
    print("\n🔍 Searching...")
    searcher = LeannSearcher("fast_demo.leann")
    
    query = "What models are good for slower systems?"
    results = searcher.search(query, top_k=3)
    
    print(f"Query: {query}")
    for i, result in enumerate(results):
        print(f"{i+1}. {result['content']} (Score: {result['score']:.3f})")
    
    # Chat with fast model
    print("\n💬 Chat with fast model:")
    try:
        chat = LeannChat(
            "fast_demo.leann",
            llm_config={
                "type": "ollama",
                "model": "llama3.2:1b" # Fast 1B parameter model
            }
        )
        
        response = chat.chat("What are the benefits of smaller AI models?")
        print(f"AI: {response}")
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        print("   Install fast model: ollama pull llama3.2:1b")
        print("   Start Ollama: ollama serve")

if __name__ == "__main__":
    main()