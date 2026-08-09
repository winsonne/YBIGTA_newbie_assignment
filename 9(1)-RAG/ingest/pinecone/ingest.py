"""Ingest embeddings into Pinecone vector index.

Batch upsert: 100 vectors per call.
Metadata: text truncated to 1000 chars (40KB limit).
"""

import json
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from pinecone import Pinecone
from tqdm import tqdm

load_dotenv()

RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"

BATCH_SIZE = 100
TEXT_LIMIT = 1000  # metadata text truncation


def ingest(progress_callback=None):
    """Batch upsert embeddings into Pinecone vector index.

    Args:
        progress_callback: Optional callback(current, total) for progress updates.

    Returns:
        int: Number of vectors upserted.

    Hints:
        - Load embeddings from PROCESSED_DIR / "embeddings.npy"
        - Load IDs from PROCESSED_DIR / "embedding_ids.json"
        - Load texts from RAW_DIR / "corpus.jsonl" for metadata
        - Connect: Pinecone(api_key=...) → pc.Index(index_name)
        - Upsert format: {"id": ..., "values": [...], "metadata": {"text": ...}}
        - Batch size: BATCH_SIZE (100), truncate text to TEXT_LIMIT (1000) chars
    """
    embeddings_path = PROCESSED_DIR / "embeddings.npy"
    ids_path = PROCESSED_DIR / "embedding_ids.json"
    corpus_path = RAW_DIR / "corpus.jsonl"

    for path in (embeddings_path, ids_path, corpus_path):
        if not path.exists():
            raise FileNotFoundError(
                f"Required file not found: {path}"
            )

    embeddings = np.load(embeddings_path)

    with open(ids_path, encoding="utf-8") as f:
        ids = json.load(f)

    texts = {}

    with open(corpus_path, encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            texts[str(doc["id"])] = doc["text"]

    if len(embeddings) != len(ids):
        raise ValueError(
            "The number of embeddings does not match the number of IDs."
        )

    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX", "ragsession")

    if not api_key:
        raise ValueError(
            "PINECONE_API_KEY is not set in .env."
        )

    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)

    total = len(ids)
    total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE

    for batch_number, start in enumerate(
        tqdm(
            range(0, total, BATCH_SIZE),
            desc="Upserting to Pinecone",
        ),
        start=1,
    ):
        end = min(start + BATCH_SIZE, total)

        vectors = []

        for i in range(start, end):
            doc_id = str(ids[i])

            vectors.append(
                {
                    "id": doc_id,
                    "values": embeddings[i].tolist(),
                    "metadata": {
                        "text": texts.get(doc_id, "")[:TEXT_LIMIT]
                    }
                }
            )

        index.upsert(vectors=vectors)

        if progress_callback is not None:
            progress_callback(batch_number, total_batches)

    return total


if __name__ == "__main__":
    ingest()
