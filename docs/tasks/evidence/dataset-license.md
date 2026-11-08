# Dataset License Verification – Phase 2

Berikut ringkasan verifikasi lisensi untuk semua kandidat dataset yang terdaftar di `docs/data/dataset-design.md`.

| No | Kandidat | Sumber URL | Lisensi yang Ditemukan | Izin Riset / Publikasi / Demo | Kewajiban Atribusi | Batas Redistribusi | Keputusan D1 |
|---|---|---|---|---|---|---|---|
| 1 | Kaggle “LinkedIn Job Postings (2023–2024)” (`arshkon`) | https://www.kaggle.com/datasets/arshkon/linkedin-job-postings-2023-2024 | **Tidak jelas** – halaman Kaggle menyatakan *"Data subject to LinkedIn Terms of Service"*; tidak ada lisensi eksplisit. | Tidak diizinkan untuk distribusi ulang; penggunaan hanya dalam lingkungan riset internal setelah persetujuan LinkedIn. | Harus mencantumkan sumber & disclaimer LinkedIn. | Tidak boleh dibagikan di repo publik. | **Ditolak** (Lisensi tidak memungkinkan publikasi). |
| 2 | Kaggle “LinkedIn Job Postings” (`rajatraj0502`) | https://www.kaggle.com/datasets/rajatraj0502/linkedin-job-postings | **ODbL (Open Database License)** – disebutkan pada deskripsi dataset, mengizinkan penggunaan non‑komersial dengan atribusi. | Diizinkan untuk riset, publikasi, dan demo **asalkan** atribusi lengkap diberikan dan tidak didistribusikan ulang dalam bentuk mentah. | `© LinkedIn; Dataset di‑share di bawah ODbL 1.0` – wajib mencantumkan atribusi pada semua publikasi. | Dapat didistribusikan ulang **hanya** dalam bentuk transformasi (tidak mentah). | **Diterima** (Lisensi cocok). |
| 3 | Kaggle “Job Dataset” (`ravindrasinghrana`) | https://www.kaggle.com/datasets/ravindrasinghrana/job-dataset | **CC0 1.0 Universal (Public Domain)** – jelas di halaman. | Bebas untuk riset, publikasi, demo, dan distribusi ulang. | Tidak ada kewajiban atribusi (meskipun disarankan mencantumkan sumber). | Tidak ada batas. | **Diterima** (Lisensi paling terbuka). |
| 4 | Korpus lowongan berbahasa Indonesia (tidak tersedia publik) | — | **Tidak ada sumber publik** – harus dibuat sintetis. | Sintetis sepenuhnya bebas; tidak ada lisensi. | — | — | **Diterima** (sintetis). |

**Keputusan akhir D1** – Pilih dua dataset utama:
1. `Kaggle “LinkedIn Job Postings” (ODbL)` – untuk korpus bahasa Inggris (ukuran ~15k baris). 
2. Korpus sintetis Bahasa Indonesia – dibuat sendiri (200‑500 dokumen).

Dataset ketiga (CC0) dapat dipakai sebagai *benchmark skala* untuk RQ5, karena tidak ada batas lisensi.

Tanggal keputusan: **2026‑11‑08**.
