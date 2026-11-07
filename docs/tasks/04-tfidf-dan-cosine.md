# Fase 4 — TF-IDF dan Cosine Similarity

**Minggu:** 5–6  
**Estimasi:** ±6,5 hari  
**Status:** Belum dimulai  
**Prasyarat:** Gate F3 lulus; baseline dan query set tersedia  
**Gate keluar:** F4 — TC01–TC04 lulus, indeks dapat dibangun ulang, konfigurasi E2 siap

---

## Tujuan

Membangun mesin retrieval utama: preprocessing bersama, indeks TF-IDF per field,
Cosine Similarity, penggabungan skor, dan tie-break yang deterministik.

---

## Tugas

### P4-01 — Modul preprocessing delapan langkah

- [ ] Implementasikan case folding.
- [ ] Implementasikan normalisasi teks: buang HTML/URL, rapikan spasi dan tanda baca,
  samakan variasi tulisan.
- [ ] Implementasikan deteksi bahasa per dokumen.
- [ ] Implementasikan tokenisasi.
- [ ] Implementasikan stopword removal.
- [ ] Implementasikan stemming per bahasa.
- [ ] Implementasikan normalisasi singkatan dan variasi istilah.
- [ ] Implementasikan penggabungan field berbobot.
- [ ] Buat skema konfigurasi (YAML) agar langkah dapat dinyalakan/dimatikan.
- [ ] Pastikan pipeline dokumen dan query identik.

- **Output:** Modul preprocessing dan konfigurasi.
- **Estimasi:** 1,0 hari.
- **Dependensi:** P2-08.
- **Acceptance:** Pipeline deterministik; konfigurasi tercatat; dokumen dan query
  melewati langkah yang sama.

### P4-02 — Tokenisasi kasus khusus

- [ ] Pastikan `c++`, `node.js`, `s1`, dan istilah bertitik tidak terpotong salah.
- [ ] Tangani tanda hubung dan garis miring.
- [ ] Tambahkan test untuk setiap kasus.

- **Output:** Aturan tokenisasi dan test.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P4-01.
- **Acceptance:** Test kasus khusus lulus; tidak ada regresi pada teks biasa.

### P4-03 — Stopword Indonesia, Inggris, dan domain

- [ ] Siapkan daftar stopword Indonesia dan Inggris terpisah.
- [ ] Tambahkan stopword domain (`lowongan`, `dibutuhkan`, dan sejenisnya).
- [ ] Pastikan stopword tidak membuang term teknis penting.
- [ ] Buat opsi on/off untuk eksperimen E2.

- **Output:** Daftar stopword dan konfigurasi.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P4-01.
- **Acceptance:** Stopword dapat dinyalakan/dimatikan; dampaknya dapat diuji.

### P4-04 — Stemming per bahasa

- [ ] Pilih stemmer Indonesia dan Inggris yang tersedia dan terverifikasi.
- [ ] Kunci versi pustaka.
- [ ] Terapkan stemming sesuai bahasa dokumen.
- [ ] Untuk dokumen campuran, catat kebijakan (misalnya tidak di-stem atau
  stem mengikuti bahasa dominan).
- [ ] Uji sampel kata berimbuhan.

- **Output:** Integrasi stemmer dan kebijakan bahasa campuran.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P4-01.
- **Acceptance:** Versi stemmer tercatat; kebijakan campuran eksplisit; sampel
  stemming diperiksa.

### P4-05 — Kamus normalisasi singkatan dan variasi istilah

- [ ] Susun kamus awal: `swe` → `software engineer`, `s1` → `sarjana`,
  `fresh grad` → `fresh graduate`, dan variasi lain.
- [ ] Terapkan kamus yang sama pada dokumen dan query.
- [ ] Catat bahwa ini normalisasi leksikal, bukan pemahaman semantik.
- [ ] Uji dampak kamus pada sampel query.

- **Output:** Kamus normalisasi dan test.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P4-01.
- **Acceptance:** Kamus konsisten di kedua sisi; tidak ada klaim semantik.

### P4-06 — Indeks TF-IDF per field

- [ ] Vektorkan `title`, `skills`, dan `description` secara terpisah.
- [ ] Gunakan `sublinear_tf=True`, `smooth_idf=True`, dan normalisasi L2.
- [ ] Hitung IDF dari koleksi dokumen, bukan dari query.
- [ ] Simpan vocabulary, IDF, matriks sparse, dan metadata konfigurasi.
- [ ] Simpan hash dataset, versi pustaka, dan tanggal build.
- [ ] Buat perintah build ulang satu langkah.

- **Output:** Indeks TF-IDF per field dan metadata.
- **Estimasi:** 1,0 hari.
- **Dependensi:** P4-01, P4-04, P4-05.
- **Acceptance:** Indeks dapat dibangun ulang; metadata lengkap; ukuran dicatat.

### P4-07 — Cosine Similarity dan penggabungan skor field

- [ ] Hitung cosine per field.
- [ ] Gabungkan dengan bobot awal `title=0,4`, `skills=0,3`, `description=0,3`.
- [ ] Normalisasi ulang bobot bila field kosong.
- [ ] Pastikan skor berada di rentang 0–1 untuk term non-negatif.
- [ ] Buat bobot dapat dikonfigurasi.

- **Output:** Fungsi scoring dan konfigurasi bobot.
- **Estimasi:** 0,75 hari.
- **Dependensi:** P4-06.
- **Acceptance:** Skor sesuai rumus; field kosong tidak merusak skor; bobot dapat diubah.

### P4-08 — Tie-break deterministik

- [ ] Urutkan skor menurun.
- [ ] Jika skor sama, tanggal terbit terbaru lebih dulu.
- [ ] Jika tanggal sama, `job_id` menaik.
- [ ] Tulis test untuk skor dan tanggal yang sama.

- **Output:** Aturan tie-break dan test.
- **Estimasi:** 0,25 hari.
- **Dependensi:** P4-07.
- **Acceptance:** Urutan stabil di semua run.

### P4-09 — Test TC01–TC04

- [ ] TC01: nilai IDF sesuai rumus pada korpus mini N = 4.
- [ ] TC02: peringkat query `data analyst python` = d1, d2, d4, d3 dengan cosine
  0,7891; 0,5552; 0,4602; 0,0000.
- [ ] TC03: norma L2 vektor dokumen dan query = 1.
- [ ] TC04: deterministik saat skor sama.
- [ ] Jalankan seluruh test dan simpan log.

- **Output:** Test TC01–TC04 dan log.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P4-07, P4-08.
- **Acceptance:** Semua test lulus dengan toleransi yang terdokumentasi.

### P4-10 — CLI build dan manifest eksperimen

- [ ] Buat perintah build indeks dari dataset dan konfigurasi.
- [ ] Catat hash dataset, hash konfigurasi, versi kode/pustaka, seed, dan waktu build.
- [ ] Simpan manifest di `artifacts/index/<config_hash>/`.
- [ ] Pastikan build gagal dengan pesan jelas bila data tidak ada.

- **Output:** CLI build dan manifest.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P4-06.
- **Acceptance:** Build dapat diulang; manifest cukup untuk reproduksi.

### P4-11 — Konfigurasi eksperimen E2

- [ ] Siapkan konfigurasi: stopword on/off.
- [ ] Siapkan konfigurasi stemming: none / English / Indonesian.
- [ ] Siapkan bobot field: seragam vs title+skills lebih tinggi.
- [ ] Siapkan n-gram: unigram vs unigram+bigram.
- [ ] Pastikan setiap konfigurasi memiliki nama dan hash.

- **Output:** Set konfigurasi E2.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P4-01, P4-07.
- **Acceptance:** Konfigurasi dapat dijalankan tanpa mengubah kode; hash tercatat.

---

## Deliverable Fase

- [ ] Modul preprocessing delapan langkah.
- [ ] Indeks TF-IDF per field dengan metadata.
- [ ] Fungsi scoring dan tie-break.
- [ ] Test TC01–TC04 lulus.
- [ ] CLI build dan manifest.
- [ ] Konfigurasi E2.

---

## Gate F4

- [ ] TC01–TC04 lulus atau kegagalan dijelaskan.
- [ ] Indeks dapat dibangun ulang dengan satu perintah.
- [ ] Metadata build lengkap (dataset, konfigurasi, versi, seed).
- [ ] Konfigurasi E2 siap dan dapat dijalankan.
- [ ] Tidak ada kebocoran skor mentah ke antarmuka publik (diverifikasi di F6).

Jika gate belum lulus, jangan mulai F5.

---

## Risiko Fase

| Risiko | Mitigasi |
|---|---|
| Implementasi TF-IDF berbeda dari rumus | Uji TC01–TC03 dengan contoh manual |
| Stemming merusak istilah teknis | Uji sampel; sediakan opsi none; laporkan hasil |
| Field kosong mengubah bobot | Normalisasi ulang bobot; uji kasus field kosong |
| Indeks tidak reproducible | Manifest hash dan versi; build dari sumber |
| Bobot 0,4/0,3/0,3 dianggap final | Perlakukan sebagai hipotesis; uji di E2 |

---

## Traceability

- `docs/02-system-design.md` Bagian 4.
- `docs/research/research-and-evaluation.md` Bagian 5–7.
- ADR-0002, ADR-0003.
- `docs/delivery/roadmap.md` Tahap 4.
