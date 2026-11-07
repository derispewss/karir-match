# Fase 8 — Laporan dan Demo

**Minggu:** 11–12  
**Estimasi:** ±6,5 hari  
**Status:** Belum dimulai  
**Prasyarat:** Gate F7 lulus; MVP berjalan; hasil evaluasi tersedia  
**Gate keluar:** F8 — laporan final, demo berhasil, klaim didukung data

---

## Tujuan

Menyusun laporan penelitian dan demonstrasi yang jujur: setiap klaim menunjuk ke
eksperimen, metrik, dan konfigurasi yang mendukung, serta keterbatasan dinyatakan.

---

## Tugas

### P8-01 — Outline laporan

- [ ] Ikuti template akademik kampus.
- [ ] Susun bab: pendahuluan, tinjauan pustaka, metode, rancangan sistem, hasil,
  pembahasan, kesimpulan, keterbatasan, lampiran.
- [ ] Petakan setiap RQ ke bab hasil.
- [ ] Catat halaman/format yang diwajibkan.

- **Output:** Outline laporan.
- **Estimasi:** 0,25 hari.
- **Dependensi:** P1-07.
- **Acceptance:** Outline mencakup semua RQ dan ruang lingkup.

### P8-02 — Tulis metode dan arsitektur

- [ ] Jelaskan design science research dan urutan kerja.
- [ ] Jelaskan dataset, preprocessing, TF-IDF, cosine, dan personalisasi.
- [ ] Jelaskan arsitektur modular monolith dan batas modul.
- [ ] Sertakan diagram yang konsisten dengan `docs/02-system-design.md`.
- [ ] Jelaskan pemilihan baseline dan protokol evaluasi.

- **Output:** Bab metode dan rancangan sistem.
- **Estimasi:** 1,0 hari.
- **Dependensi:** P8-01.
- **Acceptance:** Metode dapat direplikasi; tidak ada klaim yang tidak dijelaskan.

### P8-03 — Tulis hasil

- [ ] Sajikan E1–E5 dengan tabel dan grafik.
- [ ] Pisahkan hasil per bahasa.
- [ ] Tampilkan baseline vs usulan, ablation, dan latensi.
- [ ] Sertakan ukuran efek, interval kepercayaan, dan p-value.
- [ ] Jelaskan hasil yang tidak signifikan tanpa menyembunyikannya.

- **Output:** Bab hasil.
- **Estimasi:** 1,0 hari.
- **Dependensi:** P7-09, P7-11.
- **Acceptance:** Setiap angka dapat dilacak ke manifest/run file.

### P8-04 — Tulis pembahasan, keterbatasan, dan klaim

- [ ] Jelaskan mengapa hasil terjadi, bukan hanya angkanya.
- [ ] Hubungkan dengan literatur dan research gap.
- [ ] Nyatakan keterbatasan: TF-IDF, dataset, query set, simulasi, anotasi.
- [ ] Terapkan kebijakan klaim: tidak ada “unggul” tanpa data.
- [ ] Tulis pekerjaan lanjutan yang realistis.

- **Output:** Bab pembahasan dan keterbatasan.
- **Estimasi:** 1,0 hari.
- **Dependensi:** P8-03.
- **Acceptance:** Setiap klaim menunjuk bukti; keterbatasan eksplisit.

### P8-05 — Verifikasi sitasi dan atribusi

- [ ] Periksa setiap sitasi di daftar pustaka.
- [ ] Verifikasi DOI/metadata yang masih ditandai belum terverifikasi.
- [ ] Cantumkan atribusi dataset sesuai lisensi.
- [ ] Tandai preprint sebagai preprint.
- [ ] Hapus rujukan yang tidak dibaca.

- **Output:** Daftar pustaka final dan atribusi.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P1-03, P8-02–P8-04.
- **Acceptance:** Tidak ada sitasi yang belum diverifikasi; atribusi lengkap.

### P8-06 — Siapkan lampiran

- [ ] Lampirkan query set dan pedoman anotasi.
- [ ] Lampirkan ringkasan relevance judgment (tanpa data pribadi).
- [ ] Lampirkan konfigurasi eksperimen dan manifest.
- [ ] Lampirkan tabel metrik lengkap.
- [ ] Sertakan tautan/arsip artefak bila diizinkan.

- **Output:** Lampiran laporan.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P7-11.
- **Acceptance:** Lampiran cukup untuk reproduksi; tidak ada data sensitif.

### P8-07 — Slide dan skrip demo

- [ ] Susun slide: masalah, solusi, arsitektur, hasil, keterbatasan.
- [ ] Tulis skrip demo untuk enam poin: cari, penjelasan, simpan, feed, dashboard,
  label simulasi.
- [ ] Siapkan data demo yang bersih.
- [ ] Siapkan akun demo tanpa data pribadi.

- **Output:** Slide dan skrip demo.
- **Estimasi:** 0,75 hari.
- **Dependensi:** P6-24, P8-03.
- **Acceptance:** Demo dapat diikuti tanpa penjelasan di luar skrip.

### P8-08 — Latihan demo dan fallback

- [ ] Latih demo minimal dua kali.
- [ ] Ukur waktu; potong bagian yang tidak penting.
- [ ] Siapkan fallback: screenshot, rekaman, atau data offline bila layanan gagal.
- [ ] Siapkan jawaban untuk pertanyaan sulit (skor, personalisasi, simulasi, lisensi).

- **Output:** Demo terlatih dan rencana fallback.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P8-07.
- **Acceptance:** Demo selesai dalam batas waktu; fallback tersedia.

### P8-09 — Demo day

- [ ] Jalankan demo sesuai skrip.
- [ ] Catat pertanyaan, masukan, dan kendala teknis.
- [ ] Jangan mengklaim lebih dari yang ditunjukkan.
- [ ] Simpan rekaman bila diizinkan.

- **Output:** Catatan demo dan masukan.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P8-08.
- **Acceptance:** Demo berjalan; masukan tercatat.

### P8-10 — Revisi dan finalisasi laporan

- [ ] Perbaiki laporan berdasarkan masukan demo/pembimbing.
- [ ] Periksa konsistensi angka antara laporan, dashboard, dan manifest.
- [ ] Periksa format, daftar isi, dan daftar pustaka.
- [ ] Simpan versi final dan salinan PDF.

- **Output:** Laporan final.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P8-09.
- **Acceptance:** Tidak ada angka yang berbeda antar dokumen; format sesuai ketentuan.

---

## Deliverable Fase

- [ ] Laporan final (dan PDF).
- [ ] Slide presentasi.
- [ ] Skrip dan data demo.
- [ ] Lampiran query set, judgment, konfigurasi, manifest.
- [ ] Daftar pustaka terverifikasi dan atribusi dataset.

---

## Gate F8

- [ ] Semua RQ terjawab atau dinyatakan tidak terjawab dengan alasan.
- [ ] Setiap klaim menunjuk eksperimen/metrik/konfigurasi.
- [ ] Keterbatasan dan hasil negatif dilaporkan.
- [ ] Sitasi dan atribusi terverifikasi.
- [ ] Demo berhasil atau kegagalan dijelaskan.
- [ ] Angka konsisten antara laporan, dashboard, dan manifest.

---

## Risiko Fase

| Risiko | Mitigasi |
|---|---|
| Laporan terlambat | Mulai menulis sejak hasil pertama, bukan Minggu 11 |
| Angka tidak konsisten | Satu sumber manifest; cek silang sebelum final |
| Demo gagal saat hari-H | Fallback screenshot/rekaman; data demo lokal |
| Klaim berlebihan | Review dengan kebijakan klaim |
| Sitasi belum diverifikasi | Verifikasi di P8-05; hapus yang tidak dibaca |
| Waktu presentasi melebihi | Latihan dan potong bagian non-esensial |

---

## Traceability

- `docs/delivery/roadmap.md` Bagian 7–10.
- `docs/delivery/risk-register.md` Bagian 3.
- `docs/research/research-and-evaluation.md` Bagian 9–11.
