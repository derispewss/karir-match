# Fase 5 — Personalisasi

**Minggu:** 6–7  
**Estimasi:** ±5,5 hari  
**Status:** Belum dimulai  
**Prasyarat:** Gate F4 lulus; indeks TF-IDF dan scoring tersedia  
**Gate keluar:** F5 — TC07–TC10 lulus, profil simulasi siap, D4 diputuskan

---

## Tujuan

Membangun feed rekomendasi berbasis profil vektor yang dapat dijelaskan, di-ablation,
dan tidak mengklaim machine learning adaptif.

---

## Tugas

### P5-01 — Pembentukan profil vektor

- [ ] Implementasikan agregasi vektor lowongan yang diinteraksikan.
- [ ] Terapkan bobot sinyal: klik detail = 1, simpan = 3, lamar = 5.
- [ ] Terapkan peluruhan waktu `δ(a) = 2^(-a/14)` dengan half-life 14 hari.
- [ ] Normalisasi profil L2.
- [ ] Hitung satu dokumen paling banyak sekali per jenis sinyal.
- [ ] Batasi interaksi aktif (usulan 50 terbaru).
- [ ] Buat parameter dapat dikonfigurasi.

- **Output:** Modul pembentukan profil.
- **Estimasi:** 1,0 hari.
- **Dependensi:** P4-07.
- **Acceptance:** Profil dapat direproduksi dari event dan konfigurasi; norma = 1;
  tidak ada dominasi satu interaksi.

### P5-02 — FinalScore dan cold start

- [ ] Implementasikan `FinalScore = α·QueryScore + β·ProfileScore`.
- [ ] Pastikan `α + β = 1` dan `α, β ≥ 0`.
- [ ] Implementasikan `β = 0` untuk pengguna tanpa riwayat.
- [ ] Implementasikan opsi `β` naik bertahap bila diaktifkan.
- [ ] Catat parameter α, β, β_max, dan n₀ di konfigurasi.

- **Output:** Fungsi FinalScore dan konfigurasi.
- **Estimasi:** 0,75 hari.
- **Dependensi:** P5-01.
- **Acceptance:** `β = 0` menghasilkan skor sama dengan QueryScore; parameter
  eksperimen tercatat.

### P5-03 — Batas interaksi dan deduplikasi sinyal

- [ ] Pastikan satu dokumen tidak dihitung berulang untuk sinyal yang sama.
- [ ] Terapkan batas interaksi aktif.
- [ ] Tangani event duplikat atau tidak valid.
- [ ] Tulis test untuk deduplikasi.

- **Output:** Aturan deduplikasi dan test.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P5-01.
- **Acceptance:** Event duplikat tidak menggandakan bobot; batas interaksi berlaku.

### P5-04 — Slot non-personalisasi

- [ ] Sisihkan sekitar 20% slot Top-N untuk hasil non-personalisasi.
- [ ] Beri label `source: "non_personalized"` pada respons.
- [ ] Pastikan slot tetap ada saat profil tersedia.
- [ ] Pastikan pengguna baru mendapat feed non-personalisasi tanpa alasan palsu.

- **Output:** Mekanisme slot non-personalisasi.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P5-02.
- **Acceptance:** Jumlah slot sesuai konfigurasi; label dapat diaudit.

### P5-05 — Alasan rekomendasi

- [ ] Buat alasan yang dapat dilacak ke interaksi atau term.
- [ ] Contoh: “Mirip dengan lowongan yang Anda simpan.”
- [ ] Jangan memakai kalimat generik yang tidak dapat diverifikasi.
- [ ] Jangan menampilkan skor mentah kepada pengguna biasa.
- [ ] Sertakan `source_job_id` bila memungkinkan (keputusan terbuka).

- **Output:** Generator alasan rekomendasi.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P5-01.
- **Acceptance:** Setiap alasan dapat ditelusuri ke data; tidak ada klaim personalisasi
  palsu untuk pengguna baru.

### P5-06 — Profil persona simulasi

- [ ] Buat 6–10 profil persona.
- [ ] Pilih 3–8 lowongan seed per persona.
- [ ] Buat interaksi simulasi yang realistis (klik, simpan, lamar).
- [ ] Tandai semua interaksi dengan `is_simulated = true`.
- [ ] Simpan daftar seed terpisah dari kandidat evaluasi.
- [ ] Dokumentasikan bahwa ini bukan perilaku pengguna nyata.

- **Output:** Profil simulasi dan data interaksi.
- **Estimasi:** 1,0 hari.
- **Dependensi:** P2-08, P5-01.
- **Acceptance:** 6–10 profil; seed 3–8; label simulasi lengkap; seed tidak masuk
  kandidat evaluasi.

### P5-07 — Test TC07–TC10

- [ ] TC07: `β = 0` setara tanpa personalisasi.
- [ ] TC08: profil memengaruhi urutan.
- [ ] TC09: tidak ada dominasi satu interaksi; norma profil = 1.
- [ ] TC10: lowongan tersimpan tidak muncul lagi di feed.
- [ ] Simpan log hasil test.

- **Output:** Test TC07–TC10 dan log.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P5-02, P5-03, P5-04, P5-06.
- **Acceptance:** Semua test lulus atau kegagalan dijelaskan.

### P5-08 — Konfigurasi E3 dan E4

- [ ] Siapkan konfigurasi tanpa profil (`α = 1`).
- [ ] Siapkan konfigurasi profil penuh.
- [ ] Siapkan konfigurasi hanya klik detail.
- [ ] Siapkan konfigurasi hanya simpan/lamar.
- [ ] Siapkan variasi jumlah seed: 1, 3, 5, 8.
- [ ] Siapkan sweep α dari 1,0 sampai 0,5 dengan langkah 0,1.
- [ ] Siapkan variasi half-life dan batas interaksi bila memungkinkan.

- **Output:** Set konfigurasi E3/E4.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P5-02.
- **Acceptance:** Semua konfigurasi dapat dijalankan tanpa mengubah kode; hash tercatat.

### P5-09 — Keputusan D4: QueryScore pada feed tanpa query

- [ ] Tinjau tiga opsi: `α = 0`; QueryScore dari preferensi; QueryScore dari query terakhir.
- [ ] Pilih satu opsi berdasarkan konsistensi produk dan kemudahan evaluasi.
- [ ] Catat keputusan di ADR atau konfigurasi.
- [ ] Pastikan implementasi hanya memakai satu opsi yang eksplisit.

- **Output:** Keputusan D4 tercatat.
- **Estimasi:** 0,25 hari.
- **Dependensi:** P5-02.
- **Acceptance:** Tidak ada jalur kode yang memakai opsi ganda secara diam-diam.

---

## Deliverable Fase

- [ ] Modul profil vektor dan FinalScore.
- [ ] Slot non-personalisasi dan alasan rekomendasi.
- [ ] 6–10 profil simulasi berlabel.
- [ ] Test TC07–TC10 lulus.
- [ ] Konfigurasi E3/E4.
- [ ] Keputusan D4.

---

## Gate F5

- [ ] TC07–TC10 lulus atau kegagalan dijelaskan.
- [ ] Profil simulasi tersedia dan berlabel `is_simulated`.
- [ ] Seed profil dikeluarkan dari kandidat evaluasi.
- [ ] Konfigurasi E3/E4 siap.
- [ ] D4 diputuskan dan tercatat.
- [ ] Tidak ada klaim ML adaptif pada dokumentasi atau UI.

Jika gate belum lulus, jangan mulai F7 (F6 boleh berjalan paralel).

---

## Risiko Fase

| Risiko | Mitigasi |
|---|---|
| Profil terlalu sempit | Batas interaksi, peluruhan, slot non-personalisasi |
| Sinyal implicit berisik | Bobot 1:3:5; laporkan ablation; jangan klaim relevansi absolut |
| Feedback loop | 20% slot non-personalisasi; catat posisi tayang |
| Evaluasi memakai perilaku nyata | Gunakan profil simulasi berlabel; jangan klaim pengguna nyata |
| D4 tertunda | Tetapkan default eksplisit dan catat sebagai keputusan sementara |

---

## Traceability

- `docs/02-system-design.md` Bagian 5.
- `docs/research/research-and-evaluation.md` Bagian 6.
- ADR-0004.
- `docs/delivery/roadmap.md` Tahap 5.
