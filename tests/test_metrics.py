"""Unit test untuk skrip evaluasi metrik IR."""

from research.metrics import precision_at_k, recall_at_k, reciprocal_rank, average_precision, ndcg_at_k

def test_precision_and_recall_at_k():
    ranked = ["doc1", "doc2", "doc3", "doc4", "doc5"]
    relevant = {"doc1", "doc3"}
    
    assert precision_at_k(ranked, relevant, k=2) == 0.5  # doc1 in top 2 (1/2)
    assert precision_at_k(ranked, relevant, k=4) == 0.5  # doc1, doc3 in top 4 (2/4)
    assert recall_at_k(ranked, relevant, k=2) == 0.5     # 1 of 2 relevant
    assert recall_at_k(ranked, relevant, k=3) == 1.0     # 2 of 2 relevant

def test_reciprocal_rank():
    assert reciprocal_rank(["doc1", "doc2"], {"doc1"}) == 1.0
    assert reciprocal_rank(["doc2", "doc1"], {"doc1"}) == 0.5
    assert reciprocal_rank(["doc2", "doc3"], {"doc1"}) == 0.0

def test_ndcg_ideal_is_one():
    ranked = ["doc1", "doc2", "doc3"]
    qrels = {"doc1": 2, "doc2": 1, "doc3": 0}
    # Ranking persis sama dengan ideal, nilai nDCG harus 1.0
    assert ndcg_at_k(ranked, qrels, k=3) == 1.0
