# ADR-0010: Autentikasi dan Manajemen Sesi

- **Status:** Diterima — bearer token JWT untuk MVP
- **Tanggal:** 7 November 2026 (diperbarui 8 November 2026)
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

## Keputusan Transport (D3)

Mekanisme yang dipilih untuk MVP adalah **bearer token JWT**:

- Token diterbitkan oleh `POST /auth/login` dan `POST /auth/register`.
- Payload token berisi `sub` (ID pengguna) dan `exp`; masa berlaku 30 menit.
- Algoritma `HS256`; `SECRET_KEY` dibaca dari environment variable.
- Frontend menyimpan token di `localStorage` dengan kunci `karirmatch_token` dan
  mengirimnya melalui header `Authorization: Bearer <token>`.
- Logout bersifat client-side: token dihapus dari penyimpanan klien. Server tidak
  menyimpan daftar token yang dicabut pada MVP ini.
- Endpoint yang membutuhkan login memvalidasi tanda tangan dan masa berlaku token.
- Rate limit login 5 percobaan per menit per IP dengan pesan error generik.

Catatan keamanan: `localStorage` rentan terhadap XSS. Untuk MVP, risiko dikurangi dengan
CSP dasar, tidak menampilkan HTML mentah dari input pengguna, dan tidak menyimpan data
sensitif di token. Jika aplikasi naik ke produksi, pertimbangkan cookie `HttpOnly` +
CSRF atau rotasi/refresh token dengan pencabutan server-side.

### Konsekuensi transport

- API dapat dipakai klien non-browser tanpa perubahan kontrak.
- Tidak ada state sesi di server; logout tidak mencabut token yang sudah diterbitkan.
- Masa berlaku pendek (30 menit) membatasi dampak token yang bocor.
- Perlu audit XSS dan CSP sebelum deployment publik.

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

- [x] Pilih cookie atau token sebelum implementasi auth — bearer token JWT.
- [x] Tentukan masa berlaku sesi/token — 30 menit.
- [x] Implementasikan rate limit login.
- [x] Tambahkan test akses admin (TC12) dan akses data pengguna lain.
- [x] Catat keputusan transport di ADR baru atau pembaruan ADR ini.
- [ ] Audit XSS/CSP dan pertimbangkan cookie `HttpOnly` sebelum deployment publik.

## Referensi

- Grand Design Bagian 7 (Autentikasi; Security; Privacy).
- `02-system-design.md` Bagian 12.
- `03-api-spec.md` Bagian 2.2.
- `data/database-design.md` Bagian 3.1.
