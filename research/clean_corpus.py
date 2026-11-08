"""Pipeline Pembersihan, Normalisasi, Deduplikasi, dan PII Stripping KarirMatch."""

import hashlib
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


def clean_text(text: str) -> str:
    """Membersihkan HTML tag, link/URL, spasi berlebih, dan karakter anomali."""
    if not text:
        return ""
    # Hapus tag HTML
    text = re.sub(r"<[^>]+>", " ", text)
    # Hapus URL
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    # Hapus email (PII)
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", " ", text)
    # Hapus nomor telepon lokal / internasional (PII)
    text = re.sub(r"\b(?:\+?62|08)[0-9]{8,12}\b", " ", text)
    # Normalisasi spasi dan whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def compute_dedup_hash(title: str, company: str, description: str) -> str:
    """Menghitung hash SHA-256 untuk mendeteksi duplikat konten."""
    norm_content = f"{title.lower().strip()}|{company.lower().strip()}|{description.lower().strip()}"
    return hashlib.sha256(norm_content.encode("utf-8")).hexdigest()


def process_corpus(input_path: Path, output_path: Path) -> Tuple[int, int, int]:
    """Membaca korpus mentah, membersihkan, menghapus PII, mendeduplikasi, dan menyimpan."""
    with open(input_path, "r", encoding="utf-8") as f:
        raw_docs = json.load(f)

    seen_hashes = set()
    cleaned_docs = []
    dropped_empty = 0
    dropped_duplicates = 0

    for doc in raw_docs:
        title = clean_text(doc.get("title", ""))
        desc = clean_text(doc.get("description", ""))
        company = clean_text(doc.get("company", ""))
        skills = clean_text(doc.get("skills", ""))

        # Validasi field wajib
        if not title or not desc:
            dropped_empty += 1
            continue

        dedup_hash = compute_dedup_hash(title, company, desc)
        if dedup_hash in seen_hashes:
            dropped_duplicates += 1
            continue

        seen_hashes.add(dedup_hash)

        processed_doc = {
            "id": doc.get("id"),
            "title": title,
            "company": company,
            "job_category": doc.get("job_category", "Lainnya"),
            "location": doc.get("location", "Indonesia"),
            "experience_level": doc.get("experience_level", "All Levels"),
            "employment_type": doc.get("employment_type", "Full-time"),
            "skills": skills,
            "description": desc,
            "language": doc.get("language", "id"),
            "is_simulated": doc.get("is_simulated", True),
            "is_active": doc.get("is_active", True),
            "dedup_hash": dedup_hash,
        }
        cleaned_docs.append(processed_doc)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_docs, f, ensure_ascii=False, indent=2)

    return len(cleaned_docs), dropped_empty, dropped_duplicates


if __name__ == "__main__":
    raw_file = Path("data/raw/synthetic_jobs_id.json")
    clean_file = Path("data/processed/corpus_id_v1.json")
    total_clean, empty, dups = process_corpus(raw_file, clean_file)
    print(f"Hasil Pipeline: {total_clean} bersih, {empty} kosong dibuang, {dups} duplikat dibuang.")
