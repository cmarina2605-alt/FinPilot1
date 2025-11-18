
# ------------------------------------------------------------

import os
import re
from typing import List, Dict, Any, Optional, Union

import fitz  # PyMuPDF
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from sentence_transformers import SentenceTransformer


# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------
PERSIST_DIR = "chroma_db"
COLLECTION_NAME = "finpilot_documents"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_WORDS = 400  # chunk size ~400 words


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def clean_text(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def split_words(text: str) -> List[str]:
    return [w for w in re.split(r"\s+", text) if w]


def chunk_text_words(text: str, chunk_size: int = CHUNK_WORDS) -> List[str]:
    """
    Splits a text into word-based chunks.
    """
    tokens = split_words(text)
    chunks = []
    for i in range(0, len(tokens), chunk_size):
        chunk = " ".join(tokens[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks


def extract_pdf_pages(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Returns: [{page: 1, text: "..."} , ...]
    """
    pages = []
    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc):
            text = clean_text(page.get_text("text"))
            if text:
                pages.append({"page": i + 1, "text": text})
    return pages


# ------------------------------------------------------------
# CHROMA DB INITIALIZATION
# ------------------------------------------------------------
def get_collection():
    os.makedirs(PERSIST_DIR, exist_ok=True)
    client = chromadb.PersistentClient(path=PERSIST_DIR)

    col = client.get_or_create_collection(
        COLLECTION_NAME,
        embedding_function=SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL),
        metadata={"hnsw:space": "cosine"}
    )
    return col


# ------------------------------------------------------------
# INGEST — PAGE + CHUNK METADATA (REAL)
# ------------------------------------------------------------
def ingest_pdf(source: Union[str, bytes], filename: str = None):
    """
    FULL ingestion with REAL: filename + page + chunk metadata.
    Works with any standard PDF.
    """
    try:
        # --- Load PDF ---
        if isinstance(source, bytes):
            if filename is None:
                filename = "uploaded.pdf"
            doc = fitz.open(stream=source, filetype="pdf")
        else:
            if not os.path.exists(source):
                raise FileNotFoundError(f"PDF not found: {source}")
            doc = fitz.open(source)
            filename = os.path.basename(source) if filename is None else filename

        chunks = []
        metadatas = []

        # --- Extract and chunk per page ---
        for page_idx, page in enumerate(doc):
            page_num = page_idx + 1
            text = clean_text(page.get_text("text"))

            if not text:
                continue

            page_chunks = chunk_text_words(text, CHUNK_WORDS)

            for ci, chunk in enumerate(page_chunks):
                chunks.append(chunk)
                metadatas.append({
                    "source": filename,
                    "page": page_num,
                    "chunk": ci
                })

        if not chunks:
            return {"status": "warning", "message": "No text found in PDF"}

        # --- Embeddings ---
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(chunks).tolist()

        # --- Save to Chroma ---
        collection = get_collection()
        ids = [f"{filename}_p{m['page']}_c{m['chunk']}" for m in metadatas]

        collection.add(
            ids=ids,
            documents=chunks,
            metadatas=metadatas,
            embeddings=embeddings
        )

        return {
            "status": "ok",
            "source": filename,
            "chunks": len(chunks),
            "message": f"PDF '{filename}' ingested with {len(chunks)} chunks and metadata"
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


def ingest_folder(folder: str):
    """Bulk ingestion."""
    if not os.path.isdir(folder):
        raise NotADirectoryError(folder)
    results = []
    for f in sorted(os.listdir(folder)):
        if f.lower().endswith(".pdf"):
            path = os.path.join(folder, f)
            results.append(ingest_pdf(path, filename=f))
    return results


# ------------------------------------------------------------
# QUERY
# ------------------------------------------------------------
def query(question: str, k: int = 4, where: Optional[Dict[str, Any]] = None):
    """
    Semantic search (RAG). Returns chunks with metadata.
    """
    col = get_collection()

    res = col.query(
        query_texts=[question],
        n_results=max(k, 1),
        where=where,
        include=["documents", "metadatas", "distances"]
    )

    docs = res["documents"][0]
    metas = res["metadatas"][0]
    dists = res["distances"][0]

    items = []
    for d, m, dist in zip(docs, metas, dists):
        items.append({
            "text": d,
            "source": m["source"],
            "page": m["page"],
            "chunk": m["chunk"],
            "distance": float(dist)
        })

    return {"question": question, "results": items}


# ------------------------------------------------------------
# CONTEXT BUILDER FOR LLM
# ------------------------------------------------------------
def build_context(results: Dict[str, Any]) -> str:
    """
    Formats retrieved chunks into a single context block:
      [Filename p.X c.Y] text...
    """
    lines = []
    for r in results.get("results", []):
        tag = f"[{r['source']} p.{r['page']} c.{r['chunk']}]"
        lines.append(f"{tag} {r['text']}")
    return "\n\n".join(lines)
