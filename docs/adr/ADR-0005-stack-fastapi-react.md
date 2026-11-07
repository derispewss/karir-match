# ADR-0005: Stack FastAPI + React dengan Fallback Django

- **Status:** Diterima dengan syarat
- **Tanggal:** 7 November 2026
- **Pemilik:** Deris Firmansyah
- **Sumber:** Grand Design Bagian 7 Teknologi dan arsitektur implementasi
- **Menggantikan:** —
- **Digantikan oleh:** —

## Konteks

Prototipe membutuhkan:

- API yang cepat dibangun, tervalidasi, dan terdokumentasi;
- antarmuka web untuk pencarian, detail, preferensi, bookmark, feed, dan dashboard;
- logika riset yang dapat dijalankan dari skrip tanpa server;
- pengembangan oleh satu orang dalam sekitar 12 minggu;
- risiko keterbatasan pengalaman React sebelum tahap 6.

Grand Design menetapkan FastAPI + React (Vite) dengan fallback Django monolit jika React
belum dikuasai.

## Keputusan

- **Backend:** FastAPI.
  - Validasi input dengan skema bawaan/Pydantic.
  - Dokumentasi OpenAPI otomatis.
  - Modul retrieval, rekomendasi, preprocessing, dan evaluasi berada di paket Python murni
    yang tidak bergantung pada FastAPI.
- **Frontend:** React + Vite, CSS sederhana, tanpa library state besar.
- **Fallback:** jika React belum dikuasai sebelum tahap 6, pindah ke Django monolit.
  Modul retrieval dan rekomendasi tidak berubah; hanya lapisan web yang diganti.
- **Bukan:** microservices, GraphQL, atau framework frontend berat.
- **Keputusan final:** ditinjau pada akhir tahap 5 / awal tahap 6.

## Alternatif yang dipertimbangkan

| Alternatif | Alasan tidak dipilih sebagai default |
|---|---|
| Django monolit | Fallback yang sah; lebih mudah jika React menjadi risiko, tetapi dokumentasi API otomatis dan pemisahan frontend/backend kurang langsung |
| Flask | Ringan, tetapi validasi dan dokumentasi OpenAPI perlu dirakit sendiri |
| Next.js | Menambah kompleksitas dan dependensi; tidak diperlukan untuk MVP |
| Server-rendered templates | Mengurangi kebutuhan React, tetapi interaksi pencarian/feed lebih terbatas |
| Microservices + SPA | Overhead operasional berlebihan |

## Konsekuensi

### Positif

- FastAPI memberi validasi, OpenAPI, dan kecepatan pengembangan.
- Pemisahan frontend/backend memudahkan kontrak API dan pengujian.
- Logika riset dapat diuji tanpa server.
- Fallback Django menjaga jadwal jika React menjadi hambatan.

### Negatif / biaya

- Dua stack (Python + JavaScript) menambah konteks dan build tooling.
- Perlu CORS, autentikasi lintas origin, dan deployment frontend.
- Jika fallback Django dipakai, sebagian pekerjaan frontend/API dapat berubah.
- React tanpa library state besar dapat menyulitkan state kompleks, tetapi MVP relatif
  sederhana.

## Tindak lanjut

- Evaluasi kemampuan React sebelum tahap 6.
- Jika fallback dipakai, buat ADR baru yang menggantikan ADR ini dan catat dampaknya.
- Pertahankan kontrak API dan paket riset agar perubahan framework tidak menyentuh
  algoritma.
- Catat versi Node, Python, dan dependensi.

## Referensi

- Grand Design Bagian 7 (Teknologi dan arsitektur implementasi).
- `02-system-design.md` Bagian 9.
- `03-api-spec.md`.
