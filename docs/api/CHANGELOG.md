# Changelog Kontrak API

Semua perubahan kontrak pada `docs/api/openapi.yaml` dicatat di sini.

## 0.1.0 — 2026-11-08

- Menambahkan parameter `category`, `location`, `skill`, `employment_type`, dan
  `experience_level` pada `GET /api/jobs/search`.
- Menambahkan `employment_type`, `experience_level`, `source`, `is_active`, dan
  `is_simulated` pada detail lowongan.
- Menambahkan `employment_type`, `experience_level`, dan `is_simulated` pada hasil
  pencarian.
- Menambahkan `source`, `reason`, dan `is_simulated` pada item rekomendasi.
- Menambahkan `is_simulated` pada item bookmark.
- Menambahkan `count` dan `next_offset` pada daftar bookmark, serta `created`
  pada respons pembuatan bookmark (201 baru / 200 sudah ada).
- Menambahkan `is_simulated` pada respons event; hanya admin yang dapat
  menandai event sebagai simulasi.
- Menambahkan `config_hash` dan `dataset_hash` pada ringkasan dan hasil run
  evaluasi admin.
- Menetapkan `DELETE /api/me/bookmarks/{job_id}` sebagai operasi idempoten
  dengan respons 204.
