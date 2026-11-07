# Fase 6 — Backend dan Frontend MVP

**Minggu:** 6–9 (paralel dengan F4–F5)  
**Estimasi:** ±13,5 hari  
**Status:** Belum dimulai  
**Prasyarat:** Gate F4 dan F5 untuk integrasi; keputusan D2 dan D3 sebelum mulai  
**Gate keluar:** F6 — alur utama dapat didemokan, test integration lulus, OpenAPI valid

---

## Tujuan

Membangun prototipe web yang memakai mesin retrieval dan rekomendasi: pencarian,
filter, detail, autentikasi, preferensi, bookmark, feed, event tracking, dan
dashboard evaluasi admin.

---

## Tugas Backend

### P6-01 — Skema database dan migrasi

- [ ] Implementasikan tabel: `users`, `user_preferences`, `job_categories`, `jobs`,
  `skills`, `job_skills`, `saved_jobs`, `search_history`, `interaction_events`,
  `recommendation_logs`.
- [ ] Implementasikan tabel evaluasi: `eval_queries`, `relevance_judgments`, `eval_runs`.
- [ ] Tambahkan constraint: email unik, composite PK bookmark, grade 0–2, enum event.
- [ ] Aktifkan `PRAGMA foreign_keys = ON` untuk SQLite.
- [ ] Buat indeks sesuai `docs/data/database-design.md` Bagian 5.
- [ ] Siapkan migrasi naik/turun.

- **Output:** Skema database dan migrasi.
- **Estimasi:** 0,75 hari.
- **Dependensi:** P0-02.
- **Acceptance:** Migrasi berjalan di SQLite dan PostgreSQL; constraint diuji;
  skema sesuai dokumen.

### P6-02 — Lapisan repository dan seed data

- [ ] Buat lapisan akses data dengan kueri berparameter/ORM.
- [ ] Buat seed kategori, skills, dan lowongan dari dataset v1.
- [ ] Pastikan seed idempoten dan dapat dijalankan ulang.
- [ ] Jangan menaruh data pribadi nyata di seed.

- **Output:** Repository dan seed script.
- **Estimasi:** 0,25 hari.
- **Dependensi:** P6-01, P2-08.
- **Acceptance:** Seed dua kali tidak menggandakan data; kueri tidak memakai
  string interpolation.

### P6-03 — Autentikasi dan sesi

- [ ] Putuskan D3: session cookie atau bearer token.
- [ ] Hash kata sandi dengan bcrypt atau argon2; jangan menulis algoritma sendiri.
- [ ] Implementasikan register, login, logout.
- [ ] Terapkan rate limit login dan pesan error generik.
- [ ] Jika cookie: `HttpOnly`, `Secure` di deployment, `SameSite` sesuai; proteksi CSRF.
- [ ] Jika token: masa berlaku, penyimpanan aman, dan logout yang mengakhiri token.
- [ ] Tulis test registrasi duplikat, kredensial salah, dan rate limit.

- **Output:** Endpoint autentikasi dan test.
- **Estimasi:** 1,0 hari.
- **Dependensi:** P6-01, D3.
- **Acceptance:** Kata sandi tidak pernah tersimpan/log dalam bentuk mentah; error
  tidak membocorkan keberadaan email; rate limit bekerja.

### P6-04 — Endpoint pencarian dan detail lowongan

- [ ] Implementasikan `GET /api/jobs/search` dengan query, filter, sort, limit.
- [ ] Validasi `limit`, `sort`, dan tipe filter.
- [ ] Kembalikan `match_level`, `matched_terms`, dan `reason`; jangan kirim skor mentah.
- [ ] Implementasikan `GET /api/jobs/{job_id}`.
- [ ] Tangani empty state dan indeks belum siap (503).
- [ ] Tentukan kebijakan lowongan tidak aktif dan terapkan konsisten.

- **Output:** Endpoint jobs dan test kontrak.
- **Estimasi:** 0,75 hari.
- **Dependensi:** P4-07, P6-01.
- **Acceptance:** Respons sesuai `docs/api/openapi.yaml`; pengguna anonim dapat
  mencari; tidak ada skor mentah di respons publik.

### P6-05 — Endpoint preferensi

- [ ] Implementasikan `GET /api/me/preferences`.
- [ ] Implementasikan `PUT /api/me/preferences`.
- [ ] Validasi tipe data; array kosong valid.
- [ ] Periksa kepemilikan data di server.

- **Output:** Endpoint preferensi dan test.
- **Estimasi:** 0,25 hari.
- **Dependensi:** P6-01, P6-03.
- **Acceptance:** Hanya pemilik dapat membaca/mengubah; preferensi langsung dipakai
  pada pencarian/feed berikutnya.

### P6-06 — Endpoint bookmark idempoten

- [ ] Implementasikan `GET /api/me/bookmarks` dengan limit/offset.
- [ ] Implementasikan `POST /api/me/bookmarks`.
- [ ] Implementasikan `DELETE /api/me/bookmarks/{job_id}`.
- [ ] Pastikan simpan ganda menghasilkan satu baris (TC11).
- [ ] Pastikan hapus bookmark yang tidak ada tetap 204.
- [ ] Catat event `save` secara otomatis tanpa duplikasi.

- **Output:** Endpoint bookmark dan test.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P6-01, P6-03.
- **Acceptance:** TC11 lulus; bookmark hanya dapat diakses pemiliknya.

### P6-07 — Event tracking

- [ ] Implementasikan `POST /api/events`.
- [ ] Validasi `event_type` dan field wajib per tipe.
- [ ] Set `is_simulated` di server, bukan dari klien biasa.
- [ ] Deduplikasi event `save` per pengguna + lowongan + jenis sinyal.
- [ ] Jangan menyimpan isi lamaran, CV, atau data sensitif.
- [ ] Catat posisi tayang untuk analisis position bias.

- **Output:** Endpoint event dan test.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P6-03.
- **Acceptance:** Event simulasi tidak masuk agregat produk; tidak ada data sensitif.

### P6-08 — Endpoint feed rekomendasi

- [ ] Implementasikan `GET /api/me/recommendations`.
- [ ] Kecualikan lowongan yang sudah disimpan (TC10).
- [ ] Terapkan cold start `β = 0` dan slot non-personalisasi.
- [ ] Sertakan alasan dan `source`; `match_level` opsional bila valid.
- [ ] Jangan kirim skor mentah.
- [ ] Terapkan keputusan D4 secara konsisten.

- **Output:** Endpoint rekomendasi dan test.
- **Estimasi:** 0,75 hari.
- **Dependensi:** P5-02, P5-04, P5-05, P6-03.
- **Acceptance:** Feed sesuai kontrak; TC10 lulus; pengguna baru tidak menerima
  alasan personalisasi palsu.

### P6-09 — Penghapusan data pengguna

- [ ] Implementasikan `DELETE /api/me/data`.
- [ ] Hapus preferensi, bookmark, riwayat pencarian, event, dan log rekomendasi
  dalam satu transaksi.
- [ ] Jangan menghapus data evaluasi.
- [ ] Buat operasi idempoten.

- **Output:** Endpoint hapus data dan test.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P6-01, P6-03.
- **Acceptance:** Data pengguna terhapus; data evaluasi tetap; respons 204.

### P6-10 — Endpoint admin evaluasi

- [ ] Implementasikan `GET /api/admin/eval/summary`.
- [ ] Implementasikan `POST /api/admin/eval/run`.
- [ ] Terapkan role admin; pengguna biasa mendapat 403 (TC12).
- [ ] Validasi `config_path` terhadap direktori konfigurasi yang diizinkan.
- [ ] Batasi eksekusi sinkron; arahkan evaluasi berat ke CLI.
- [ ] Tampilkan `config_hash` dan `dataset_hash` pada hasil.

- **Output:** Endpoint admin dan test.
- **Estimasi:** 0,75 hari.
- **Dependensi:** P6-03, P7-11 (untuk data hasil).
- **Acceptance:** TC12 lulus; tidak ada path traversal; hasil tanpa hash ditolak.

### P6-11 — Error envelope, logging, dan keamanan

- [ ] Terapkan format error konsisten (`error.code`, `message`, `details`, `request_id`).
- [ ] Tambahkan request ID dan structured logging.
- [ ] Jangan log kata sandi, token, isi lamaran, atau data sensitif.
- [ ] Tambahkan header keamanan dan CORS terbatas.
- [ ] Pastikan stack trace tidak dikirim ke klien.

- **Output:** Middleware error/logging dan konfigurasi keamanan.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P6-03.
- **Acceptance:** Error tidak membocorkan detail internal; log tidak memuat rahasia.

### P6-12 — Sinkronisasi kontrak OpenAPI

- [ ] Pastikan setiap endpoint sesuai `docs/api/openapi.yaml`.
- [ ] Validasi spec dengan `openapi-spec-validator`.
- [ ] Tambahkan contract test untuk status code dan skema utama.
- [ ] Perbarui spec bila ada perubahan kontrak dan catat di changelog.

- **Output:** OpenAPI tersinkron dan tervalidasi.
- **Estimasi:** 0,25 hari.
- **Dependensi:** P6-04–P6-10.
- **Acceptance:** Spec valid; tidak ada operation ID duplikat; contract test lulus.

---

## Tugas Frontend

### P6-13 — Scaffold frontend, routing, dan API client

- [ ] Siapkan React + Vite (atau Django sesuai D2).
- [ ] Buat routing halaman: cari, detail, login, register, preferensi, bookmark, feed, admin.
- [ ] Buat API client dengan penanganan error dan base URL dari environment.
- [ ] Jangan menaruh rahasia di frontend.

- **Output:** Scaffold frontend dan API client.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P0-03, D2.
- **Acceptance:** Halaman dapat dibuka; API client menangani error dengan pesan aman.

### P6-14 — Halaman pencarian

- [ ] Search bar, filter lokasi/kategori/tipe/level, dan sort.
- [ ] Tampilkan hasil dengan tingkat kecocokan dan istilah yang cocok.
- [ ] Tampilkan empty, loading, dan error state.
- [ ] Tampilkan filter aktif dan cara menghapusnya.
- [ ] Jangan menampilkan skor mentah atau persentase.

- **Output:** Halaman pencarian.
- **Estimasi:** 0,75 hari.
- **Dependensi:** P6-04, P6-13.
- **Acceptance:** Alur cari–filter–sort berfungsi; empty state jelas.

### P6-15 — Halaman detail lowongan

- [ ] Tampilkan judul, perusahaan, lokasi, tipe, level, kategori, deskripsi,
  kualifikasi, skills, tanggal, dan sumber.
- [ ] Sediakan tombol simpan dan event `view`/`rec_click` sesuai konteks.
- [ ] Tandai lowongan tidak aktif sesuai kebijakan.
- [ ] Tampilkan ikon info bahwa tingkat kecocokan bukan peluang diterima.

- **Output:** Halaman detail.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P6-04, P6-06, P6-13.
- **Acceptance:** Detail dapat dibuka dari pencarian, bookmark, dan feed.

### P6-16 — Halaman registrasi dan login

- [ ] Form registrasi dan login dengan validasi.
- [ ] Tampilkan pesan error generik untuk kredensial salah.
- [ ] Tangani status login dan logout.
- [ ] Jangan menyimpan token di tempat yang tidak aman.

- **Output:** Halaman auth.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P6-03, P6-13.
- **Acceptance:** Alur register–login–logout berfungsi; error tidak membocorkan email.

### P6-17 — Halaman preferensi

- [ ] Form kategori, lokasi, tipe, dan level.
- [ ] Simpan dan tampilkan preferensi saat ini.
- [ ] Tampilkan konfirmasi dan error yang jelas.
- [ ] Pastikan array kosong valid.

- **Output:** Halaman preferensi.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P6-05, P6-13.
- **Acceptance:** Perubahan tersimpan dan dipakai pada pencarian/feed berikutnya.

### P6-18 — Halaman bookmark

- [ ] Daftar bookmark dengan pagination.
- [ ] Hapus bookmark dan tangani respons idempoten.
- [ ] Tampilkan empty state.
- [ ] Tautkan ke detail lowongan.

- **Output:** Halaman bookmark.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P6-06, P6-13.
- **Acceptance:** Simpan/hapus berfungsi; tidak ada bookmark milik pengguna lain.

### P6-19 — Halaman feed rekomendasi

- [ ] Tampilkan Top-N dengan alasan.
- [ ] Tandai slot non-personalisasi.
- [ ] Tampilkan label “simulasi” bila data simulasi ditampilkan.
- [ ] Tampilkan empty state untuk pengguna baru dengan arahan mengisi preferensi.
- [ ] Jangan menampilkan alasan personalisasi palsu.

- **Output:** Halaman feed.
- **Estimasi:** 0,75 hari.
- **Dependensi:** P6-08, P6-13.
- **Acceptance:** Feed dapat dibedakan personalisasi vs non-personalisasi; alasan
  dapat dilacak.

### P6-20 — Dashboard evaluasi admin

- [ ] Tampilkan ringkasan metrik per eksperimen, bahasa, dan split.
- [ ] Tampilkan `config_hash` dan `dataset_hash`.
- [ ] Sediakan tombol jalankan evaluasi dengan batas waktu.
- [ ] Sembunyikan akses untuk non-admin.

- **Output:** Dashboard admin.
- **Estimasi:** 0,75 hari.
- **Dependensi:** P6-10, P6-13.
- **Acceptance:** Hanya admin dapat mengakses; angka selalu disertai konteks konfigurasi.

### P6-21 — Aksesibilitas dasar

- [ ] Pastikan alur utama dapat dioperasikan dengan keyboard.
- [ ] Periksa kontras warna.
- [ ] Pastikan label formulir eksplisit.
- [ ] Jangan menyampaikan status hanya lewat warna.
- [ ] Sediakan teks alternatif untuk ikon info.

- **Output:** Checklist aksesibilitas.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P6-14–P6-20.
- **Acceptance:** Checklist terisi; masalah kritis diperbaiki.

---

## Tugas Integrasi

### P6-22 — Integration test alur utama

- [ ] Uji register–login–cari–simpan–feed–hapus data.
- [ ] Uji TC11 (bookmark idempoten), TC12 (akses admin), TC13 (event simulasi).
- [ ] Uji otorisasi data pengguna lain.
- [ ] Uji empty state dan error format.

- **Output:** Integration test dan log.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P6-03–P6-10.
- **Acceptance:** Semua test lulus; tidak ada akses lintas pengguna.

### P6-23 — Docker Compose dan health check

- [ ] Siapkan Docker Compose untuk aplikasi dan PostgreSQL.
- [ ] Siapkan volume untuk indeks/artefak.
- [ ] Tambahkan health check aplikasi dan database.
- [ ] Pastikan rahasia dibaca dari environment.
- [ ] Uji rebuild indeks di container.

- **Output:** Docker Compose dan dokumentasi deployment.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P6-01, P6-11.
- **Acceptance:** `docker compose up` menjalankan aplikasi; health check lulus.

### P6-24 — Seed demo dan smoke test

- [ ] Siapkan data demo yang aman dan berlabel simulasi bila relevan.
- [ ] Jalankan smoke test alur demo.
- [ ] Catat langkah demo dan fallback bila layanan gagal.

- **Output:** Data demo dan smoke test.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P6-22, P6-23.
- **Acceptance:** Demo dapat dijalankan dari keadaan bersih; tidak ada data pribadi.

---

## Deliverable Fase

- [ ] API sesuai kontrak OpenAPI.
- [ ] UI MVP: cari, detail, auth, preferensi, bookmark, feed, dashboard.
- [ ] Integration test dan smoke test.
- [ ] Docker Compose dan health check.
- [ ] Data demo berlabel.

---

## Gate F6

- [ ] Alur utama dapat diselesaikan dari UI.
- [ ] Semua endpoint sesuai `docs/api/openapi.yaml`; spec valid.
- [ ] TC11, TC12, TC13 lulus.
- [ ] Otorisasi kepemilikan data diuji.
- [ ] Tidak ada skor mentah di endpoint publik.
- [ ] Tidak ada rahasia atau data pribadi di repo/log.
- [ ] Docker Compose berjalan dan health check lulus.
- [ ] D2 dan D3 tercatat.

---

## Risiko Fase

| Risiko | Mitigasi |
|---|---|
| React belum dikuasai | Fallback Django sesuai ADR-0005; putuskan sebelum mulai |
| Kontrak API berubah | Contract test; perbarui spec dan changelog |
| Auth cookie vs token tertunda | Putuskan D3 di awal fase; catat di ADR |
| UI mengirim skor mentah | Audit respons; test khusus |
| Docker tidak tersedia | Sediakan cara menjalankan lokal; dokumentasikan |
| Waktu habis | Prioritaskan cari, simpan, feed; dashboard bisa menyusul |

---

## Traceability

- `docs/03-api-spec.md`.
- `docs/api/openapi.yaml`.
- `docs/data/database-design.md`.
- `docs/02-system-design.md` Bagian 8–12.
- ADR-0005, ADR-0006, ADR-0010.
- `docs/delivery/roadmap.md` Tahap 6.
