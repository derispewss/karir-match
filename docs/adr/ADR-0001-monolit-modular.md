# ADR-0001: Modular Monolith

- **Status:** Diterima
- **Tanggal:** 7 November 2026
- **Pemilik:** Deris Firmansyah
- **Sumber:** Grand Design Bagian 5 Arsitektur logis; Bagian 7 Teknologi dan arsitektur implementasi
- **Menggantikan:** —
- **Digantikan oleh:** —

## Konteks

KarirMatch adalah prototipe riset dengan satu pelaksana, jadwal sekitar 12 minggu, dan
koleksi lowongan berukuran ribuan dokumen. Sistem membutuhkan pencarian, rekomendasi,
autentikasi, event tracking, dan evaluasi offline.

Pemisahan modul tetap diperlukan agar logika retrieval dan rekomendasi dapat diuji dan
diganti tanpa mengubah framework. Namun, kompleksitas operasional microservices
(misalnya service discovery, jaringan antar-layanan, deployment terpisah, dan observability
terdistribusi) tidak sepadan dengan skala dan waktu proyek.

## Keputusan

Gunakan **modular monolith**:

- Satu aplikasi FastAPI yang dapat di-deploy sebagai satu unit.
- Lima modul in-process:
  1. Retrieval Engine
  2. Recommendation Engine
  3. Autentikasi
  4. Event Tracking
  5. Modul Evaluasi dan Analitik
- Empat aset bersama:
  1. Modul Preprocessing
  2. Indeks TF-IDF
  3. Database
  4. Query set + relevance judgment
- Modul berkomunikasi lewat pemanggilan fungsi/interface Python, bukan HTTP internal.
- Batas modul dijaga lewat struktur paket dan kontrak fungsi, bukan pemisahan proses.
- Logika riset (preprocessing, retrieval, ranking, evaluasi) berada di paket Python murni
  yang tidak bergantung pada FastAPI.

## Alternatif yang dipertimbangkan

| Alternatif | Alasan tidak dipilih |
|---|---|
| Microservices per modul | Overhead jaringan, deployment, observability, dan konsistensi data terlalu besar untuk satu pelaksana |
| Serverless function per endpoint | Cold start, batas eksekusi, dan pengelolaan indeks in-memory tidak cocok |
| Monolith tanpa batas modul | Cepat di awal, tetapi logika riset dan framework bercampur; sulit diuji dan di-ablation |
| Django monolit | Kandidat fallback jika React tidak dikuasai; tetap modular, tetapi bukan pilihan utama |

## Konsekuensi

### Positif

- Deployment sederhana: satu aplikasi, satu database, satu indeks.
- Transaksi database mudah; tidak ada konsistensi eventual antar-layanan.
- Latensi rendah karena retrieval dan rekomendasi berjalan in-process.
- Logika riset dapat dijalankan dari skrip tanpa server.
- Biaya hosting dan operasional rendah.

### Negatif / biaya

- Semua modul di-deploy bersama; satu bug dapat memengaruhi seluruh aplikasi.
- Skala horizontal terbatas pada satu proses/host.
- Batas modul bisa terkikis jika tidak disiplin.
- Tidak ada isolasi kegagalan antar-modul.

Mitigasi:

- Struktur paket yang jelas dan review batas modul.
- Test unit per modul dan integration test API.
- Konfigurasi eksperimen di berkas, bukan di kode framework.
- Pemicu evolusi ke pemisahan layanan dicatat di ADR-0009.

## Tindak lanjut

- Tetapkan struktur direktori: `app/api`, `app/modules/retrieval`, `app/modules/recommendation`,
  `app/modules/auth`, `app/modules/events`, `app/modules/evaluation`, `research/`.
- Pastikan modul retrieval/rekomendasi tidak mengimpor FastAPI.
- Tambahkan test batas modul bila memungkinkan.
- Tinjau kembali bila koleksi jauh melebihi 20.000 dokumen, butuh multi-node, atau ada
  beberapa tim yang perlu deploy independen.

## Referensi

- Grand Design Bagian 5 (Arsitektur logis: 5 modul, 4 penyimpanan).
- Grand Design Bagian 7 (Teknologi dan arsitektur implementasi).
- `02-system-design.md` Bagian 3.
