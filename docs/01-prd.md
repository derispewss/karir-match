# Product Requirements Document (PRD) — KarirMatch

**Status:** Disetujui v1.0  
**Pemilik:** Deris Firmansyah  
**Sumber:** Grand Design Produk Inovatif KarirMatch Bagian 1, Bagian 2, Bagian 6, Bagian 7  
**Terakhir diperbarui:** 7 November 2026  
**Tahap:** Perancangan prototipe dan eksperimen offline; belum ada validasi pengguna

---

## 1. Ringkasan Produk

**KarirMatch** adalah prototipe web untuk mencari dan merekomendasikan lowongan kerja.
Fitur utamanya adalah pencarian dan peringkat hasil dengan **TF-IDF + Cosine Similarity**,
serta feed rekomendasi berbasis profil preferensi yang dibentuk dari lowongan yang pernah
dibuka, disimpan, atau dilamar.

Pengguna sasaran (hipotesis awal, belum divalidasi): mahasiswa tingkat akhir, fresh
graduate, dan pencari kerja yang berpindah karier.

Masalah yang hendak diselesaikan: pencari kerja menghadapi banyak dokumen lowongan, dan
pencocokan kata kunci sederhana dapat melewatkan dokumen relevan yang memakai istilah
berbeda atau menghasilkan peringkat yang kurang sesuai. Besar dampaknya masih harus
dibuktikan lewat literatur dan eksperimen.

**Inovasi inti, dalam batas yang dapat diklaim:**

- Pencarian (retrieval dan ranking) dengan TF-IDF dan Cosine Similarity.
- Rekomendasi berbasis profil vektor dari interaksi pengguna.
- Penjelasan hasil: istilah yang cocok pada pencarian dan alasan “mirip dengan lowongan
  yang Anda simpan” pada feed.
- Personalisasi berupa pembobotan preferensi berbasis aturan di ruang vektor, **bukan
  machine learning adaptif**, bukan embedding transformer, dan bukan LLM.

---

## 2. Latar Belakang dan Problem Statement

Pencari kerja harus membandingkan banyak lowongan dengan istilah yang tidak seragam.
Pencocokan kata kunci sederhana memiliki dua masalah yang ingin diuji:

1. **Vocabulary mismatch** — query dan dokumen memakai istilah berbeda untuk konsep yang
   sama (misalnya “programmer” vs “software developer”).
2. **Peringkat kurang sesuai** — semua term dianggap sama penting, sehingga kata umum
   dapat mengalahkan kata spesifik; urutan kata dan sinonim tidak dikenali.

TF-IDF memberi bobot lebih besar pada term yang jarang dan diskriminatif, sedangkan
Cosine Similarity mengukur kemiripan arah vektor query dan dokumen. Keduanya mudah
dijelaskan dan tidak membutuhkan data latih. Namun TF-IDF **tidak** menangkap sinonim,
semantik, maupun urutan kata; keterbatasan ini harus dinyatakan, bukan disembunyikan.

**Pernyataan yang masih berupa hipotesis:**

- “Pencocokan kata kunci sederhana kurang relevan.”
- “Personalisasi meningkatkan kualitas rekomendasi.”
- “Pengguna membutuhkan penjelasan mengapa lowongan muncul.”

Ketiganya diuji, bukan diasumsikan sebagai fakta.

---

## 3. Tujuan, Non-Goals, dan Ukuran Keberhasilan

### 3.1 Tujuan produk

| ID | Tujuan | Cara mengetahui |
|---|---|---|
| G-01 | Pengguna dapat menemukan lowongan relevan lebih cepat lewat query dan filter | Metrik retrieval offline; usability test dasar |
| G-02 | Pengguna memahami mengapa sebuah lowongan muncul | Kelengkapan alasan pada UI; usability test |
| G-03 | Pengguna dapat menyimpan dan menemukan kembali lowongan | Alur bookmark; test idempotensi |
| G-04 | Pengguna mendapat rekomendasi yang dapat dijelaskan dari riwayat interaksi | Evaluasi E3/E4; alasan pada feed |
| G-05 | Pengguna dapat mengontrol data preferensi dan riwayatnya | Fitur hapus data; uji akses |
| G-06 | Peneliti dapat mengukur kualitas sistem secara offline tanpa log besar | Dashboard evaluasi; relevance judgment |

### 3.2 Non-goals

- Bukan sistem rekomendasi adaptif berbasis machine learning.
- Bukan pencari kerja semantik berbasis embedding/LLM.
- Bukan platform rekrutmen dua sisi; sisi perekrut di luar lingkup.
- Bukan layanan lamaran kerja penuh; aplikasi tidak mengirim lamaran.
- Bukan jaminan peluang diterima; skor bukan probabilitas.
- Bukan generalisasi di luar satu koleksi, query set, dan profil simulasi.

### 3.3 Ukuran keberhasilan

Keberhasilan kualitas ranking **tidak** memakai ambang “baik” absolut. Angka hanya
bermakna relatif terhadap baseline pada koleksi, query set, dan relevance judgment yang
sama. Arah selisih dilaporkan apa adanya; hasil tidak signifikan adalah hasil yang sah.

| Dimensi | Ukuran | Target awal |
|---|---|---|
| Kualitas retrieval | P@K, R@K, F1@K, MAP, NDCG@K; K = 10 utama, K = 5 dan 20 pelengkap | Dibandingkan dengan baseline keyword matching; tidak ada ambang absolut |
| Efisiensi | Median dan p95 latensi pencarian; ukuran indeks | Median < 300 ms; p95 < 1.000 ms pada koleksi hingga 5.000 dokumen (usulan) |
| Kesepakatan anotasi | Cohen’s κ pada subset anotasi ganda | Dilaporkan; tidak ada ambang yang ditetapkan di awal |
| Produk | CTR, save rate, application click-through, zero-result rate | Hanya dilaporkan bila ada pengguna nyata dalam jumlah memadai; tanpa itu statusnya rencana |

---

## 4. Persona dan Jobs to Be Done

Persona berikut adalah **hipotesis awal**. Validasi minimal yang direncanakan: wawancara
singkat dengan 5–8 orang per segmen.

| Persona | Tujuan | Pain points (hipotesis) | Skenario |
|---|---|---|---|
| **Raka**, mahasiswa tingkat akhir informatika | Mendapat magang atau posisi junior sebelum lulus | Tidak tahu istilah jabatan yang tepat; terlalu banyak hasil tidak relevan | Mencari “data”, menyaring tipe magang, menyimpan tiga lowongan |
| **Sinta**, fresh graduate akuntansi | Pekerjaan penuh waktu pertama di kota tertentu | Lowongan menumpuk lintas bidang; kualifikasi sulit dibandingkan | Mengisi preferensi kategori dan lokasi, membuka feed rekomendasi, melamar satu lowongan |
| **Budi**, pencari kerja pindah karier | Beralih dari operasional ke analisis data | Pengalaman lama tidak cocok dengan istilah baru; ragu level yang realistis | Mencari dengan istilah lama dan baru, membandingkan hasil, menyimpan lowongan junior analis |

### Jobs to be done

- **Raka:** “Saat mencari magang, saya ingin cepat menemukan lowongan yang sesuai level
  saya.”
- **Sinta:** “Saat banyak lowongan masuk, saya ingin disarankan yang paling mirip dengan
  yang pernah saya simpan.”
- **Budi:** “Saat berpindah karier, saya ingin tahu kata kunci apa yang cocok dengan
  pengalaman saya.”
- **Semua:** “Saya ingin tahu mengapa lowongan ini muncul.”

---

## 5. Prinsip Desain Produk

1. **Dapat dijelaskan** — setiap hasil menunjukkan istilah yang cocok atau alasan
   rekomendasi.
2. **Pencarian tanpa syarat** — tidak perlu akun atau riwayat untuk mencari.
3. **Kontrol pengguna** — pengguna dapat melihat dan menghapus data preferensi dan
   riwayatnya.
4. **Minimal data pribadi** — hanya data yang dibutuhkan untuk fitur.
5. **Tidak berlebihan klaim** — skor bukan probabilitas; antarmuka tidak memakai kata
   “AI cerdas” untuk aturan pembobotan.

---

## 6. Lingkup Produk

### 6.1 MVP

- Search bar.
- Filter lokasi, kategori, dan tipe pekerjaan.
- Sort relevansi dan tanggal.
- Daftar dan detail lowongan.
- Registrasi dan autentikasi.
- Profil preferensi.
- Bookmark.
- Feed rekomendasi Top-N dengan alasan.
- Event tracking.
- Dashboard evaluasi.

### 6.2 Pengembangan lanjutan

- Halaman pengelolaan riwayat pencarian.
- Penjelasan kata cocok yang lebih kaya.
- Diversifikasi hasil dengan MMR.
- Tombol “tidak tertarik”.
- Saran istilah pencarian.
- Ekspor hasil evaluasi.

### 6.3 Di luar ruang lingkup awal

- Notifikasi email.
- Chat dengan perekrut.
- Unggah dan parsing CV.
- Pengiriman lamaran dari dalam aplikasi.
- Embedding transformer atau LLM sebagai inti.
- Aplikasi seluler native.
- Sisi perekrut.

### 6.4 Peta fitur dan ketersediaan data

Prioritas: **T** = Tinggi, **S** = Sedang, **R** = Rendah.

| Fitur | Manfaat | Tugas AI/ML/STKI | Data input → keluaran | Prioritas | Ketersediaan data |
|---|---|---|---|---|---|
| **F1** Pencarian lowongan | Menemukan lowongan yang cocok lewat query | Retrieval dan ranking (TF-IDF + Cosine Similarity) | Query teks + teks lowongan → daftar Top-K terurut | T | Ada (korpus publik; lisensi harus diverifikasi); korpus Indonesia sintetis belum ada |
| **F2** Feed rekomendasi | Menyarankan lowongan mirip yang pernah disimpan | Content-based recommendation (profil vektor TF-IDF) | Interaksi (klik detail, simpan, lamar) + vektor lowongan → Top-N dengan alasan | S | Profil persona simulasi belum ada; log pengguna nyata belum ada |
| **F3** Penjelasan hasil | Menunjukkan mengapa lowongan muncul | Explainability sederhana | Skor per query + term yang cocok → tingkat kecocokan (Tinggi/Sedang/Rendah) dan kata yang disorot | S | Ada (turunan F1) |
| **F4** Dashboard evaluasi | Mengukur kualitas sistem tanpa log besar | Evaluasi retrieval offline | Query set + relevance judgment → tabel metrik | S | Belum ada; judgment harus dibuat |

**Fitur yang layak menjadi eksperimen:** F1 sebagai fitur utama (RQ1, RQ2, RQ5) dan F2
sebagai lanjutan dalam riset yang sama (RQ3, RQ4). F3 dan F4 mendukung penyajian dan
pengukuran.

---

## 7. Functional Requirements

Setiap requirement di bawah ini adalah **tetap** bila berasal dari Grand Design, atau
**usulan** bila detail operasionalnya ditambahkan. Acceptance criteria dirancang agar
dapat diuji.

### 7.1 Pencarian dan hasil

#### FR-SEARCH-01 — Pencarian lowongan tanpa login

- **Prioritas:** T
- **Sumber:** F1, Grand Design Bagian 2
- **Deskripsi:** Pengguna dapat memasukkan query teks dan menerima daftar lowongan
  Top-K yang diurutkan berdasarkan relevansi. Pencarian tidak memerlukan akun.
- **Acceptance criteria:**
  - Query kosong atau hanya berisi stopword menghasilkan empty state, bukan error 500.
  - Hasil memuat lowongan yang berstatus aktif.
  - Urutan deterministik: skor menurun; jika skor sama, tanggal terbit terbaru lebih
    dulu; jika tanggal sama, `job_id` menaik.
  - Pengguna anonim dapat mencari tanpa diarahkan ke halaman login.

#### FR-SEARCH-02 — Filter wajib

- **Prioritas:** T
- **Sumber:** F1, atribut dataset
- **Deskripsi:** Pengguna dapat memfilter hasil berdasarkan lokasi, kategori, tipe
  pekerjaan, dan level pengalaman.
- **Acceptance criteria:**
  - Dokumen yang tidak lolos filter tidak muncul di hasil (TC06).
  - Filter tidak memengaruhi skor; filter membuang kandidat sebelum/sesudah ranking
    sesuai urutan yang konsisten dan terdokumentasi.
  - Kombinasi filter yang tidak menghasilkan dokumen menampilkan empty state.

#### FR-SEARCH-03 — Sort relevansi dan tanggal

- **Prioritas:** T
- **Sumber:** Grand Design Bagian 2
- **Deskripsi:** Pengguna dapat memilih urutan berdasarkan relevansi atau tanggal
  terbit.
- **Acceptance criteria:**
  - Sort tanggal tidak mengubah skor, hanya urutan tampilan.
  - Sort relevansi memakai tie-break FR-SEARCH-01.

#### FR-SEARCH-04 — Empty state dan zero-result event

- **Prioritas:** T
- **Sumber:** TC05, Grand Design Bagian 6
- **Deskripsi:** Bila tidak ada hasil, UI menampilkan pesan “tidak ada hasil” dan
  mencatat event zero-result.
- **Acceptance criteria:**
  - Tidak ada hasil → HTTP 200 dengan daftar kosong dan pesan yang jelas.
  - Event zero-result tercatat tanpa menyimpan data pribadi yang tidak diperlukan.

#### FR-SEARCH-05 — Batas hasil

- **Prioritas:** S
- **Sumber:** Usulan operasional
- **Deskripsi:** Jumlah hasil dibatasi oleh parameter `limit` dengan nilai default dan
  maksimum yang dikonfigurasi.
- **Acceptance criteria:**
  - `limit` di luar rentang ditolak dengan error validasi.
  - Respons menyatakan jumlah hasil yang dikembalikan.

### 7.2 Detail lowongan

#### FR-JOB-01 — Melihat detail lowongan

- **Prioritas:** T
- **Sumber:** Grand Design Bagian 2
- **Deskripsi:** Pengguna dapat membuka halaman detail lowongan dari hasil pencarian,
  bookmark, atau feed rekomendasi.
- **Acceptance criteria:**
  - Detail menampilkan judul, perusahaan, lokasi, tipe, level, kategori, deskripsi,
    kualifikasi, skills, tanggal terbit, dan sumber.
  - Lowongan yang tidak aktif ditandai atau tidak dapat diakses sesuai kebijakan.
  - Membuka detail dari feed mencatat event `rec_click`; membuka dari pencarian mencatat
    event `view` (bila pelacakan diaktifkan untuk pengguna/login).

### 7.3 Akun dan preferensi

#### FR-AUTH-01 — Registrasi, login, dan logout

- **Prioritas:** T
- **Sumber:** Grand Design Bagian 2, Bagian 7
- **Deskripsi:** Pengguna dapat membuat akun, masuk, dan keluar. Kata sandi di-hash
  dengan bcrypt atau argon2; algoritma hash tidak ditulis sendiri.
- **Acceptance criteria:**
  - Registrasi menolak email duplikat dan input tidak valid.
  - Login dengan kredensial salah tidak membocorkan apakah email terdaftar.
  - Logout mengakhiri sesi/token.
  - Percobaan login dibatasi (rate limit) dan kesalahan dicatat tanpa menyimpan kata
    sandi.

#### FR-PREF-01 — Melihat dan mengubah preferensi

- **Prioritas:** T
- **Sumber:** Grand Design Bagian 2, endpoint `/api/me/preferences`
- **Deskripsi:** Pengguna yang login dapat membaca dan mengubah preferensi kategori,
  lokasi, tipe pekerjaan, dan level pengalaman.
- **Acceptance criteria:**
  - Perubahan tersimpan dan langsung dipakai pada pencarian/feed berikutnya.
  - Preferensi kosong valid dan tidak menyebabkan error.
  - Hanya pemilik data yang dapat membaca/mengubah preferensinya.

### 7.4 Bookmark

#### FR-BOOK-01 — Daftar, simpan, dan hapus bookmark

- **Prioritas:** T
- **Sumber:** Grand Design Bagian 2, TC11
- **Deskripsi:** Pengguna dapat menyimpan lowongan, melihat daftar simpanan, dan
  menghapusnya. Operasi simpan dan hapus bersifat idempoten.
- **Acceptance criteria:**
  - Menyimpan lowongan yang sama dua kali menghasilkan satu baris dan tidak error
    (TC11).
  - Menghapus bookmark yang tidak ada tidak menghasilkan error 500.
  - Bookmark hanya dapat diakses pemiliknya.
  - Lowongan yang disimpan tidak muncul lagi di feed rekomendasi (TC10).

### 7.5 Feed rekomendasi

#### FR-REC-01 — Feed Top-N dengan alasan

- **Prioritas:** S
- **Sumber:** F2, Grand Design Bagian 2, Bagian 5
- **Deskripsi:** Pengguna yang login dan memiliki riwayat interaksi menerima feed Top-N
  berisi lowongan yang mirip dengan profilnya, disertai alasan.
- **Acceptance criteria:**
  - Setiap item feed memiliki alasan yang dapat dibaca, misalnya “mirip dengan lowongan
    yang Anda simpan”.
  - Urutan ditentukan oleh `FinalScore = α·QueryScore + β·ProfileScore`; detail
    penerapan pada feed tanpa query dicatat sebagai keputusan terbuka di
    `02-system-design.md`.
  - Profil dan skor dapat direproduksi dari konfigurasi yang tercatat.

#### FR-REC-02 — Cold start

- **Prioritas:** S
- **Sumber:** Grand Design Bagian 5
- **Deskripsi:** Pengguna tanpa riwayat memakai `β = 0`; feed menjadi hasil
  non-personalisasi. Lowongan baru tetap dapat muncul karena vektornya dibentuk dari teks.
- **Acceptance criteria:**
  - Pengguna baru tidak menerima error dan tidak melihat alasan personalisasi palsu.
  - `β = 0` menghasilkan `FinalScore` yang sama dengan `QueryScore` (TC07).

#### FR-REC-03 — Slot non-personalisasi

- **Prioritas:** S
- **Sumber:** Grand Design Bagian 5
- **Deskripsi:** Sebagian slot Top-N (usulan 20%) dikhususkan untuk hasil
  non-personalisasi untuk mitigasi feedback loop.
- **Acceptance criteria:**
  - Feed dengan profil tetap memuat slot non-personalisasi sesuai konfigurasi.
  - Slot tersebut diberi label atau dapat dibedakan untuk evaluasi.

#### FR-REC-04 — Diversifikasi dan “tidak tertarik”

- **Prioritas:** R (pengembangan lanjutan)
- **Sumber:** Grand Design Bagian 2
- **Deskripsi:** MMR dan tombol “tidak tertarik” tidak termasuk MVP; disiapkan sebagai
  pengembangan lanjutan.
- **Acceptance criteria:** Tidak diuji pada MVP; keputusan implementasi dicatat di ADR
  bila dikerjakan.

### 7.6 Penjelasan hasil

#### FR-EXP-01 — Tingkat kecocokan dan istilah yang cocok

- **Prioritas:** S
- **Sumber:** F3, Grand Design Bagian 2
- **Deskripsi:** Setiap hasil pencarian menampilkan tingkat kecocokan **Tinggi /
  Sedang / Rendah** dan istilah query yang cocok. Tingkat kecocokan dihitung relatif
  terhadap hasil query tersebut.
- **Acceptance criteria:**
  - Tidak menampilkan skor mentah atau persentase kepada pengguna biasa.
  - Istilah yang disorot berasal dari term query yang benar-benar cocok.
  - Ambang Tinggi/Sedang/Rendah dapat dikonfigurasi dan dikalibrasi; nilai awal dicatat
    sebagai keputusan terbuka.

#### FR-EXP-02 — Penjelasan batas skor

- **Prioritas:** S
- **Sumber:** Grand Design Bagian 2
- **Deskripsi:** Ikon info menjelaskan bahwa tingkat kecocokan adalah kemiripan teks,
  bukan peluang diterima.
- **Acceptance criteria:**
  - Teks bantuan tersedia dan dapat diakses keyboard.
  - Tidak ada klaim “AI cerdas”, probabilitas, atau prediksi penerimaan.

### 7.7 Event tracking

#### FR-EVENT-01 — Mencatat interaksi

- **Prioritas:** T
- **Sumber:** Grand Design Bagian 2, Bagian 7
- **Deskripsi:** Sistem mencatat event `view`, `save`, `apply_click`, dan `rec_click`
  untuk pengguna yang login, serta event pencarian/zero-result sesuai kebutuhan evaluasi.
- **Acceptance criteria:**
  - Event memiliki tipe, waktu, pengguna (bila login), lowongan (bila relevan), dan
    posisi tayang (bila tersedia).
  - Event hanya dapat ditulis untuk pengguna yang berhak.
  - Event tidak menyimpan isi lamaran atau data sensitif.

#### FR-EVENT-02 — Pemisahan data simulasi

- **Prioritas:** T
- **Sumber:** Grand Design Bagian 4, Bagian 6, TC13
- **Deskripsi:** Interaksi simulasi diberi penanda `is_simulated = true` dan tidak
  dihitung sebagai metrik produk.
- **Acceptance criteria:**
  - Event simulasi tidak masuk agregat metrik produk (TC13).
  - UI/dashboard memberi label “simulasi” pada data simulasi.

### 7.8 Dashboard evaluasi

#### FR-EVAL-01 — Ringkasan dan eksekusi evaluasi offline

- **Prioritas:** S
- **Sumber:** F4, Grand Design Bagian 2, Bagian 7
- **Deskripsi:** Admin/peneliti dapat melihat ringkasan metrik dan menjalankan evaluasi
  offline terhadap query set dan relevance judgment.
- **Acceptance criteria:**
  - Hanya admin yang dapat mengakses endpoint evaluasi; pengguna biasa mendapat 403
    (TC12).
  - Evaluasi memakai konfigurasi eksperimen yang tercatat (preprocessing, bobot, α,
    seed, versi).
  - Data evaluasi terpisah dari data produk.
  - Hasil menampilkan metrik per konfigurasi dan per bahasa.

### 7.9 Privasi dan kontrol data

#### FR-PRIV-01 — Menghapus riwayat dan event pengguna

- **Prioritas:** T
- **Sumber:** Grand Design Bagian 2, Bagian 7
- **Deskripsi:** Pengguna dapat menghapus riwayat pencarian, preferensi, bookmark, dan
  event interaksi miliknya.
- **Acceptance criteria:**
  - Penghapusan hanya berlaku untuk data pengguna yang login.
  - Data evaluasi dan data produk lain tidak ikut terhapus.
  - Respons sukses tetap diberikan bila sebagian data sudah tidak ada.

#### FR-PRIV-02 — Minimalisasi data dan pseudonim

- **Prioritas:** T
- **Sumber:** Grand Design Bagian 6
- **Deskripsi:** Hanya data yang dibutuhkan fitur yang dikumpulkan; log analitik memakai
  pseudonim; isi lamaran tidak disimpan.
- **Acceptance criteria:**
  - Tidak ada atribut sensitif (usia, jenis kelamin, agama) sebagai sinyal rekomendasi.
  - Log tidak memuat kata sandi, token, atau isi lamaran.

### 7.10 Requirement lanjutan (belum MVP)

| ID | Requirement | Sumber | Catatan |
|---|---|---|---|
| FR-FUT-01 | Halaman pengelolaan riwayat pencarian | Grand Design Bagian 2 | Dapat digabung dengan FR-PRIV-01 |
| FR-FUT-02 | Penjelasan kata cocok yang lebih kaya | Grand Design Bagian 2 | Perlu data term per field |
| FR-FUT-03 | Diversifikasi MMR | Grand Design Bagian 2 | Mengubah ranking; perlu evaluasi |
| FR-FUT-04 | Tombol “tidak tertarik” | Grand Design Bagian 2 | Sinyal negatif eksplisit; belum masuk model |
| FR-FUT-05 | Saran istilah pencarian | Grand Design Bagian 2 | Dapat memakai kamus normalisasi |
| FR-FUT-06 | Ekspor hasil evaluasi | Grand Design Bagian 2 | CSV/JSON |

---

## 8. UX Requirements

### 8.1 Halaman MVP

| Halaman | Isi minimum | Akses |
|---|---|---|
| Pencarian | Search bar, filter, sort, daftar hasil, empty state | Publik |
| Detail lowongan | Informasi lowongan, skills, sumber, tombol simpan | Publik |
| Registrasi/Login | Form, validasi, pesan error | Publik |
| Preferensi | Kategori, lokasi, tipe, level | Login |
| Bookmark | Daftar simpanan, hapus | Login |
| Feed rekomendasi | Top-N, alasan, label simulasi bila relevan | Login |
| Dashboard evaluasi | Ringkasan metrik, tombol jalankan evaluasi | Admin |

### 8.2 Penyajian skor tanpa menyesatkan

- Tampilkan **Tinggi / Sedang / Rendah** dengan batas relatif terhadap hasil query itu,
  bukan angka mentah atau persentase.
- Ikon info: “Tingkat ini menunjukkan kemiripan teks, bukan peluang Anda diterima.”
- Skor mentah hanya tersedia di dashboard peneliti/admin.
- Jangan memakai istilah “AI cerdas”, “probabilitas”, atau “prediksi” untuk aturan
  pembobotan.
- Alasan rekomendasi harus spesifik dan dapat dilacak ke interaksi atau term, bukan
  kalimat generik yang tidak dapat diverifikasi.

### 8.3 Empty, error, dan loading state

- Query tanpa hasil: pesan “tidak ada hasil” dan saran memperluas filter/istilah.
- Filter terlalu sempit: tampilkan filter aktif dan cara menghapusnya.
- Gagal memuat: pesan error yang dapat dicoba ulang; jangan menampilkan stack trace.
- Loading: indikator yang tidak menggeser layout secara berlebihan.

### 8.4 Aksesibilitas

- Dapat dioperasikan dengan keyboard.
- Kontras warna memadai.
- Label formulir eksplisit.
- Status kecocokan tidak boleh disampaikan hanya lewat warna; gunakan teks/ikon.
- Ikon info memiliki teks alternatif.

---

## 9. Non-Functional Requirements (Ringkasan)

Detail implementasi ada di `02-system-design.md` Bagian 11.

| ID | Kategori | Requirement | Target awal |
|---|---|---|---|
| NFR-PERF-01 | Performance | Latensi pencarian | Median < 300 ms; p95 < 1.000 ms pada koleksi hingga 5.000 dokumen |
| NFR-PERF-02 | Performance | Waktu bangun indeks | Tercatat per ukuran koleksi; tanpa ambang ketat |
| NFR-REL-01 | Reliability | Pemulihan indeks | Indeks dan konfigurasi dapat dibangun ulang dari data sumber dengan satu perintah |
| NFR-REL-02 | Reliability | Cadangan database | Berkala; prosedur pemulihan dicatat |
| NFR-SEC-01 | Security | Autentikasi dan data | Kata sandi di-hash; kueri berparameter; batas percobaan login; header keamanan standar; rahasia di environment |
| NFR-PRIV-01 | Privacy | Data pengguna | Minimum; pseudonim pada log; hapus riwayat; tidak menyimpan isi lamaran |
| NFR-A11Y-01 | Accessibility | Antarmuka | Keyboard, kontras, label formulir |
| NFR-MAINT-01 | Maintainability | Kode | Modul retrieval/rekomendasi terpisah dari framework; konfigurasi eksperimen di berkas; cakupan uji modul inti minimal sekitar 70% |
| NFR-DATA-01 | Data quality | Korpus | Duplikat dibuang lewat hash; field wajib terisi; lowongan kedaluwarsa ditandai tidak aktif |

---

## 10. Metrik Produk dan Batas Pelaporan

Metrik produk **hanya** dilaporkan bila ada pengguna nyata dalam jumlah memadai:

- CTR hasil pencarian.
- Save rate.
- Application click-through.
- Zero-result rate.

Tanpa pengguna nyata, metrik tersebut berstatus **rencana**, bukan hasil. Interaksi
simulasi tidak boleh dicampur dengan metrik produk dan harus memiliki `is_simulated`.
Usability test dasar dengan 5–8 peserta dapat dilakukan dengan persetujuan tertulis dan
konsultasi prosedur etik kampus.

---

## 11. Asumsi, Kendala, dan Dependensi

| Jenis | Isi | Dampak bila salah |
|---|---|---|
| Asumsi | Persona mewakili pengguna sasaran | Prioritas fitur dan skenario uji perlu direvisi |
| Asumsi | Korpus publik dapat dipakai sesuai lisensi | Dataset harus diganti atau dibatasi |
| Asumsi | Query set 40–60 cukup untuk evaluasi | Kekuatan statistik dan generalisasi terbatas |
| Asumsi | Annotator kedua tersedia untuk Cohen’s κ | Kesepakatan anotasi tidak dapat diukur penuh |
| Kendala | Pelaksana tunggal; 12 minggu | Beban anotasi dan pengembangan harus dikendalikan |
| Kendala | TF-IDF tidak menangkap sinonim/semantik | Klaim kualitas harus dibatasi |
| Kendala | Interaksi pengguna nyata belum ada | Personalisasi diuji dengan profil simulasi |
| Dependensi | Lisensi dan ketentuan dataset | Harus diverifikasi sebelum unduh/pakai |
| Dependensi | Stack final (React atau Django) | Menentukan jadwal tahap 6 |

---

## 12. Keputusan Terbuka

Keputusan berikut belum final dan tidak boleh dianggap sebagai kontrak:

1. Jumlah query dan kedalaman pool yang realistis untuk jadwal.
2. Varian gain DCG (eksponensial vs linear) dan perlakuan query tanpa dokumen relevan.
3. Apakah BM25 ikut sebagai pembanding opsional.
4. Kalibrasi batas Tinggi/Sedang/Rendah.
5. Penggunaan sesi anonim untuk event pencarian.
6. Keputusan stack final: React + Vite atau Django monolit.
7. Mekanisme autentikasi: session cookie atau bearer token.
8. Cara membentuk `QueryScore` pada feed rekomendasi tanpa query aktif.
9. Apakah event `search`/`zero_result` masuk tabel event atau hanya `search_history`.

---

## 13. Traceability

| Requirement | Fitur | RQ terkait | Dokumen pendukung |
|---|---|---|---|
| FR-SEARCH-01–05 | F1 | RQ1, RQ2, RQ5 | `02-system-design.md` Bagian 4; `research/research-and-evaluation.md` Bagian 7 |
| FR-JOB-01 | F1 | — | `data/database-design.md` |
| FR-AUTH-01 | MVP | — | `03-api-spec.md`; `02-system-design.md` Bagian 11 |
| FR-PREF-01 | F2 | RQ3 | `03-api-spec.md`; `data/database-design.md` |
| FR-BOOK-01 | F2 | RQ3, RQ4 | `03-api-spec.md`; TC10, TC11 |
| FR-REC-01–04 | F2 | RQ3, RQ4 | `02-system-design.md` Bagian 5; `research/research-and-evaluation.md` Bagian 7 |
| FR-EXP-01–02 | F3 | — | `02-system-design.md` Bagian 6; ADR-0007 |
| FR-EVENT-01–02 | F2, F4 | RQ3, RQ4 | `data/database-design.md`; TC13 |
| FR-EVAL-01 | F4 | RQ1–RQ5 | `03-api-spec.md`; `research/research-and-evaluation.md` Bagian 8 |
| FR-PRIV-01–02 | MVP | — | `02-system-design.md` Bagian 11; ADR-0008 |

---

**Rujukan utama:** `GRAND_DESIGN_PRODUK_INOVATIF_KarirMatch.pdf` Bagian 1, Bagian 2, Bagian 6, Bagian 7.
