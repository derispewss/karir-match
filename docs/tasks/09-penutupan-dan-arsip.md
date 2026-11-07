# Fase 9 — Penutupan dan Arsip

**Minggu:** 12  
**Estimasi:** ±2,25 hari  
**Status:** Belum dimulai  
**Prasyarat:** Gate F8 lulus  
**Gate keluar:** F9 — rilis, arsip, repo bersih, serah terima selesai

---

## Tujuan

Menutup proyek dengan rapi: merilis versi final, mengarsipkan bukti, membersihkan
rahasia dan data pribadi, serta mencatat pelajaran untuk pekerjaan lanjutan.

---

## Tugas

### P9-01 — Rilis versi final

- [ ] Pastikan semua perubahan sudah di-commit.
- [ ] Buat tag `v1.0` (jika memakai Git).
- [ ] Tulis changelog singkat: fitur, perbaikan, batasan.
- [ ] Pastikan README menyebut versi dan status.

- **Output:** Tag rilis dan changelog.
- **Estimasi:** 0,25 hari.
- **Dependensi:** P8-10.
- **Acceptance:** Versi dapat diidentifikasi dari commit/tag.

### P9-02 — Arsip dataset, judgment, dan manifest

- [ ] Arsipkan dataset v1, query set, relevance judgment, dan manifest.
- [ ] Sertakan checksum untuk setiap artefak.
- [ ] Simpan salinan di lokasi yang aman dan dapat diakses pembimbing.
- [ ] Jangan menyertakan data pribadi atau data yang tidak boleh didistribusikan.

- **Output:** Arsip lengkap dengan checksum.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P7-11, P8-06.
- **Acceptance:** Checksum cocok; arsip dapat dipulihkan; lisensi dipatuhi.

### P9-03 — Pemeriksaan keamanan dan privasi

- [ ] Cari rahasia di repository: `.env`, token, kata sandi, kunci API.
- [ ] Cari data pribadi di log, seed, dan lampiran.
- [ ] Pastikan `.gitignore` mencakup data dan artefak sensitif.
- [ ] Hapus data yang tidak diperlukan; rotasi kredensial bila pernah bocor.
- [ ] Periksa izin akses arsip.

- **Output:** Checklist keamanan dan repo bersih.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P9-01.
- **Acceptance:** Tidak ada rahasia/PII di repo; akses arsip terbatas.

### P9-04 — Finalisasi README dan known issues

- [ ] Perbarui README: cara setup, menjalankan, menguji, dan rebuild indeks.
- [ ] Catat known issues dan batasan versi.
- [ ] Catat cara memakai data demo.
- [ ] Tautkan dokumentasi dan task board.

- **Output:** README final dan daftar known issues.
- **Estimasi:** 0,25 hari.
- **Dependensi:** P9-01.
- **Acceptance:** Orang lain dapat menjalankan proyek mengikuti README.

### P9-05 — Keterbatasan dan pekerjaan lanjutan

- [ ] Rangkum keterbatasan teknis, data, dan evaluasi.
- [ ] Daftar pekerjaan lanjutan: embedding, BM25, MMR, collaborative filtering,
  notifikasi, sisi perekrut.
- [ ] Tandai mana yang memerlukan ADR baru.
- [ ] Jangan menjanjikan pekerjaan yang tidak akan dikerjakan.

- **Output:** Daftar keterbatasan dan roadmap lanjutan.
- **Estimasi:** 0,25 hari.
- **Dependensi:** P8-04.
- **Acceptance:** Daftar realistis dan konsisten dengan laporan.

### P9-06 — Serah terima dan publikasi

- [ ] Serahkan laporan, arsip, dan akses demo kepada pembimbing.
- [ ] Catat izin publikasi dan atribusi.
- [ ] Publikasikan hanya bagian yang diizinkan.
- [ ] Simpan bukti serah terima.

- **Output:** Bukti serah terima dan catatan publikasi.
- **Estimasi:** 0,25 hari.
- **Dependensi:** P9-02, P9-04.
- **Acceptance:** Penerima mengonfirmasi; publikasi sesuai izin.

### P9-07 — Retrospektif

- [ ] Catat apa yang berjalan baik.
- [ ] Catat apa yang menghambat dan seharusnya berbeda.
- [ ] Perbarui template tugas untuk proyek berikutnya.
- [ ] Tutup papan tugas dengan status akhir.

- **Output:** Catatan retrospektif.
- **Estimasi:** 0,25 hari.
- **Dependensi:** P9-06.
- **Acceptance:** Pelajaran utama tercatat; tidak ada tugas menggantung tanpa status.

---

## Deliverable Fase

- [ ] Tag rilis `v1.0` dan changelog.
- [ ] Arsip dataset, judgment, manifest, dan checksum.
- [ ] Checklist keamanan/privasi.
- [ ] README final dan known issues.
- [ ] Daftar keterbatasan dan pekerjaan lanjutan.
- [ ] Bukti serah terima.
- [ ] Catatan retrospektif.

---

## Gate F9

- [ ] Rilis dapat diidentifikasi dan dijalankan.
- [ ] Arsip lengkap dan checksum cocok.
- [ ] Tidak ada rahasia atau data pribadi di repo/arsip publik.
- [ ] README cukup untuk menjalankan proyek.
- [ ] Serah terima dikonfirmasi.
- [ ] Semua tugas memiliki status akhir (selesai/dibatalkan dengan alasan).

---

## Risiko Fase

| Risiko | Mitigasi |
|---|---|
| Rahasia terlanjur masuk Git | Rotasi kredensial; bersihkan riwayat bila perlu |
| Dataset tidak boleh didistribusikan | Arsipkan hanya metadata/hash; patuhi lisensi |
| Arsip hilang | Simpan dua salinan; checksum |
| Tugas menggantung | Review papan tugas; tandai selesai/dibatalkan |
| Publikasi melebihi izin | Periksa izin pembimbing dan lisensi dataset |

---

## Traceability

- `docs/delivery/roadmap.md` Bagian 7–9.
- `docs/delivery/risk-register.md`.
- `docs/data/dataset-design.md` Bagian 9–10.
