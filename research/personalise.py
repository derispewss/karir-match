"""Personalisation layer for KarirMatch (Phase 5).

Re-ranks the TF‑IDF results by combining query‑document similarity with
profile‑document similarity using a parameter alpha in [0, 1]:

FinalScore = (1 - alpha) * Score_TFIDF + alpha * Cosine(Profile, Doc)
"""

import json
import yaml
import pickle
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import linear_kernel
from scipy import sparse


def load_config():
    with open("config/preprocess.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_personalisation_config():
    with open("config/personalisation.yaml", "r", encoding="utf-8") as f:
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


def build_profile_vector(seed_doc_ids, docs, field_vec, weights):
    """Aggregate the TF‑IDF representations of seed documents into a profile vector."""
    doc_id_to_idx = {doc["id"]: idx for idx, doc in enumerate(docs)}
    seed_indices = [doc_id_to_idx[did] for did in seed_doc_ids if did in doc_id_to_idx]

    if not seed_indices:
        return None

    # Compute weighted profile similarities per field
    total_docs = len(docs)
    profile_field_sims = np.zeros(total_docs)

    for field, (vec, mat) in field_vec.items():
        w = weights.get(field, 0.33)
        # Average vector across seeds
        seed_submatrix = mat[seed_indices, :]
        profile_vec = seed_submatrix.mean(axis=0)
        profile_vec = np.asarray(profile_vec)
        # Cosine similarity against all documents
        sims = linear_kernel(profile_vec, mat).flatten()
        profile_field_sims += w * sims

    return profile_field_sims


def re_rank(tfidf_scores, profile_sims, alpha=0.5):
    """Combine TF-IDF scores and profile similarities using alpha weight."""
    if profile_sims is None:
        return tfidf_scores
    return (1.0 - alpha) * tfidf_scores + alpha * profile_sims


def run_personalisation_sweep(
    query_run_file: Path,
    index_dir: Path,
    profiles_file: Path,
    output_dir: Path,
    alphas=None,
    top_k: int = 10
):
    if alphas is None:
        alphas = [0.0, 0.5, 1.0]

    cfg = load_config()
    weights = cfg["field_weights"]
    docs, field_vec = load_index(index_dir)
    doc_ids = [d["id"] for d in docs]
    doc_id_to_idx = {did: idx for idx, did in enumerate(doc_ids)}

    with open(profiles_file, "r", encoding="utf-8") as f:
        profiles = json.load(f)

    # Precompute profile similarity vectors
    profile_sim_map = {}
    for p in profiles:
        pid = p["persona_id"]
        profile_sim_map[pid] = build_profile_vector(p["seed_doc_ids"], docs, field_vec, weights)

    # Read base TF-IDF run
    runs_by_query = {}
    with open(query_run_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 6:
                qid, _, did, rank, score, _ = parts[:6]
                if qid not in runs_by_query:
                    runs_by_query[qid] = []
                runs_by_query[qid].append((did, float(score)))

    output_dir.mkdir(parents=True, exist_ok=True)

    for alpha in alphas:
        out_file = output_dir / f"run_tfidf_alpha_{alpha:.1f}.txt"
        with open(out_file, "w", encoding="utf-8") as out_f:
            for qid, results in runs_by_query.items():
                # Pick a persona deterministically for the query
                assigned_pid = profiles[int(hash(qid)) % len(profiles)]["persona_id"]
                p_sims = profile_sim_map.get(assigned_pid)

                scored_candidates = []
                for did, tfidf_score in results:
                    idx = doc_id_to_idx.get(did)
                    psim = p_sims[idx] if (p_sims is not None and idx is not None) else 0.0
                    final_score = (1.0 - alpha) * tfidf_score + alpha * psim
                    scored_candidates.append((did, final_score))

                # Deterministic tie-break: final_score descending, did ascending
                scored_candidates.sort(key=lambda x: (-x[1], x[0]))

                for rank, (did, final_score) in enumerate(scored_candidates[:top_k], start=1):
                    out_f.write(f"{qid} Q0 {did} {rank} {final_score:.4f} p13n_a{alpha:.1f}\n")

        print(f"Generated personalised run: {out_file} (alpha={alpha})")


if __name__ == "__main__":
    run_personalisation_sweep(
        query_run_file=Path("artifacts/run_tfidf.txt"),
        index_dir=Path("artifacts/tfidf_index"),
        profiles_file=Path("research/profiles.json"),
        output_dir=Path("artifacts"),
        alphas=[0.0, 0.5, 1.0]
    )
