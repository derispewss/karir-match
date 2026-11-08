"""Implementasi Perhitungan Metrik Evaluasi Information Retrieval (IR).

Metrik yang didukung:
- Precision@K (P@K)
- Recall@K (R@K)
- Mean Average Precision (MAP)
- Normalized Discounted Cumulative Gain (nDCG@K)
- Mean Reciprocal Rank (MRR)
"""

import math
from typing import Dict, List, Set


def precision_at_k(ranked_doc_ids: List[str], relevant_doc_ids: Set[str], k: int = 10) -> float:
    """Menghitung P@K: proporsi dokumen relevan di top K hasil."""
    if k <= 0:
        return 0.0
    top_k = ranked_doc_ids[:k]
    if not top_k:
        return 0.0
    relevant_in_top_k = sum(1 for doc_id in top_k if doc_id in relevant_doc_ids)
    return relevant_in_top_k / k


def recall_at_k(ranked_doc_ids: List[str], relevant_doc_ids: Set[str], k: int = 10) -> float:
    """Menghitung R@K: proporsi total dokumen relevan yang berhasil ditemukan di top K."""
    if not relevant_doc_ids or k <= 0:
        return 0.0
    top_k = ranked_doc_ids[:k]
    relevant_in_top_k = sum(1 for doc_id in top_k if doc_id in relevant_doc_ids)
    return relevant_in_top_k / len(relevant_doc_ids)


def reciprocal_rank(ranked_doc_ids: List[str], relevant_doc_ids: Set[str]) -> float:
    """Menghitung Reciprocal Rank (RR): 1 / rank kemunculan dokumen relevan pertama."""
    for rank, doc_id in enumerate(ranked_doc_ids, start=1):
        if doc_id in relevant_doc_ids:
            return 1.0 / rank
    return 0.0


def average_precision(ranked_doc_ids: List[str], relevant_doc_ids: Set[str]) -> float:
    """Menghitung Average Precision (AP) untuk satu query."""
    if not relevant_doc_ids:
        return 0.0

    hit_count = 0
    sum_precisions = 0.0

    for rank, doc_id in enumerate(ranked_doc_ids, start=1):
        if doc_id in relevant_doc_ids:
            hit_count += 1
            sum_precisions += hit_count / rank

    return sum_precisions / len(relevant_doc_ids)


def dcg_at_k(ranked_doc_ids: List[str], qrels: Dict[str, int], k: int = 10) -> float:
    """Menghitung DCG@K dengan gain linear: sum(rel_i / log2(i + 1))."""
    dcg = 0.0
    for rank, doc_id in enumerate(ranked_doc_ids[:k], start=1):
        rel = qrels.get(doc_id, 0)
        dcg += rel / math.log2(rank + 1)
    return dcg


def ndcg_at_k(ranked_doc_ids: List[str], qrels: Dict[str, int], k: int = 10) -> float:
    """Menghitung nDCG@K ternormalisasi terhadap Ideal DCG (IDCG)."""
    dcg = dcg_at_k(ranked_doc_ids, qrels, k)

    # Urutkan secara ideal berdasarkan skor relevansi tertinggi
    ideal_ratings = sorted(qrels.values(), reverse=True)
    idcg = sum(rel / math.log2(rank + 1) for rank, rel in enumerate(ideal_ratings[:k], start=1))

    if idcg == 0.0:
        return 0.0
    return dcg / idcg
