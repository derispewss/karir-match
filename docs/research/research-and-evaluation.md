# Riset dan Evaluasi — KarirMatch

**Status:** Disetujui v1.0  
**Pemilik:** Deris Firmansyah  
**Sumber:** Grand Design Produk Inovatif KarirMatch Bagian 3, Bagian 6  
**Terakhir diperbarui:** 7 November 2026  
**Jenis riset:** Design science research dengan evaluasi eksperimen kuantitatif offline

---

## 1. Ringkasan

Riset ini menguji dua fitur KarirMatch:

- **F1 — Pencarian:** retrieval dan ranking dengan TF-IDF + Cosine Similarity
  dibandingkan baseline keyword matching.
- **F2 — Feed rekomendasi:** content-based recommendation dengan profil vektor dari
  interaksi pengguna.

F3 (penjelasan) dan F4 (dashboard evaluasi) mendukung penyajian dan pengukuran, bukan
objek utama eksperimen.

**Kontribusi yang diklaim bukan metode baru.** TF-IDF dan Cosine Similarity adalah metode
mapan. Kontribusi dibatasi pada:

1. Desain evaluasi komparatif yang adil dalam satu protokol.
2. Analisis pengaruh variasi preprocessing.
3. Ablation terukur untuk komponen personalisasi pada lowongan berbahasa Indonesia dan
   Inggris, dengan hasil dilaporkan per bahasa.

Klaim research gap tetap bersyarat: pencarian literatur sejauh ini terbatas pada beberapa
kueri web, bukan survei sistematis. Jika ternyata sudah banyak karya serupa, kontribusi
diubah menjadi replikasi terkontrol atau analisis sensitivitas, dan itu tetap sah.

---

## 2. Fokus dan Kendala STKI

| Kendala | Implikasi |
|---|---|
| **Vocabulary mismatch** | Query dan dokumen memakai istilah berbeda untuk konsep yang sama (misalnya “programmer” vs “software developer”) |
| **Keterbatasan TF-IDF** | Tidak menangkap sinonim, semantik, maupun urutan kata |
| **Teks campuran Indonesia–Inggris** | Manfaat preprocessing tidak pasti; hasil harus dilaporkan per bahasa |
| **Hasil sama untuk semua pengguna** | Personalisasi berbasis aturan diuji sebagai pembeda |
| **Data dan anotasi terbatas** | Klaim harus dibatasi pada koleksi, query set, dan judgment yang dibuat sendiri |

---

## 3. Studi Literatur dan Research Gap

### 3.1 Studi terdahulu

| Studi | Pendekatan dan hasil | Keterbatasan / research gap |
|---|---|---|
| Maghfirli dkk. (2026) | Sistem temu kembali lowongan berbahasa Indonesia dengan VSM, TF-IDF, dan cosine; 350 dokumen (300 lowongan, 50 noise), 10 query; precision rata-rata 0,840 (top-10) dan 0,880 (top-15) | Dataset kecil, label relevan/non-relevan biner, tidak membahas ablation preprocessing maupun personalisasi |
| Ula dan Faisal (2025) | Mencocokkan resume pencari kerja (dataset publik Kaggle) dengan deskripsi lowongan memakai TF-IDF dan cosine | Pencocokan dokumen ke dokumen, bukan pencarian berbasis query |
| Raharjo dkk. (2022) | TF-IDF + cosine untuk rekomendasi pekerjaan; abstrak melaporkan MRR 0,857 dan MAP 0,833 pada evaluasi mereka sendiri | Dataset dan judgment berbeda, sehingga angkanya tidak dapat dibandingkan dengan KarirMatch |
| Çelik Ertuğrul dan Bitirim (2025) | Tinjauan sistematis (19 artikel survei dan 57 artikel solusi) yang mengelompokkan teknik content-based, collaborative, hybrid, dan knowledge-based | Peta bidang secara umum; tidak menguji protokol evaluasi untuk kasus ini |

### 3.2 Rujukan pendukung

- **Thakur dkk. (2021), BEIR:** melaporkan BM25 sebagai baseline kuat pada banyak dataset,
  sehingga BM25 layak menjadi pembanding opsional. Hasilnya pada domain umum, bukan
  lowongan kerja.
- **Mashayekhi dkk. (2022; revisi 2023, preprint arXiv):** survei e-recruitment berbasis
  tantangan; berguna untuk pembahasan cold-start, bias, dan privasi.
- **Zou dkk. (2024):** meninjau teknik job recommendation dan menjelaskan user profiling
  serta job profiling pada pendekatan content-based.
- **Yap dkk. (2025):** membahas model hybrid dan metrik evaluasi (precision, recall, NDCG,
  RMSE, MAE).
- **Marcuzzo dkk. (2022):** menjelaskan implicit feedback sebagai sinyal lemah tanpa
  interaksi negatif eksplisit, serta protokol evaluasi dan metrik sistem rekomendasi.
- **Mustikasari dkk. (2021):** membandingkan stemmer bahasa Indonesia pada kata
  berimbuhan (Sastrawi 95,2%, Nazief dan Adriani 92,4%, Arifin dan Setiono 89%); mengukur
  kualitas stemmer, bukan dampaknya pada retrieval.

### 3.3 Keterbatasan inti yang diakui

- TF-IDF tidak menangkap sinonim dan semantik.
- Personalisasi berbasis aturan pembobotan, bukan machine learning adaptif.
- Hasil tidak dapat digeneralisasi di luar dataset dan query set yang dipakai.
- Pernyataan “keyword sederhana kurang relevan” dan “personalisasi meningkatkan kualitas”
  diperlakukan sebagai hipotesis yang diuji, bukan fakta.

---

## 4. Pertanyaan Riset dan Hipotesis

### 4.1 Research questions

| ID | Pertanyaan |
|---|---|
| **RQ1** | Seberapa baik ranking TF-IDF + Cosine dibanding baseline keyword matching (P@K, MAP, NDCG@K)? |
| **RQ2** | Bagaimana variasi preprocessing (stopword, stemming, normalisasi, bobot field, n-gram) memengaruhi kualitas retrieval? |
| **RQ3** | Bagaimana pengaruh personalisasi berbasis profil terhadap kualitas rekomendasi? |
| **RQ4** | Seberapa besar kontribusi komponen profil, dan bagaimana sensitivitas terhadap α? |
| **RQ5** | Apakah latensi dan ukuran indeks layak untuk skala dataset proyek? |

### 4.2 Hipotesis dan uji statistik

Dua sisi, α-signifikansi 0,05 sebagai usulan awal, koreksi Holm–Bonferroni. Karena sampel
kecil, ukuran efek dan interval kepercayaan dilaporkan di samping p-value. **Hasil tidak
signifikan adalah hasil yang sah.**

| RQ | H0 | H1 | Unit analisis | Uji statistik |
|---|---|---|---|---|
| RQ1 | Tidak ada perbedaan median NDCG@10 antara TF-IDF + Cosine dan keyword baseline | Median NDCG@10 berbeda dari baseline | Query (berpasangan) | Wilcoxon signed-rank; paired t-test hanya jika normalitas selisih terpenuhi |
| RQ2 | Konfigurasi preprocessing tidak memengaruhi NDCG@10 | Setidaknya satu konfigurasi memberi NDCG@10 berbeda | Query | Friedman, post-hoc Wilcoxon dengan koreksi Holm |
| RQ3 | Personalisasi tidak mengubah NDCG@10 | Personalisasi mengubah NDCG@10 | Pasangan (profil, query) atau profil | Wilcoxon signed-rank; selisih per profil dan interval kepercayaan bootstrap |
| RQ4 | Nilai α tidak memengaruhi NDCG@10 | Ada α yang memberi NDCG@10 berbeda | Profil | Analisis sensitivitas deskriptif, ditambah Friedman bila profil cukup |
| RQ5 | Latensi tidak melampaui ambang | Latensi melampaui ambang | Ukuran koleksi | Statistik deskriptif (median, p95) |

---

## 5. Metodologi

### 5.1 Urutan kerja

Design science research dengan evaluasi eksperimen kuantitatif offline:

```text
Identifikasi masalah
→ Studi literatur
→ Akuisisi data
→ Preprocessing
→ EDA (komposisi korpus, statistik field kosong dan duplikat)
→ Pemodelan (indeks TF-IDF, ranking, profil)
→ Evaluasi
→ Integrasi fitur ke prototipe web
```

### 5.2 Baseline dan usulan

| Konfigurasi | Metode | Alasan |
|---|---|---|
| **Baseline** | Keyword matching sederhana (skor = proporsi term query yang muncul); BM25 opsional sebagai pembanding | Perbandingan adil dan transparan |
| **Usulan 1** | TF-IDF (sublinear TF, smooth IDF, normalisasi L2) + Cosine Similarity, field berbobot (`title`, `skills`, `description`) = (0,4; 0,3; 0,3) sebagai bobot awal | Relevan untuk retrieval, kompleksitas rendah, mudah dijelaskan, tidak butuh data latih |
| **Usulan 2** | `FinalScore = α·QueryScore + β·ProfileScore`, `α + β = 1`; profil vektor agregat dari interaksi berbobot 1:3:5 (klik detail, simpan, lamar) dengan peluruhan waktu (half-life usulan 14 hari) | Satu ruang vektor dengan query; interpretabilitas tinggi; mudah diablation |

Rasio bobot 1:3:5 adalah hipotesis desain yang diuji lewat ablation, bukan hasil empiris.

### 5.3 Strategi pemodelan

- Tidak ada pelatihan model. Yang dipisah adalah **query**: validation (memilih α dan
  konfigurasi preprocessing) dan test (dilaporkan sekali), usulan awal 30/70 atau 40/60.
- Pencegah leakage:
  - Dokumen seed profil dikeluarkan dari kandidat evaluasi.
  - Judgment dibuat tanpa melihat daftar seed dan tanpa melihat sistem mana yang
    menghasilkan dokumen.
- Parameter yang dituning di validation:
  - konfigurasi preprocessing;
  - bobot field;
  - α (grid 1,0 sampai 0,5, langkah 0,1);
  - half-life;
  - batas interaksi aktif.
- Seed acak, versi kode, dan versi pustaka dicatat agar hasil dapat direproduksi.

---

## 6. Rancangan Eksperimen

### 6.1 Skenario uji

| Eksperimen | Skenario | Variabel diubah | Menjawab |
|---|---|---|---|
| **E1** | Baseline keyword matching | Tidak ada | Titik acuan RQ1 |
| **E2** | TF-IDF + Cosine vs baseline, uji berpasangan per query | Stopword (ya/tidak); stemming (tidak / stemmer Inggris / stemmer Indonesia); bobot field (seragam vs judul dan skills lebih tinggi); n-gram (unigram vs unigram + bigram) | RQ1, RQ2 |
| **E3** | Personalisasi dengan 6–10 profil simulasi berbasis persona (seed 3–8 lowongan per persona), berlabel simulasi | Ada/tidak profil; α | RQ3 |
| **E4** | Ablation: tanpa profil (α = 1), profil penuh, hanya klik detail, hanya simpan/lamar, jumlah seed (1, 3, 5, 8), bobot seragam vs berbeda; sweep α | Sumber sinyal, jumlah seed, bobot, α | RQ4 |
| **E5** | Latensi dan ukuran indeks pada 1.000, 5.000, 20.000 dokumen; ulang minimal 30 kali dengan warm-up dibuang; perangkat keras dicatat | Ukuran koleksi, konfigurasi preprocessing | RQ5 |

### 6.2 Detail eksperimen

**E1 — Baseline**

- Skor = proporsi term query yang muncul di dokumen.
- Tidak memakai IDF, bobot field, atau personalisasi.
- Menjadi pembanding utama untuk E2.

**E2 — Retrieval**

- Semua konfigurasi memakai koleksi, query set, dan judgment yang sama.
- Uji berpasangan per query.
- Variabel:
  - stopword removal on/off;
  - stemming: none / English stemmer / Indonesian stemmer;
  - bobot field: seragam vs title+skills lebih tinggi;
  - n-gram: unigram vs unigram+bigram.
- Hasil per bahasa dilaporkan terpisah.

**E3 — Personalisasi**

- 6–10 profil persona; 3–8 lowongan seed per persona.
- Interaksi diberi label simulasi.
- Bandingkan tanpa profil vs dengan profil; sweep α.
- Metrik utama NDCG@10; metrik pendukung P@K, MAP.
- Jangan mengklaim perilaku pengguna nyata.

**E4 — Ablation**

- Tanpa profil (α = 1).
- Profil penuh.
- Hanya klik detail.
- Hanya simpan/lamar.
- Jumlah seed: 1, 3, 5, 8.
- Bobot sinyal seragam vs berbeda (1:3:5).
- Sweep α.
- Analisis sensitivitas half-life dan batas interaksi bila memungkinkan.

**E5 — Efisiensi**

- Ukuran koleksi: 1.000, 5.000, 20.000 dokumen.
- Ulang minimal 30 kali; buang warm-up.
- Catat median dan p95 latensi (ms), ukuran indeks (MB), perangkat keras.
- Pisahkan waktu preprocessing query, pencarian, dan ranking bila memungkinkan.

### 6.3 Uji ketahanan

- Dokumen yang sengaja dijejali kata kunci (*keyword stuffing*).
- Query tanpa term yang dikenal.
- Query terlalu umum.
- Dokumen dengan field kosong.
- Dokumen duplikat.
- Teks campuran Indonesia–Inggris.

---

## 7. Metrik dan Kriteria

### 7.1 Metrik retrieval

K = 10 sebagai utama; K = 5 dan 20 pelengkap.

- **P@K, R@K, F1@K, MAP** memakai binerisasi:
  - relevan jika grade ≥ 1;
  - ketat jika grade = 2.
- **NDCG@K** memakai grade langsung (0, 1, 2).

```text
P@K = |{relevan di Top-K}| / K

R@K = |{relevan di Top-K}| / R

F1@K = 2 × P@K × R@K / (P@K + R@K)

AP = (1/R) × Σ_{k=1}^{K} P@k × rel(k)

MAP = (1/|Q|) × Σ_{q∈Q} AP_q

DCG@K = Σ_{i=1}^{K} (2^{rel_i} - 1) / log2(i + 1)

NDCG@K = DCG@K / IDCG@K
```

Catatan:

- `R` adalah jumlah dokumen relevan untuk query di pool. Recall bergantung pada pool,
  sehingga **recall absolut tidak diketahui**.
- DCG memakai varian gain eksponensial (bentuk klasik memakai gain linear); satu varian
  dipilih, ditulis di laporan, dan dipakai konsisten.
- Query tanpa dokumen relevan dikecualikan atau bernilai 0; kebijakannya ditulis eksplisit.

### 7.2 Metrik efisiensi

- Latensi median dan p95 (ms).
- Ukuran indeks (MB).
- Waktu bangun indeks (dicatat, tanpa ambang ketat).

### 7.3 Uji statistik

- RQ1 dan RQ3: Wilcoxon signed-rank berpasangan.
- RQ2: Friedman dengan post-hoc Wilcoxon dan koreksi Holm.
- RQ4: analisis sensitivitas; Friedman bila profil cukup.
- Interval kepercayaan bootstrap untuk selisih per profil.
- Cohen’s κ untuk kesepakatan annotator.
- α-signifikansi 0,05 (usulan awal).
- Laporkan ukuran efek dan interval kepercayaan; jangan hanya p-value.

### 7.4 Ambang keberhasilan

- **Tidak ada ambang “baik” mutlak untuk kualitas ranking.** Angka hanya bermakna relatif
  terhadap baseline pada koleksi, query set, dan judgment yang sama.
- Arah selisih dilaporkan apa adanya; hasil tidak signifikan adalah hasil yang sah.
- Efisiensi: target awal (usulan, perlu validasi) median < 300 ms dan p95 < 1.000 ms pada
  koleksi hingga 5.000 dokumen.

### 7.5 Pemetaan RQ ke bukti

| RQ | Eksperimen | Metrik utama | Uji | Bukti tambahan |
|---|---|---|---|---|
| RQ1 | E1, E2 | NDCG@10, MAP, P@10 | Wilcoxon | Effect size, CI, analisis kasus gagal |
| RQ2 | E2 | NDCG@10 | Friedman + post-hoc | Perbandingan konfigurasi, per bahasa |
| RQ3 | E3 | NDCG@10 | Wilcoxon | Selisih per profil, bootstrap CI |
| RQ4 | E4 | NDCG@10 | Sensitivitas/Friedman | Kontribusi komponen, sweep α |
| RQ5 | E5 | Median/p95 latensi, ukuran indeks | Deskriptif | Perangkat keras, konfigurasi |

---

## 8. Relevance Judgment

### 8.1 Skala

| Grade | Arti |
|---:|---|
| 0 | Tidak relevan |
| 1 | Cukup relevan |
| 2 | Sangat relevan |

### 8.2 Prosedur

1. Tulis pedoman: relevan jika judul, skills, atau kualifikasi sesuai niat query; sangat
   relevan jika juga sesuai level pengalaman dan lokasi yang disebut query; sertakan
   contoh batas kasus.
2. Pilot pada 5 query; bandingkan dua annotator; perbaiki pedoman.
3. Minimal 2 annotator; 25% (usulan) dinilai ganda untuk Cohen’s κ.
4. Pooling Top-15 dari semua sistem; anotasi buta.
5. Hitung κ pada subset ganda; selisih diselesaikan lewat diskusi; κ sebelum diskusi tetap
   dilaporkan.
6. Simpan judgment CSV beserta versi pedoman.
7. Jangan membuat klik sintetis dan menyajikannya sebagai perilaku pengguna.

### 8.3 Beban anotasi

```text
40 query × 45 dokumen unik per query = 1.800 pasangan
```

Belum termasuk judgment profil. Jika terlalu berat, kurangi jumlah query atau kedalaman
pool dan catat sebagai keterbatasan.

---

## 9. Analisis dan Pelaporan

Setiap hasil harus memuat:

- RQ dan eksperimen.
- Konfigurasi (preprocessing, bobot, α, half-life, seed, versi).
- Ukuran koleksi, jumlah query, dan bahasa.
- Metrik utama dan pendukung.
- Selisih relatif terhadap baseline.
- Ukuran efek dan interval kepercayaan.
- p-value dan koreksi jika uji jamak.
- Analisis kasus gagal per query.
- Keterbatasan yang relevan.

**Aturan interpretasi:**

- Jangan membandingkan angka absolut dengan studi lain yang memakai dataset/judgment
  berbeda.
- Jangan menyimpulkan “lebih baik” tanpa pembanding pada protokol yang sama.
- Jangan menyembunyikan hasil negatif atau tidak signifikan.
- Jangan menggeneralisasi ke seluruh pasar kerja.

---

## 10. Ancaman Validitas

| Jenis | Ancaman | Mitigasi |
|---|---|---|
| Construct | Klik dianggap relevansi | Klik hanya sinyal lemah; judgment manusia untuk evaluasi |
| Construct | NDCG@10 tidak mewakili semua kebutuhan | Laporkan P@K, MAP, K=5/20; analisis kasus |
| Internal | Data leakage dari seed profil | Keluarkan seed dari kandidat; anotasi buta |
| Internal | Tuning di test set | Validation/test terpisah; test dilaporkan sekali |
| Internal | Perbedaan konfigurasi antar sistem | Satu protokol, koleksi, query, dan judgment |
| External | Dataset tidak representatif | Laporkan komposisi; per bahasa; batas generalisasi |
| External | Korpus Indonesia sintetis | Nyatakan sintetis; jangan klaim kondisi pasar |
| Conclusion | Sampel query kecil | Laporkan CI, effect size; tidak signifikan tetap sah |
| Conclusion | Uji jamak | Koreksi Holm; rencanakan uji |
| Annotation | Subjektivitas dan kelelahan | Pedoman, pilot, κ, subset ganda |
| Simulation | Interaksi simulasi dianggap nyata | `is_simulated`; label; metrik produk terpisah |
| Feedback loop | Personalisasi memperkuat bias | 20% slot non-personalisasi; catat posisi; pantau keragaman |

---

## 11. Kebijakan Klaim

### Boleh diklaim

- Perbandingan terukur pada koleksi, query set, dan judgment yang dibuat sendiri.
- Perubahan metrik apa adanya, termasuk bila tidak signifikan.
- Desain sistem yang transparan.
- Keterbatasan dan kasus gagal.

### Tidak boleh diklaim

- Keunggulan sebelum eksperimen.
- Skor sebagai probabilitas.
- Interaksi simulasi sebagai perilaku pengguna.
- “AI adaptif” atau reinforcement learning.
- Generalisasi di luar dataset.
- Sitasi yang belum diverifikasi.
- “Personalisasi meningkatkan kualitas” tanpa hasil yang mendukung.

---

## 12. Reproducibility

Simpan bersama setiap eksperimen:

- Versi kode (commit hash).
- Versi pustaka (scikit-learn, SciPy, stemmer, Python).
- Konfigurasi preprocessing dan bobot.
- Seed acak.
- Hash dataset dan query set.
- Hash konfigurasi.
- Perangkat keras untuk benchmark.
- Tanggal eksekusi.
- Skrip evaluasi dan test case.

**Aturan:** hasil tanpa manifest tidak dianggap reproducible.

---

## 13. Keputusan Terbuka

1. Jumlah query final dan kedalaman pool.
2. Varian gain DCG (eksponensial vs linear).
3. Perlakuan query tanpa dokumen relevan (exclude vs 0).
4. Apakah BM25 ikut sebagai pembanding.
5. Kalibrasi batas Tinggi/Sedang/Rendah.
6. Split validation/test: 30/70 atau 40/60.
7. Jumlah profil simulasi dan seed per persona.
8. Apakah evaluasi personalisasi memakai pasangan (profil, query) atau level profil.
9. Alat dan format anotasi.
10. Apakah hasil per bahasa digabung untuk analisis sekunder (bukan klaim utama).

---

## 14. Traceability

| Bagian | Sumber Grand Design |
|---|---|
| RQ dan hipotesis | Bagian 3 Pertanyaan riset; Bagian 3 Hipotesis dan uji statistik |
| Literatur | Bagian 3 Studi terdahulu; rujukan |
| Kontribusi/kebaruan | Bagian 3 Kontribusi dan kebaruan |
| Metodologi | Bagian 5 Metodologi |
| Baseline/usulan | Bagian 5 Metode |
| Preprocessing | Bagian 5 Pipeline preprocessing |
| Formulasi skor | Bagian 5 Formulasi TF-IDF; Pembentukan profil |
| E1–E5 | Bagian 6 Skenario uji |
| Metrik | Bagian 6 Metrik dan kriteria; Rumus metrik |
| Judgment | Bagian 6 Pembuatan relevance judgment |
| Statistik | Bagian 3, Bagian 6 |
| Ancaman validitas | Bagian 3, Bagian 4, Bagian 6 |
| Klaim | Bagian 7 Yang boleh dan tidak boleh diklaim |

---

**Rujukan lengkap:** `references.md`.
