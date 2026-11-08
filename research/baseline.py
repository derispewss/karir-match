"""Implementasi Baseline Keyword Matching (Boolean / Term-Overlap Proportion).

Menghitung skor sebagai proporsi term query yang muncul di dokumen:
Skor = (jumlah term query unik yang muncul di dokumen) / (total term query unik)
"""

import re
from typing import Any, Dict, List


def tokenize(text: str) -> List[str]:
    """Tokenisasi sederhana berbasis huruf/angka dan lowercase."""
    if not text:
        return []
    return re.findall(r"\b\w+\b", text.lower())


def score_document(query_terms: set, doc_text: str) -> float:
    """Menghitung proporsi kemunculan term query di dalam teks dokumen."""
    if not query_terms:
        return 0.0
    doc_tokens = set(tokenize(doc_text))
    matched_terms = query_terms.intersection(doc_tokens)
    return len(matched_terms) / len(query_terms)


def search_keyword_baseline(query: str, documents: List[Dict[str, Any]], top_k: int = 10) -> List[Dict[str, Any]]:
    """Mencari dokumen dengan keyword baseline matching dan tie-break deterministik."""
    q_tokens = set(tokenize(query))
    if not q_tokens:
        return []

    scored_results = []
    for doc in documents:
        # Gabungkan title, skills, dan description
        full_text = f"{doc.get('title', '')} {doc.get('skills', '')} {doc.get('description', '')}"
        score = score_document(q_tokens, full_text)
        if score > 0.0:
            scored_results.append({
                "id": doc.get("id"),
                "title": doc.get("title"),
                "company": doc.get("company"),
                "score": round(score, 4),
            })

    # Tie-break deterministik: score menurun (-score), lalu id menaik
    scored_results.sort(key=lambda x: (-x["score"], str(x["id"])))
    return scored_results[:top_k]
