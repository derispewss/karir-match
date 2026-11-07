# Fase 0 — Persiapan Proyek dan Lingkungan

**Minggu:** 1  
**Estimasi:** ±2,25 hari  
**Status:** Selesai (Lolos Gate F0)  
**Prasyarat:** Dokumen baseline v1.0 disetujui  
**Gate keluar:** F0 — lingkungan reproducible, repo siap, papan tugas aktif

---

## Tujuan

Menyiapkan fondasi teknis dan administrasi sebelum pekerjaan riset dimulai, agar
tidak ada waktu terbuang untuk memperbaiki struktur proyek di tengah jalan.

---

## Tugas

### P0-01 — Inisialisasi repository dan struktur direktori

- [x] Jalankan `git init` dan buat commit awal.
- [ ] Buat `.gitignore` untuk Python, Node, `.env`, database lokal, dan artefak besar.
- [x] Buat `.gitignore` untuk Python, Node, `.env`, database lokal, dan artefak besar.
- [x] Buat struktur direktori:
  - `app/` — kode aplikasi (API, modul);
  - `research/` — paket Python murni untuk retrieval, rekomendasi, evaluasi;
  - `configs/` — konfigurasi eksperimen;
  - `data/raw/`, `data/processed/` — data mentah dan bersih (tidak di-commit);
  - `artifacts/` — indeks, run file, manifest (tidak di-commit);
  - `tests/` — unit dan integration test;
  - `docs/` — dokumentasi baseline;
  - `docs/tasks/` — papan tugas dan PDF pelaksanaan.
- [x] Tambahkan catatan bahwa data dan artefak besar tidak masuk Git.

- **Output:** Repository dengan struktur direktori dan commit awal.
- **Estimasi:** 0,5 hari.
- **Dependensi:** —
- **Acceptance:** `git status` bersih setelah commit awal; struktur direktori
  sesuai daftar; `.gitignore` mencegah `.env`, database, dan artefak masuk.
- **Bukti:** Git repo diinisialisasi; `.gitignore` aktif; direktori `app/`, `research/`, `configs/`, `data/`, `artifacts/`, `tests/`, `docs/`, `frontend/` siap; commit awal disiapkan.

### P0-02 — Environment Python dengan Conda dan kualitas kode

- [x] Pasang Miniconda atau Anaconda; catat versi dan sumber unduhannya.
- [x] Pilih dan catat versi Python (usulan 3.11+).
- [x] Buat environment Conda bernama `karirmatch`:
  `conda create -n karirmatch python=3.11 -y`.
- [x] Aktifkan environment dan catat perintahnya: `conda activate karirmatch`.
- [x] Buat `environment.yml` dengan dependensi terkunci; utamakan channel
  `conda-forge`, dan gunakan `pip` hanya untuk paket yang tidak tersedia di Conda.
- [x] Simpan lock file (`conda list --explicit > environment.lock`) agar build
  dapat direproduksi.
- [x] Pasang `pytest`, formatter, dan linter (usulan: ruff) di environment Conda.
- [x] Pastikan `pytest` dapat dijalankan dari checkout bersih setelah
  `conda env create -f environment.yml`.
- [x] Catat perintah setup Conda di README.

- **Output:** Environment Conda reproducible (`environment.yml` dan
  `environment.lock`).
- **Estimasi:** 0,5 hari.
- **Dependensi:** P0-01.
- **Acceptance:** Checkout baru dapat disiapkan dengan
  `conda env create -f environment.yml` dalam < 10 menit; `pytest` berjalan
  tanpa error konfigurasi; tidak ada dependensi yang dipasang ke environment
  global.
- **Bukti:** Miniconda3 (conda 26.9.4), Python 3.11.18 di env `karirmatch`, `environment.yml` & `environment.lock`, `pytest` (2 passed), `ruff check` & `ruff format` lolos.

### P0-03 — Environment frontend dan keputusan awal stack

- [x] Pasang Node LTS dan catat versinya.
- [x] Siapkan scaffold Vite (React) **atau** catat keputusan untuk memakai Django.
- [x] Pastikan `npm run dev` dan `npm run build` berjalan.
- [x] Catat bahwa keputusan final stack (D2) diambil paling lambat akhir Minggu 5.

- **Output:** Frontend scaffold atau catatan keputusan stack.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P0-01.
- **Acceptance:** Frontend dapat dijalankan dan di-build, atau D2 dijadwalkan
  dengan kriteria keputusan yang jelas.
- **Bukti:** Node v26.13.0, npm 11.20.0, scaffold React + Vite di folder `frontend/`, `npm run build` sukses (dist/).

### P0-04 — Konfigurasi, rahasia, dan README operasional

- [x] Buat `.env.example` berisi variabel yang dibutuhkan (database, secret key,
  CORS origin) tanpa nilai rahasia.
- [x] Pastikan `.env` tidak di-commit.
- [x] Buat README berisi cara setup, menjalankan, dan menguji.
- [x] Tambahkan health check sederhana bila aplikasi sudah ada.

- **Output:** `.env.example`, README operasional.
- **Estimasi:** 0,25 hari.
- **Dependensi:** P0-01, P0-02.
- **Acceptance:** Aplikasi dapat dijalankan dengan menyalin `.env.example` dan
  mengisi nilai lokal; tidak ada rahasia di repository.
- **Bukti:** `.env.example` tersedia, `.gitignore` mengabaikan `.env*`, README.md operasional, FastAPI health check di `/health` teruji via `tests/test_health.py`.

### P0-05 — Papan tugas dan konvensi kerja

- [x] Aktifkan folder `docs/tasks/` sebagai papan tugas.
- [x] Sepakati konvensi commit (misalnya `feat:`, `fix:`, `docs:`, `test:`).
- [x] Sepakati jadwal review mingguan (Senin/Jumat).
- [x] Catat cara menandai tugas berjalan, blocked, dan dibatalkan.
- [x] Siapkan tempat pencatatan bukti (commit, log, artefak).

- **Output:** Papan tugas aktif dan konvensi kerja.
- **Estimasi:** 0,25 hari.
- **Dependensi:** P0-01.
- **Acceptance:** Review pertama dijadwalkan; konvensi commit dan status tugas
  tertulis di `docs/tasks/README.md`.
- **Bukti:** `docs/tasks/` aktif dengan 10 markdown fase dan PDF, konvensi commit tercatat, `docs/tasks/evidence/` siap.

### P0-06 — Administrasi riset, metadata, dan etika

- [x] Konfirmasi NIM yang benar (`A11.2024.15624` atau `A11.2024.15625`).
- [x] Konfirmasi judul, nama, dan afiliasi untuk laporan.
- [x] Jadwalkan konsultasi awal dengan pembimbing.
- [x] Siapkan template persetujuan tertulis untuk wawancara/usability test.
- [x] Tanyakan prosedur etik kampus untuk penelitian dengan pengguna.
- [x] Catat kontak annotator potensial untuk Cohen's κ.

- **Output:** Metadata terkonfirmasi, jadwal konsultasi, template consent.
- **Estimasi:** 0,25 hari.
- **Dependensi:** —
- **Acceptance:** NIM terkonfirmasi secara tertulis atau dicatat sebagai risiko;
  jadwal pembimbing dan prosedur etik tercatat.
- **Bukti:** NIM terkonfirmasi `A11.2024.15624`, dicatat di risk register dan docs admin/ethics `docs/research/consent-template.md`.

---

## Deliverable Fase

- [x] Repository dengan struktur direktori dan commit awal.
- [x] Environment Conda (`karirmatch`) dan frontend yang dapat dijalankan.
- [x] `.env.example` dan README operasional.
- [x] Papan tugas aktif beserta konvensi.
- [x] Metadata riset dan administrasi etika tercatat.

---

## Gate F0

- [x] Checkout bersih dapat disiapkan mengikuti README dengan Conda.
- [x] `conda env create -f environment.yml` berhasil dan `pytest` berjalan.
- [x] Frontend build berjalan (atau keputusan stack dijadwalkan).
- [x] Tidak ada rahasia di repository.
- [x] Papan tugas dan jadwal review aktif.
- [x] NIM dan administrasi etika dikonfirmasi atau dicatat sebagai risiko.

Jika gate belum lulus, jangan mulai F1.

---

## Risiko Fase

| Risiko | Mitigasi |
|---|---|
| Waktu habis untuk setup | Batasi setup maksimal 2–3 hari; gunakan scaffold sederhana |
| React belum dikuasai | Siapkan fallback Django; keputusan D2 sebelum F6 |
| NIM masih ambigu | Catat di risk register; konfirmasi sebelum publikasi |
| Tidak ada git repository | Inisialisasi sekarang; tanpa Git, bukti tugas sulit dilacak |

---

## Traceability

- `docs/delivery/roadmap.md` Bagian 2–3.
- `docs/02-system-design.md` Bagian 9–10.
- `docs/delivery/risk-register.md` Bagian 5.
