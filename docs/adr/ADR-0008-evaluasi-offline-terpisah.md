# ADR-0008: Evaluasi Offline dan Data Evaluasi Terpisah

- **Status:** Diterima
- **Tanggal:** 7 November 2026
- **Pemilik:** Deris Firmansyah
- **Sumber:** Grand Design Bagian 4 Label/target; Bagian 6 Rancangan eksperimen dan evaluasi
- **Menggantikan:** —
- **Digantikan oleh:** —

## Konteks

Sistem perlu diukur kualitasnya, tetapi:

- belum ada pengguna nyata dan log produksi;
- klik bukan ground truth relevansi;
- interaksi simulasi tidak boleh dianggap perilaku nyata;
- data pengguna harus dilindungi;
- hasil harus dapat direproduksi dan dipertanggungjawabkan.

Online A/B testing tidak realistis untuk prototipe riset dengan satu pelaksana dan
pengguna terbatas.

## Keputusan

Gunakan **evaluasi offline** dengan protokol tetap:

- Relevance judgment manusia dengan skala 0–2:
  - 0 tidak relevan;
  - 1 cukup relevan;
  - 2 sangat relevan.
- Minimal 2 annotator; 25% (usulan) dinilai ganda untuk Cohen’s κ.
- Pooling Top-15 dari semua sistem; anotasi buta.
- Query set 40–60; split validation/test; test dilaporkan sekali.
- Metrik: P@K, R@K, F1@K, MAP, NDCG@K; K = 10 utama, K = 5 dan 20 pelengkap.
- Uji statistik: Wilcoxon signed-rank, Friedman + post-hoc Holm, bootstrap CI,
  Cohen’s κ; α = 0,05 (usulan).
- Data evaluasi disimpan di tabel terpisah (`eval_queries`, `relevance_judgments`) tanpa
  FK ke `users`.
- Interaksi simulasi diberi `is_simulated = true` dan tidak dihitung sebagai metrik produk.
- Jangan membuat klik sintetis dan menyajikannya sebagai perilaku pengguna.
- Hasil dilaporkan dengan konfigurasi, hash dataset, seed, versi kode/pustaka.

## Alternatif yang dipertimbangkan

| Alternatif | Alasan tidak dipilih |
|---|---|
| Online A/B testing | Tidak ada pengguna nyata dalam jumlah memadai; waktu terbatas |
| Klik sebagai ground truth | Klik dipengaruhi posisi, judul, dan bias; bukan relevansi |
| Satu annotator | Tidak dapat mengukur kesepakatan; risiko bias tinggi |
| Judgment oleh LLM | Tidak menjadi inti; dapat dipertimbangkan sebagai alat bantu, tetapi tidak menggantikan manusia pada protokol ini |
| Data evaluasi dicampur tabel produk | Risiko privasi dan kontaminasi metrik |

## Konsekuensi

### Positif

- Kualitas diukur dengan ground truth manusia.
- Protokol dapat direproduksi.
- Data pengguna dan data evaluasi terpisah.
- Hasil dapat dilaporkan jujur, termasuk yang tidak signifikan.
- Metrik produk tidak dicampur dengan simulasi.

### Negatif / biaya

- Anotasi memakan waktu dan tenaga.
- Ground truth terbatas pada query/pool yang dibuat.
- Generalisasi terbatas.
- Perlu annotator kedua.
- Evaluasi offline tidak mengukur kepuasan pengguna nyata.

Mitigasi:

- Pedoman anotasi dan pilot 5 query.
- Kurangi jumlah query/pool jika beban terlalu berat, dan catat sebagai keterbatasan.
- Laporkan effect size dan CI.
- Gunakan usability test terpisah untuk pengalaman pengguna.

## Tindak lanjut

- Tulis pedoman anotasi.
- Rekrut annotator kedua.
- Buat query set dan split.
- Siapkan skrip evaluasi dan manifest.
- Pastikan endpoint admin hanya membaca data evaluasi.

## Referensi

- Grand Design Bagian 4 (Label/target).
- Grand Design Bagian 6 (Rancangan eksperimen dan evaluasi; relevance judgment).
- `research/research-and-evaluation.md` Bagian 6–10.
- `data/dataset-design.md` Bagian 5.
- `data/database-design.md` Bagian 4.
