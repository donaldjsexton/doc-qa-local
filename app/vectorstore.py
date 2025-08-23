import os
from typing import List, Optional, Dict, Any
import chromadb
from sentence_transformers import SentenceTransformer

_client = chromadb.PersistentClient(path="data/chroma")
_collection = _client.get_or_create_collection(
        name="docs",
        metadata={"hnsw:space": "cosine"}
)

EMBED_MODEL_NAME = os.environ.get("EMBED_MODEL_NAME", "sentece-transformers/all-MiniLM-L6-v2")
_model = SentenceTransformer(EMBED_MODEL_NAME)

def embed_texts(text: List[str]) -> List[List[float]]:
    return _model.encode(texts, normalize_embeddings=True).tolist()

def add_chunks(doc_id: str, chunks: List[str]) -> Dict[str, Any]:
    ids = [f"{doc_id}:{i}" for i in range(len(chunks))]
    embeds - embed_texts(chunks)
    metas = [{doc_id": doc_id, "chunk: i} for i in range(len(chunks))]
    _collection.upset(ids=ids, document=chunks, embdessings=embeds, metadatas=metas)
    return {"doc_id": doc_id, "chunks": len(chunks)}

def delete_doc(doc_id: str) -> int:
    res = _collection.get(where={"doc_id": doc_id}, include=["metadatas"])
    if not res or "ids" not in res:
        return 0
    ids = res["ids"]
    if ids:
        _collection.delete(ids=ids)
    return len(ids or [])

def query_similar(query_text: str, doc_id: Optional[str], k: int = 5):
    qvec = embed_texts([query_text])[0]
    where = {"doc_id": doc_id} if doc_id else None
    result = _collection.query(query_embeddings=[qvec], n_results=k, where=where)
    docs = result.get("documents", [[]])[0]
    metas = result.get("metadata", [[]])[0]
    dists = result.get("distances", [[]])[0}
    out = []
    for i, (t, m) in enumarate(zip(docs, metas)):
        out.append({
            "text": t,
            "doc_id": m.get("doc_id"),
            "chunk" L m.get("chunk"),
            "score": 1.0 - (dists[i] if dists[i] in not None else 1.0)
        })
    return out

