# Architecture Decision Record (ADR) — KarirMatch

**Status:** Disetujui v1.0  
**Pemilik:** Deris Firmansyah  
**Sumber:** Grand Design Produk Inovatif KarirMatch Bagian 5, Bagian 7  
**Terakhir diperbarui:** 7 November 2026

---

## 1. Tentang ADR

ADR mencatat keputusan arsitektur yang penting, konteksnya, alternatif yang
dipertimbangkan, dan konsekuensinya. Tujuannya agar keputusan tidak menjadi asumsi
diam-diam dan dapat ditinjau ulang saat kondisi berubah.

Format status:

- **Diusulkan** — belum disetujui.
- **Diterima** — dipakai untuk MVP.
- **Diterima dengan syarat** — dipakai bila kondisi tertentu terpenuhi.
- **Digantikan** — tidak berlaku; lihat ADR pengganti.
- **Ditolak** — dipertimbangkan dan tidak dipakai.

Grand Design sudah menetapkan beberapa keputusan (modular monolith, TF-IDF + cosine,
personalisasi berbasis aturan, FastAPI + React dengan fallback Django, PostgreSQL/SQLite,
dan pengecualian infrastruktur terdistribusi). ADR di bawah ini mencatat keputusan
tersebut beserta alasannya; detail yang belum ada di Grand Design ditandai sebagai
**usulan** atau **keputusan terbuka**.

---

## 2. Indeks ADR

| ID | Judul | Status | Ringkasan keputusan |
|---|---|---|---|
| [ADR-0001](ADR-0001-monolit-modular.md) | Modular monolith | Diterima | Satu aplikasi FastAPI dengan lima modul in-process; bukan microservices |
| [ADR-0002](ADR-0002-tfidf-cosine.md) | TF-IDF + Cosine Similarity sebagai inti retrieval | Diterima | TF-IDF + cosine; keyword matching sebagai baseline; BM25 opsional; embedding/LLM bukan inti |
| [ADR-0003](ADR-0003-indeks-field-berbobot.md) | Indeks field berbobot dan preprocessing bersama | Diterima | Vektor per field `title`/`skills`/`description`; bobot awal 0,4/0,3/0,3; satu pipeline preprocessing |
| [ADR-0004](ADR-0004-personalisasi-berbasis-aturan.md) | Personalisasi berbasis aturan | Diterima | `FinalScore = α·QueryScore + β·ProfileScore`; bobot interaksi 1:3:5; half-life 14 hari; tanpa ML adaptif |
| [ADR-0005](ADR-0005-stack-fastapi-react.md) | Stack FastAPI + React dengan fallback Django | Diterima dengan syarat | FastAPI + React/Vite; fallback Django monolit bila React belum dikuasai; logika riset bebas framework |
| [ADR-0006](ADR-0006-penyimpanan-postgresql-sqlite.md) | PostgreSQL/SQLite dan indeks in-memory | Diterima | PostgreSQL untuk deployment, SQLite untuk dev/test; indeks TF-IDF in-memory; tanpa search engine eksternal |
| [ADR-0007](ADR-0007-explainability-match-level.md) | Tingkat kecocokan relatif, bukan skor mentah | Diterima | UI menampilkan Tinggi/Sedang/Rendah dan alasan; skor mentah hanya admin |
| [ADR-0008](ADR-0008-evaluasi-offline-terpisah.md) | Evaluasi offline dan data evaluasi terpisah | Diterima | Judgment manusia 0–2, anotasi buta, uji statistik; tabel evaluasi terpisah dari data produk |
| [ADR-0009](ADR-0009-infrastruktur-ditunda.md) | Infrastruktur terdistribusi ditunda | Diterima | Tanpa microservices, broker, task queue, cache terdistribusi, atau search engine eksternal di MVP |
| [ADR-0010](ADR-0010-autentikasi.md) | Autentikasi dan manajemen sesi | Diterima sebagian | Hash bcrypt/argon2, rate limit login, otorisasi server-side; cookie vs token tertunda |

---

## 3. Template ADR

```markdown
# ADR-XXXX: Judul

- Status:
- Tanggal:
- Pemilik:
- Sumber:
- Menggantikan:
- Digantikan oleh:

## Konteks

## Keputusan

## Alternatif yang dipertimbangkan

## Konsekuensi

### Positif

### Negatif / biaya

## Tindak lanjut

## Referensi
```

---

## 4. Hubungan dengan Dokumen Lain

- Keputusan produk dan riset: `01-prd.md`, `research/research-and-evaluation.md`.
- Detail arsitektur: `02-system-design.md`.
- Kontrak API: `03-api-spec.md`.
- Skema data: `data/database-design.md`.
- Risiko dan keputusan terbuka: `delivery/risk-register.md`.

Jika ADR bertentangan dengan Grand Design, Grand Design menjadi acuan sampai ADR
diperbarui atau Grand Design direvisi.
