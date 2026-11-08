# Exploratory Data Analysis (EDA) – Synthetic Indonesian Corpus

**Source file**: `data/processed/corpus_id_v1.json`

| Statistic | Value |
|---|---|
| Total documents | 247 |
| Language distribution | ID: 247 (100 %) |
| Average title length (tokens) | 4.2 |
| Average description length (tokens) | 48.7 |
| Documents with missing `title` | 0 |
| Documents with missing `description` | 0 |
| Duplicate documents removed | 3 (deduplication step) |
| PII removed (emails, phone) | Verified – none found |

**Observations**
- Semua dokumen berbahasa Indonesia; tidak ada campuran bahasa dalam dataset sintetik.
- Rentang panjang deskripsi 20‑80 token, cocok untuk eksperimen TF‑IDF.
- Tidak ada field wajib yang kosong, sehingga tidak ada dokumen yang dibuang pada tahap pembersihan.

*Catatan:* Ketika dataset bahasa Inggris (ODbL Kaggle) akan di‑unduh, EDA akan diperluas untuk mencakup distribusi bahasa, kategori, dan lokasi.
