#!/usr/bin/env python3
"""
Ollama-specific LEANN Demo
"""

import os
import sys
from pathlib import Path

# Add packages to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'packages', 'leann-core', 'src'))

from leann import LeannBuilder, LeannSearcher, LeannChat

def main():
    print("🚀 Ollama LEANN Demo")
    print("   Using Ollama for both embeddings and chat")
    
    # Sample text chunks
    chunks = [
        "Ollama is a local AI model runner for privacy and speed.",
        "It supports many open-source models like Llama, Mistral, and CodeLlama.",
        "Ollama can run models locally without internet connection.",
        "It integrates perfectly with LEANN for private AI applications.",
        "You can use Ollama for both embeddings and chat generation.",
        "Local models ensure your data never leaves your computer.",
        "Ollama supports GPU acceleration for faster processing.",
        "It's perfect for developers who want privacy and control."
    ]
    
    # Build index with Ollama embeddings
    print("\n🔨 Building index with Ollama embeddings...")
    builder = LeannBuilder(
        embedding_model="mxbai-embed-large:latest", # Using Ollama for embeddings
        embedding_mode="ollama",
        backend_name="hnsw",
    )
    
    builder.build_index(chunks)
    builder.save_index("ollama_demo.leann")
    print("✅ Index built with Ollama!")
    
    # Search
    print("\n🔍 Searching...")
    searcher = LeannSearcher("ollama_demo.leann")
    
    query = "What is Ollama and how does it work?"
    results = searcher.search(query, top_k=3)
    
    print(f"Query: {query}")
    for i, result in enumerate(results):
        print(f"{i+1}. {result['content']} (Score: {result['score']:.3f})")
    
    # Chat with Ollama
    print("\n💬 Chat with Ollama:")
    try:
        chat = LeannChat(
            "ollama_demo.leann",
            llm_config={
                "type": "ollama",
                "model": "llama3.2:latest" # Using Ollama for chat
            }
        )
        
        response = chat.chat("Explain Ollama's benefits for developers")
        print(f"AI: {response}")
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        print("   Make sure Ollama is running: ollama serve")
        print("   Install models: ollama pull llama3.2:latest")
        print("   Install embedding model: ollama pull mxbai-embed-large:latest")

if __name__ == "__main__":
    main()