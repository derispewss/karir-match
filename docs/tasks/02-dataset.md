# Fase 2 — Dataset

**Minggu:** 2–4  
**Estimasi:** ±8 hari  
**Status:** Belum dimulai  
**Prasyarat:** Gate F1 lulus; kandidat dataset dan lisensi tersedia  
**Gate keluar:** F2 — korpus v1 beku, lisensi tercatat, manifest dan EDA lengkap

---

## Tujuan

Menghasilkan korpus yang bersih, berlisensi jelas, terdokumentasi, dan dapat
direproduksi untuk evaluasi retrieval serta rekomendasi.

---

## Tugas

### P2-01 — Verifikasi lisensi dan ketentuan dataset (gate D1)

- [x] Baca lisensi dan terms of service di halaman sumber asli, bukan ringkasan pihak ketiga.
- [x] Catat apakah penggunaan untuk riset, publikasi, dan demo diizinkan.
- [x] Catat kewajiban atribusi dan batasan redistribusi.
- [x] Jika lisensi tidak jelas atau melarang penggunaan, ganti kandidat.
- [x] Catat keputusan D1 beserta tanggal dan alasan.

- **Output:** Catatan lisensi per dataset; keputusan D1.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P1-08.
- **Acceptance:** Dataset yang dipilih memiliki lisensi tertulis yang mengizinkan
  penggunaan; keputusan dan risikonya tercatat.
- **Bukti:** Keputusan D1 terdokumentasi di `docs/tasks/evidence/dataset-license.md`. Dataset ODbL & CC0 disetujui, dataset tanpa kepastian lisensi ditolak.

### P2-02 — Akuisisi dataset dan manifest awal

- [ ] Unduh dataset yang disetujui ke `data/raw/` (tidak di-commit).
- [ ] Catat URL sumber, tanggal akses, versi, ukuran, dan hash SHA-256.
- [ ] Simpan data mentah tanpa modifikasi.
- [ ] Catat jumlah baris, kolom, dan bahasa.

- **Output:** Data mentah dan manifest awal.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P2-01.
- **Acceptance:** Hash cocok; data mentah tidak diubah; manifest memuat sumber
  dan tanggal akses.

### P2-03 — Korpus bahasa Indonesia sintetis

- [ ] Buat 200–500 dokumen lowongan sintetis berbahasa Indonesia.
- [ ] Variasikan: singkatan (`swe`, `s1`), campuran Indonesia–Inggris, level,
  lokasi, tipe pekerjaan, dan gaya penulisan.
- [ ] Gunakan template dan tulis sendiri; jangan menyalin lowongan nyata tanpa izin.
- [ ] Tandai korpus sebagai **sintetis** di manifest dan nama file.
- [ ] Jangan memakai data pribadi nyata.

- **Output:** Korpus Indonesia sintetis berlabel.
- **Estimasi:** 2,0 hari.
- **Dependensi:** P2-01.
- **Acceptance:** 200–500 dokumen; variasi istilah terdokumentasi; label sintetis
  jelas; tidak ada PII.

### P2-04 — Pipeline pembersihan dan deduplikasi

- [ ] Buang HTML, URL, dan karakter kontrol.
- [ ] Normalisasi spasi, tanda baca, dan variasi tulisan (`front-end`, `front end`,
  `frontend`).
- [ ] Deteksi bahasa per dokumen (`id`, `en`, `mixed`) dengan heuristik yang dicatat.
- [ ] Validasi field wajib: `title` dan `description`.
- [ ] Deduplikasi dengan hash `title + company + description` ternormalisasi;
  pertahankan yang terbaru.
- [ ] Tulis unit test untuk normalisasi dan deduplikasi.

- **Output:** Pipeline pembersihan dan data bersih.
- **Estimasi:** 1,5 hari.
- **Dependensi:** P2-02, P2-03.
- **Acceptance:** Pipeline deterministik; duplikat berkurang dan jumlahnya dicatat;
  dokumen tanpa field wajib dibuang dan dilaporkan.

### P2-05 — Normalisasi filter dan penghapusan PII

- [ ] Normalisasi kategori, lokasi, tipe pekerjaan, dan level pengalaman.
- [ ] Buat kamus sinonim untuk nilai filter yang sering muncul.
- [ ] Buang email, telepon, dan URL pribadi dari teks lowongan (usulan).
- [ ] Pastikan tidak ada atribut sensitif yang dipakai sebagai sinyal.

- **Output:** Nilai filter ternormalisasi; teks bebas PII.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P2-04.
- **Acceptance:** Tidak ada email/telepon di sampel teks; kategori dan lokasi
  konsisten; keputusan PII tercatat.

### P2-06 — Exploratory Data Analysis (EDA)

- [ ] Hitung jumlah dokumen per bahasa, kategori, lokasi, tipe, dan level.
- [ ] Hitung field kosong, duplikat, dan distribusi panjang teks.
- [ ] Identifikasi ketidakseimbangan dan dokumen anomali.
- [ ] Tulis ringkasan EDA beserta implikasinya terhadap evaluasi.

- **Output:** Laporan EDA.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P2-04.
- **Acceptance:** Komposisi korpus terdokumentasi; batas generalisasi dinyatakan.

### P2-07 — Korpus skala untuk E5

- [ ] Buat sampel deterministik 1.000, 5.000, dan 20.000 dokumen.
- [ ] Gunakan seed yang dicatat; jaga proporsi bahasa/kategori bila relevan.
- [ ] Pastikan korpus skala hanya untuk latensi/ukuran indeks, bukan klaim relevansi.
- [ ] Catat hash tiap ukuran.

- **Output:** Tiga korpus skala dan manifestnya.
- **Estimasi:** 1,0 hari.
- **Dependensi:** P2-04.
- **Acceptance:** Sampel dapat direproduksi dengan seed; hash dan jumlah dokumen
  tercatat.

### P2-08 — Bekukan dataset v1

- [ ] Tetapkan versi `dataset-v1`.
- [ ] Hitung hash data bersih dan simpan manifest lengkap.
- [ ] Pisahkan data mentah dan data bersih.
- [ ] Catat konfigurasi preprocessing yang dipakai.
- [ ] Jangan mengubah dataset v1 setelah evaluasi dimulai tanpa versi baru.

- **Output:** Dataset v1 beku dan manifest.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P2-04, P2-05, P2-07.
- **Acceptance:** Hash stabil; perubahan apa pun menghasilkan versi baru.

### P2-09 — Dokumentasi sumber dan atribusi

- [ ] Lengkapi manifest: sumber, lisensi, tanggal akses, versi, hash, bahasa,
  jumlah dokumen, dan pemilik.
- [ ] Tulis atribusi sesuai lisensi.
- [ ] Catat batasan penggunaan dataset di laporan dan antarmuka bila perlu.

- **Output:** Manifest dan atribusi.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P2-08.
- **Acceptance:** Atribusi sesuai lisensi; manifest dapat dibaca tanpa membuka kode.

### P2-10 — Review etika dan legalitas

- [ ] Konsultasikan penggunaan dataset dan data sintetis dengan pembimbing.
- [ ] Pastikan tidak ada scraping yang melanggar ketentuan situs.
- [ ] Catat kewajiban pelindungan data pribadi yang relevan.
- [ ] Siapkan pernyataan etika untuk laporan.

- **Output:** Catatan review etika/legalitas.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P2-01, P2-09.
- **Acceptance:** Tidak ada penggunaan data yang tidak jelas izinnya; pernyataan
  etika tersedia.

---

## Deliverable Fase

- [ ] Dataset mentah dan bersih dengan hash.
- [ ] Korpus Indonesia sintetis berlabel.
- [ ] Pipeline pembersihan dan deduplikasi.
- [ ] Laporan EDA.
- [ ] Korpus skala 1k/5k/20k.
- [ ] Dataset v1 beku dan manifest.
- [ ] Catatan lisensi, atribusi, dan etika.

---

## Gate F2

- [ ] Lisensi dataset utama tertulis dan mengizinkan penggunaan.
- [ ] Dataset v1 beku dengan hash dan manifest lengkap.
- [ ] Korpus Indonesia sintetis berlabel dan tidak diklaim sebagai data pasar.
- [ ] Duplikat, field kosong, dan PII ditangani; hasilnya dicatat.
- [ ] EDA selesai dan batas generalisasi dinyatakan.
- [ ] Review etika/legalitas dicatat.

Jika gate belum lulus, jangan mulai F3.

---

## Risiko Fase

| Risiko | Mitigasi |
|---|---|
| Lisensi dataset tidak jelas | Ganti kandidat; jangan mengunduh sebelum verifikasi |
| Data LinkedIn tunduk pada ToS platform | Konsultasikan; batasi penggunaan; siapkan dataset alternatif |
| Korpus Indonesia tidak representatif | Nyatakan sintetis; jangan klaim kondisi pasar |
| Beban membuat korpus sintetis | Gunakan template dan variasi terkontrol; target 200 dokumen bila waktu sempit |
| PII lolos ke indeks | Uji sampel; buang email/telepon/URL; catat prosedur |

---

## Traceability

- `docs/data/dataset-design.md` Bagian 2–10.
- `docs/delivery/roadmap.md` Tahap 2.
- `docs/delivery/risk-register.md` RISK-DATA-01–05.
