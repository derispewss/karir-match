# Task Board — KarirMatch

**Status:** Aktif — baseline dokumen v1.0  
**Pemilik:** Deris Firmansyah  
**Sumber:** `docs/delivery/roadmap.md`, `docs/01-prd.md`, `docs/research/research-and-evaluation.md`, `docs/delivery/risk-register.md`  
**Periode:** Minggu 1–12 (tanggal relatif)  
**Terakhir diperbarui:** 8 November 2026  
**Versi PDF:** [`KarirMatch-Task-Board-v1.0.pdf`](KarirMatch-Task-Board-v1.0.pdf)

Folder ini memecah rencana 12 minggu menjadi tugas yang dapat dicentang, dari
persiapan proyek sampai penutupan dan arsip. Setiap fase memiliki deliverable,
acceptance criteria, dan **gate** yang harus lulus sebelum fase berikutnya dimulai.

> **Aturan utama:** tugas hanya dicentang bila acceptance criteria terpenuhi dan
> buktinya tercatat. Keberadaan kode atau dokumen saja bukan bukti tugas selesai.

---

## 1. Cara Pakai

### 1.1 Status tugas

| Tanda | Arti |
|---|---|
| `- [ ]` | Belum dikerjakan |
| `- [x]` | Selesai dan acceptance terpenuhi |
| `**Status:** Berjalan` | Sedang dikerjakan; tulis di bawah judul tugas |
| `**Blocked:** ...` | Terhambat; tulis alasan dan pihak yang dibutuhkan |
| `**Dibatalkan:** ...` | Tidak dikerjakan; tulis alasan dan dampaknya |

Jangan memakai tanda setengah jadi. Jika tugas sebagian selesai, biarkan `[ ]` dan
tulis **Status: Berjalan** beserta sisa pekerjaannya.

### 1.2 Bukti (evidence)

Setiap tugas selesai harus menunjuk minimal satu bukti:

- path file atau commit hash;
- hasil test/benchmark;
- tautan artefak (run file, manifest, tabel);
- catatan review pembimbing;
- tangkapan layar atau rekaman demo.

Contoh:

```markdown
- [x] P4-09 Uji TC01–TC04
  - Bukti: `tests/test_retrieval.py`; hasil pytest 12 passed; log di `artifacts/eval/tc01-04.log`
```

### 1.3 Ritme mingguan

| Waktu | Aktivitas |
|---|---|
| Senin | Pilih tugas minggu ini dari fase aktif; perbarui status |
| Rabu | Cek hambatan; eskalasi risiko baru ke `docs/delivery/risk-register.md` |
| Jumat | Review acceptance, centang tugas selesai, catat bukti, tinjau gate |
| Akhir fase | Jalankan gate; jangan lanjut bila gate belum lulus |

### 1.4 Urutan pengerjaan

Kerjakan fase secara berurutan, kecuali pekerjaan yang memang boleh paralel
(UI/API dengan retrieval). Jika satu gate gagal, perbaiki dulu atau catat
keputusan untuk melanjutkan dengan risiko yang diterima.

### 1.5 Environment Conda

Environment Python menggunakan **Conda**, bukan `venv`, agar dependensi riset
dan aplikasi terisolasi serta dapat direproduksi:

```bash
conda env create -f environment.yml
conda activate karirmatch
```

- Nama environment: `karirmatch`.
- Definisi dependensi: `environment.yml` (utamakan `conda-forge`).
- Lock file: `environment.lock` dari `conda list --explicit`.
- Jangan memasang dependensi proyek ke environment global.
- Detail tugas ada di [`00-persiapan.md`](00-persiapan.md) P0-02.

---

## 2. Peta Fase

| Fase | Minggu | Fokus | Deliverable utama | Gate | File |
|---|---:|---|---|---|---|
| **F0** | 1 | Persiapan proyek dan lingkungan | Repo, environment, papan tugas, daftar keputusan | F0 | [`00-persiapan.md`](00-persiapan.md) |
| **F1** | 1–2 | Literatur dan requirement | Matriks literatur, RQ final, PRD ditinjau | F1 | [`01-literatur-dan-requirement.md`](01-literatur-dan-requirement.md) |
| **F2** | 2–4 | Dataset | Korpus v1, manifest, EDA, lisensi tercatat | F2 | [`02-dataset.md`](02-dataset.md) |
| **F3** | 4–5 | Baseline dan query set | Baseline keyword, skrip metrik, query set, pedoman anotasi | F3 | [`03-baseline-dan-query-set.md`](03-baseline-dan-query-set.md) |
| **F4** | 5–6 | TF-IDF dan Cosine | Indeks field, scoring, TC01–TC04, konfigurasi E2 | F4 | [`04-tfidf-dan-cosine.md`](04-tfidf-dan-cosine.md) |
| **F5** | 6–7 | Personalisasi | Profil vektor, FinalScore, TC07–TC10, profil simulasi | F5 | [`05-personalisasi.md`](05-personalisasi.md) |
| **F6** | 6–9 | Backend dan frontend MVP | API, UI, integration test, Docker Compose | F6 | [`06-backend-dan-frontend-mvp.md`](06-backend-dan-frontend-mvp.md) |
| **F7** | 9–11 | Eksperimen dan evaluasi | E1–E5, statistik, analisis kesalahan, manifest | F7 | [`07-eksperimen-dan-evaluasi.md`](07-eksperimen-dan-evaluasi.md) |
| **F8** | 11–12 | Laporan dan demo | Laporan, slide, demo, lampiran | F8 | [`08-laporan-dan-demo.md`](08-laporan-dan-demo.md) |
| **F9** | 12 | Penutupan dan arsip | Rilis, arsip, repo bersih, retrospektif | F9 | [`09-penutupan-dan-arsip.md`](09-penutupan-dan-arsip.md) |

**Mapping ke roadmap:** Fase 0 adalah persiapan tambahan; Fase 1–8 sama dengan
Tahap 1–8 di `docs/delivery/roadmap.md`; Fase 9 adalah penutupan setelah demo.

---

## 3. Critical Path

```text
Lisensi dataset (F2)
→ Korpus bersih (F2)
→ Baseline (F3)
→ TF-IDF + Cosine (F4)
→ Personalisasi (F5)
→ Eksperimen (F7)
→ Laporan dan demo (F8)
```

Critical path tambahan yang sering terlupakan:

1. **Query set dan pedoman anotasi** harus siap sebelum evaluasi, bukan di akhir.
2. **Annotator kedua** harus dikonfirmasi sebelum F7; tanpa itu Cohen's κ terbatas.
3. **Keputusan stack** harus diambil sebelum F6; jika tidak, UI tertunda.
4. **Konfigurasi eksperimen** harus dikunci sebelum test set dilaporkan.
5. **Lisensi dataset** adalah gate keras; jangan mengunduh sebelum tercatat.

---

## 4. Gate Keputusan

Keputusan berikut memblokir tugas lain bila tertunda. Tenggat bersifat usulan dan
harus dikonfirmasi saat review mingguan.

| ID | Keputusan | Tenggat | Fase | Dampak bila terlambat | Rujukan |
|---|---|---|---|---|---|
| **D1** | Dataset Inggris final dan lisensinya | Akhir Minggu 2 | F2 | Korpus tidak dapat dipakai; F3–F7 mundur | `risk-register.md` RISK-DATA-02 |
| **D2** | Stack final: React + Vite atau Django | Akhir Minggu 5 | F6 | UI tidak dapat dimulai | ADR-0005 |
| **D3** | Autentikasi: session cookie atau bearer token | Awal Minggu 6 | F6 | Kontrak auth dan test tertunda | ADR-0010 |
| **D4** | Cara membentuk `QueryScore` pada feed tanpa query | Akhir Minggu 6 | F5 | Feed tidak dapat diimplementasikan konsisten | `02-system-design.md` Bagian 5.2 |
| **D5** | Split validation/test: 30/70 atau 40/60 | Awal Minggu 9 | F7 | Evaluasi tidak dapat dimulai | `dataset-design.md` Bagian 7 |
| **D6** | Jumlah query final dan kedalaman pool | Akhir Minggu 4 | F3/F7 | Beban anotasi tidak terkendali | `research-and-evaluation.md` Bagian 8 |
| **D7** | Kalibrasi batas Tinggi/Sedang/Rendah | Akhir Minggu 9 | F6/F7 | UI memakai ambang sementara | ADR-0007 |
| **D8** | Apakah E5 20k dokumen dijalankan | Awal Minggu 10 | F7 | Scope E5 tidak jelas | `roadmap.md` |
| **D9** | Kebijakan retensi event dan riwayat | Akhir Minggu 8 | F6 | Data menumpuk tanpa kebijakan | `database-design.md` Bagian 6 |
| **D10** | Alat dan format anotasi | Akhir Minggu 4 | F3 | Anotasi tidak konsisten | `research-and-evaluation.md` Bagian 8 |

---

## 5. Beban Kerja (Usulan)

Estimasi adalah **hari kerja ideal** untuk satu pelaksana, bukan komitmen.

| Fase | Estimasi (hari) | Catatan |
|---|---:|---|
| F0 | 2,25 | Setup dan administrasi |
| F1 | 4,25 | Termasuk validasi persona opsional |
| F2 | 8,0 | Termasuk korpus Indonesia sintetis |
| F3 | 5,25 | Baseline, metrik, query set, pilot anotasi |
| F4 | 6,5 | Preprocessing dan indeks |
| F5 | 5,5 | Profil dan ablation setup |
| F6 | 13,5 | API + UI + integration |
| F7 | 9,0 | Anotasi, E1–E5, statistik |
| F8 | 6,5 | Laporan dan demo |
| F9 | 2,25 | Arsip dan penutupan |
| **Total** | **63,0** | **> 60 hari kerja** |

**Konsekuensi:** tidak ada buffer. Jika progres melambat, lakukan scope cut secara
berurutan:

1. E5 20k dokumen → 1k/5k, catat sebagai keterbatasan.
2. Query set 60 → 40, catat penurunan kekuatan statistik.
3. Korpus Indonesia 500 → 200 dokumen.
4. Usability test 8 → 5 peserta atau digabung dengan demo.
5. Fitur lanjutan (MMR, saran istilah, ekspor evaluasi) tetap di luar MVP.

Jangan mengurangi jumlah annotator di bawah 2 tanpa mencatat keterbatasan.

---

## 6. Definition of Done Global

Sebuah fase selesai bila:

- [ ] Semua tugas wajib fase itu selesai atau dibatalkan dengan alasan.
- [ ] Acceptance criteria tugas terpenuhi dan bukti tercatat.
- [ ] Deliverable fase tersedia di path yang disepakati.
- [ ] Test yang relevan lulus; kegagalan yang diketahui dijelaskan.
- [ ] Dokumentasi terdampak diperbarui (PRD, system design, API spec, ADR, dataset).
- [ ] Tidak ada rahasia, token, kata sandi, atau data pribadi di repo/log.
- [ ] Risiko baru dicatat di `docs/delivery/risk-register.md`.
- [ ] Gate fase lulus dan dicatat tanggalnya.

**Definition of Done per area** (kode, dataset, evaluasi, UI, laporan) ada di
`docs/delivery/roadmap.md` Bagian 7.

---

## 7. Aturan Perubahan

- Menambah tugas: buat ID baru di fase yang sesuai, jangan menomori ulang tugas lama.
- Menghapus tugas: tandai **Dibatalkan** dan tulis alasan; jangan hapus baris.
- Mengubah acceptance: catat tanggal dan alasan di file fase.
- Mengubah urutan fase: buat catatan di README ini dan perbarui critical path.
- Keputusan yang sudah diambil: perbarui ADR terkait, lalu dokumen turunan.
- Jangan mengubah estimasi tanpa mencatat alasan; estimasi bukan target kinerja.

---

## 8. Traceability

| Fase | Dokumen acuan |
|---|---|
| F0 | `docs/README.md`, `docs/delivery/roadmap.md` |
| F1 | `docs/01-prd.md`, `docs/research/research-and-evaluation.md`, `docs/references.md` |
| F2 | `docs/data/dataset-design.md` |
| F3 | `docs/research/research-and-evaluation.md` Bagian 7–8; `docs/delivery/roadmap.md` |
| F4 | `docs/02-system-design.md` Bagian 4; ADR-0002, ADR-0003 |
| F5 | `docs/02-system-design.md` Bagian 5; ADR-0004 |
| F6 | `docs/03-api-spec.md`, `docs/api/openapi.yaml`, `docs/data/database-design.md` |
| F7 | `docs/research/research-and-evaluation.md` Bagian 6–12 |
| F8 | `docs/delivery/roadmap.md` Bagian 7–10; `docs/delivery/risk-register.md` |
| F9 | `docs/delivery/roadmap.md`; `docs/delivery/risk-register.md` |
