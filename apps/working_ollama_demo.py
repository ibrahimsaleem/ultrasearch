#!/usr/bin/env python3
"""
Working Ollama Demo - System Test
"""

import os
import sys
import subprocess
from pathlib import Path

# Add packages to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'packages', 'leann-core', 'src'))

from leann import LeannBuilder, LeannSearcher, LeannChat

def test_ollama_connection():
    """Test Ollama connection"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Ollama is running")
            print(f"Available models: {result.stdout}")
            return True
        else:
            print("❌ Ollama not responding")
            return False
    except Exception as e:
        print(f"❌ Ollama error: {e}")
        return False

def test_embedding_model():
    """Test embedding model"""
    try:
        result = subprocess.run(['ollama', 'pull', 'mxbai-embed-large:latest'], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ Embedding model available")
            return True
        else:
            print("❌ Embedding model not available")
            return False
    except Exception as e:
        print(f"❌ Embedding model error: {e}")
        return False

def test_chat_model():
    """Test chat model"""
    try:
        result = subprocess.run(['ollama', 'pull', 'llama3.2:latest'], 
                              capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print("✅ Chat model available")
            return True
        else:
            print("❌ Chat model not available")
            return False
    except Exception as e:
        print(f"❌ Chat model error: {e}")
        return False

def main():
    print("🚀 Working Ollama Demo - System Test")
    
    # Test Ollama connection
    print("\n🔧 Testing Ollama connection...")
    if not test_ollama_connection():
        print("   Please start Ollama: ollama serve")
        return
    
    # Test embedding model
    print("\n🔧 Testing embedding model...")
    if not test_embedding_model():
        print("   Installing embedding model...")
        test_embedding_model()
    
    # Test chat model
    print("\n🔧 Testing chat model...")
    if not test_chat_model():
        print("   Installing chat model...")
        test_chat_model()
    
    # Sample text chunks
    chunks = [
        "This is a working demo of LEANN with Ollama.",
        "The system has been tested and verified to work.",
        "Ollama is running and models are available.",
        "You can now use LEANN for private AI search.",
        "The system is ready for laptop-wide indexing."
    ]
    
    # Build index
    print("\n🔨 Building index...")
    builder = LeannBuilder(
        embedding_model="all-MiniLM-L6-v2",
        embedding_mode="sentence-transformers",
        backend_name="hnsw"
    )
    
    builder.build_index(chunks)
    builder.save_index("working_demo.leann")
    print("✅ Index built!")
    
    # Search
    print("\n🔍 Searching...")
    searcher = LeannSearcher("working_demo.leann")
    
    query = "Is the system working?"
    results = searcher.search(query, top_k=3)
    
    print(f"Query: {query}")
    for i, result in enumerate(results):
        print(f"{i+1}. {result['content']} (Score: {result['score']:.3f})")
    
    # Chat
    print("\n💬 Chat test:")
    try:
        chat = LeannChat(
            "working_demo.leann",
            llm_config={
                "type": "ollama",
                "model": "llama3.2:latest"
            }
        )
        
        response = chat.chat("Confirm the system is working")
        print(f"AI: {response}")
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        print("   Check Ollama status: ollama list")

if __name__ == "__main__":
    main()