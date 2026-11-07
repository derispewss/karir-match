# Fase 7 — Eksperimen dan Evaluasi

**Minggu:** 9–11  
**Estimasi:** ±9 hari  
**Status:** Belum dimulai  
**Prasyarat:** Gate F4, F5, F6; query set dan pedoman anotasi siap  
**Gate keluar:** F7 — E1–E5 selesai, statistik dan analisis kesalahan terdokumentasi

---

## Tujuan

Menjalankan evaluasi offline yang adil dan reproducible untuk menjawab RQ1–RQ5,
termasuk hasil yang tidak signifikan, lalu menyimpannya sebagai bukti yang dapat
dilacak.

---

## Tugas

### P7-01 — Bekukan query set dan split (D5)

- [ ] Tinjau query set v1 dan perbaiki masalah yang ditemukan saat pilot.
- [ ] Putuskan split validation/test: 30/70 atau 40/60.
- [ ] Pastikan query test tidak dipakai untuk tuning.
- [ ] Bekukan versi query set dan hash.
- [ ] Catat keputusan D5 beserta alasan.

- **Output:** Query set final dan split.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P3-04, P3-06, D5.
- **Acceptance:** Split terdokumentasi; query test tidak berubah setelah evaluasi dimulai.

### P7-02 — Lengkapi relevance judgment

- [ ] Anotasi seluruh query set dengan minimal 2 annotator.
- [ ] Nilai ganda minimal 25% subset untuk Cohen's κ.
- [ ] Gunakan pooling Top-15 dari semua sistem.
- [ ] Jaga anotasi tetap buta: tanpa identitas sistem dan tanpa seed profil.
- [ ] Simpan judgment sebagai CSV beserta versi pedoman.
- [ ] Pantau progres harian dan beban annotator.

- **Output:** Relevance judgment lengkap.
- **Estimasi:** 2,5 hari.
- **Dependensi:** P3-05, P3-07, P7-01.
- **Acceptance:** Semua query memiliki judgment; subset ganda tersedia; tidak ada
  kebocoran identitas sistem.

### P7-03 — Cohen's κ dan adjudikasi

- [ ] Hitung κ sebelum diskusi pada subset ganda.
- [ ] Diskusikan perbedaan dan hasilkan judgment final.
- [ ] Laporkan κ sebelum dan sesudah adjudikasi bila relevan.
- [ ] Catat contoh kasus batas yang sulit.

- **Output:** Nilai κ dan judgment final.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P7-02.
- **Acceptance:** κ dilaporkan apa adanya; proses adjudikasi terdokumentasi.

### P7-04 — Jalankan E1 (baseline)

- [ ] Jalankan baseline keyword matching pada split test.
- [ ] Simpan run file, konfigurasi, seed, dan versi kode.
- [ ] Hitung metrik P@K, R@K, F1@K, MAP, NDCG@K.
- [ ] Catat waktu eksekusi.

- **Output:** Hasil E1 dan run file.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P3-01, P7-01, P7-02.
- **Acceptance:** Hasil dapat dihitung ulang dari run file dan qrels.

### P7-05 — Jalankan E2 (TF-IDF dan variasi preprocessing)

- [ ] Jalankan semua konfigurasi E2 pada split test.
- [ ] Bandingkan dengan baseline secara berpasangan per query.
- [ ] Laporkan hasil per bahasa (`id`, `en`, `mixed`).
- [ ] Simpan run file dan hash konfigurasi.

- **Output:** Hasil E2 per konfigurasi dan bahasa.
- **Estimasi:** 0,75 hari.
- **Dependensi:** P4-11, P7-02.
- **Acceptance:** Semua konfigurasi memakai koleksi, query, dan judgment yang sama.

### P7-06 — Jalankan E3 (personalisasi)

- [ ] Jalankan feed dengan dan tanpa profil pada profil simulasi.
- [ ] Sweep α sesuai konfigurasi.
- [ ] Hitung NDCG@10 sebagai metrik utama, didukung P@K dan MAP.
- [ ] Laporkan selisih per profil dan interval kepercayaan bootstrap.
- [ ] Jangan mengklaim perilaku pengguna nyata.

- **Output:** Hasil E3.
- **Estimasi:** 0,75 hari.
- **Dependensi:** P5-06, P5-08, P7-02.
- **Acceptance:** Hasil per profil tersedia; seed dikeluarkan dari kandidat evaluasi.

### P7-07 — Jalankan E4 (ablation)

- [ ] Tanpa profil (`α = 1`).
- [ ] Profil penuh.
- [ ] Hanya klik detail.
- [ ] Hanya simpan/lamar.
- [ ] Variasi jumlah seed: 1, 3, 5, 8.
- [ ] Bobot sinyal seragam vs 1:3:5.
- [ ] Sweep α dan analisis sensitivitas half-life/batas interaksi bila memungkinkan.

- **Output:** Hasil E4 dan analisis sensitivitas.
- **Estimasi:** 0,75 hari.
- **Dependensi:** P5-08, P7-06.
- **Acceptance:** Setiap komponen dapat dibandingkan; hasil tidak digabung tanpa label.

### P7-08 — Jalankan E5 (latensi dan ukuran indeks)

- [ ] Jalankan pada 1.000, 5.000, dan 20.000 dokumen.
- [ ] Ulangi minimal 30 kali; buang warm-up.
- [ ] Catat median dan p95 latensi (ms), ukuran indeks (MB), dan waktu build.
- [ ] Catat perangkat keras dan versi pustaka.
- [ ] Jika 20k tidak selesai, catat sebagai keterbatasan (D8).

- **Output:** Hasil E5 dan catatan perangkat keras.
- **Estimasi:** 0,75 hari.
- **Dependensi:** P2-07, P4-06, D8.
- **Acceptance:** Metode pengukuran dapat diulang; target dibandingkan apa adanya.

### P7-09 — Uji statistik

- [ ] RQ1 dan RQ3: Wilcoxon signed-rank berpasangan.
- [ ] RQ2: Friedman dengan post-hoc Wilcoxon dan koreksi Holm.
- [ ] RQ4: analisis sensitivitas; Friedman bila profil cukup.
- [ ] RQ5: statistik deskriptif median/p95.
- [ ] Laporkan effect size dan interval kepercayaan, bukan hanya p-value.
- [ ] Catat α-signifikansi yang dipakai.

- **Output:** Tabel uji statistik.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P7-04–P7-08.
- **Acceptance:** Setiap uji sesuai unit analisis; koreksi uji jamak diterapkan.

### P7-10 — Analisis kasus gagal

- [ ] Pilih query dengan penurunan atau hasil terburuk.
- [ ] Klasifikasikan penyebab: sinonim, bahasa campuran, field kosong, keyword stuffing,
  level/lokasi tidak cocok.
- [ ] Tulis contoh konkret dan implikasinya.
- [ ] Hubungkan dengan keterbatasan TF-IDF.

- **Output:** Analisis kesalahan per query.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P7-04–P7-07.
- **Acceptance:** Setiap kasus memiliki penjelasan dan bukti; tidak ada generalisasi
  berlebihan.

### P7-11 — Manifest dan arsip eksperimen

- [ ] Simpan versi kode, versi pustaka, konfigurasi, seed, hash dataset/query set,
  dan tanggal eksekusi.
- [ ] Simpan run file dan tabel metrik.
- [ ] Pastikan setiap angka dapat ditelusuri ke manifest.
- [ ] Arsipkan artefak di luar repository bila besar.

- **Output:** Manifest eksperimen lengkap.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P7-04–P7-09.
- **Acceptance:** Hasil tanpa manifest tidak dianggap reproducible.

### P7-12 — Isi dashboard evaluasi

- [ ] Masukkan hasil E1–E5 ke dashboard/API admin.
- [ ] Pastikan setiap angka disertai `config_hash` dan `dataset_hash`.
- [ ] Tampilkan hasil per bahasa dan split.
- [ ] Jangan mencampur data simulasi dengan metrik produk.

- **Output:** Dashboard evaluasi terisi.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P6-10, P7-11.
- **Acceptance:** Dashboard hanya dapat diakses admin; angka dapat diaudit.

### P7-13 — Review hasil dengan pembimbing

- [ ] Siapkan ringkasan hasil dan grafik utama.
- [ ] Catat pertanyaan dan masukan pembimbing.
- [ ] Perbaiki analisis atau klaim yang tidak didukung.
- [ ] Perbarui laporan/dokumen terkait.

- **Output:** Catatan review hasil.
- **Estimasi:** 0,5 hari.
- **Dependensi:** P7-09, P7-10.
- **Acceptance:** Klaim utama telah ditinjau; perubahan tercatat.

---

## Deliverable Fase

- [ ] Query set final dan split.
- [ ] Relevance judgment lengkap dan nilai κ.
- [ ] Hasil E1–E5.
- [ ] Tabel uji statistik dan effect size.
- [ ] Analisis kasus gagal.
- [ ] Manifest eksperimen.
- [ ] Dashboard evaluasi terisi.

---

## Gate F7

- [ ] E1–E5 selesai; penundaan 20k dicatat sebagai keterbatasan bila terjadi.
- [ ] Semua hasil memakai koleksi, query set, dan judgment yang sama.
- [ ] κ dilaporkan; adjudikasi terdokumentasi.
- [ ] Uji statistik dan effect size tersedia.
- [ ] Analisis kesalahan tersedia.
- [ ] Manifest lengkap dan hasil dapat direproduksi.
- [ ] Tidak ada klaim yang melebihi bukti.

---

## Risiko Fase

| Risiko | Mitigasi |
|---|---|
| Beban anotasi melebihi waktu | Kurangi query/pool sejak F3; pantau harian |
| Annotator kedua tidak tersedia | Cari sejak F1; jika gagal, catat keterbatasan |
| Test set dipakai untuk tuning | Kunci konfigurasi sebelum test; catat pelanggaran bila terjadi |
| Hasil tidak signifikan | Laporkan apa adanya; itu hasil yang sah |
| E5 20k tidak selesai | Jalankan 1k/5k; catat D8 |
| Data simulasi dianggap nyata | Label `is_simulated`; pisahkan metrik produk |

---

## Traceability

- `docs/research/research-and-evaluation.md` Bagian 6–12.
- `docs/data/dataset-design.md` Bagian 5, 7.
- `docs/delivery/roadmap.md` Tahap 7.
- ADR-0008.
