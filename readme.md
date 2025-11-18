# FinPilot AI – Academic Documentation
### *Local Retrieval-Augmented Generation System for Document Analysis*

---

## 1. Introduction

FinPilot AI is an academic project that demonstrates how Retrieval-Augmented Generation (RAG) can be combined with a fully local Large Language Model (LLM) using Ollama to create a secure, offline knowledge assistant for professionals.

The system enables users to upload internal PDFs, extract and index their contents with semantic embeddings, and query them using natural language—receiving accurate answers grounded strictly in the original documents.

FinPilot showcases a transparent, reproducible, and privacy-preserving AI workflow capable of supporting knowledge-intensive work across sectors: legal, compliance, HR, auditing, policy, research, and general corporate operations. All processing, retrieval, and inference run entirely on-device, ensuring full data control, traceability, and verifiable outputs.

---

## 2. Objectives of the Project

The project aims to:

1. Implement a complete RAG system using local documents and vector embeddings.
2. Demonstrate the extraction and processing of financial documentation.
3. Provide traceable, page-level citations for all model responses.
4. Run fully offline using local LLM inference through Ollama.
5. Provide an intuitive and clear user interface.
6. Automatically load models if they are not already installed.
7. Include platform-specific launch scripts for Windows and Linux.

---

## 3. System Features

- 100% offline execution
- PDF ingestion and extraction
- Page-level metadata tracking
- 400-word semantic chunking
- Vector embeddings via `all-MiniLM-L6-v2` (Sentence Transformers)
- Persistent vector storage with ChromaDB
- Automatic download of missing models
- Local LLM inference via Ollama
- Custom UI with chat interface and model selection
- Loading spinner while PDFs ingest
- Platform-specific startup scripts:
  - **start.bat** for Windows
  - **start.sh** for Linux

---

## 4. Startup Scripts (Windows & Linux)

To simplify usage in academic environments, FinPilot AI includes native launch scripts:

### **4.1 Windows – `start.bat`**
Runs the virtual environment and starts the server automatically.

```bat
@echo off
call venv\Scripts\activate
uvicorn app:app --reload
pause
```

### **4.2 Linux – `start.sh`**
Enables execution, activates the venv, and launches the server.

```bash
#!/bin/bash
source venv/bin/activate
uvicorn app:app --reload
```text

Make it executable:

```bash
chmod +x start.sh
```

---

## 5. Automatic Model Loading

FinPilot AI checks whether the selected model is installed locally.
If missing, the system automatically:

1. Detects the missing model
2. Executes `ollama pull <model>`
3. Waits for installation
4. Continues processing

This ensures the system works seamlessly on first launch without prior setup.

---

## 6. Architecture Overview

FinPilot AI consists of three main layers:

### **6.1 Document Processing**
- PDF text extraction
- Cleaning and normalization
- 400-word chunking
- Embedding generation
- Metadata storage in ChromaDB

### **6.2 Retrieval Augmentation (RAG Engine)**
- Converts queries to embeddings
- Performs semantic similarity search
- Selects relevant chunks
- Provides grounded context

### **6.3 Local LLM Inference**
- Injects retrieved context into prompts
- Runs locally via Ollama
- Produces verifiable answers with citations

---

## 7. System Diagram (Academic Format)

```
                 ┌───────────────────────────┐
                 │         PDF Upload        │
                 └─────────────┬─────────────┘
                               ▼
                     ┌────────────────┐
                     │ Text Extraction│
                     └────────┬───────┘
                              ▼
                      ┌───────────────┐
                      │   Chunking     │
                      └───────┬────────┘
                              ▼
                     ┌─────────────────┐
                     │  Embeddings     │
                     └────────┬────────┘
                              ▼
                  ┌───────────────────────┐
                  │  ChromaDB Vector Store│
                  └─────────┬─────────────┘
                            ▼
                ┌────────────────────────────┐
                │  User Query (Web Interface) │
                └────────────┬───────────────┘
                             ▼
                   ┌─────────────────┐
                   │  Semantic RAG   │
                   └─────────┬────────┘
                             ▼
                   ┌──────────────────────┐
                   │ Local LLM (Ollama)   │
                   └─────────┬────────────┘
                             ▼
              ┌────────────────────────────┐
              │ Final Answer + Citations   │
              └────────────────────────────┘
```

---

## 8. Installation Guide

### **8.1 Clone repository**
```bash
git clone <https://github.com/cmarina2605-alt/FinPilot1>
cd FinPilot
```

### **8.2 Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

### **8.3 Install requirements**
```bash
pip install -r requirements.txt
```

### **8.4 Install Ollama**
<https://ollama.com>

### **8.5 (Optional) Pull models manually**
```bash
ollama pull llama3:8b
ollama pull gemma2:2b
ollama pull phi3
ollama pull mistral
```

### **8.6 Start the system**
Windows:
```bat
start.bat
```

Linux:
```bash
./start.sh
```

---

## 9. Citation Example

```text
[Financial_Manual.pdf p.12 c.0]
```

---

## 10. Example Questions for Evaluation

### **Governance & Internal Control**
- “Explain the distinction between ex-ante and ex-post internal controls.”
- “How do oversight bodies enforce accountability in financial operations?”

### **Budgeting & Fiscal Execution**
- “What phases make up the government budget cycle?”
- “How should deviations during budget execution be managed?”

### **Documentation & Auditing**
- “What evidence is required for validating a financial recommendation?”
- “Which recordkeeping standards ensure audit readiness?”

### **Risk Management**
- “What macroeconomic factors increase fiscal vulnerability?”
- “How should contingent liabilities be monitored?”

### **Financial Management Information Systems (FMIS)**
- “Which modules must an FMIS contain to support the full public finance cycle?”
- “How does process digitalization improve reporting accuracy?”

---

## 11. Academic Value

FinPilot AI demonstrates essential academic concepts:

### **11.1 Retrieval-Augmented Generation**
Shows how external knowledge grounds LLM answers.

### **11.2 Explainability**
All outputs cite exact document locations.

### **11.3 Offline Artificial Intelligence**
Highlights privacy-preserving AI systems.

### **11.4 Vector Databases**
Real-world application of embeddings and semantic search.

### **11.5 Full-Stack AI Engineering**
Integrates backend, frontend, RAG, and LLM inference into one complete system.

---

## 12. Conclusion

FinPilot AI is a fully functional academic demonstration of modern AI-driven document analysis.
Its architecture, offline operation, explainability, and practical utilities make it suitable for academic submission and professional evaluation.








