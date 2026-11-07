# ADR-0003: Indeks Field Berbobot dan Preprocessing Bersama

- **Status:** Diterima
- **Tanggal:** 7 November 2026
- **Pemilik:** Deris Firmansyah
- **Sumber:** Grand Design Bagian 4 Atribut; Bagian 5 Pipeline preprocessing; Bagian 5 Formulasi TF-IDF
- **Menggantikan:** —
- **Digantikan oleh:** —

## Konteks

Lowongan memiliki beberapa field teks dengan kekuatan sinyal berbeda:

- `title` paling menunjukkan niat query;
- `skills` menunjukkan kebutuhan kompetensi;
- `description` dan `qualifications` memberi konteks, tetapi panjang dan bervariasi.

Jika semua field digabung tanpa bobot, field panjang dapat mendominasi atau judul yang
pendek tenggelam. Jika pipeline preprocessing dokumen dan query berbeda, hasil tidak adil
dan sulit direproduksi.

## Keputusan

Gunakan **indeks per field dengan penggabungan skor berbobot**:

- Vektorkan `title`, `skills`, dan `description` secara terpisah.
- Bobot awal: `title = 0,4`, `skills = 0,3`, `description = 0,3`.
- Jumlah bobot = 1.
- Jika field kosong, field tersebut dilewati dan bobot field tersisa dinormalisasi ulang.
- Gunakan **satu modul preprocessing** untuk dokumen dan query.
- Normalisasi L2 per vektor field dan query.
- IDF dihitung dari koleksi dokumen, bukan dari query.
- Bobot field adalah parameter eksperimen (E2/E4), bukan konstanta yang tidak boleh diubah.

## Alternatif yang dipertimbangkan

| Alternatif | Alasan tidak dipilih |
|---|---|
| Satu field gabungan | Sederhana, tetapi judul/skills tidak diberi bobot dan panjang field mendominasi |
| Bobot seragam | Adil secara naif, tetapi mengabaikan sinyal judul yang kuat; dipakai sebagai pembanding E2 |
| Bobot dipelajari | Tidak ada data latih dan menghindari klaim ML yang tidak dapat dibuktikan |
| Indeks terpisah per field tanpa penggabungan | Mirip dengan keputusan ini, tetapi tanpa late fusion skor jadi tidak jelas |
| Preprocessing berbeda untuk query dan dokumen | Menyebabkan ketidakadilan dan hasil tidak dapat direproduksi |

## Konsekuensi

### Positif

- Judul dan skills dapat memberikan sinyal yang lebih kuat.
- Field kosong tidak merusak skor.
- Pipeline yang sama mengurangi risiko mismatch.
- Bobot dapat diuji dan dilaporkan.
- Explainability lebih baik karena term dapat dilacak ke field.

### Negatif / biaya

- Indeks lebih besar: tiga matriks sparse per konfigurasi.
- Implementasi penggabungan skor lebih rumit.
- Bobot 0,4/0,3/0,3 adalah hipotesis; bisa salah dan harus diuji.
- Perlu memastikan normalisasi ulang bobot saat field kosong.

Mitigasi:

- Test TC01–TC03 untuk IDF, cosine, dan normalisasi.
- E2 membandingkan bobot seragam vs title+skills lebih tinggi.
- Catat konfigurasi bobot di manifest eksperimen.

## Tindak lanjut

- Definisikan format konfigurasi bobot field.
- Implementasikan normalisasi ulang bobot untuk field kosong.
- Uji pengaruh field weights di E2.
- Dokumentasikan hasil di laporan, termasuk jika bobot awal tidak unggul.

## Referensi

- Grand Design Bagian 4 (Atribut dan alasan).
- Grand Design Bagian 5 (Pipeline preprocessing; formulasi TF-IDF).
- `02-system-design.md` Bagian 4.
- `research/research-and-evaluation.md` Bagian 6.
