#!/usr/bin/env python3
"""
Simple LEANN Demo with Ollama
"""

import os
import sys
from pathlib import Path

# Add packages to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'packages', 'leann-core', 'src'))

from leann import LeannBuilder, LeannSearcher, LeannChat

def main():
    print("🚀 Simple LEANN Demo")
    
    # Sample text chunks
    chunks = [
        "LEANN is a revolutionary vector database for RAG systems.",
        "It provides 97% less storage than traditional vector databases.",
        "The system uses graph-based selective recomputation for efficiency.",
        "LEANN supports multiple backends including HNSW and DiskANN.",
        "It's perfect for personal AI applications and laptop-wide search.",
        "The system can index documents, code, emails, and browser history.",
        "LEANN enables fast semantic search across your entire laptop.",
        "It integrates with Ollama for local AI processing and privacy."
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
        "How much storage does it save?",
        "What can it search?",
        "Does it work with Ollama?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        results = searcher.search(query, top_k=2)
        
        for i, result in enumerate(results):
            print(f"{i+1}. {result['content']} (Score: {result['score']:.3f})")
    
    # Chat with Ollama
    print("\n💬 Interactive chat demo with Ollama:")
    print("   (Using local Ollama models - fully private!)")
    
    try:
        # Configure chat to use Ollama
        chat = LeannChat(
            "demo_knowledge.leann",
            llm_config={
                "type": "ollama",
                "model": "llama3.2:latest"  # Use your available model
            }
        )
        
        chat_queries = [
            "Tell me about LEANN's storage efficiency",
            "What makes LEANN different from other vector databases?",
            "How can I use LEANN for laptop search?"
        ]
        
        for query in chat_queries:
            print(f"\nUser: {query}")
            response = chat.chat(query)
            print(f"AI: {response}")
            
    except Exception as e:
        print(f"❌ Error during chat: {e}")
        print("   Make sure Ollama is running: ollama serve")
        print("   And that you have llama3.2:latest model installed")

if __name__ == "__main__":
    main()