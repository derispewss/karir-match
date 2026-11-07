# ADR-0006: PostgreSQL/SQLite dan Indeks In-Memory

- **Status:** Diterima
- **Tanggal:** 7 November 2026
- **Pemilik:** Deris Firmansyah
- **Sumber:** Grand Design Bagian 5 Arsitektur logis; Bagian 7 Teknologi dan database
- **Menggantikan:** —
- **Digantikan oleh:** —

## Konteks

Sistem membutuhkan penyimpanan data produk dan evaluasi, serta indeks pencarian untuk
koleksi ribuan dokumen.

Kendala:

- satu pelaksana dan deployment satu host;
- PostgreSQL untuk deployment, SQLite untuk pengembangan/pengujian;
- tidak ada kebutuhan horizontal scaling pada MVP;
- indeks harus dapat dibangun ulang dan dihitung cepat;
- data evaluasi harus terpisah dari data produk.

## Keputusan

- **Database deployment:** PostgreSQL.
- **Database pengembangan/pengujian:** SQLite, dengan skema yang sama.
- **Indeks pencarian:** TF-IDF sparse in-memory (scikit-learn/SciPy), disimpan sebagai
  artefak dan dimuat saat startup.
- **Bukan:** Elasticsearch/OpenSearch, vector database, atau layanan pencarian eksternal.
- **Bukan:** cache terdistribusi atau replika database pada MVP.
- Evaluasi offline memakai tabel terpisah (`eval_`) atau schema terpisah.
- Indeks menyimpan metadata: hash dataset, konfigurasi preprocessing, versi pustaka,
  tanggal build.

## Alternatif yang dipertimbangkan

| Alternatif | Alasan tidak dipilih |
|---|---|
| PostgreSQL full-text search | Menambah ketergantungan pada fitur DB dan menyulitkan portabilitas SQLite; TF-IDF perlu kontrol bobot/field yang eksplisit |
| Elasticsearch/OpenSearch | Overhead operasional besar untuk ribuan dokumen; di luar ruang lingkup |
| SQLite untuk deployment | Konkurensi tulis terbatas; PostgreSQL lebih aman untuk deployment |
| Vector database | Tidak diperlukan untuk TF-IDF; menambah kompleksitas |
| Indeks di disk setiap request | Lambat dan tidak perlu; muat di memori |

## Konsekuensi

### Positif

- Deployment sederhana: satu database + satu file/volume indeks.
- Skema sama antara pengembangan dan deployment.
- Pencarian cepat karena indeks di memori.
- Indeks dapat dibangun ulang secara deterministik.
- Tidak ada biaya layanan search engine.

### Negatif / biaya

- SQLite tidak cocok untuk konkurensi tulis tinggi.
- Indeks in-memory terbatas pada memori satu proses.
- Perlu waktu startup untuk memuat indeks.
- Tidak ada skalabilitas horizontal.
- Fitur query lanjutan terbatas dibanding search engine.

Mitigasi:

- Gunakan PostgreSQL di deployment.
- Batasi skala MVP pada ribuan dokumen.
- Bangun indeks secara offline dan muat saat startup.
- Sediakan perintah rebuild dan backup.
- Tinjau ulang bila koleksi jauh melebihi 20.000 dokumen atau butuh multi-node.

## Tindak lanjut

- Pilih ORM/migrasi (usulan: SQLAlchemy + Alembic).
- Pastikan `PRAGMA foreign_keys = ON` untuk SQLite.
- Buat skrip build indeks dan manifest.
- Uji restore database dan rebuild indeks.
- Catat waktu build dan ukuran indeks pada E5.

## Referensi

- Grand Design Bagian 5 (Arsitektur logis).
- Grand Design Bagian 7 (Database; teknologi).
- `02-system-design.md` Bagian 7, Bagian 9, Bagian 10.
- `data/database-design.md`.
