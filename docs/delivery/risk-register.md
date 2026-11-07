# Risk Register dan Kebijakan Klaim — KarirMatch

**Status:** Disetujui v1.0  
**Pemilik:** Deris Firmansyah  
**Sumber:** Grand Design Produk Inovatif KarirMatch Bagian 3, Bagian 4, Bagian 6, Bagian 7  
**Terakhir diperbarui:** 7 November 2026

---

## 1. Cara Menggunakan Register

- **Prioritas** mengikuti Grand Design: Tinggi, Sedang, Rendah.
- **Status** menunjukkan apakah risiko sudah dimitigasi, masih terbuka, atau diterima.
- **Pemicu** adalah tanda awal bahwa risiko sedang terjadi.
- Setiap risiko harus memiliki mitigasi yang dapat dikerjakan, bukan hanya pernyataan
  umum.
- Register ditinjau di setiap milestone (`delivery/roadmap.md`).

---

## 2. Register Risiko

### 2.1 Risiko data dan legalitas

| ID | Risiko | Prioritas | Dampak | Mitigasi | Pemicu | Status |
|---|---|---|---|---|---|---|
| **RISK-DATA-01** | Dataset tidak representatif (dominan satu bidang, bahasa Inggris, atau satu platform) | Tinggi | Klaim generalisasi tidak sah; hasil bias | Dokumentasikan komposisi korpus; laporkan hasil per bahasa; nyatakan batas generalisasi | Komposisi korpus didominasi satu kategori/bahasa | Terbuka |
| **RISK-DATA-02** | Lisensi/ketentuan dataset tidak mengizinkan penggunaan | Tinggi | Dataset tidak dapat dipakai; pekerjaan harus diulang | Verifikasi lisensi dan ToS sebelum unduh; catat sumber, tanggal, versi; siapkan kandidat alternatif | Lisensi tidak jelas atau melarang penggunaan | Terbuka |
| **RISK-DATA-03** | Tidak ada korpus publik lowongan Indonesia berteks lengkap | Tinggi | Hasil bahasa Indonesia tidak dapat diklaim representatif | Gunakan korpus sintetis yang dinyatakan eksplisit; cari sumber sah; catat sebagai keterbatasan | Tidak ditemukan sumber sah sampai tahap 2 | Terbuka |
| **RISK-DATA-04** | Duplikat atau data kedaluwarsa | Sedang | Hasil tidak relevan; evaluasi terdistorsi | Hash deduplikasi; tandai `is_active`; validasi tanggal | Banyak duplikat/iklan lama | Dimitigasi sebagian |
| **RISK-DATA-05** | Kontak pribadi/PII dalam teks lowongan | Sedang | Risiko privasi | Buang email/telepon/URL pribadi sebelum indeks (usulan); review sampel | Ditemukan kontak di teks | Terbuka |

### 2.2 Risiko evaluasi dan metode

| ID | Risiko | Prioritas | Dampak | Mitigasi | Pemicu | Status |
|---|---|---|---|---|---|---|
| **RISK-EVAL-01** | Ground truth terbatas (annotator sedikit, subjektif, pooling terbatas) | Tinggi | Kesimpulan lemah; κ rendah | Pedoman tertulis; pilot; minimal dua annotator; Cohen’s κ; tafsirkan selisih relatif | κ rendah atau judgment tidak konsisten | Terbuka |
| **RISK-EVAL-02** | Beban anotasi melebihi kapasitas | Sedang | Evaluasi terlambat; kualitas turun | Kurangi jumlah query atau kedalaman pool lebih awal; jadwalkan anotasi di roadmap | Progres anotasi tertinggal | Terbuka |
| **RISK-EVAL-03** | Data leakage dari seed profil atau test set | Tinggi | Hasil terlalu optimistis | Keluarkan seed dari kandidat; anotasi buta; test dilaporkan sekali; validation/test terpisah | Metrik test jauh lebih tinggi dari validation | Terbuka |
| **RISK-METHOD-01** | Vocabulary mismatch dan keterbatasan TF-IDF pada semantik/urutan kata | Tinggi | Kualitas ranking terbatas; klaim berlebihan | Kamus normalisasi; bigram; analisis kegagalan; embedding sebagai pengembangan masa depan; jangan klaim pemahaman makna | Banyak query gagal karena sinonim | Diterima sebagai keterbatasan |
| **RISK-METHOD-02** | Generalisasi dari sampel kecil | Tinggi | Klaim di luar cakupan | Laporkan ukuran sampel, CI, effect size; sebut batas: satu koleksi, 40–60 query, profil simulasi | Permintaan generalisasi ke seluruh pasar | Diterima sebagai keterbatasan |
| **RISK-METHOD-03** | Formula dan implementasi tidak konsisten | Sedang | Hasil tidak dapat direproduksi | Test case IDF/cosine; kunci versi pustaka; konfigurasi di berkas | TC01/TC02 gagal atau hasil berubah antar run | Dimitigasi sebagian |
| **RISK-METHOD-04** | Keyword stuffing | Sedang | Ranking dimanipulasi | Sublinear TF dan normalisasi L2; uji dokumen yang dijejali | Dokumen spam naik peringkat | Dimitigasi sebagian |
| **RISK-METHOD-05** | Perbedaan hasil per bahasa tidak dilaporkan | Sedang | Klaim gabungan menyesatkan | Pisahkan hasil `id`, `en`, `mixed`; laporkan komposisi | Laporan hanya satu angka gabungan | Terbuka |

### 2.3 Risiko produk dan personalisasi

| ID | Risiko | Prioritas | Dampak | Mitigasi | Pemicu | Status |
|---|---|---|---|---|---|---|
| **RISK-SIM-01** | Interaksi simulasi disalahartikan sebagai perilaku nyata | Tinggi | Klaim produk palsu | Kolom `is_simulated`; label “simulasi” di semua tabel; metrik produk hanya dari data nyata | Event simulasi masuk agregat produk | Dimitigasi sebagian |
| **RISK-PROD-01** | Privasi riwayat pencarian dan lamaran | Tinggi | Kepercayaan pengguna rusak; risiko legal | Kumpulkan minimum; pseudonim pada log; fitur hapus data; tidak menyimpan isi lamaran; akses admin dibatasi | Ada permintaan hapus data atau audit privasi | Terbuka |
| **RISK-PROD-02** | Bias interaksi (position bias, feedback loop) | Sedang | Rekomendasi makin sempit | Slot non-personalisasi 20%; catat posisi tayang; pantau keragaman kategori; klik bukan relevansi absolut | Keragaman kategori turun | Terbuka |
| **RISK-PROD-03** | Cold-start pengguna dan lowongan | Rendah–sedang | Feed kosong/tidak relevan | Pencarian tanpa riwayat; `β = 0`; lowongan baru langsung punya vektor teks | Pengguna baru tidak mendapat hasil | Dimitigasi sebagian |
| **RISK-PROD-04** | Skor disalahartikan sebagai probabilitas | Sedang | Keputusan pengguna salah | Tampilkan Tinggi/Sedang/Rendah; ikon info; skor mentah hanya admin | Pengguna menyebut “peluang diterima” | Dimitigasi sebagian |
| **RISK-PROD-05** | Lowongan tidak aktif tetap muncul | Rendah | Pengalaman buruk | `is_active`; filter; kebijakan 404/penanda | Ada laporan lowongan kedaluwarsa | Terbuka |

### 2.4 Risiko keamanan dan operasional

| ID | Risiko | Prioritas | Dampak | Mitigasi | Pemicu | Status |
|---|---|---|---|---|---|---|
| **RISK-SEC-01** | Autentikasi lemah atau kebocoran sesi | Sedang | Akun/data pengguna terekspos | Hash bcrypt/argon2; rate limit; cookie HttpOnly/Secure; otorisasi server-side; header keamanan | Percobaan login mencurigakan | Terbuka |
| **RISK-SEC-02** | Endpoint admin diakses pengguna biasa | Sedang | Data evaluasi/konfigurasi terekspos | Role admin; test TC12; 403 | Ada akses tanpa role | Dimitigasi sebagian |
| **RISK-OPS-01** | Evaluasi berat memblokir API | Sedang | Timeout; demo gagal | Jalankan evaluasi lewat CLI; endpoint sinkron hanya untuk query set kecil | Request eval melebihi timeout | Terbuka |
| **RISK-OPS-02** | Indeks hilang/rusak saat startup | Sedang | Pencarian gagal | Rebuild satu perintah; health check; backup artefak | Aplikasi gagal memuat indeks | Dimitigasi sebagian |
| **RISK-OPS-03** | Database tidak siap | Sedang | API 503 | Backup; migrasi; health check | Koneksi DB gagal | Terbuka |

### 2.5 Risiko pelaksanaan

| ID | Risiko | Prioritas | Dampak | Mitigasi | Pemicu | Status |
|---|---|---|---|---|---|---|
| **RISK-DEL-01** | Pelaksana tunggal dengan 12 minggu | Tinggi | Pekerjaan tidak selesai | Prioritaskan MVP; parallelisasi UI/retrieval; buffer anotasi; kurangi lingkup bila perlu | Milestone tertinggal >1 minggu | Terbuka |
| **RISK-DEL-02** | React belum dikuasai | Sedang | UI tertunda | Putuskan sebelum tahap 6; fallback Django monolit | Belum ada progres UI di minggu 5 | Terbuka |
| **RISK-DEL-03** | Annotator kedua tidak tersedia | Sedang | κ tidak dapat diukur | Cari annotator sejak awal; jika tidak ada, catat keterbatasan | Belum ada komitmen di minggu 6 | Terbuka |
| **RISK-CLAIM-01** | Klaim melebihi bukti | Tinggi | Laporan tidak valid | Kebijakan klaim Bagian 3; review klaim di laporan | Ada kata “unggul” tanpa data | Terbuka |

---

## 3. Kebijakan Klaim

### Boleh diklaim

- Perbandingan terukur pada koleksi, query set, dan judgment yang dibuat sendiri.
- Perubahan metrik apa adanya, termasuk bila tidak signifikan.
- Desain sistem yang transparan.
- Keterbatasan dan kasus gagal.

### Tidak boleh diklaim

- Keunggulan sebelum eksperimen.
- Skor sebagai probabilitas.
- Interaksi simulasi sebagai perilaku pengguna.
- “AI adaptif” atau reinforcement learning.
- Generalisasi di luar dataset.
- Sitasi yang belum diverifikasi.
- “Personalisasi meningkatkan kualitas” tanpa hasil yang mendukung.
- “Lebih baik dari LinkedIn/Indeed” atau perbandingan serupa tanpa data.

**Aturan penulisan:** setiap klaim di laporan harus menunjuk ke eksperimen, metrik, dan
konfigurasi yang mendukung. Klaim tanpa rujukan dihapus atau diturunkan menjadi hipotesis.

---

## 4. Keputusan Terbuka

### 4.1 Dari Grand Design Bagian 7

1. Jumlah query dan kedalaman pool yang realistis untuk jadwal.
2. Varian gain DCG dan perlakuan query tanpa dokumen relevan.
3. Apakah BM25 ikut sebagai pembanding.
4. Kalibrasi batas Tinggi/Sedang/Rendah.
5. Penggunaan sesi anonim untuk event pencarian.
6. Keputusan stack final bergantung pada kenyamanan dengan React.

### 4.2 Dari dokumen turunan

7. Mekanisme autentikasi: session cookie atau bearer token.
8. Cara membentuk `QueryScore` pada feed tanpa query.
9. Apakah event `search`/`zero_result` masuk `interaction_events` atau `search_history`.
10. Lokasi tabel evaluasi: schema terpisah atau database terpisah.
11. Kebijakan retensi event dan riwayat.
12. Pagination di luar Top-K.
13. Apakah lowongan tidak aktif tetap dapat diakses via detail.
14. Format `DELETE` bookmark: subresource atau body.
15. Perilaku `q` kosong pada pencarian.
16. Apakah `recommendation_logs` diaktifkan.

---

## 5. Inkonsistensi dan Catatan Sumber

| Item | Temuan | Tindakan |
|---|---|---|
| NIM | Header PDF: `A11.2024.15624`; Bagian 7: `A11.2024.15625` | Terkonfirmasi pada Fase 0 (P0-06): NIM valid yang digunakan adalah `A11.2024.15624` |
| Rumus PDF | Ekstraksi teks merusak sebagian notasi | Rumus ditulis ulang dan diuji terhadap contoh N=4 (TC01/TC02) |
| Gambar arsitektur | Gambar halaman 8 tidak terbaca sebagai teks | Direkonstruksi menjadi Mermaid dan diperiksa visual |
| Lisensi dataset | Belum diverifikasi | Wajib sebelum unduh |
| Korpus Indonesia | Belum ada | Sintetis sampai sumber sah ditemukan |

---

## 6. Monitoring dan Tinjauan

| Waktu | Yang ditinjau |
|---|---|
| Setiap akhir tahap | Risiko baru, progres mitigasi, keputusan terbuka |
| Sebelum anotasi | Pedoman, jumlah query, beban annotator |
| Sebelum test set | Konfigurasi terkunci; tidak ada tuning di test |
| Sebelum demo | Klaim, data simulasi, akses admin |
| Sebelum publikasi | Lisensi, atribusi, NIM, sitasi |

**Aturan eskalasi:** jika risiko Tinggi terjadi, prioritas pekerjaan berubah untuk
mitigasi; jika tidak dapat dimitigasi, catat sebagai keterbatasan dan sesuaikan klaim.

---

## 7. Traceability

| Bagian | Sumber Grand Design |
|---|---|
| Risiko data | Bagian 4 Etika/legalitas; Bagian 6 Risiko |
| Risiko evaluasi | Bagian 6 Pembuatan relevance judgment; Bagian 6 Risiko |
| Risiko metode | Bagian 3 Keterbatasan; Bagian 5 |
| Risiko simulasi | Bagian 4 Batasan data sintetis; Bagian 6 |
| Risiko personalisasi | Bagian 5 Pencegah dominasi; Bagian 6 Risiko |
| Risiko keamanan | Bagian 6 Kebutuhan non-fungsional |
| Risiko pelaksanaan | Bagian 7 Rencana; pelaksana tunggal |
| Kebijakan klaim | Bagian 7 Yang boleh dan tidak boleh diklaim |
| Keputusan terbuka | Bagian 7 Keputusan terbuka |
