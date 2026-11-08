# Fase 3 — Baseline dan Query Set

**Minggu:** 4–5  
**Estimasi:** ±5,25 hari  
**Status:** Belum dimulai  
**Prasyarat:** Gate F2 lulus; dataset v1 tersedia  
**Gate keluar:** F3 — baseline reproducible, query set v1, pedoman anotasi v1

---

## Tujuan

Menyediakan pembanding yang adil (keyword matching), alat ukur yang benar, query
set evaluasi, dan pedoman anotasi sebelum sistem TF-IDF dibangun.

---

## Tugas

### P3-01 — Implementasi baseline keyword matching

- [x] Hitung skor sebagai proporsi term query yang muncul di dokumen.
- [ ] Terapkan aturan yang sama untuk semua dokumen (tanpa IDF, bobot field, atau personalisasi).
- [ ] Terapkan tie-break deterministik: skor menurun, tanggal terbaru, `job_id` menaik.
- [ ] Tulis unit test untuk skor dan urutan.
- [ ] Catat batasan baseline: tidak membobot term, tidak memahami sinonim.

- **Output:** Mesin baseline dan test.
- **Estimasi:** 1,0 hari.
- **Dependensi:** P2-08.
- **Acceptance:** Baseline dapat dijalankan pada korpus v1; hasil deterministik;
  skor sesuai definisi proporsi term.

### P3-02 — Skrip evaluasi metrik

- [ ] Implementasikan P@K, R@K, F1@K, MAP, dan NDCG@K.
- [ ] Dukung K = 5, 10, 20; K = 10 sebagai utama.
- [ ] Dukung binerisasi grade ≥ 1 dan grade = 2.
- [ ] Baca run file dan qrels dengan format yang terdokumentasi.
- [ ] Tulis unit test dengan contoh yang dihitung manual.

- **Output:** Skrip evaluasi dan test.
- **Estimasi:** 1,0 hari.
- **Dependensi:** P2-08.
- **Acceptance:** Hasil skrip cocok dengan contoh manual; format input/output
  terdokumentasi.

### P3-03 — Verifikasi rumus dan varian metrik

- [ ] Pilih varian gain DCG (eksponensial atau linear) dan catat di laporan.
- [ ] Tentukan perlakuan query tanpa dokumen relevan (exclude atau 0).
- [ ] Verifikasi NDCG = 1 untuk ranking ideal.
- [ ] Catat bahwa recall bergantung pada pool, bukan absolut.

- **Output:** Catatan varian metrik dan test verifikasi.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P3-02.
- **Acceptance:** Varian metrik eksplisit; test batas lulus.

### P3-04 — Penyusunan query set

- [ ] Susun 40–60 query dengan niat yang jelas.
- [ ] Stratifikasi bahasa: Indonesia, Inggris, campuran.
- [ ] Sertakan variasi level, lokasi, dan tipe pekerjaan.
- [ ] Catat niat query dan filter yang melekat.
- [ ] Pastikan query tidak memakai dokumen seed profil simulasi.
- [ ] Bekukan query set v1 beserta versi.

- **Output:** Query set v1.
- **Estimasi:** 1,0 hari.
- **Dependensi:** P2-08.
- **Acceptance:** 40–60 query; setiap query punya niat; komposisi bahasa seimbang;
  query set dapat direproduksi.

### P3-05 — Pedoman anotasi v0.1

- [ ] Definisikan grade 0/1/2 dengan contoh batas kasus.
- [ ] Jelaskan bahwa annotator tidak melihat sistem mana yang menghasilkan dokumen.
- [ ] Jelaskan bahwa annotator tidak melihat daftar seed profil.
- [ ] Tetapkan aturan untuk dokumen batas (topik cocok, level tidak cocok, dan sebaliknya).
- [ ] Simpan pedoman dengan nomor versi.

- **Output:** Pedoman anotasi v0.1.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P3-04.
- **Acceptance:** Dua annotator dapat memahami pedoman tanpa penjelasan tambahan;
  contoh batas kasus tersedia.

### P3-06 — Pilot anotasi dan Cohen's κ awal

- [ ] Pilih 5 query pilot.
- [ ] Anotasi oleh dua orang secara terpisah.
- [ ] Hitung Cohen's κ sebelum diskusi.
- [ ] Diskusikan perbedaan dan perbaiki pedoman.
- [ ] Catat waktu yang dibutuhkan per query untuk estimasi beban.

- **Output:** Hasil pilot dan pedoman v0.2.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P3-05.
- **Acceptance:** κ awal dilaporkan; pedoman direvisi; estimasi waktu anotasi
  per query tersedia.

### P3-07 — Prosedur pooling

- [ ] Gabungkan Top-15 dari semua sistem (baseline dan TF-IDF).
- [ ] Deduplikasi dokumen per query.
- [ ] Ekspor daftar anotasi tanpa identitas sistem.
- [ ] Catat jumlah dokumen unik per query.

- **Output:** Prosedur pooling dan ekspor buta.
- **Estimasi:** 0,25 hari.
- **Dependensi:** P3-02, P3-04.
- **Acceptance:** Annotator tidak dapat melihat asal sistem; pooling dapat diulang.

### P3-08 — Jalankan baseline dan simpan run file

- [ ] Jalankan baseline pada query set v1.
- [ ] Simpan run file, konfigurasi, seed, dan versi kode.
- [ ] Hitung metrik awal (tanpa judgment lengkap, gunakan pool pilot bila ada).
- [ ] Catat waktu eksekusi.

- **Output:** Run file baseline dan metrik awal.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P3-01, P3-02, P3-04.
- **Acceptance:** Run file dapat dievaluasi ulang; konfigurasi dan seed tercatat.

---

## Deliverable Fase

- [ ] Mesin baseline keyword matching.
- [ ] Skrip evaluasi P@K, R@K, F1@K, MAP, NDCG@K.
- [ ] Query set v1 (40–60 query).
- [ ] Pedoman anotasi v0.2.
- [ ] Hasil pilot dan κ awal.
- [ ] Prosedur pooling dan run file baseline.

---

## Gate F3

- [ ] Baseline berjalan dan hasilnya deterministik.
- [ ] Metrik terverifikasi dengan contoh manual.
- [ ] Query set v1 beku dengan komposisi bahasa yang dilaporkan.
- [ ] Pedoman anotasi v0.2 siap dipakai.
- [ ] Pilot κ dan estimasi beban anotasi tersedia.
- [ ] Keputusan D6 (jumlah query dan kedalaman pool) dicatat.

Jika gate belum lulus, jangan mulai F4.

---

## Risiko Fase

| Risiko | Mitigasi |
|---|---|
| Query set tidak representatif | Stratifikasi bahasa dan niat; catat batas generalisasi |
| Beban anotasi terlalu besar | Kurangi query/pool sejak awal; catat sebagai keterbatasan |
| Baseline tidak adil | Terapkan aturan sama untuk semua dokumen; dokumentasikan |
| κ rendah | Perbaiki pedoman; pilot ulang; laporkan κ apa adanya |
| Query memakai dokumen seed profil | Periksa silang; keluarkan dari kandidat evaluasi |

---

## Traceability

- `docs/research/research-and-evaluation.md` Bagian 6–8.
- `docs/delivery/roadmap.md` Tahap 3.
- `docs/data/dataset-design.md` Bagian 5.
