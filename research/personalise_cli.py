# research/personalise_cli.py
"""CLI wrapper for the personalisation sweep (Alpha values).

Generates personalised run files for each alpha defined in
`config/personalisation.yaml` and writes a manifest containing hashes of
the TF‑IDF run, the index manifest, and the personalisation config.
"""

import json
import yaml
import hashlib
from pathlib import Path
from datetime import datetime

from research.personalise import run_personalisation


def file_hash(p: Path) -> str:
    """SHA‑256 hash of a file (binary)."""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run personalisation sweep and write manifest")
    parser.add_argument(
        "--tfidf-run",
        type=Path,
        default=Path("artifacts/run_tfidf.txt"),
        help="Base TF‑IDF run file (output of research/score.py)"
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=Path("artifacts/tfidf_index"),
        help="Directory containing TF‑IDF index files"
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("artifacts"),
        help="Directory where personalised runs and manifest will be stored"
    )
    args = parser.parse_args()

    # Load alpha values from personalisation config
    with open("config/personalisation.yaml", "r", encoding="utf-8") as f:
        pers_cfg = yaml.safe_load(f)
    alphas = pers_cfg.get("alpha_values", [0.0, 0.5, 1.0])

    # Run the sweep (this creates run files under args.out)
    run_personalisation(
        tfidf_run_path=args.tfidf_run,
        index_dir=args.index,
        out_dir=args.out,
        alphas=alphas
    )

    # Build manifest with relevant hashes
    manifest = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "tfidf_run_hash": file_hash(args.tfidf_run),
        "index_manifest_hash": file_hash(args.index / "manifest.json"),
        "personalisation_config_hash": file_hash(Path("config/personalisation.yaml")),
        "alpha_values": alphas,
    }
    manifest_path = args.out / f"personalisation_manifest_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"✅ Manifest written to {manifest_path}")


if __name__ == "__main__":
    main()
