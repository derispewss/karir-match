"""Cosine similarity scoring with configurable field weights."""

import json
import pickle
import numpy as np
import yaml
from pathlib import Path
from scipy import sparse
from sklearn.metrics.pairwise import linear_kernel


def load_config():
    with open("config/preprocess.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_index(index_dir: Path):
    with open(index_dir / "docs.json", "r", encoding="utf-8") as f:
        docs = json.load(f)

    field_vec = {}
    for field in ("title", "skills", "description"):
        with open(index_dir / f"{field}_vectorizer.pkl", "rb") as f:
            vec = pickle.load(f)
        mat = sparse.load_npz(index_dir / f"{field}_matrix.npz")
        field_vec[field] = (vec, mat)

    return docs, field_vec


def rank_query(query_text: str, docs, field_vec, weights, top_k=10):
    total_docs = len(docs)
    combined_scores = np.zeros(total_docs)

    for field, (vec, mat) in field_vec.items():
        w = weights.get(field, 0.33)
        q_vec = vec.transform([query_text])
        sims = linear_kernel(q_vec, mat).flatten()
        combined_scores += w * sims

    doc_ids = [d["id"] for d in docs]
    # Tie-break deterministik: score descending, doc_id ascending
    scored_pairs = list(zip(doc_ids, combined_scores))
    scored_pairs.sort(key=lambda x: (-x[1], x[0]))

    return scored_pairs[:top_k]


def run_scoring(query_path: Path, index_dir: Path, out_path: Path, top_k=10):
    cfg = load_config()
    weights = cfg.get("field_weights", {"title": 0.4, "skills": 0.3, "description": 0.3})
    docs, field_vec = load_index(index_dir)

    with open(query_path, "r", encoding="utf-8") as f:
        queries = json.load(f)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as out_f:
        for q in queries:
            qid = q["id"]
            q_text = q.get("query", "")
            ranked = rank_query(q_text, docs, field_vec, weights, top_k=top_k)
            for rank, (did, score) in enumerate(ranked, start=1):
                out_f.write(f"{qid} Q0 {did} {rank} {score:.4f} tfidf\n")

    print(f"Run file TF-IDF written to {out_path}")


if __name__ == "__main__":
    run_scoring(
        query_path=Path("research/queries_clean.json"),
        index_dir=Path("artifacts/tfidf_index"),
        out_path=Path("artifacts/run_tfidf.txt"),
    )
