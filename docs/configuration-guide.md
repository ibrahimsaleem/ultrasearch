# 🔧 LEANN Configuration Guide

This guide covers all aspects of configuring and setting up LEANN for optimal performance.

## 📦 Installation

### 🐍 Python Installation
```bash
# Install from PyPI
pip install leann

# Install from source
git clone https://github.com/your-org/leann.git
cd leann
pip install -e .
```

### 🔧 Dependencies
```bash
# Core dependencies
pip install sentence-transformers numpy torch

# Optional backends
pip install faiss-cpu  # For HNSW backend
pip install diskann   # For DiskANN backend

# Optional features
pip install openai    # For OpenAI embeddings
pip install ollama    # For Ollama integration
```

## ⚙️ Basic Configuration

### 🚀 Quick Start
```python
from leann import LeannBuilder, LeannSearcher

# Basic configuration
builder = LeannBuilder(
    embedding_model="all-MiniLM-L6-v2",
    backend_name="hnsw"
)
```

### 🔧 Advanced Configuration
```python
# Advanced configuration
builder = LeannBuilder(
    embedding_model="all-MiniLM-L6-v2",
    embedding_mode="sentence-transformers",
    backend_name="hnsw",
    chunking_strategy="ast_aware",
    max_chunk_size=1000,
    overlap_size=100
)
```

## 🧠 Embedding Models

### 📊 Supported Models
- **Sentence Transformers**: `all-MiniLM-L6-v2`, `all-mpnet-base-v2`
- **OpenAI**: `text-embedding-ada-002`, `text-embedding-3-small`
- **Ollama**: `mxbai-embed-large`, `nomic-embed-text`
- **Custom**: Any compatible embedding model

### 🔧 Model Configuration
```python
# Sentence Transformers
builder = LeannBuilder(
    embedding_model="all-MiniLM-L6-v2",
    embedding_mode="sentence-transformers"
)

# OpenAI
builder = LeannBuilder(
    embedding_model="text-embedding-ada-002",
    embedding_mode="openai",
    openai_api_key="your-api-key"
)

# Ollama
builder = LeannBuilder(
    embedding_model="mxbai-embed-large:latest",
    embedding_mode="ollama"
)
```

## 🏗️ Backend Configuration

### 🔧 HNSW Backend
```python
# HNSW configuration
builder = LeannBuilder(
    backend_name="hnsw",
    hnsw_config={
        "m": 16,                    # Number of bi-directional links
        "ef_construction": 200,    # Construction parameter
        "ef_search": 50,           # Search parameter
        "max_elements": 1000000    # Maximum elements
    }
)
```

### 💾 DiskANN Backend
```python
# DiskANN configuration
builder = LeannBuilder(
    backend_name="diskann",
    diskann_config={
        "max_degree": 64,          # Maximum degree
        "construction_memory": "8GB",  # Construction memory
        "search_memory": "2GB",    # Search memory
        "num_threads": 8           # Number of threads
    }
)
```

## 📄 Chunking Configuration

### 🔧 AST-aware Chunking
```python
# AST-aware chunking for code
builder = LeannBuilder(
    chunking_strategy="ast_aware",
    ast_config={
        "max_chunk_size": 1000,
        "overlap_size": 100,
        "preserve_structure": True,
        "language": "python"  # or "javascript", "java", etc.
    }
)
```

### 📝 Document Chunking
```python
# Document chunking
builder = LeannBuilder(
    chunking_strategy="document",
    document_config={
        "max_chunk_size": 1000,
        "overlap_size": 100,
        "preserve_paragraphs": True,
        "split_on_sentences": True
    }
)
```

## 🔍 Search Configuration

### 🎯 Basic Search
```python
# Basic search
searcher = LeannSearcher("index.leann")
results = searcher.search("query", top_k=10)
```

### 🔧 Advanced Search
```python
# Advanced search with filtering
results = searcher.search(
    "query",
    top_k=10,
    metadata_filter={
        "type": "code",
        "language": "python",
        "date": {"$gte": "2024-01-01"}
    },
    similarity_threshold=0.7
)
```

### 🔍 Hybrid Search
```python
# Hybrid search (vector + text)
results = searcher.hybrid_search(
    "query",
    vector_weight=0.7,
    text_weight=0.3,
    top_k=10
)
```

## 🚀 Performance Tuning

### ⚡ Speed Optimization
```python
# Speed-optimized configuration
builder = LeannBuilder(
    embedding_model="all-MiniLM-L6-v2",  # Fast model
    backend_name="hnsw",
    hnsw_config={
        "m": 8,                     # Lower M for speed
        "ef_construction": 100,    # Lower ef for speed
        "ef_search": 20            # Lower ef for speed
    }
)
```

### 💾 Memory Optimization
```python
# Memory-optimized configuration
builder = LeannBuilder(
    embedding_model="all-MiniLM-L6-v2",
    backend_name="hnsw",
    hnsw_config={
        "max_elements": 100000,    # Limit elements
        "construction_memory": "2GB"  # Limit memory
    }
)
```

### 🔧 Storage Optimization
```python
# Storage-optimized configuration
builder = LeannBuilder(
    embedding_model="all-MiniLM-L6-v2",
    backend_name="hnsw",
    chunking_strategy="ast_aware",
    max_chunk_size=500,           # Smaller chunks
    overlap_size=50               # Less overlap
)
```

## 🔒 Security Configuration

### 🛡️ Access Control
```python
# Access control configuration
builder = LeannBuilder(
    access_control=True,
    permissions={
        "read": ["user1", "user2"],
        "write": ["admin"],
        "delete": ["admin"]
    }
)
```

### 🔐 Encryption
```python
# Encryption configuration
builder = LeannBuilder(
    encryption=True,
    encryption_key="your-secret-key",
    encryption_algorithm="AES-256"
)
```

## 📊 Monitoring Configuration

### 📈 Metrics
```python
# Enable metrics
builder = LeannBuilder(
    metrics=True,
    metrics_config={
        "enable_performance": True,
        "enable_usage": True,
        "enable_errors": True
    }
)
```

### 📝 Logging
```python
# Logging configuration
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

builder = LeannBuilder(
    logging=True,
    log_level="INFO"
)
```

## 🚀 Deployment Configuration

### 🐳 Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]
```

### ☁️ Cloud Deployment
```python
# Cloud configuration
builder = LeannBuilder(
    cloud_config={
        "provider": "aws",  # or "gcp", "azure"
        "region": "us-east-1",
        "instance_type": "t3.medium"
    }
)
```

## 🔧 Troubleshooting

### ❌ Common Issues

#### Import Errors
```bash
# Install missing dependencies
pip install sentence-transformers numpy torch
```

#### Memory Issues
```python
# Reduce memory usage
builder = LeannBuilder(
    max_elements=50000,  # Limit elements
    construction_memory="1GB"  # Limit memory
)
```

#### Performance Issues
```python
# Optimize for performance
builder = LeannBuilder(
    hnsw_config={
        "m": 8,              # Lower M
        "ef_construction": 100,  # Lower ef
        "ef_search": 20     # Lower ef
    }
)
```

### 🔧 Debug Mode
```python
# Enable debug mode
builder = LeannBuilder(
    debug=True,
    verbose=True
)
```

## 📚 Additional Resources

- **Features Guide**: See `features.md`
- **API Reference**: See `api.md`
- **Examples**: See `examples/` directory
- **FAQ**: See `faq.md`
- **Community**: Join our Discord server

## 📄 License

MIT License - Feel free to use and modify!