# API Specification — KarirMatch

**Status:** Disetujui v1.0  
**Pemilik:** Deris Firmansyah  
**Sumber:** Grand Design Produk Inovatif KarirMatch Bagian 2, Bagian 5, Bagian 7  
**Terakhir diperbarui:** 7 November 2026  
**Kontrak mesin:** [`api/openapi.yaml`](api/openapi.yaml) (OpenAPI 3.1, draft)

---

## 1. Ruang Lingkup

Dokumen ini mendefinisikan kontrak HTTP untuk prototipe KarirMatch. Kontrak mencakup
endpoint yang disebut di Grand Design Bagian 7 dan detail operasional yang diperlukan agar
frontend dan backend dapat dibangun secara paralel.

Yang **tidak** termasuk kontrak ini:

- Integrasi perekrut.
- Pengiriman lamaran.
- Unggah/parsing CV.
- Notifikasi email.
- Sisi admin selain evaluasi.

Detail yang belum diputuskan ditandai **keputusan terbuka** dan tidak boleh dianggap
final.

---

## 2. Konvensi

### 2.1 Base URL dan format

| Item | Nilai |
|---|---|
| Base URL pengembangan | `http://localhost:8000` |
| Prefix API | `/api` |
| Format | JSON UTF-8 (`application/json`) |
| Tanggal | ISO 8601 UTC (`2026-11-07T10:15:30Z`) |
| Tanggal terbit | `YYYY-MM-DD` |
| ID | String (usulan: UUID); jangan diasumsikan numerik |
| Versi | Draft; belum ada versioning publik |

### 2.2 Autentikasi

Grand Design membuka dua opsi: **session cookie** atau **bearer token**. Kontrak ini
netral terhadap pilihan tersebut.

- Jika session cookie: `Set-Cookie: km_session=...; HttpOnly; Secure; SameSite=Lax; Path=/`.
- Jika bearer token: `Authorization: Bearer <token>`.

Endpoint bertanda **Login** memerlukan salah satu mekanisme di atas. Endpoint bertanda
**Admin** memerlukan role `admin`. Pengguna biasa yang mengakses endpoint admin mendapat
`403` (TC12).

### 2.3 Idempotensi

- `POST /api/me/bookmarks` idempoten: menyimpan lowongan yang sama dua kali tidak membuat
  baris ganda dan tidak menghasilkan error (TC11).
- `DELETE /api/me/bookmarks/{job_id}` idempoten: menghapus bookmark yang tidak ada tetap
  `204`.
- `DELETE /api/me/data` idempoten untuk data yang sudah tidak ada.

### 2.4 Pagination dan limit

Grand Design menyebut Top-K, bukan pagination penuh. Untuk MVP:

- Pencarian memakai `limit` (default 10, maksimum 50).
- Bookmark memakai `limit` dan `offset` (usulan).
- Feed memakai `limit` (default 10, maksimum 50).
- Respons menyatakan `count` (jumlah item pada respons ini) dan, bila relevan,
  `next_offset`.

### 2.5 Format error

Semua error memakai bentuk yang sama:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Parameter limit harus antara 1 dan 50.",
    "details": [
      { "field": "limit", "issue": "out_of_range" }
    ],
    "request_id": "req_01JABCDEF"
  }
}
```

`details` dan `request_id` opsional. Jangan menampilkan stack trace, SQL, atau nama tabel
kepada klien.

| Status | Kode umum | Kapan |
|---|---|---|
| 400 | `BAD_REQUEST` | Request tidak dapat diproses |
| 401 | `UNAUTHENTICATED` | Belum login / sesi tidak valid |
| 403 | `FORBIDDEN` | Bukan pemilik data / bukan admin |
| 404 | `NOT_FOUND` | Lowongan atau resource tidak ada |
| 409 | `CONFLICT` | Email sudah terdaftar |
| 422 | `VALIDATION_ERROR` | Input tidak lolos validasi |
| 429 | `RATE_LIMITED` | Terlalu banyak percobaan login |
| 500 | `INTERNAL_ERROR` | Kesalahan tak terduga |
| 503 | `SERVICE_UNAVAILABLE` | Database/indeks belum siap |

### 2.6 Batas percobaan login

Login dibatasi per IP + email (usulan: 5 percobaan per 15 menit). Respons `429` menyertakan
header `Retry-After`. Pesan tidak boleh membocorkan apakah email terdaftar.

---

## 3. Ringkasan Endpoint

| Metode | Path | Fungsi | Akses | FR |
|---|---|---|---|---|
| POST | `/api/auth/register` | Registrasi akun | Publik | FR-AUTH-01 |
| POST | `/api/auth/login` | Login | Publik | FR-AUTH-01 |
| POST | `/api/auth/logout` | Logout | Login | FR-AUTH-01 |
| GET | `/api/jobs/search` | Pencarian Top-K dengan filter dan sort | Publik | FR-SEARCH-01–05 |
| GET | `/api/jobs/{job_id}` | Detail lowongan | Publik | FR-JOB-01 |
| GET | `/api/me/preferences` | Baca preferensi | Login | FR-PREF-01 |
| PUT | `/api/me/preferences` | Ganti preferensi | Login | FR-PREF-01 |
| GET | `/api/me/bookmarks` | Daftar bookmark | Login | FR-BOOK-01 |
| POST | `/api/me/bookmarks` | Simpan bookmark | Login | FR-BOOK-01 |
| DELETE | `/api/me/bookmarks/{job_id}` | Hapus bookmark | Login | FR-BOOK-01 |
| POST | `/api/events` | Catat interaksi | Login | FR-EVENT-01–02 |
| GET | `/api/me/recommendations` | Feed Top-N | Login | FR-REC-01–04 |
| DELETE | `/api/me/data` | Hapus riwayat/event pengguna | Login | FR-PRIV-01 |
| GET | `/api/admin/eval/summary` | Ringkasan evaluasi | Admin | FR-EVAL-01 |
| POST | `/api/admin/eval/run` | Jalankan evaluasi offline | Admin | FR-EVAL-01 |

Catatan: Grand Design menulis grup path `/api/me/bookmarks` untuk GET/POST/DELETE. Untuk
kejelasan REST, detail DELETE dimodelkan sebagai subresource `/{job_id}`. Jika implementasi
harus persis memakai satu path, alternatifnya `DELETE /api/me/bookmarks` dengan body
`{ "job_id": "..." }`; pilih satu dan catat di ADR.

---

## 4. Autentikasi

### 4.1 POST `/api/auth/register`

Membuat akun. Kata sandi di-hash di server.

**Request**

```json
{
  "email": "raka@example.com",
  "password": "kata-sandi-yang-kuat"
}
```

**Response 201**

```json
{
  "id": "usr_01JABCDEF",
  "email": "raka@example.com",
  "role": "user",
  "created_at": "2026-11-07T10:15:30Z"
}
```

**Error**

| Status | Kondisi |
|---|---|
| 409 | Email sudah terdaftar |
| 422 | Format email atau kata sandi tidak valid |

Kebijakan kata sandi (usulan): minimal 8 karakter; tidak menyimpan password mentah;
tidak mengirim password di log.

### 4.2 POST `/api/auth/login`

**Request**

```json
{
  "email": "raka@example.com",
  "password": "kata-sandi-yang-kuat"
}
```

**Response 200**

```json
{
  "id": "usr_01JABCDEF",
  "email": "raka@example.com",
  "role": "user"
}
```

Jika memakai cookie, respons menyertakan `Set-Cookie`. Jika memakai token, respons
menyertakan `access_token` dan `token_type`.

**Error**

| Status | Kondisi |
|---|---|
| 401 | Kredensial salah (pesan generik) |
| 429 | Terlalu banyak percobaan |

### 4.3 POST `/api/auth/logout`

**Response 204** — sesi/token diakhiri.

---

## 5. Lowongan

### 5.1 GET `/api/jobs/search`

Mencari lowongan. Tidak memerlukan login.

**Query parameters**

| Parameter | Tipe | Wajib | Default | Keterangan |
|---|---|---|---|---|
| `q` | string | Ya | — | Query teks; boleh kosong untuk daftar umum? Lihat catatan |
| `location` | string | Tidak | — | Filter lokasi |
| `category` | string | Tidak | — | Filter kategori |
| `employment_type` | string | Tidak | — | Contoh: `full_time`, `part_time`, `internship`, `contract`, `freelance` |
| `experience_level` | string | Tidak | — | Contoh: `entry`, `junior`, `mid`, `senior` |
| `sort` | string | Tidak | `relevance` | `relevance` atau `date` |
| `limit` | integer | Tidak | 10 | 1–50 |

**Catatan:** `q` kosong diperlakukan sebagai daftar lowongan tanpa skor teks; perilaku
ini adalah usulan dan harus konsisten dengan empty state. Jika produk hanya mendukung
pencarian berbasis query, `q` kosong dapat menghasilkan `422`.

**Contoh**

```http
GET /api/jobs/search?q=data%20analyst&location=Jakarta&sort=relevance&limit=10
```

**Response 200**

```json
{
  "query": "data analyst",
  "filters": {
    "location": "Jakarta",
    "category": null,
    "employment_type": null,
    "experience_level": null
  },
  "sort": "relevance",
  "limit": 10,
  "count": 2,
  "items": [
    {
      "job": {
        "job_id": "job_01JABCDEF",
        "title": "Data Analyst",
        "company": "Contoh Data",
        "location": "Jakarta",
        "employment_type": "full_time",
        "experience_level": "junior",
        "category": "Data",
        "publication_date": "2026-10-01",
        "skills": ["SQL", "Python", "Excel"],
        "is_active": true
      },
      "match_level": "high",
      "matched_terms": ["data", "analyst"],
      "reason": "Cocok pada judul dan skills."
    }
  ]
}
```

**Aturan respons**

- `match_level` hanya `high`, `medium`, atau `low`; UI memetakan ke Tinggi/Sedang/Rendah.
- Skor mentah **tidak** dikirim ke pengguna biasa.
- `matched_terms` berisi term query yang benar-benar cocok.
- `reason` harus dapat dilacak ke term/fitur, bukan kalimat generik.
- Tidak ada hasil → `200` dengan `count: 0`, `items: []`, dan `message` yang jelas.

**Error**

| Status | Kondisi |
|---|---|
| 422 | `limit` di luar rentang, `sort` tidak dikenal |
| 503 | Indeks belum siap |

### 5.2 GET `/api/jobs/{job_id}`

**Response 200**

```json
{
  "job_id": "job_01JABCDEF",
  "title": "Data Analyst",
  "company": "Contoh Data",
  "description": "Deskripsi lowongan dalam teks biasa.",
  "qualifications": "Kualifikasi dalam teks biasa.",
  "location": "Jakarta",
  "employment_type": "full_time",
  "experience_level": "junior",
  "category": "Data",
  "skills": ["SQL", "Python", "Excel"],
  "publication_date": "2026-10-01",
  "source_url": "https://example.com/jobs/123",
  "language": "id",
  "is_active": true
}
```

**Error:** `404` bila tidak ditemukan.

**Catatan:** lowongan tidak aktif tetap dapat ditampilkan dengan penanda, atau `404`
sesuai kebijakan produk. Pilih satu dan dokumentasikan.

---

## 6. Preferensi

### 6.1 GET `/api/me/preferences`

**Response 200**

```json
{
  "categories": ["Data", "Teknologi"],
  "locations": ["Jakarta", "Bandung"],
  "employment_types": ["full_time", "internship"],
  "experience_levels": ["entry", "junior"],
  "updated_at": "2026-11-07T10:15:30Z"
}
```

### 6.2 PUT `/api/me/preferences`

Mengganti seluruh preferensi. Array kosong valid.

**Request**

```json
{
  "categories": ["Data"],
  "locations": ["Jakarta"],
  "employment_types": ["full_time"],
  "experience_levels": ["junior"]
}
```

**Response 200** — sama dengan GET.

**Error:** `401`, `422` (tipe data salah), `403` (bukan pemilik data).

---

## 7. Bookmark

### 7.1 GET `/api/me/bookmarks`

**Query parameters**

| Parameter | Tipe | Default | Keterangan |
|---|---|---|---|
| `limit` | integer | 20 | 1–100 |
| `offset` | integer | 0 | ≥ 0 |

**Response 200**

```json
{
  "items": [
    {
      "job": {
        "job_id": "job_01JABCDEF",
        "title": "Data Analyst",
        "company": "Contoh Data",
        "location": "Jakarta",
        "employment_type": "full_time",
        "experience_level": "junior",
        "category": "Data",
        "publication_date": "2026-10-01",
        "skills": ["SQL", "Python"],
        "is_active": true
      },
      "saved_at": "2026-11-07T10:15:30Z"
    }
  ],
  "count": 1,
  "next_offset": null
}
```

### 7.2 POST `/api/me/bookmarks`

**Request**

```json
{
  "job_id": "job_01JABCDEF"
}
```

**Respons**

- `201` jika bookmark baru dibuat.
- `200` jika bookmark sudah ada (idempoten).

```json
{
  "job_id": "job_01JABCDEF",
  "saved_at": "2026-11-07T10:15:30Z",
  "created": true
}
```

`created` bernilai `false` pada penyimpanan kedua.

**Catatan event:** endpoint ini dapat mencatat event `save` secara otomatis. Klien tidak
perlu mengirim event `save` ganda; deduplikasi event diserahkan ke server.

### 7.3 DELETE `/api/me/bookmarks/{job_id}`

**Response 204** — idempoten, termasuk bila bookmark tidak ada.

---

## 8. Event Tracking

### 8.1 POST `/api/events`

Mencatat interaksi pengguna. Hanya untuk pengguna login pada MVP.

**Request**

```json
{
  "event_type": "view",
  "job_id": "job_01JABCDEF",
  "query": "data analyst",
  "position": 3
}
```

| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `event_type` | string | Ya | `view`, `save`, `apply_click`, `rec_click`; tambahan `search`, `zero_result` untuk analitik |
| `job_id` | string | Tidak | Wajib untuk event yang terkait lowongan |
| `query` | string | Tidak | Untuk event pencarian/zero-result |
| `position` | integer | Tidak | Posisi tayang, untuk analisis position bias |
| `metadata` | object | Tidak | Data tambahan yang tidak sensitif (usulan) |

`is_simulated` **tidak** dikirim klien biasa; server menetapkannya untuk data simulasi
internal. Respons menyatakan nilai tersebut agar dapat diaudit.

**Response 201**

```json
{
  "event_id": "evt_01JABCDEF",
  "event_type": "view",
  "is_simulated": false,
  "created_at": "2026-11-07T10:15:30Z"
}
```

**Error:** `401`, `403` (job bukan milik konteks yang sah), `422`.

**Aturan:**

- `apply_click` hanya mencatat klik tombol lamar; tidak mengirim lamaran.
- Jangan mengirim isi lamaran, CV, atau data sensitif.
- Event `save` idempoten per pengguna + lowongan + jenis sinyal.

---

## 9. Rekomendasi

### 9.1 GET `/api/me/recommendations`

Feed Top-N untuk pengguna login.

**Query parameters**

| Parameter | Tipe | Default | Keterangan |
|---|---|---|---|
| `limit` | integer | 10 | 1–50 |

**Response 200 — pengguna dengan profil**

```json
{
  "personalized": true,
  "non_personalized_slots": 2,
  "count": 2,
  "items": [
    {
      "job": {
        "job_id": "job_01JABCDEF",
        "title": "Junior Data Analyst",
        "company": "Contoh Data",
        "location": "Jakarta",
        "employment_type": "full_time",
        "experience_level": "junior",
        "category": "Data",
        "publication_date": "2026-10-01",
        "skills": ["SQL", "Python"],
        "is_active": true
      },
      "reason": "Mirip dengan lowongan yang Anda simpan.",
      "source": "profile"
    }
  ]
}
```

**Response 200 — pengguna baru (`β = 0`)**

```json
{
  "personalized": false,
  "non_personalized_slots": 10,
  "count": 2,
  "items": [
    {
      "job": {
        "job_id": "job_01JABCDEF",
        "title": "Data Analyst",
        "company": "Contoh Data"
      },
      "reason": "Lowongan terbaru; lengkapi preferensi untuk rekomendasi yang lebih personal.",
      "source": "non_personalized"
    }
  ]
}
```

**Aturan:**

- Lowongan yang sudah disimpan tidak muncul di feed (TC10).
- Pengguna tanpa riwayat tidak menerima alasan personalisasi palsu.
- Skor mentah tidak dikirim.
- Slot non-personalisasi (usulan 20%) diberi `source: "non_personalized"`.
- `match_level` opsional pada feed; tampilkan hanya bila ada query/definisi relatif yang
  valid. Untuk feed tanpa query, `reason` menjadi penjelasan utama.
- Detail cara menghitung `QueryScore` pada feed tanpa query adalah keputusan terbuka.

**Error:** `401`, `503` (indeks/database belum siap).

---

## 10. Penghapusan Data Pengguna

### 10.1 DELETE `/api/me/data`

Menghapus data pengguna yang terkait fitur:

- preferensi;
- bookmark;
- riwayat pencarian;
- event interaksi;
- log rekomendasi.

Akun tetap ada; penghapusan akun tidak termasuk kontrak MVP.

**Response 204**

**Catatan:** data evaluasi (query set dan judgment) tidak dihapus karena bukan data
pengguna. Operasi ini tidak menghapus data agregat anonim yang sudah tidak dapat
diidentifikasi.

---

## 11. Admin — Evaluasi

### 11.1 GET `/api/admin/eval/summary`

**Query parameters (opsional)**

| Parameter | Keterangan |
|---|---|
| `experiment_id` | `E1`–`E5` |
| `language` | `id`, `en`, `mixed` |
| `split` | `validation`, `test` |

**Response 200**

```json
{
  "generated_at": "2026-11-07T10:15:30Z",
  "experiments": [
    {
      "experiment_id": "E2",
      "config_hash": "sha256:abc123",
      "dataset_hash": "sha256:def456",
      "language": "en",
      "split": "test",
      "query_count": 40,
      "metrics": {
        "p_at_10": 0.84,
        "r_at_10": 0.61,
        "f1_at_10": 0.71,
        "map": 0.72,
        "ndcg_at_10": 0.81
      },
      "latency_ms": {
        "median": 120,
        "p95": 480
      },
      "index_size_mb": 42.5
    }
  ]
}
```

**Aturan:**

- Hanya admin (TC12).
- Metrik diberi konteks koleksi, query set, dan judgment yang sama.
- Jangan menampilkan angka tanpa `config_hash` dan `dataset_hash`.

### 11.2 POST `/api/admin/eval/run`

Menjalankan evaluasi offline. Untuk MVP, eksekusi **sinkron** dengan query set kecil;
jika melebihi batas waktu, jalankan lewat skrip CLI dan catat hasilnya. Tidak ada task
queue pada arsitektur ini.

**Request**

```json
{
  "experiment_id": "E2",
  "config_path": "configs/e2_tfidf_stem_en.yaml",
  "split": "test"
}
```

**Response 200**

```json
{
  "run_id": "eval_01JABCDEF",
  "status": "completed",
  "experiment_id": "E2",
  "config_hash": "sha256:abc123",
  "dataset_hash": "sha256:def456",
  "metrics": {
    "p_at_10": 0.84,
    "map": 0.72,
    "ndcg_at_10": 0.81
  }
}
```

**Error:** `401`, `403`, `404` (config/experiment tidak ada), `422`, `500`.

**Catatan keamanan:** `config_path` tidak boleh membebaskan akses filesystem di luar
direktori konfigurasi yang diizinkan. Validasi path dan gunakan daftar konfigurasi
yang terdaftar (usulan).

---

## 12. Skema Data Ringkas

### 12.1 `JobSummary`

Field `company`, `location`, `employment_type`, `experience_level`, `category`, dan
`publication_date` dapat kosong/tidak ada karena kualitas data sumber; klien harus
menanganinya.

| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `job_id` | string | Ya | ID lowongan |
| `title` | string | Ya | Judul |
| `company` | string | Tidak | Perusahaan |
| `location` | string | Tidak | Lokasi |
| `employment_type` | string | Tidak | Tipe pekerjaan |
| `experience_level` | string | Tidak | Level pengalaman |
| `category` | string | Tidak | Kategori |
| `publication_date` | date | Tidak | Tanggal terbit |
| `skills` | string[] | Ya | Skills; boleh array kosong |
| `is_active` | boolean | Ya | Status aktif |

### 12.2 `JobDetail`

Semua field `JobSummary` ditambah:

| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `description` | string | Ya | Teks biasa |
| `qualifications` | string | Tidak | Teks biasa |
| `source_url` | string (uri) | Tidak | Sumber lowongan |
| `language` | string | Tidak | `id`, `en`, atau `mixed` |

### 12.3 `MatchLevel`

Nilai: `high`, `medium`, `low`. UI menampilkan **Tinggi**, **Sedang**, **Rendah**.
Bukan probabilitas dan bukan skor absolut.

---

## 13. Keamanan dan Batasan

- Semua endpoint yang mengubah data pengguna memerlukan autentikasi.
- Otorisasi kepemilikan data diperiksa di server, bukan hanya di UI.
- Endpoint admin memerlukan role admin.
- Validasi input di server; jangan percaya `user_id` dari body.
- Jangan mengembalikan `password_hash`, token, atau detail internal.
- Log tidak memuat kata sandi, token, isi lamaran, atau data sensitif.
- Rate limit login; pertimbangkan rate limit umum (usulan).
- HTTPS di deployment; cookie `Secure`.
- CORS dibatasi ke origin frontend (usulan).

---

## 14. Keputusan Terbuka

1. Session cookie atau bearer token.
2. Format `DELETE` bookmark: subresource `/{job_id}` atau body pada path grup.
3. Perilaku `q` kosong: daftar umum atau `422`.
4. Apakah event `search`/`zero_result` masuk `/api/events` atau hanya `search_history`.
5. Pagination di luar Top-K untuk pencarian.
6. Format alasan rekomendasi yang lebih kaya (misalnya `source_job_id`).
7. Eksekusi evaluasi: sinkron di API atau hanya CLI.
8. Kebijakan lowongan tidak aktif: tampil dengan penanda atau `404`.

---

## 15. Traceability

| Endpoint | FR | Test case |
|---|---|---|
| `/api/jobs/search` | FR-SEARCH-01–05, FR-EXP-01–02 | TC02, TC04, TC05, TC06 |
| `/api/jobs/{job_id}` | FR-JOB-01 | — |
| `/api/auth/*` | FR-AUTH-01 | — |
| `/api/me/preferences` | FR-PREF-01 | — |
| `/api/me/bookmarks` | FR-BOOK-01 | TC10, TC11 |
| `/api/events` | FR-EVENT-01–02 | TC13 |
| `/api/me/recommendations` | FR-REC-01–04 | TC07, TC08, TC09, TC10 |
| `/api/me/data` | FR-PRIV-01–02 | — |
| `/api/admin/eval/*` | FR-EVAL-01 | TC12 |

---

**Rujukan:** Grand Design Bagian 2, Bagian 5, Bagian 7; `01-prd.md` Bagian 7; `02-system-design.md` Bagian 8;
`api/openapi.yaml`.
