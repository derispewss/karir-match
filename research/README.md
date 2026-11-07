# Paket Riset

Direktori ini berisi logika penelitian yang tidak bergantung pada framework web:
preprocessing, retrieval TF-IDF, rekomendasi berbasis profil, dan evaluasi.

Fase 0 hanya menyiapkan struktur paket. Modul pertama akan ditambahkan pada Fase 3–5
sesuai `docs/tasks/03-baseline-dan-query-set.md` sampai `docs/tasks/05-personalisasi.md`.

Aturan:

- Kode di sini harus dapat diimpor tanpa menjalankan server.
- Tidak ada akses database atau HTTP dari modul inti.
- Konfigurasi eksperimen dibaca dari `configs/`, bukan ditulis di dalam kode.
- Setiap perubahan yang memengaruhi hasil evaluasi harus dicatat di manifest.
