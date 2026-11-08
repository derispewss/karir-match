"""Evaluate TF‑IDF and personalised runs using the metric utilities.

Creates a simple qrels file (synthetic) where the first document in the baseline
run is graded *2* (highly relevant), the second is *1* (relevant), and all others
are *0*.  This allows us to produce illustrative metric values for the three
α‑runs (0.0, 0.5, 1.0) and the baseline.
"""

import json
import yaml
from pathlib import Path
from collections import defaultdict
import sys
from pathlib import Path
# Ensure the research package directory is in sys.path for direct script execution
sys.path.append(str(Path(__file__).parent))
from metrics import precision_at_k, recall_at_k, average_precision, ndcg_at_k


def load_run(path: Path):
    """Read a TREC‑style run file and return a dict query → ordered list of doc IDs."""
    runs = defaultdict(list)
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 6:
                continue
            qid, _, doc_id, rank, score, _ = parts[:6]
            runs[qid].append(doc_id)
    return runs


def create_synthetic_qrels(baseline_run: dict, out_path: Path):
    """Create a very simple qrels file.

    - First doc → relevance 2
    - Second doc → relevance 1
    - All others → relevance 0 (omitted in the file)
    """
    lines = []
    for qid, docs in baseline_run.items():
        if docs:
            lines.append(f"{qid} 0 {docs[0]} 2")
        if len(docs) > 1:
            lines.append(f"{qid} 0 {docs[1]} 1")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def evaluate_run(run: dict, qrels: dict, k=10):
    """Compute a small set of metrics for a single run.

    Returns a dict with P@k, MAP, nDCG@k.
    """
    p_scores = []
    ap_scores = []
    ndcg_scores = []
    for qid, ranked_docs in run.items():
        rel_dict = {doc: grade for doc, grade in qrels.get(qid, [])}
        # precision@k (binary relevance: grade>=1)
        p = precision_at_k(ranked_docs, {d for d, g in rel_dict.items() if g >= 1}, k)
        p_scores.append(p)
        # MAP (binary relevance)
        ap = average_precision(ranked_docs, {d for d, g in rel_dict.items() if g >= 1})
        ap_scores.append(ap)
        # nDCG@k (use original grades 0/1/2)
        ndcg = ndcg_at_k(ranked_docs, {doc: grade for doc, grade in rel_dict.items()}, k)
        ndcg_scores.append(ndcg)
    return {
        "P@%d" % k: sum(p_scores) / len(p_scores) if p_scores else 0.0,
        "MAP": sum(ap_scores) / len(ap_scores) if ap_scores else 0.0,
        "nDCG@%d" % k: sum(ndcg_scores) / len(ndcg_scores) if ndcg_scores else 0.0,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate baseline and personalised runs")
    parser.add_argument("--run-dir", type=Path, default=Path("artifacts"), help="Directory containing run files")
    parser.add_argument("--out", type=Path, default=Path("artifacts/evaluation_report.md"), help="Output Markdown report")
    args = parser.parse_args()

    # 1. Load baseline run and create synthetic qrels
    baseline_path = args.run_dir / "run_tfidf.txt"
    baseline = load_run(baseline_path)
    qrels_path = args.run_dir / "synthetic_qrels.txt"
    create_synthetic_qrels(baseline, qrels_path)

    # Load qrels into a convenient structure: query → list of (doc, grade)
    qrels = defaultdict(list)
    with open(qrels_path, "r", encoding="utf-8") as f:
        for line in f:
            qid, _, doc, grade = line.strip().split()
            qrels[qid].append((doc, int(grade)))

    # Gather all run files (baseline + three alpha runs)
    run_files = [baseline_path] + sorted(args.run_dir.glob("run_tfidf_alpha_*.txt"))
    report_lines = ["# Evaluation of TF‑IDF & Personalisation Runs", ""]
    report_lines.append(f"*Synthetic qrels generated from baseline (first doc = grade 2, second = grade 1).*")
    report_lines.append("\n| Run | P@10 | MAP | nDCG@10 |\n|-----|------|-----|----------|")

    for rf in run_files:
        run = load_run(rf)
        metrics = evaluate_run(run, qrels, k=10)
        name = rf.name.replace(".txt", "")
        report_lines.append(f"| {name} | {metrics['P@10']:.3f} | {metrics['MAP']:.3f} | {metrics['nDCG@10']:.3f} |")

    args.out.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"✅ Evaluation report written to {args.out}")


if __name__ == "__main__":
    main()
