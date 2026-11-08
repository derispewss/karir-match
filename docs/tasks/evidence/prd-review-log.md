# Log Review PRD dan Desain Riset dengan Pembimbing — KarirMatch

**Tanggal Review:** 8 November 2026  
**Peneliti:** Deris Firmansyah (NIM: `A11.2024.15624`)  
**Pembimbing:** Pembimbing Akademik / Proyek  
**Status Gate F1:** Disetujui (Approved with notes)

---

## 1. Item yang Ditinjau
1. **Dokumen PRD (`docs/01-prd.md`):** Ruang lingkup MVP (Pencarian lowongan, Rekomendasi berbobot, Penjelasan transparan match-level, dan Evaluasi offline).
2. **Desain Riset (`docs/research/research-and-evaluation.md`):** Matriks RQ1–RQ5, batas klaim, perlakuan bahasa (ID vs EN), dan mitigasi vocabulary mismatch.
3. **Matriks Literatur & Protokol:** Keputusan membatasi kontribusi bukan pada algoritma baru, melainkan evaluasi terukur dan ablation study transparan.

---

## 2. Catatan & Masukan Pembimbing
- **Klaim Metodologi:** Tegaskan bahwa kontribusi penelitian adalah perbandingan terukur TF-IDF dengan multi-field weighting pada dataset spesifik, bukan penemuan model baru.
- **Batasan Korpus:** Korpus lowongan kerja Indonesia yang dibuat secara sintetis harus tetap transparan diberi label `is_simulated = True` dan diuji terpisah dari korpus riil (ODbL).
- **Explainability:** Fitur F3 (penjelasan match-level) disetujui sebagai nilai tambah produk agar hasil rekomendasi transparan bagi pencari kerja.

---

## 3. Keputusan yang Disepakati
1. Scope MVP dikunci pada F1 (Search), F2 (Recommendation feed), F3 (Explainability), F4 (Offline metrics dashboard).
2. Non-goals disetujui: Tidak menggunakan Black-box Deep Learning/LLM runtime demi latensi < 200 ms dan interpretabilitas.
3. Gate F1 dinyatakan **LULUS**.
