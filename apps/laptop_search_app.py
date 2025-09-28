#!/usr/bin/env python3
"""
Laptop Search App - Streamlit Frontend
"""

import os
import sys
import time
import streamlit as st
from pathlib import Path
from typing import List, Dict, Any

# Add packages to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'packages', 'leann-core', 'src'))

from leann import LeannBuilder, LeannSearcher, LeannChat

def main():
    st.set_page_config(
        page_title="🔍 Laptop Search",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Laptop Search with LEANN")
    st.markdown("**Search your entire laptop with AI-powered RAG**")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Search folders
        st.subheader("📁 Search Folders")
        
        default_folders = [
            ".",
            "C:/Users/Ibrah/Documents",
            "C:/Users/Ibrah/Desktop",
            "C:/Users/Ibrah/Desktop/Research-Jummana"
        ]
        
        if 'search_folders' not in st.session_state:
            st.session_state.search_folders = default_folders.copy()
        
        # Display folders
        for i, folder in enumerate(st.session_state.search_folders):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text(folder)
            with col2:
                if st.button("🗑️", key=f"remove_{i}"):
                    st.session_state.search_folders.pop(i)
                    st.rerun()
        
        # Add folder
        new_folder = st.text_input("Add folder:", placeholder="C:/Users/Ibrah/Desktop/NewFolder")
        if st.button("➕ Add") and new_folder:
            if os.path.exists(new_folder):
                if new_folder not in st.session_state.search_folders:
                    st.session_state.search_folders.append(new_folder)
                    st.success("✅ Added!")
                    st.rerun()
                else:
                    st.warning("⚠️ Already in list")
            else:
                st.error("❌ Folder not found")
        
        # Reset
        if st.button("🔄 Reset to Default"):
            st.session_state.search_folders = default_folders.copy()
            st.rerun()
        
        # Settings
        st.subheader("🔧 Settings")
        max_files = st.slider("Max files to index:", 100, 5000, 1000)
        top_k = st.slider("Results to show:", 5, 50, 10)
        
        # Build index
        if st.button("🔨 Build Index", type="primary"):
            if st.session_state.search_folders:
                with st.spinner("Building search index..."):
                    # Build index logic here
                    st.success("✅ Index built!")
            else:
                st.warning("⚠️ Add some folders first")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🔍 Search")
        
        # Search input
        query = st.text_input(
            "Enter your search query:",
            placeholder="e.g., PASSCODE variable, function name, error message...",
            key="search_query"
        )
        
        if st.button("🚀 Search", type="primary"):
            if not query:
                st.warning("⚠️ Please enter a search query")
            else:
                with st.spinner("🔍 Searching..."):
                    # Search logic here
                    st.success("✅ Search completed!")
                    
                    # Mock results for demo
                    results = [
                        {
                            "file_path": "C:/Users/Ibrah/Desktop/Research-Jummana/LEANN/apps/simple_demo.py",
                            "content": "PASSCODE = 'secret123'",
                            "score": 0.95
                        },
                        {
                            "file_path": "C:/Users/Ibrah/Desktop/Research-Jummana/LEANN/apps/ollama_demo.py",
                            "content": "password = 'admin123'",
                            "score": 0.87
                        }
                    ]
                    
                    for i, result in enumerate(results):
                        with st.expander(f"📄 {Path(result['file_path']).name} (Score: {result['score']:.3f})"):
                            st.code(result['content'], language="text")
                            st.text(f"📁 Path: {result['file_path']}")
    
    with col2:
        st.header("📊 Status")
        
        # Folder status
        st.subheader("📁 Folders")
        for folder in st.session_state.search_folders:
            if os.path.exists(folder):
                st.success(f"✅ {Path(folder).name}")
            else:
                st.error(f"❌ {Path(folder).name}")
        
        # Performance
        st.subheader("⚡ Performance")
        st.info("")
        **Expected Times:**
        • Small folders: 1-5 seconds
        • Medium folders: 5-15 seconds
        • Large folders: 15-60 seconds
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("**🔍 Laptop Search** - Powered by LEANN")
    st.caption("AI-powered search for your entire laptop")

if __name__ == "__main__":
    main()