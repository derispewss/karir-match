"""Build TF‑IDF indexes per field (title, skills, description) and save metadata."""

import json
import pickle
import yaml
from pathlib import Path
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer


def load_config():
    with open("config/preprocess.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_field_vectorizer(docs, field, tfidf_params):
    corpus = [doc.get(field, "") for doc in docs]
    vec = TfidfVectorizer(**tfidf_params)
    X = vec.fit_transform(corpus)
    return vec, X


def build_index(corpus_path: Path, out_dir: Path):
    cfg = load_config()
    with open(corpus_path, "r", encoding="utf-8") as f:
        docs = json.load(f)

    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / "docs.json", "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)

    field_vecs = {}
    for field in ("title", "skills", "description"):
        vec, X = build_field_vectorizer(docs, field, cfg["tfidf_params"])
        with open(out_dir / f"{field}_vectorizer.pkl", "wb") as f:
            pickle.dump(vec, f)
        with open(out_dir / f"{field}_matrix.npz", "wb") as f:
            sparse.save_npz(f, X)

        field_vecs[field] = {
            "vocab_size": len(vec.vocabulary_),
            "matrix_shape": list(X.shape),
            "vectorizer_file": f"{field}_vectorizer.pkl",
        }

    manifest = {
        "built_at": str(Path.cwd()),
        "corpus_path": str(corpus_path),
        "total_docs": len(docs),
        "field_info": field_vecs,
        "config": cfg,
    }
    with open(out_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"TF-IDF Index successfully built under {out_dir}")


if __name__ == "__main__":
    build_index(Path("data/processed/corpus_id_v1.json"), Path("artifacts/tfidf_index"))
