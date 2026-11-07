# KarirMatch — Dokumentasi Produk dan Teknis

**Status:** Disetujui v1.0  
**Pemilik:** Deris Firmansyah  
**Sumber utama:** `GRAND_DESIGN_PRODUK_INOVATIF_KarirMatch.pdf` (13 halaman)  
**Terakhir diperbarui:** 7 November 2026

Dokumentasi ini menurunkan Grand Design Produk Inovatif KarirMatch menjadi dokumen
yang dapat dipakai untuk perancangan, implementasi, evaluasi, dan penulisan laporan.
Struktur dokumen mengikuti tujuh bagian Grand Design, tetapi isinya dipisahkan menurut
fungsi: produk, sistem, data, riset, keputusan arsitektur, dan pelaksanaan.

> **Cara membaca status:** angka target, ambang, bobot, dan detail kontrak yang tidak
> ada di Grand Design ditandai sebagai **usulan** atau **keputusan terbuka**. Jangan
> memperlakukannya sebagai hasil atau fakta sampai diuji dan disetujui.

---

## 1. Peta Dokumen

| Dokumen | Isi utama | Bagian Grand Design |
|---|---|---|
| [`01-prd.md`](01-prd.md) | Product Requirements Document: masalah, persona, lingkup, kebutuhan fungsional, UX, metrik, asumsi | Bagian 1, Bagian 2, Bagian 6, Bagian 7 |
| [`02-system-design.md`](02-system-design.md) | Arsitektur logis, modul, pipeline retrieval dan rekomendasi, stack, deployment, NFR, pengujian | Bagian 5, Bagian 7 |
| [`03-api-spec.md`](03-api-spec.md) | Katalog endpoint, autentikasi, request/response, error, contoh | Bagian 2, Bagian 5, Bagian 7 |
| [`api/openapi.yaml`](api/openapi.yaml) | Kontrak OpenAPI 3.1 versi draft untuk endpoint utama | Bagian 2, Bagian 5, Bagian 7 |
| [`data/dataset-design.md`](data/dataset-design.md) | Sumber data, korpus, atribut, relevance judgment, kualitas data, etika dan legalitas | Bagian 4 |
| [`data/database-design.md`](data/database-design.md) | Skema database, relasi, indeks, retensi, pemisahan data evaluasi | Bagian 4, Bagian 5, Bagian 7 |
| [`research/research-and-evaluation.md`](research/research-and-evaluation.md) | Fokus riset, literatur, RQ, hipotesis, eksperimen, metrik, statistik, ancaman validitas | Bagian 3, Bagian 6 |
| [`adr/README.md`](adr/README.md) | Indeks Architecture Decision Record | Bagian 5, Bagian 7 |
| [`delivery/roadmap.md`](delivery/roadmap.md) | Rencana 12 minggu, milestone, luaran, definition of done | Bagian 7 |
| [`tasks/README.md`](tasks/README.md) | Papan tugas per fase, acceptance criteria, gate keputusan, estimasi beban kerja; tersedia juga [versi PDF](tasks/KarirMatch-Task-Board-v1.0.pdf) | Bagian 7 |
| [`delivery/risk-register.md`](delivery/risk-register.md) | Risiko, mitigasi, kebijakan klaim, keputusan terbuka | Bagian 3, Bagian 6, Bagian 7 |
| [`references.md`](references.md) | Daftar rujukan dari Grand Design | Rujukan |
| [`glossary.md`](glossary.md) | Istilah produk, retrieval, rekomendasi, dan evaluasi | Semua |

---

## 2. Traceability ke Grand Design

| Bagian Grand Design | Topik | Dokumen turunan |
|---|---|---|
| Bagian 1 Produk Utama dan Alasan Penggunaan | Nama produk, pengguna, masalah, inovasi inti, nilai tambah, persona, JTBD, prinsip desain | `01-prd.md` Bagian 1–5 |
| Bagian 2 Peta Kebutuhan Fitur Produk | F1–F4, prioritas, ketersediaan data, ruang lingkup MVP, fitur lanjutan, luar lingkup, penyajian skor | `01-prd.md` Bagian 6–8; `03-api-spec.md`; `02-system-design.md` Bagian 4–7 |
| Bagian 3 Fokus Penelitian, Literatur, dan Kebaruan | Kendala STKI, RQ1–RQ5, hipotesis, uji statistik, studi terdahulu, kontribusi, keterbatasan | `research/research-and-evaluation.md` Bagian 1–5; `references.md` |
| Bagian 4 Rancangan Dataset dan Atribut | Sumber korpus, kandidat dataset, atribut, label, kualitas data, etika dan legalitas | `data/dataset-design.md`; `data/database-design.md` |
| Bagian 5 Metodologi Penelitian dan Pilihan Metode AI/ML/STKI | Design science research, baseline, TF-IDF + cosine, preprocessing, profil, arsitektur logis, strategi pemodelan | `02-system-design.md` Bagian 3–8; `research/research-and-evaluation.md` Bagian 6; `adr/` |
| Bagian 6 Rancangan Eksperimen dan Evaluasi | E1–E5, uji ketahanan, metrik, uji statistik, relevance judgment, NFR, test case, risiko | `research/research-and-evaluation.md` Bagian 7–10; `02-system-design.md` Bagian 11–12; `delivery/risk-register.md` |
| Bagian 7 Rencana Pelaksanaan dan Luaran | Jadwal 12 minggu, pelaksana, luaran, ukuran dampak, teknologi, database, endpoint, risiko, klaim, keputusan terbuka | `delivery/roadmap.md`; `02-system-design.md`; `03-api-spec.md`; `delivery/risk-register.md` |

---

## 3. Urutan Baca yang Disarankan

**Untuk product/reviewer**
1. `01-prd.md`
2. `research/research-and-evaluation.md` Bagian 1–4
3. `delivery/risk-register.md`

**Untuk engineering**
1. `01-prd.md` Bagian 6–8
2. `02-system-design.md`
3. `03-api-spec.md` dan `api/openapi.yaml`
4. `data/database-design.md`
5. `adr/README.md`

**Untuk peneliti/pembimbing**
1. `research/research-and-evaluation.md`
2. `data/dataset-design.md`
3. `research/research-and-evaluation.md` Bagian 8–11
4. `references.md`

**Untuk operasional/demo**
1. `delivery/roadmap.md`
2. `tasks/README.md` dan file fase yang sedang aktif
3. `02-system-design.md` Bagian 9–12
4. `delivery/risk-register.md`

---

## 4. Konvensi ID

| Prefix | Arti | Contoh |
|---|---|---|
| `FR-` | Functional requirement | `FR-SEARCH-01` |
| `NFR-` | Non-functional requirement | `NFR-PERF-01` |
| `F1`–`F4` | Fitur produk dari Grand Design Bagian 2 | `F1` pencarian |
| `RQ1`–`RQ5` | Research question | `RQ1` |
| `E1`–`E5` | Eksperimen | `E3` personalisasi |
| `TC01`–`TC13` | Test case dari Grand Design Bagian 6 | `TC02` |
| `ADR-0001`–`ADR-0010` | Architecture Decision Record | `ADR-0002` |
| `RISK-` | Risiko | `RISK-DATA-01` |
| `P0-01`–`P9-07` | Tugas pelaksanaan di folder `tasks/` | `P4-09` |

Setiap requirement harus dapat dilacak ke fitur, sumber data, dan (bila relevan) RQ.

---

## 5. Sumber Kebenaran dan Penandaan

Hierarki acuan:

1. **Grand Design PDF** — keputusan produk, riset, dan arsitektur yang sudah ditetapkan.
2. **Dokumen di folder ini** — penjabaran operasional dan detail implementasi.
3. **Kode dan konfigurasi** — realisasi; bila berbeda, perbedaan harus dicatat di ADR
   atau changelog.

Tiga label yang dipakai konsisten:

- **Tetap** — berasal langsung dari Grand Design dan tidak boleh diubah tanpa revisi
  dokumen sumber.
- **Usulan** — detail yang ditambahkan untuk membuat dokumen dapat dieksekusi; belum
  tervalidasi.
- **Keputusan terbuka** — belum dipilih; dicatat agar tidak menjadi asumsi diam-diam.

Konflik yang ditemukan saat ekstraksi PDF dicatat di `delivery/risk-register.md` Bagian 5.

---

## 6. Catatan Ekstraksi PDF

- Teks diekstrak dari 13 halaman PDF. Gambar arsitektur pada halaman 8 diperiksa
  secara visual dan direkonstruksi menjadi diagram Mermaid di `02-system-design.md`.
- Rumus pada PDF dirender tidak sempurna oleh ekstraktor teks. Rumus di dokumentasi ini
  ditulis ulang dalam notasi yang dapat dibaca dan diperiksa; makna dan nilainya
  mengikuti contoh perhitungan PDF (N = 4, query “data analyst python”).
- PDF mencantumkan NIM `A11.2024.15624` pada header dan `A11.2024.15625` pada Bagian 7.
  Dokumen ini tidak memakai NIM; perbedaan tersebut dicatat untuk dikonfirmasi sebelum
  publikasi.
- Semua angka performa, bobot field, ambang kecocokan, α, half-life, dan ukuran korpus
  adalah **usulan awal** sesuai PDF, bukan hasil pengukuran.

---

## 7. Status dan Perubahan

**Status keseluruhan:** Disetujui v1.0 — disetujui 7 November 2026; belum ada implementasi.  
**Task board:** v1.0 — 8 November 2026, folder [`tasks/`](tasks/README.md).

Persetujuan ini menetapkan seluruh dokumen sebagai **baseline v1.0**. Keputusan terbuka
yang tercatat di `delivery/risk-register.md` Bagian 4 tetap perlu diputuskan sebelum
implementasi; keputusan tersebut tidak otomatis selesai karena dokumen disetujui.

| Versi | Tanggal | Perubahan |
|---|---|---|
| 0.1 | 2026-11-07 | Dokumentasi awal diturunkan dari Grand Design PDF: PRD, system design, API spec, dataset, database, riset/evaluasi, 10 ADR, roadmap, risk register, referensi, glosarium. |
| 1.0 | 2026-11-07 | Seluruh dokumen disetujui sebagai baseline; status diubah dari Draft v0.1 menjadi Disetujui v1.0. |

**Aturan perubahan:** perubahan pada keputusan produk/riset harus memperbarui Grand
Design atau ADR terkait, lalu dokumen turunan yang terdampak. Jangan mengubah angka
target di dokumen turunan tanpa mencatat alasan dan tanggal.
