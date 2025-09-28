#!/usr/bin/env python3
"""
🚀 UltraSearch - Lightning Fast RAG Search
Ultra-fast search system using RAG technology for laptop-wide searching
"""

import os
import sys
import time
import json
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional
import streamlit as st
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
from datetime import datetime
import re

# Configuration
DEFAULT_SEARCH_FOLDERS = [
    ".",
    "C:/Users/Ibrah/Documents",
    "C:/Users/Ibrah/Desktop",
    "C:/Users/Ibrah/Desktop/Research-Jummana"
]

SEARCH_EXTENSIONS = ['.py', '.txt', '.md', '.json', '.yaml', '.yml', '.csv', '.log', '.js', '.html', '.css', '.xml', '.sql', '.java', '.cpp', '.c', '.h']

class UltraSearch:
    def __init__(self):
        self.model = None
        self.index = None
        self.documents = []
        self.embeddings = []
        self.folder_stats = {}
        
    def load_model(self):
        """Load the sentence transformer model"""
        if self.model is None:
            with st.spinner("🤖 Loading AI model..."):
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
        return self.model
    
    def build_index(self, folders: List[str], max_files: int = 1000):
        """Build search index from folders"""
        self.documents = []
        self.embeddings = []
        self.folder_stats = {}
        
        total_files = 0
        processed_files = 0
        
        # Count total files first
        for folder in folders:
            if not os.path.exists(folder):
                continue
            for root, _, files in os.walk(folder):
                for file in files:
                    if any(file.endswith(ext) for ext in SEARCH_EXTENSIONS):
                        total_files += 1
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Process files
        for folder in folders:
            if not os.path.exists(folder):
                continue
                
            folder_files = 0
            for root, _, files in os.walk(folder):
                for file in files:
                    if any(file.endswith(ext) for ext in SEARCH_EXTENSIONS):
                        if processed_files >= max_files:
                            break
                            
                        file_path = Path(root) / file
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                
                            # Chunk content if too large
                            chunks = self._chunk_text(content, max_chunk_size=1000)
                            
                            for i, chunk in enumerate(chunks):
                                if chunk.strip():
                                    self.documents.append({
                                        'file_path': str(file_path),
                                        'content': chunk,
                                        'folder': folder,
                                        'chunk_id': i,
                                        'file_size': len(content)
                                    })
                            
                            folder_files += 1
                            processed_files += 1
                            
                            # Update progress
                            progress = processed_files / min(total_files, max_files)
                            progress_bar.progress(progress)
                            status_text.text(f"Processing {file_path.name}... ({processed_files}/{min(total_files, max_files)})")
                            
                        except Exception as e:
                            continue
                            
            self.folder_stats[folder] = {
                'files_processed': folder_files,
                'exists': True
            }
        
        # Generate embeddings
        if self.documents:
            status_text.text("🤖 Generating embeddings...")
            model = self.load_model()
            
            texts = [doc['content'] for doc in self.documents]
            self.embeddings = model.encode(texts, show_progress_bar=True)
            
            # Build FAISS index
            status_text.text("🔍 Building search index...")
            dimension = self.embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(self.embeddings)
            self.index.add(self.embeddings)
            
            status_text.text(f"✅ Index built with {len(self.documents)} documents")
            progress_bar.progress(1.0)
        
        return len(self.documents)
    
    def _chunk_text(self, text: str, max_chunk_size: int = 1000) -> List[str]:
        """Split text into chunks"""
        if len(text) <= max_chunk_size:
            return [text]
        
        chunks = []
        words = text.split()
        current_chunk = []
        current_size = 0
        
        for word in words:
            if current_size + len(word) + 1 > max_chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_size = len(word)
            else:
                current_chunk.append(word)
                current_size += len(word) + 1
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Search using RAG"""
        if not self.index or not self.documents:
            return []
        
        start_time = time.time()
        
        # Generate query embedding
        model = self.load_model()
        query_embedding = model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.documents):
                doc = self.documents[idx]
                results.append({
                    'file_path': doc['file_path'],
                    'content': doc['content'],
                    'folder': doc['folder'],
                    'score': float(score),
                    'chunk_id': doc['chunk_id']
                })
        
        search_time = time.time() - start_time
        
        return results, search_time
    
    def get_folder_stats(self) -> Dict[str, Any]:
        """Get statistics about indexed folders"""
        return self.folder_stats

def main():
    st.set_page_config(
        page_title="🚀 UltraSearch",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 UltraSearch - Lightning Fast RAG Search")
    st.markdown("**Ultra-fast search system using RAG technology for your entire laptop**")
    
    # Initialize session state
    if 'ultra_search' not in st.session_state:
        st.session_state.ultra_search = UltraSearch()
    
    if 'search_folders' not in st.session_state:
        st.session_state.search_folders = DEFAULT_SEARCH_FOLDERS.copy()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Search folders
        st.subheader("📁 Search Folders")
        
        # Display current folders
        for i, folder in enumerate(st.session_state.search_folders):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text(folder)
            with col2:
                if st.button("🗑️", key=f"remove_{i}"):
                    st.session_state.search_folders.pop(i)
                    st.rerun()
        
        # Add new folder
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
        
        # Reset folders
        if st.button("🔄 Reset to Default"):
            st.session_state.search_folders = DEFAULT_SEARCH_FOLDERS.copy()
            st.rerun()
        
        # Search settings
        st.subheader("🔧 Search Settings")
        max_files = st.slider("Max files to index:", 100, 5000, 1000)
        top_k = st.slider("Results to show:", 5, 50, 10)
        
        # Build index button
        if st.button("🔨 Build Index", type="primary"):
            if st.session_state.search_folders:
                with st.spinner("Building search index..."):
                    doc_count = st.session_state.ultra_search.build_index(
                        st.session_state.search_folders, 
                        max_files
                    )
                    st.success(f"✅ Index built with {doc_count} documents!")
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
            elif not st.session_state.ultra_search.index:
                st.warning("⚠️ Build index first!")
            else:
                with st.spinner("🔍 Searching..."):
                    results, search_time = st.session_state.ultra_search.search(query, top_k)
                
                if results:
                    st.success(f"✅ Found {len(results)} results in {search_time:.3f}s")
                    
                    # Display results
                    for i, result in enumerate(results):
                        with st.expander(f"📄 {Path(result['file_path']).name} (Score: {result['score']:.3f})"):
                            st.code(result['content'], language="text")
                            st.text(f"📁 Path: {result['file_path']}")
                            st.text(f"📂 Folder: {result['folder']}")
                            st.text(f"🎯 Score: {result['score']:.3f}")
                    
                    # AI Analysis
                    st.subheader("🤖 AI Analysis")
                    analysis = f"Found {len(results)} relevant results for '{query}':\n\n"
                    
                    # Group by file type
                    file_types = {}
                    folders_found = set()
                    
                    for result in results:
                        ext = Path(result['file_path']).suffix
                        file_types[ext] = file_types.get(ext, 0) + 1
                        folders_found.add(result['folder'])
                    
                    analysis += f"📁 Folders: {len(folders_found)}\n"
                    analysis += f"📄 File types: {', '.join(file_types.keys())}\n\n"
                    
                    if file_types:
                        most_common = max(file_types.items(), key=lambda x: x[1])
                        analysis += f"Most common: {most_common[0]} ({most_common[1]} files)\n\n"
                    
                    analysis += "Top matches:\n"
                    for i, result in enumerate(results[:3]):
                        analysis += f"{i+1}. {Path(result['file_path']).name} (Score: {result['score']:.3f})\n"
                    
                    st.write(analysis)
                    
                else:
                    st.warning("⚠️ No results found")
                    st.info("💡 Try:")
                    st.text("• Different keywords")
                    st.text("• Build index first")
                    st.text("• Check folder paths")
    
    with col2:
        st.header("📊 Index Status")
        
        if st.session_state.ultra_search.folder_stats:
            for folder, stats in st.session_state.ultra_search.folder_stats.items():
                if stats['exists']:
                    st.success(f"✅ {Path(folder).name}")
                    st.text(f"📄 Files: {stats['files_processed']}")
                else:
                    st.error(f"❌ {Path(folder).name}")
                st.divider()
        
        # Performance info
        st.header("⚡ Performance")
        st.info("""
        **Expected Times:**
        • Index building: 30-120s
        • Search: < 0.1s
        • AI analysis: < 0.5s
        """)
        
        # Index info
        if st.session_state.ultra_search.index:
            st.success(f"✅ Index ready: {len(st.session_state.ultra_search.documents)} documents")
        else:
            st.warning("⚠️ No index built yet")
    
    # Footer
    st.markdown("---")
    st.markdown("**🚀 UltraSearch** - Lightning Fast RAG Search")
    st.caption("Powered by Sentence Transformers + FAISS + Streamlit")

if __name__ == "__main__":
    main()