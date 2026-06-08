"""embed.py — Stage 3 (EMBED + STORE): embed chunks and store them in ChromaDB.

chunk.py writes the combined chunk list to documents/chunks.json. This stage
embeds each chunk's `text` field with all-MiniLM-L6-v2 and stores the resulting
vector alongside the chunk's metadata in a persistent ChromaDB collection, so
retriever.py (Stage 4) can run semantic search over the corpus.

We don't compute embeddings by hand: ChromaDB's SentenceTransformerEmbeddingFunction
is attached to the collection, so handing `collection.add()` the raw text strings
lets ChromaDB vectorize them with the same model retrieval will use for queries.

Run `python embed.py` to (re)build the vector store from documents/chunks.json.
"""

import json
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions
from config import EMBEDDING_MODEL, CHROMA_PATH, CHROMA_COLLECTION

CHUNKS_PATH = "documents/chunks.json"

# Fields that are NOT stored as metadata: `text` is the document body ChromaDB
# embeds, and `chunk_id` becomes the entry id. Everything else travels as metadata.
_NON_METADATA_FIELDS = {"text", "chunk_id"}

# Embedding function and client are created once at import. sentence-transformers
# downloads the model on first use (30-60s the first time, cached after).
_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
_client = chromadb.PersistentClient(path=CHROMA_PATH)


def get_collection():
    """Return the persistent ChromaDB collection, creating it if needed.

    Cosine space matches the retrieval stage: all-MiniLM-L6-v2 vectors are
    compared by cosine distance.
    """
    return _client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        embedding_function=_ef, # type: ignore
        metadata={"hnsw:space": "cosine"},
    )


def _metadata(chunk: dict) -> dict:
    """Build a chunk's metadata dict: every field except `text` and `chunk_id`.

    ChromaDB metadata values must be str/int/float/bool — None is rejected — so
    null-valued fields (e.g. `rating` on RateMyDorm, `dorm` on Reddit) are
    dropped rather than stored. The fields differ per source type by design;
    retrieval reads them defensively with .get().
    """
    return {
        key: value
        for key, value in chunk.items()
        if key not in _NON_METADATA_FIELDS and value is not None
    }


def embed_and_store(chunks: list[dict]) -> int:
    """Embed `chunks` and store them in the ChromaDB collection.

    Builds three parallel lists from the chunk dicts produced by chunk.py and
    hands them to collection.add(); ChromaDB embeds the documents via the
    attached SentenceTransformer function.
      - documents : raw chunk text (chunk["text"])
      - metadatas : one dict per chunk — all fields except `text`/`chunk_id`,
                    with None-valued fields omitted
      - ids       : chunk["chunk_id"]

    Returns the collection's total entry count after the add.
    """
    if not chunks:
        print("No chunks to embed.")
        return get_collection().count()

    collection = get_collection()
    collection.add(
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[_metadata(chunk) for chunk in chunks],
        ids=[chunk["chunk_id"] for chunk in chunks],
    )
    total = collection.count()
    print(f"Stored {len(chunks)} chunk(s); collection now holds {total} entr(ies).")
    
    # View the first 5 records
    # preview = collection.get(limit=5)
    # print(preview)

    return total


def main():
    chunks = json.loads(Path(CHUNKS_PATH).read_text(encoding="utf-8"))

    # Rebuild from scratch so re-runs are idempotent and the count check below is
    # meaningful: collection.add() would otherwise error on already-present ids.
    try:
        _client.delete_collection(CHROMA_COLLECTION)
    except Exception:
        pass  # collection didn't exist yet — nothing to clear

    stored = embed_and_store(chunks)

    # Verification: the stored count must equal the number of source chunks.
    print(f"\nSource chunks: {len(chunks)} | Stored in ChromaDB: {stored}")
    print("Count match:", "OK" if stored == len(chunks) else "MISMATCH")
    


if __name__ == "__main__":
    main()
