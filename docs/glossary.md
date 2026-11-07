# Glosarium — KarirMatch

**Status:** Disetujui v1.0  
**Sumber:** Grand Design Produk Inovatif KarirMatch; dokumen turunan  
**Terakhir diperbarui:** 7 November 2026

---

## 1. Produk dan Konsep

| Istilah | Definisi |
|---|---|
| **KarirMatch** | Prototipe web pencarian dan rekomendasi lowongan kerja |
| **F1 — Pencarian** | Fitur menemukan lowongan lewat query dan filter |
| **F2 — Feed rekomendasi** | Fitur menyarankan lowongan berdasarkan profil interaksi |
| **F3 — Penjelasan hasil** | Fitur menunjukkan tingkat kecocokan dan istilah yang cocok |
| **F4 — Dashboard evaluasi** | Fitur mengukur kualitas sistem secara offline |
| **Persona** | Representasi pengguna hipotetis (Raka, Sinta, Budi); belum tervalidasi |
| **JTBD** | *Jobs to be done* — tujuan yang ingin dicapai pengguna |
| **MVP** | Versi minimum yang mencakup cari, filter, detail, auth, preferensi, bookmark, feed, event, dashboard |
| **Cold start** | Kondisi pengguna atau lowongan baru yang belum punya cukup data |
| **Feedback loop** | Siklus ketika rekomendasi memengaruhi interaksi, lalu memperkuat rekomendasi itu sendiri |
| **Position bias** | Kecenderungan pengguna mengklik item di posisi atas, bukan karena relevansi |
| **Implicit feedback** | Sinyal interaksi tidak eksplisit (klik, simpan, lamar) yang lemah dan berisik |

---

## 2. Retrieval dan Ranking

| Istilah | Definisi |
|---|---|
| **Retrieval** | Proses mengambil dokumen kandidat yang relevan dengan query |
| **Ranking** | Proses mengurutkan dokumen kandidat berdasarkan skor |
| **TF** | *Term frequency* — frekuensi term dalam dokumen/field |
| **IDF** | *Inverse document frequency* — bobot term berdasarkan kelangkaannya di koleksi |
| **TF-IDF** | Produk TF dan IDF; memberi bobot lebih besar pada term yang jarang dan diskriminatif |
| **Sublinear TF** | `1 + ln(tf)`; mengurangi efek term yang diulang berlebihan |
| **Smooth IDF** | `ln((1+N)/(1+df)) + 1`; mencegah nilai 0 dan pembagian nol |
| **Normalisasi L2** | Membagi vektor dengan norma L2 sehingga panjang dokumen tidak mendominasi |
| **Cosine Similarity** | Ukuran kemiripan arah dua vektor; pada vektor L2-normal sama dengan dot product |
| **QueryScore** | Skor kemiripan query–dokumen |
| **Field weight** | Bobot untuk field `title`, `skills`, `description` |
| **Tie-break** | Aturan penentu urutan saat skor sama (tanggal terbaru, lalu `job_id` menaik) |
| **Top-K** | K dokumen teratas yang dikembalikan |
| **Vocabulary mismatch** | Query dan dokumen memakai istilah berbeda untuk konsep yang sama |
| **Keyword stuffing** | Praktik mengulang kata kunci untuk menaikkan peringkat |
| **BM25** | Baseline retrieval lain yang kuat; hanya pembanding opsional |
| **Embedding** | Representasi vektor semantik; bukan inti MVP |
| **LLM** | *Large language model*; bukan inti MVP |

---

## 3. Rekomendasi

| Istilah | Definisi |
|---|---|
| **Content-based recommendation** | Rekomendasi berdasarkan kemiripan konten dengan profil pengguna |
| **Collaborative filtering** | Rekomendasi berdasarkan kemiripan antar-pengguna/item; tidak dipakai |
| **Profil vektor (`p_u`)** | Agregat vektor lowongan yang diinteraksikan pengguna |
| **ProfileScore** | Cosine antara profil dan vektor lowongan |
| **FinalScore** | `α·QueryScore + β·ProfileScore` |
| **α (alpha)** | Bobot komponen query |
| **β (beta)** | Bobot komponen profil |
| **Half-life** | Waktu paruh peluruhan bobot interaksi; usulan 14 hari |
| **Bobot sinyal** | Bobot interaksi: klik detail 1, simpan 3, lamar 5 |
| **Non-personalized slot** | Slot hasil yang tidak dipersonalisasi; usulan 20% |
| **MMR** | *Maximal Marginal Relevance*; diversifikasi hasil; pengembangan lanjutan |
| **Ablation** | Menguji kontribusi komponen dengan mematikannya satu per satu |

---

## 4. Evaluasi

| Istilah | Definisi |
|---|---|
| **Relevance judgment** | Penilaian manusia terhadap relevansi dokumen untuk query |
| **Grade 0/1/2** | Tidak relevan / cukup relevan / sangat relevan |
| **Pooling** | Menggabungkan Top-K dari semua sistem untuk dianotasi |
| **Anotasi buta** | Annotator tidak tahu sistem mana yang menghasilkan dokumen |
| **Cohen’s κ** | Ukuran kesepakatan antar-annotator |
| **P@K** | Precision pada K hasil teratas |
| **R@K** | Recall pada K hasil teratas; bergantung pada pool |
| **F1@K** | Harmonic mean P@K dan R@K |
| **AP** | Average Precision untuk satu query |
| **MAP** | Mean Average Precision |
| **DCG@K** | Discounted Cumulative Gain pada K |
| **NDCG@K** | DCG ternormalisasi dengan IDCG |
| **K** | Jumlah hasil teratas; K=10 utama, K=5/20 pelengkap |
| **Wilcoxon signed-rank** | Uji non-parametrik berpasangan |
| **Friedman** | Uji non-parametrik untuk beberapa konfigurasi |
| **Holm–Bonferroni** | Koreksi uji jamak |
| **Bootstrap CI** | Interval kepercayaan dengan resampling |
| **Effect size** | Ukuran besarnya perbedaan, bukan hanya signifikansi |
| **Validation/test split** | Pemisahan query untuk tuning dan pelaporan akhir |
| **Leakage** | Kebocoran informasi yang membuat hasil terlalu optimistis |
| **Keyword baseline** | Skor proporsi term query yang muncul di dokumen |

---

## 5. Data dan Privasi

| Istilah | Definisi |
|---|---|
| **Korpus** | Kumpulan dokumen lowongan yang dipakai |
| **Korpus sintetis** | Data buatan, bukan data pasar nyata |
| **`is_simulated`** | Penanda bahwa event/interaksi berasal dari simulasi |
| **Deduplikasi** | Penghapusan dokumen duplikat lewat hash |
| **Relevance judgment CSV** | Berkas judgment beserta versi pedoman |
| **PII** | *Personally identifiable information* — data pribadi |
| **Pseudonim** | Identitas pengganti pada log |
| **Data minimization** | Hanya mengumpulkan data yang dibutuhkan |
| **Lisensi dataset** | Ketentuan penggunaan dataset |
| **ToS** | *Terms of service* — ketentuan layanan sumber data |

---

## 6. Arsitektur dan Operasional

| Istilah | Definisi |
|---|---|
| **Modular monolith** | Satu aplikasi dengan modul internal yang berbatas jelas |
| **Microservices** | Layanan terpisah yang berkomunikasi lewat jaringan; tidak dipakai |
| **Message broker** | Perantara pesan asynchronous; tidak dipakai |
| **Task queue** | Antrean tugas latar; tidak dipakai |
| **Distributed cache** | Cache lintas node; tidak dipakai |
| **In-memory index** | Indeks TF-IDF yang dimuat ke memori |
| **Docker Compose** | Orkestrasi container sederhana untuk satu host |
| **PostgreSQL** | Database deployment |
| **SQLite** | Database pengembangan/pengujian |
| **OpenAPI** | Spesifikasi kontrak HTTP |
| **ADR** | *Architecture Decision Record* |
| **NFR** | *Non-functional requirement* |
| **SLA** | *Service level agreement*; tidak ditetapkan untuk prototipe |
| **Reproducibility** | Kemampuan menjalankan ulang eksperimen dengan hasil yang sama |

---

## 7. Singkatan

| Singkatan | Arti |
|---|---|
| **STKI** | Sistem Temu Kembali Informasi |
| **VSM** | Vector Space Model |
| **RQ** | Research Question |
| **E1–E5** | Eksperimen 1–5 |
| **TC** | Test Case |
| **FR** | Functional Requirement |
| **NFR** | Non-functional Requirement |
| **ADR** | Architecture Decision Record |
| **PRD** | Product Requirements Document |
| **MVP** | Minimum Viable Product |
| **JTBD** | Jobs to be Done |
| **PII** | Personally Identifiable Information |
| **CTR** | Click-through rate |
| **NDCG** | Normalized Discounted Cumulative Gain |
| **MAP** | Mean Average Precision |
| **MMR** | Maximal Marginal Relevance |
