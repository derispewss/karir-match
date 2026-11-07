# ADR-0002: TF-IDF + Cosine Similarity sebagai Inti Retrieval

- **Status:** Diterima
- **Tanggal:** 7 November 2026
- **Pemilik:** Deris Firmansyah
- **Sumber:** Grand Design Bagian 3 Fokus Penelitian; Bagian 5 Metode
- **Menggantikan:** —
- **Digantikan oleh:** —

## Konteks

Fitur utama KarirMatch adalah pencarian lowongan. Sistem harus:

- berjalan tanpa data latih;
- dapat dijelaskan kepada pengguna dan pembimbing;
- cukup cepat pada koleksi ribuan dokumen;
- mudah di-ablation untuk riset;
- tidak mengklaim kemampuan semantik yang tidak dimiliki.

Baseline yang adil adalah keyword matching sederhana. TF-IDF + Cosine Similarity
menimbang term berdasarkan kepentingannya dan mengukur kemiripan vektor, tetapi tidak
menangkap sinonim, semantik, atau urutan kata.

## Keputusan

Gunakan **TF-IDF + Cosine Similarity** sebagai mesin retrieval utama:

- TF-IDF dengan `sublinear_tf=True`, `smooth_idf=True`, dan normalisasi L2.
- Vektor query memakai IDF dari koleksi dokumen, bukan dihitung ulang dari query.
- Cosine Similarity untuk skor.
- **Baseline:** keyword matching sederhana (skor = proporsi term query yang muncul).
- **Opsional:** BM25 sebagai pembanding tambahan, jika waktu dan data memungkinkan.
- **Bukan inti:** embedding transformer, LLM, atau model semantik lain. Paling jauh
  menjadi pengembangan masa depan atau baseline pembanding.

## Alternatif yang dipertimbangkan

| Alternatif | Alasan tidak dipilih sebagai inti |
|---|---|
| Keyword matching saja | Tidak membobot term; menjadi baseline, bukan solusi |
| BM25 | Baseline kuat, tetapi keputusan Grand Design memakai TF-IDF + cosine; BM25 dipertahankan sebagai pembanding opsional |
| Embedding transformer | Butuh model/data tambahan, kurang transparan, dan di luar ruang lingkup awal |
| LLM untuk ranking | Tidak dapat diandalkan untuk reproduksibilitas, biaya, dan explainability; bukan inti |
| Hybrid TF-IDF + embedding | Menambah kompleksitas dan variabel yang belum diuji; dapat menjadi pengembangan lanjutan |

## Konsekuensi

### Positif

- Tidak membutuhkan data latih.
- Mudah dijelaskan: term, bobot IDF, dan cosine.
- Cepat untuk koleksi ribuan dokumen.
- Mudah di-ablation: stopword, stemming, bobot field, n-gram.
- Hasil dapat direproduksi dengan konfigurasi dan versi yang dicatat.

### Negatif / biaya

- Tidak menangkap sinonim dan semantik.
- Tidak memperhatikan urutan kata.
- Sangat bergantung pada kualitas preprocessing dan normalisasi istilah.
- Kualitas ranking harus dibuktikan lewat eksperimen, bukan diasumsikan.

Mitigasi:

- Kamus normalisasi singkatan dan variasi istilah.
- Bigram sebagai variabel eksperimen.
- Analisis kasus gagal per query.
- Klaim dibatasi pada koleksi dan query set yang diuji.
- Embedding/LLM sebagai pengembangan masa depan, bukan klaim saat ini.

## Tindak lanjut

- Implementasikan baseline keyword dan TF-IDF + cosine dalam satu protokol evaluasi.
- Jalankan E1 dan E2.
- Uji TC01–TC04 (IDF, ranking, normalisasi, determinisme).
- Putuskan apakah BM25 ikut sebagai pembanding.
- Catat versi scikit-learn/SciPy dan parameter vektorisasi.

## Referensi

- Grand Design Bagian 3 (Fokus penelitian, literatur, kebaruan).
- Grand Design Bagian 5 (Metode, formulasi TF-IDF).
- `02-system-design.md` Bagian 4.
- `research/research-and-evaluation.md` Bagian 5–7.
