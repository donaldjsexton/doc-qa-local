# Doc Q&A (Local)

Local-only document Q&A with FastAPI, sentence-transformers (embeddings), Chroma (vector DB), and an extractive QA model (Transformers).

## Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

## Run
uvicorn app.main:app --reload
# open http://127.0.0.1:8000

## Models
- Embeddings: sentence-transformers/all-MiniLM-L6-v2
- QA: distilbert-base-cased-distilled-squad
Swap QA model:
export QA_MODEL=deepset/roberta-base-squad2
