# Roadmap Pelaksanaan — KarirMatch

**Status:** Disetujui v1.0  
**Pemilik:** Deris Firmansyah  
**Sumber:** Grand Design Produk Inovatif KarirMatch Bagian 7  
**Terakhir diperbarui:** 7 November 2026  
**Durasi:** Sekitar 12 minggu (usulan)  
**Pelaksana:** Deris Firmansyah (pelaksana tunggal)

---

## 1. Ringkasan

Roadmap ini menerjemahkan Grand Design Bagian 7 menjadi tahapan, output, dan kriteria selesai.
Semua tanggal bersifat relatif (Minggu 1–12), bukan tanggal kalender, sampai jadwal
akademik final ditetapkan.

Urutan besar:

```text
Literatur & requirement
→ Dataset
→ Baseline retrieval
→ TF-IDF + cosine
→ Personalisasi
→ Backend/frontend MVP (paralel)
→ Eksperimen & evaluasi
→ Laporan & demo
```

---

## 2. Prinsip Perencanaan

1. **Data dan lisensi lebih dulu** — jangan membangun di atas dataset yang belum jelas
   lisensinya.
2. **Baseline sebelum optimasi** — baseline keyword harus ada sebelum TF-IDF dibandingkan.
3. **Evaluasi bukan tahap akhir** — query set dan pedoman anotasi disiapkan lebih awal.
4. **UI paralel, bukan penghambat** — backend/frontend MVP berjalan paralel dengan
   retrieval.
5. **Satu pelaksana** — hindari pekerjaan yang tidak punya pemilik.
6. **Buffer untuk anotasi** — beban anotasi adalah risiko jadwal utama.
7. **Keputusan stack sebelum tahap 6** — React vs Django harus diputuskan agar tidak
   memblokir UI.

---

## 3. Timeline

| Tahap | Minggu | Output | Kriteria selesai |
|---|---:|---|---|
| **1. Literature review dan requirement** | 1–2 | Matriks literatur, log pencarian, requirement tertulis | RQ dan ruang lingkup disetujui; dokumen PRD dan riset tersedia |
| **2. Dataset preparation** | 2–4 | Korpus bersih, dokumentasi sumber dan lisensi, korpus Indonesia sintetis | Lisensi tercatat; dataset manifest lengkap; kualitas data diperiksa |
| **3. Baseline retrieval** | 4–5 | Mesin keyword matching dan skrip evaluasi dasar | Baseline dapat dijalankan pada query set awal |
| **4. TF-IDF dan Cosine** | 5–6 | Mesin retrieval utama dan konfigurasi preprocessing | TC01–TC04 lulus; konfigurasi eksperimen tercatat |
| **5. Personalisasi** | 6–7 | Profil vektor, FinalScore, profil simulasi | TC07–TC10 lulus; E3/E4 dapat dijalankan |
| **6. Backend dan frontend MVP** (paralel dengan tahap 4–5) | 6–9 | API dan antarmuka: cari, simpan, feed, dashboard evaluasi | Alur utama dapat didemokan; test API lulus |
| **7. Eksperimen dan evaluasi** | 9–11 | Judgment lengkap, hasil E1–E4, uji statistik, analisis kesalahan | Metrik dan uji terdokumentasi; hasil dapat direproduksi |
| **8. Laporan dan demonstrasi** | 11–12 | Laporan, README, demo | Klaim didukung data; keterbatasan dan reproducibility tercatat |

---

## 4. Milestone dan Exit Criteria

| Milestone | Akhir minggu | Exit criteria |
|---|---:|---|
| **M1 — Requirements baseline** | 2 | RQ, persona, lingkup MVP, dan non-goals tertulis; matriks literatur awal |
| **M2 — Data siap** | 4 | Korpus Inggris dan Indonesia tersedia; lisensi/atribusi tercatat; duplikat dan field wajib diperiksa |
| **M3 — Baseline berjalan** | 5 | Keyword matching + skrip evaluasi dasar dapat dijalankan |
| **M4 — Retrieval utama** | 6 | TF-IDF + cosine berjalan; TC01–TC04 lulus; konfigurasi terkunci |
| **M5 — Personalisasi** | 7 | Profil vektor + FinalScore; TC07–TC10 lulus; profil simulasi tersedia |
| **M6 — MVP web** | 9 | Pencarian, filter, detail, auth, preferensi, bookmark, feed, event, dashboard admin dapat dipakai |
| **M7 — Evaluasi lengkap** | 11 | E1–E4 selesai; E5 pada 1k/5k/20k (penundaan 20k dicatat sebagai keterbatasan); statistik dan analisis kesalahan |
| **M8 — Laporan dan demo** | 12 | Laporan, README, demo, dataset/judgment, manifest reproducibility |

---

## 5. Rincian Pekerjaan per Tahap

### Tahap 1 — Literature review dan requirement (Minggu 1–2)

**Aktivitas**

- Susun matriks literatur 2021–2026.
- Catat log pencarian dan kriteria inklusi/eksklusi.
- Finalkan RQ, hipotesis, dan ruang lingkup.
- Validasi persona awal (wawancara singkat bila memungkinkan).
- Tinjau lisensi kandidat dataset.

**Output**

- Matriks literatur.
- Log pencarian.
- Requirement tertulis (PRD ini).
- Daftar kandidat dataset dan status lisensi.

**Dependensi**

- Akses ke sumber literatur.
- Persetujuan pembimbing untuk ruang lingkup.

### Tahap 2 — Dataset preparation (Minggu 2–4)

**Aktivitas**

- Verifikasi lisensi dan ketentuan dataset.
- Unduh subset 3.000–5.000 dokumen Inggris.
- Buat korpus Indonesia sintetis 200–500 dokumen.
- Bersihkan HTML/URL, normalisasi, deduplikasi, deteksi bahasa.
- Catat manifest: sumber, lisensi, tanggal akses, hash, versi.
- Siapkan korpus skala 1k/5k/20k untuk E5.

**Output**

- Korpus bersih.
- Dokumentasi sumber dan lisensi.
- Korpus Indonesia sintetis berlabel.
- Dataset manifest.

**Dependensi**

- Lisensi jelas sebelum unduh.
- Keputusan tentang sumber Indonesia.

**Risiko**

- Lisensi tidak mengizinkan penggunaan → ganti dataset/korpus.
- Korpus Indonesia tidak representatif → nyatakan sebagai keterbatasan.

### Tahap 3 — Baseline retrieval (Minggu 4–5)

**Aktivitas**

- Implementasikan keyword matching sederhana.
- Buat skrip evaluasi dasar (P@K, MAP, NDCG).
- Siapkan query set awal (40–60 query).
- Buat pedoman anotasi versi awal.
- Pilot anotasi 5 query.

**Output**

- Mesin baseline.
- Skrip evaluasi.
- Query set awal.
- Pedoman anotasi.

**Dependensi**

- Korpus siap.
- Query set disusun.

### Tahap 4 — TF-IDF dan Cosine (Minggu 5–6)

**Aktivitas**

- Implementasikan pipeline preprocessing 8 langkah.
- Bangun indeks TF-IDF per field.
- Implementasikan cosine dan penggabungan bobot.
- Implementasikan tie-break deterministik.
- Uji TC01–TC04.
- Siapkan konfigurasi eksperimen (stopword, stemming, bobot, n-gram).

**Output**

- Mesin retrieval utama.
- Indeks TF-IDF.
- Konfigurasi preprocessing.
- Test unit.

**Dependensi**

- Baseline dan korpus.
- Keputusan versi scikit-learn/SciPy.

### Tahap 5 — Personalisasi (Minggu 6–7)

**Aktivitas**

- Implementasikan pembentukan profil dan peluruhan waktu.
- Implementasikan `FinalScore`.
- Buat 6–10 profil simulasi (3–8 seed per persona).
- Implementasikan slot non-personalisasi.
- Uji TC07–TC10.
- Siapkan E3/E4.

**Output**

- Profil vektor.
- FinalScore.
- Profil simulasi.
- Konfigurasi α/β.

**Dependensi**

- Retrieval utama.
- Data interaksi simulasi.

### Tahap 6 — Backend dan frontend MVP (Minggu 6–9, paralel)

**Aktivitas**

- Bangun API sesuai `03-api-spec.md`.
- Autentikasi, preferensi, bookmark, event, rekomendasi, admin eval.
- Bangun UI: pencarian, filter, detail, auth, preferensi, bookmark, feed, dashboard.
- Implementasikan penjelasan Tinggi/Sedang/Rendah.
- Integrasikan event tracking.
- Uji API dan alur utama.

**Output**

- API MVP.
- UI MVP.
- Dokumentasi OpenAPI.
- Test integration.

**Dependensi**

- Keputusan stack (React vs Django) sebelum tahap 6.
- Kontrak API disepakati.

**Risiko**

- React belum dikuasai → fallback Django.
- Waktu habis → prioritaskan alur cari, simpan, feed.

### Tahap 7 — Eksperimen dan evaluasi (Minggu 9–11)

**Aktivitas**

- Lengkapi relevance judgment (minimal 2 annotator; 25% ganda).
- Hitung Cohen’s κ.
- Jalankan E1–E4.
- Jalankan E5 pada 1k/5k/20k. Jika 20k tidak selesai, catat sebagai keterbatasan; jangan
  mengganti angka 20k dengan klaim yang tidak diuji.
- Uji statistik dan effect size.
- Analisis kasus gagal per query.
- Simpan manifest eksperimen.

**Output**

- Judgment lengkap.
- Hasil E1–E4.
- Hasil E5.
- Tabel metrik dan statistik.
- Analisis kesalahan.

**Dependensi**

- Query set dan pedoman final.
- Annotator kedua.
- Konfigurasi eksperimen terkunci.

**Risiko**

- Beban anotasi → kurangi query/pool sejak awal.
- Annotator tidak tersedia → κ terbatas; catat sebagai keterbatasan.

### Tahap 8 — Laporan dan demonstrasi (Minggu 11–12)

**Aktivitas**

- Tulis laporan dengan klaim yang didukung data.
- Lengkapi README dan dokumentasi reproducibility.
- Siapkan demo: cari, filter, simpan, feed, penjelasan, dashboard.
- Siapkan dataset dan judgment untuk lampiran.
- Review keterbatasan dan keputusan terbuka.

**Output**

- Laporan.
- README.
- Demo.
- Dataset/judgment.
- Manifest reproducibility.

**Dependensi**

- Hasil evaluasi.
- MVP berjalan.

---

## 6. Critical Path dan Dependensi

```text
Lisensi dataset
→ Korpus bersih
→ Baseline
→ TF-IDF
→ Personalisasi
→ Eksperimen
→ Laporan
```

Critical path:

1. **Lisensi dataset** — tanpa ini, korpus tidak dapat dipakai.
2. **Query set + pedoman anotasi** — harus siap sebelum evaluasi; jangan menunggu akhir.
3. **Annotator kedua** — dibutuhkan untuk Cohen’s κ; belum ditentukan.
4. **Keputusan stack** — sebelum tahap 6; jika terlambat, UI tertunda.
5. **Konfigurasi eksperimen** — harus dikunci sebelum test set dilaporkan.

Pekerjaan paralel:

- UI/API dapat berjalan paralel dengan retrieval.
- Anotasi dapat dimulai setelah query set awal siap.
- Penulisan laporan dimulai sejak hasil pertama, bukan minggu 11.

---

## 7. Definition of Done

### Kode

- Berjalan di lingkungan pengembangan dan deployment.
- Test unit/integration lulus.
- Tidak ada rahasia di repository.
- Konfigurasi eksperimen di berkas.
- README cara menjalankan.

### Dataset

- Sumber, lisensi, tanggal akses, versi, hash tercatat.
- Atribusi sesuai lisensi.
- Data sintetis diberi label.
- Kualitas data diperiksa.

### Evaluasi

- Query set dan judgment versi final.
- Konfigurasi, seed, versi kode/pustaka tercatat.
- Metrik dan uji statistik dilaporkan.
- Kasus gagal dianalisis.
- Hasil tidak signifikan tetap dilaporkan.

### UI

- Alur utama dapat diselesaikan.
- Penjelasan hasil tampil.
- Empty/error/loading state jelas.
- Aksesibilitas dasar (keyboard, kontras, label).

### Laporan

- Klaim sesuai kebijakan klaim.
- Keterbatasan ditulis.
- Reproducibility didokumentasikan.
- Tidak ada sitasi yang belum diverifikasi.

---

## 8. Sumber Daya

| Peran | Orang | Catatan |
|---|---|---|
| Pelaksana | Deris Firmansyah | Seluruh tahapan; tanpa pembagian peran |
| Annotator kedua | Belum ditentukan | Diperlukan untuk Cohen’s κ; di luar proyek |
| Pembimbing | Belum disebut | Konsultasi metode, etika, dan klaim |

**Kebutuhan eksternal:** annotator tambahan untuk penilaian ganda. Jika tidak tersedia,
laporkan κ sebagai keterbatasan dan gunakan satu annotator dengan audit sampel.

---

## 9. Luaran

- Mesin retrieval dan rekomendasi yang teruji, dengan konfigurasi dan seed yang membuat
  hasil dapat direproduksi.
- Prototipe web: pencarian, filter, detail, bookmark, feed rekomendasi dengan alasan,
  event tracking, dan dashboard evaluasi.
- Dataset beserta dokumentasi sumber, lisensi, dan pembersihan.
- Relevance judgment (CSV) beserta pedoman anotasi.
- Laporan penelitian dengan klaim yang didukung data, termasuk keterbatasan.
- Dokumentasi reproducibility.
- README dan demo.

---

## 10. Ukuran Dampak dan Demo

- Dampak pada kualitas ranking diukur lewat metrik retrieval dan dilaporkan relatif
  terhadap baseline.
- Metrik produk (CTR, save rate, application click-through, zero-result rate) hanya
  dilaporkan bila ada pengguna nyata dalam jumlah memadai. Tanpa itu, statusnya rencana.
- Usability test dasar 5–8 peserta dapat dilakukan dengan persetujuan tertulis dan
  konsultasi prosedur etik kampus.
- Demo harus menunjukkan:
  1. pencarian dan filter;
  2. penjelasan hasil;
  3. simpan bookmark;
  4. feed rekomendasi dengan alasan;
  5. dashboard evaluasi;
  6. data simulasi ditandai.

---

## 11. Keputusan yang Memengaruhi Jadwal

1. React vs Django (sebelum tahap 6).
2. Dataset Inggris final dan lisensi (tahap 2).
3. Sumber korpus Indonesia (tahap 2).
4. Jumlah query dan kedalaman pool (tahap 3).
5. Annotator kedua (tahap 6–7).
6. Split validation/test (tahap 7).
7. Apakah E5 20k dokumen dijalankan atau hanya 1k/5k (tahap 7).

---

## 12. Traceability

| Tahap | Sumber Grand Design |
|---|---|
| 1 | Bagian 7 Tahap 1 |
| 2 | Bagian 7 Tahap 2; Bagian 4 |
| 3 | Bagian 7 Tahap 3 |
| 4 | Bagian 7 Tahap 4; Bagian 5 |
| 5 | Bagian 7 Tahap 5; Bagian 5 |
| 6 | Bagian 7 Tahap 6 |
| 7 | Bagian 7 Tahap 7; Bagian 6 |
| 8 | Bagian 7 Tahap 8 |
| Luaran | Bagian 7 Luaran |
| Pelaksana | Bagian 7 Pelaksana tunggal |
