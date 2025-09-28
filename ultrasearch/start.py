#!/usr/bin/env python3
"""
🚀 UltraSearch Launcher
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 Starting UltraSearch - Lightning Fast RAG Search...")
    print("📱 App will be available at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop")
    print()
    print("✨ Features:")
    print("  ⚡ Lightning fast search with RAG")
    print("  🧠 AI-powered embeddings")
    print("  📁 Multi-folder indexing")
    print("  🔍 Smart content search")
    print("  📊 Real-time performance metrics")
    print("  🤖 AI analysis of results")
    print()
    
    try:
        # Run the app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n👋 UltraSearch stopped!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()