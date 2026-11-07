# Konfigurasi Eksperimen

Direktori ini menyimpan konfigurasi eksperimen dalam YAML, misalnya:

- `e2-preprocessing-*.yml` — stopword, stemming, bobot field, n-gram;
- `e3-personalization-*.yml` — nilai `alpha`, `beta`, dan profil;
- `e4-ablation-*.yml` — ablation sinyal dan jumlah seed.

Aturan:

- Setiap konfigurasi memiliki nama dan hash yang dicatat di manifest.
- Jangan mengubah konfigurasi yang sudah dipakai untuk test set; buat versi baru.
- Rahasia dan path lokal tidak boleh masuk ke konfigurasi yang di-commit.
