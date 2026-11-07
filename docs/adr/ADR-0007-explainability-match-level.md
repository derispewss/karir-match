# ADR-0007: Tingkat Kecocokan Relatif, Bukan Skor Mentah

- **Status:** Diterima
- **Tanggal:** 7 November 2026
- **Pemilik:** Deris Firmansyah
- **Sumber:** Grand Design Bagian 2 Menampilkan skor tanpa menyesatkan; F3
- **Menggantikan:** —
- **Digantikan oleh:** —

## Konteks

Cosine Similarity menghasilkan skor yang:

- bukan probabilitas;
- tidak sebanding secara absolut antar query;
- dipengaruhi panjang dokumen, jumlah term, dan IDF koleksi.

Menampilkan angka mentah atau persentase dapat membuat pengguna mengira itu peluang
diterima. Namun, pengguna tetap perlu tahu mengapa sebuah lowongan muncul.

## Keputusan

- UI menampilkan **Tinggi / Sedang / Rendah**.
- Batas dihitung **relatif terhadap hasil query itu**, bukan ambang absolut lintas query.
- Tampilkan istilah query yang cocok dan alasan rekomendasi.
- Ikon info menjelaskan: “Tingkat ini menunjukkan kemiripan teks, bukan peluang Anda
  diterima.”
- **Tidak** menampilkan skor mentah atau persentase kepada pengguna biasa.
- Skor mentah hanya tersedia di dashboard peneliti/admin.
- Tidak memakai istilah “AI cerdas”, “probabilitas”, atau “prediksi” untuk aturan
  pembobotan.
- Ambang Tinggi/Sedang/Rendah adalah parameter yang dapat dikonfigurasi dan dikalibrasi;
  nilai awalnya adalah keputusan terbuka.

## Alternatif yang dipertimbangkan

| Alternatif | Alasan tidak dipilih |
|---|---|
| Menampilkan skor 0–1 | Disalahartikan sebagai probabilitas atau kualitas absolut |
| Persentase kecocokan | Lebih menyesatkan karena tampak seperti peluang |
| Bintang 1–5 | Tidak menjelaskan dasar penilaian dan tetap terasa absolut |
| Tanpa penjelasan | Tidak memenuhi prinsip “dapat dijelaskan” |
| Penjelasan model ML | Tidak relevan; sistem bukan ML adaptif |

## Konsekuensi

### Positif

- Mengurangi misinterpretasi skor sebagai peluang diterima.
- Alasan dapat dilacak ke term/interaksi.
- Konsisten dengan prinsip transparansi dan tidak berlebihan klaim.
- Pengguna tetap mendapat sinyal yang berguna.

### Negatif / biaya

- Ambang relatif perlu dikalibrasi dan diuji.
- Label relatif dapat berubah antar query; pengguna mungkin membandingkan antar query.
- Penjelasan berbasis TF-IDF terbatas pada term yang benar-benar cocok.
- Dashboard admin perlu memisahkan skor mentah dari UI publik.

Mitigasi:

- Kalibrasi ambang pada data uji.
- Usability test untuk memastikan label dipahami.
- Teks bantuan yang jelas.
- Audit agar skor mentah tidak bocor ke endpoint publik.

## Tindak lanjut

- Tentukan metode kalibrasi ambang (misalnya kuantil distribusi skor per query).
- Uji FR-EXP-01/02.
- Pastikan endpoint publik tidak mengembalikan skor mentah.
- Catat versi ambang di konfigurasi.

## Referensi

- Grand Design Bagian 2 (Menampilkan skor tanpa menyesatkan).
- `01-prd.md` Bagian 8.2.
- `03-api-spec.md` Bagian 5.
