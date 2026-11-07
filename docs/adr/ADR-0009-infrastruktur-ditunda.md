# ADR-0009: Infrastruktur Terdistribusi Ditunda

- **Status:** Diterima
- **Tanggal:** 7 November 2026
- **Pemilik:** Deris Firmansyah
- **Sumber:** Grand Design Bagian 7 “Sengaja tidak dipakai”
- **Menggantikan:** —
- **Digantikan oleh:** —

## Konteks

MVP memiliki:

- koleksi ribuan dokumen yang muat di memori;
- satu pelaksana;
- satu host deployment;
- beban pengguna terbatas pada demo dan evaluasi;
- jadwal 12 minggu.

Menambahkan microservices, message broker, antrean tugas, cache terdistribusi, atau mesin
pencari eksternal akan menambah biaya operasional dan permukaan kegagalan tanpa manfaat
yang terbukti.

## Keputusan

Untuk MVP, **sengaja tidak memakai**:

- microservices;
- message broker;
- antrean tugas (task queue) terdistribusi;
- cache terdistribusi;
- mesin pencari eksternal (Elasticsearch/OpenSearch);
- vector database;
- Kubernetes atau orkestrasi cluster.

Yang dipakai:

- satu aplikasi FastAPI modular;
- satu database PostgreSQL (SQLite untuk dev/test);
- indeks TF-IDF in-memory;
- Docker Compose pada satu host;
- evaluasi offline sinkron atau lewat skrip CLI.

Keputusan ini dapat ditinjau ulang bila pemicu evolusi tercapai.

## Alternatif yang dipertimbangkan

| Alternatif | Alasan ditunda |
|---|---|
| Microservices | Overhead jaringan, deployment, dan observability |
| Kafka/RabbitMQ | Tidak ada alur asynchronous yang kritis |
| Celery/Redis | Evaluasi offline dapat dijalankan sinkron/CLI |
| Elasticsearch | Ribuan dokumen muat di memori; menambah layanan baru |
| Kubernetes | Satu host; orkestrasi berlebihan |
| CDN/cache | Trafik demo belum membutuhkan |

## Konsekuensi

### Positif

- Operasional sederhana dan murah.
- Waktu pengembangan lebih banyak untuk retrieval, evaluasi, dan kualitas.
- Lebih sedikit komponen yang bisa gagal.
- Debugging dan reproduksibilitas lebih mudah.

### Negatif / biaya

- Skalabilitas horizontal terbatas.
- Tidak ada isolasi kegagalan antar-modul.
- Evaluasi berat dapat memblokir request jika dijalankan sinkron.
- Tidak ada background job untuk tugas panjang.
- Ketersediaan bergantung pada satu host.

Mitigasi:

- Jalankan evaluasi berat lewat CLI, bukan endpoint.
- Batasi ukuran koleksi dan beban demo.
- Siapkan backup dan rebuild indeks.
- Catat pemicu evolusi dan buat ADR baru sebelum menambah komponen.

## Pemicu evolusi

Tinjau keputusan ini bila salah satu terjadi:

- Koleksi jauh melebihi 20.000 dokumen atau tidak muat di memori.
- Kebutuhan multi-node, ketersediaan tinggi, atau banyak tenant.
- Kebutuhan task async yang benar-benar kritis (misalnya evaluasi besar, impor data
  berkala, notifikasi).
- Kebutuhan pencarian semantik yang terbukti dari evaluasi.
- Kebutuhan integrasi eksternal atau sisi perekrut.
- Tim bertambah dan perlu deploy independen.

## Tindak lanjut

- Pantau ukuran indeks, latensi, dan memori.
- Catat kapan pemicu tercapai.
- Jika pemicu tercapai, buat ADR baru yang menggantikan ADR ini.
- Jangan menambah infrastruktur hanya karena “best practice” tanpa kebutuhan terukur.

## Referensi

- Grand Design Bagian 7 (Teknologi dan arsitektur implementasi; “Sengaja tidak dipakai”).
- `02-system-design.md` Bagian 2, Bagian 15.
