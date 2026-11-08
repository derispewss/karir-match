"""Run baseline keyword matching on the synthetic Indonesian corpus and generate a run file.

Output format (TREC run file):
query-id Q0 doc-id rank score run-tag
"""

import json
from pathlib import Path
from baseline import search_keyword_baseline


def load_corpus(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_queries(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_run_file(results, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for qid, docs in results.items():
            for rank, doc in enumerate(docs, start=1):
                f.write(f"{qid} Q0 {doc['id']} {rank} {doc['score']:.4f} baseline\n")


def main():
    corpus_path = Path("data/processed/corpus_id_v1.json")
    query_path = Path("research/query_set_v1.json")
    run_path = Path("artifacts/run_baseline.txt")

    corpus = load_corpus(corpus_path)
    queries = load_queries(query_path)

    results = {}
    for q in queries:
        qid = q["id"]
        query_text = q["query"]
        results[qid] = search_keyword_baseline(query_text, corpus, top_k=10)

    write_run_file(results, run_path)
    print(f"Baseline run file written to {run_path} (queries: {len(results)})")

if __name__ == "__main__":
    main()
