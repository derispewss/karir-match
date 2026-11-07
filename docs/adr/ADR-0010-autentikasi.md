# ADR-0010: Autentikasi dan Manajemen Sesi

- **Status:** Diterima sebagian — mekanisme transport (cookie vs token) tertunda
- **Tanggal:** 7 November 2026
- **Pemilik:** Deris Firmansyah
- **Sumber:** Grand Design Bagian 7 (Autentikasi; Kebutuhan non-fungsional Security/Privacy)
- **Menggantikan:** —
- **Digantikan oleh:** —

## Konteks

KarirMatch menyimpan preferensi, bookmark, riwayat pencarian, dan event interaksi. Data
tersebut perlu dilindungi, tetapi sistem adalah prototipe dengan satu pelaksana dan tidak
memiliki tim keamanan.

Grand Design membuka pilihan **session cookie atau token**. Mekanisme final belum
diputuskan. Yang tidak boleh ditawar: kata sandi di-hash, kueri berparameter, dan akses
admin dibatasi.

## Keputusan

Prinsip yang diterima:

- Kata sandi di-hash dengan **bcrypt atau argon2**; tidak menulis algoritma hash sendiri.
- Tidak menyimpan kata sandi mentah di database, log, atau respons.
- Login dibatasi (rate limit) dan pesan error tidak membocorkan apakah email terdaftar.
- Otorisasi kepemilikan data diperiksa di server, bukan hanya di UI.
- Endpoint admin/evaluasi memerlukan role `admin`; pengguna biasa mendapat `403`.
- Sesi/token memiliki masa berlaku dan dapat diakhiri lewat logout.
- Jika memakai cookie: `HttpOnly`, `Secure` di deployment HTTPS, dan `SameSite` yang
  sesuai.
- Jika memakai bearer token: token tidak disimpan di log; pertimbangkan hash token di
  server jika memakai server-side session.
- Rahasia (secret key, kredensial database) di environment variable, bukan repository.
- Tidak memakai autentikasi pihak ketiga/OAuth pada MVP.

Mekanisme transport final (cookie vs token) dipilih saat implementasi dan dicatat sebagai
keputusan lanjutan.

## Alternatif yang dipertimbangkan

| Alternatif | Penilaian |
|---|---|
| Session cookie | Sederhana untuk web; perlu proteksi CSRF dan SameSite |
| Bearer token | Cocok untuk API/klien lain; perlu penyimpanan token yang aman |
| OAuth pihak ketiga | Di luar ruang lingkup dan menambah dependensi |
| HTTP Basic | Tidak memadai untuk aplikasi web |
| Menyimpan kata sandi dengan SHA/MD5 | Tidak aman; ditolak |

## Konsekuensi

### Positif

- Baseline keamanan yang jelas.
- Tidak ada algoritma kriptografi buatan sendiri.
- Otorisasi data dan admin eksplisit.
- Dapat memilih cookie/token sesuai kebutuhan frontend.

### Negatif / biaya

- Dua opsi transport menunda finalisasi kontrak.
- Cookie memerlukan perhatian CSRF; token memerlukan perhatian penyimpanan di klien.
- Rate limit dan logout perlu implementasi serta pengujian.
- Belum ada kebijakan rotasi sesi/refresh token.

## Tindak lanjut

- Pilih cookie atau token sebelum implementasi auth.
- Tentukan masa berlaku sesi/token.
- Implementasikan rate limit login.
- Tambahkan test akses admin (TC12) dan akses data pengguna lain.
- Catat keputusan transport di ADR baru atau pembaruan ADR ini.

## Referensi

- Grand Design Bagian 7 (Autentikasi; Security; Privacy).
- `02-system-design.md` Bagian 12.
- `03-api-spec.md` Bagian 2.2.
- `data/database-design.md` Bagian 3.1.
