# Fase 1 — Literatur dan Requirement

**Minggu:** 1–2  
**Estimasi:** ±4,25 hari  
**Status:** Belum dimulai  
**Prasyarat:** Gate F0 lulus  
**Gate keluar:** F1 — RQ final, matriks literatur, PRD ditinjau pembimbing

---

## Tujuan

Memastikan masalah, pertanyaan riset, dan ruang lingkup produk didukung literatur
yang relevan dan disetujui sebelum data dikumpulkan atau kode ditulis.

---

## Tugas

### P1-01 — Protokol pencarian literatur

- [ ] Tentukan basis data: Google Scholar, IEEE Xplore, ACM DL, Scopus (bila ada akses).
- [ ] Tulis string pencarian untuk topik: job retrieval, job recommendation,
  TF-IDF, cosine similarity, content-based recommendation, e-recruitment.
- [ ] Tetapkan kriteria inklusi: 2021–2026, relevan dengan retrieval/rekomendasi
  lowongan, bahasa Inggris atau Indonesia, teks lengkap tersedia.
- [ ] Tetapkan kriteria eksklusi: opini tanpa data, domain tidak relevan, duplikat.
- [ ] Catat tanggal pencarian dan jumlah hasil per query.

- **Output:** Protokol pencarian dan log pencarian.
- **Estimasi:** 0,5 hari.
- **Dependensi:** —
- **Acceptance:** Protokol dapat diulang orang lain; log memuat query, tanggal,
  dan kriteria.

### P1-02 — Matriks literatur

- [ ] Baca dan ringkas minimal 10 rujukan utama dari `docs/references.md`.
- [ ] Tambahkan studi relevan baru hanya jika benar-benar dibaca.
- [ ] Isi matriks: penulis/tahun, metode, dataset, metrik, hasil, keterbatasan,
  relevansi dengan KarirMatch.
- [ ] Tandai mana yang menjadi baseline, pembanding, atau pendukung.

- **Output:** Matriks literatur.
- **Estimasi:** 1,0 hari.
- **Dependensi:** P1-01.
- **Acceptance:** Setiap baris memiliki metode, dataset, dan keterbatasan; tidak
  ada rujukan yang belum dibaca.

### P1-03 — Verifikasi metadata dan DOI

- [ ] Verifikasi DOI, jurnal, volume, dan halaman lewat Crossref atau situs penerbit.
- [ ] Tandai preprint sebagai preprint.
- [ ] Perbarui `docs/references.md` bila ada koreksi.
- [ ] Jangan mengutip angka dari studi lain sebagai pembanding langsung tanpa
  dataset dan judgment yang sama.

- **Output:** Daftar rujukan terverifikasi.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P1-02.
- **Acceptance:** Semua rujukan yang dipakai memiliki metadata terverifikasi atau
  ditandai belum terverifikasi.

### P1-04 — Finalisasi RQ, hipotesis, dan uji statistik

- [ ] Tinjau RQ1–RQ5 di `docs/research/research-and-evaluation.md`.
- [ ] Pastikan setiap RQ punya eksperimen, metrik, dan uji statistik.
- [ ] Pastikan hipotesis dinyatakan sebagai hipotesis, bukan fakta.
- [ ] Catat perubahan RQ beserta alasannya.

- **Output:** RQ dan hipotesis final.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P1-02.
- **Acceptance:** Tidak ada RQ tanpa bukti rencana; semua uji statistik sesuai
  unit analisis.

### P1-05 — Validasi persona (opsional, dengan persetujuan)

- [ ] Rekrut 5–8 orang per segmen bila memungkinkan.
- [ ] Siapkan pertanyaan wawancara singkat dan lembar persetujuan.
- [ ] Catat pain point, istilah yang dipakai, dan ekspektasi penjelasan hasil.
- [ ] Jika tidak dapat dilakukan, nyatakan persona sebagai hipotesis.

- **Output:** Catatan wawancara atau pernyataan bahwa persona belum divalidasi.
- **Estimasi:** 0,5–1,0 hari.
- **Dependensi:** P0-06.
- **Acceptance:** Tidak ada data pribadi berlebih; kutipan dianonimkan; status
  validasi persona jelas.

### P1-06 — Finalisasi ruang lingkup MVP dan non-goals

- [ ] Tinjau F1–F4 dan FR di `docs/01-prd.md`.
- [ ] Kunci fitur MVP dan fitur lanjutan.
- [ ] Kunci non-goals: bukan ML adaptif, bukan embedding/LLM, bukan sisi perekrut.
- [ ] Catat mekanisme perubahan lingkup.

- **Output:** Lingkup MVP terkunci.
- **Estimasi:** 0,25 hari.
- **Dependensi:** P1-04.
- **Acceptance:** Setiap fitur MVP punya FR dan acceptance; fitur di luar lingkup
  tercatat eksplisit.

### P1-07 — Review PRD dan desain riset dengan pembimbing

- [ ] Kirim PRD, ringkasan RQ, dan rencana evaluasi ke pembimbing.
- [ ] Catat masukan dan keputusan yang berubah.
- [ ] Perbarui dokumen terkait.

- **Output:** Catatan review dan dokumen revisi.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P1-04, P1-06.
- **Acceptance:** Masukan tertulis; perubahan dokumen terlacak.

### P1-08 — Daftar kandidat dataset dan status lisensi

- [ ] Tinjau kandidat dataset di `docs/data/dataset-design.md`.
- [ ] Catat lisensi, ketentuan, ukuran, bahasa, dan risiko masing-masing.
- [ ] Pilih dua kandidat utama dan satu cadangan.
- [ ] Jangan mengunduh sebelum lisensi diverifikasi (gate D1).

- **Output:** Daftar kandidat dataset dengan status lisensi.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P1-01.
- **Acceptance:** Setiap kandidat punya status lisensi; keputusan D1 dijadwalkan.

---

## Deliverable Fase

- [ ] Protokol dan log pencarian literatur.
- [ ] Matriks literatur 2021–2026.
- [ ] Rujukan terverifikasi.
- [ ] RQ, hipotesis, dan uji statistik final.
- [ ] PRD dan desain riset ditinjau pembimbing.
- [ ] Daftar kandidat dataset dan status lisensi.

---

## Gate F1

- [ ] RQ1–RQ5 final dan disetujui pembimbing.
- [ ] Matriks literatur memadai untuk klaim research gap.
- [ ] Ruang lingkup MVP dan non-goals terkunci.
- [ ] Kandidat dataset dan lisensi siap untuk diverifikasi di F2.
- [ ] Persona dinyatakan tervalidasi atau sebagai hipotesis.

Jika gate belum lulus, jangan mulai F2.

---

## Risiko Fase

| Risiko | Mitigasi |
|---|---|
| Literatur tidak mendukung klaim kebaruan | Ubah klaim menjadi replikasi terkontrol atau analisis sensitivitas |
| RQ terlalu banyak untuk 12 minggu | Prioritaskan RQ1–RQ3; RQ4–RQ5 sebagai pendukung |
| Pembimbing tidak tersedia | Jadwalkan lebih awal; catat asumsi sementara |
| Wawancara persona tidak diizinkan | Gunakan persona sebagai hipotesis dan catat keterbatasan |

---

## Traceability

- `docs/01-prd.md` Bagian 1–5.
- `docs/research/research-and-evaluation.md` Bagian 1–5.
- `docs/references.md`.
- `docs/delivery/roadmap.md` Tahap 1.
