"""Menghasilkan sampel korpus skala 1k, 5k, dan 20k untuk pengujian efisiensi latensi dan ukuran indeks (RQ5)."""

import json
import random
from pathlib import Path

# Set seed deterministik
random.seed(42)

def generate_scale_corpora():
    source_clean = Path("data/processed/corpus_id_v1.json")
    with open(source_clean, "r", encoding="utf-8") as f:
        base_docs = json.load(f)

    target_sizes = [1000, 5000, 20000]

    for size in target_sizes:
        out_docs = []
        for i in range(1, size + 1):
            seed_doc = random.choice(base_docs)
            scaled_doc = dict(seed_doc)
            scaled_doc["id"] = f"scale-{size}-{i:05d}"
            scaled_doc["is_simulated"] = True
            out_docs.append(scaled_doc)

        out_path = Path(f"data/processed/scale_{size}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out_docs, f, ensure_ascii=False)
        print(f"Berhasil menghasilkan korpus skala: {out_path} ({len(out_docs)} dokumen)")

if __name__ == "__main__":
    generate_scale_corpora()
