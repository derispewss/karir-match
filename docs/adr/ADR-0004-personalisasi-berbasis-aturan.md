# ADR-0004: Personalisasi Berbasis Aturan

- **Status:** Diterima
- **Tanggal:** 7 November 2026
- **Pemilik:** Deris Firmansyah
- **Sumber:** Grand Design Bagian 5 Pembentukan profil dan skor akhir; Bagian 5 Pencegah dominasi
- **Menggantikan:** —
- **Digantikan oleh:** —

## Konteks

Feed rekomendasi perlu menyarankan lowongan yang mirip dengan yang pernah dibuka,
disimpan, atau dilamar. Data yang tersedia terbatas:

- tidak ada data latih berlabel;
- interaksi pengguna nyata belum ada;
- implicit feedback lemah dan tidak memiliki interaksi negatif eksplisit;
- sistem harus dapat dijelaskan dan di-ablation.

Personalisasi adaptif (online learning, reinforcement learning) tidak dapat dibuktikan
dengan data yang ada dan akan menimbulkan klaim yang berlebihan.

## Keputusan

Gunakan **personalisasi berbasis aturan di ruang vektor**:

- Profil pengguna `p_u` adalah agregat vektor lowongan yang diinteraksikan.
- Bobot sinyal: klik detail = 1, simpan = 3, lamar = 5.
- Peluruhan waktu: `δ(a) = 2^(-a/14)` dengan half-life 14 hari (usulan).
- Profil dinormalisasi L2.
- Satu dokumen dihitung paling banyak sekali per jenis sinyal.
- Interaksi aktif dibatasi, misalnya 50 terbaru.
- Skor akhir:

  ```text
  FinalScore(u,d) = α·QueryScore(u,d) + β·ProfileScore(u,d)
  α + β = 1, α,β ≥ 0
  ProfileScore(u,d) = cos(p_u, v_d)
  ```

- Pengguna tanpa riwayat memakai `β = 0`.
- Opsional: `β` naik bertahap, `β = β_max × min(1, n/n₀)`.
- Sebagian slot Top-N (usulan 20%) dikhususkan untuk hasil non-personalisasi.
- “Tidak tertarik” tidak masuk MVP; mengabaikan hasil tidak identik dengan tidak suka.
- **Bukan** collaborative filtering, matrix factorization, atau reinforcement learning.

## Alternatif yang dipertimbangkan

| Alternatif | Alasan tidak dipilih |
|---|---|
| Collaborative filtering | Butuh banyak pengguna dan interaksi; data belum ada |
| Matrix factorization | Butuh data latih dan sulit dijelaskan |
| Learning-to-rank | Tidak ada label dan menghindari klaim ML adaptif |
| Profil berbasis embedding | Di luar ruang lingkup awal dan kurang transparan |
| Tanpa personalisasi | Tidak memenuhi kebutuhan F2; tetap menjadi fallback `β = 0` |

## Konsekuensi

### Positif

- Dapat dijelaskan: alasan “mirip dengan lowongan yang Anda simpan”.
- Mudah di-ablation: sumber sinyal, bobot, jumlah seed, α, half-life.
- Tidak membutuhkan pelatihan model.
- Cold-start pengguna ditangani dengan `β = 0`.
- Cold-start lowongan ditangani karena vektor lowongan baru langsung tersedia.

### Negatif / biaya

- Sinyal implicit lemah dan berisik.
- Position bias dan feedback loop mungkin terjadi.
- Bobot 1:3:5 adalah hipotesis, bukan hasil empiris.
- Profil dapat terlalu sempit jika interaksi sedikit.
- Evaluasi memakai profil simulasi, bukan pengguna nyata.

Mitigasi:

- 20% slot non-personalisasi.
- Catat posisi tayang.
- Batasi interaksi aktif dan gunakan peluruhan.
- Normalisasi profil dan satu dokumen sekali per sinyal.
- Laporkan hasil per profil dan analisis sensitivitas α.
- Jangan mengklaim perilaku pengguna nyata.

## Tindak lanjut

- Implementasikan pembentukan profil dan `FinalScore`.
- Uji TC07–TC10.
- Jalankan E3 dan E4.
- Putuskan cara `QueryScore` dibentuk pada feed tanpa query (keputusan terbuka).
- Kalibrasi α, β, half-life, dan batas interaksi di validation set.

## Referensi

- Grand Design Bagian 5 (Pembentukan profil dan skor akhir; pencegah dominasi).
- `02-system-design.md` Bagian 5.
- `research/research-and-evaluation.md` Bagian 6.
