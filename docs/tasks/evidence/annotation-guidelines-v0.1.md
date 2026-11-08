# Pedoman Anotasi Relevansi — KarirMatch v0.1

Dokumen ini menjadi acuan penilaian relevansi (*relevance judgment*) antara kueri pencarian dan dokumen lowongan kerja.

---

## 1. Skala Relevansi

| Grade | Kategori | Definisi Operasional | Contoh Kasus |
|:---:|---|---|---|
| **0** | **Tidak Relevan** | Dokumen tidak sesuai dengan topik utama kueri, peran pekerjaan berbeda, atau bidang sama sekali tidak cocok. | Query: *"Backend Python"* <br>Dokumen: *"Digital Marketing Specialist"* |
| **1** | **Cukup Relevan** | Dokumen berada pada rumpun yang sesuai, namun teknologi pendukung atau level pengalaman yang diminta kueri kurang spesifik/parsial. | Query: *"Backend Python FastAPI"* <br>Dokumen: *"Fullstack Node.js / Python Flask"* |
| **2** | **Sangat Relevan** | Posisi pekerjaan dan seluruh keahlian/teknologi inti yang diminta kueri tercantum secara eksplisit pada lowongan. | Query: *"Backend Python FastAPI"* <br>Dokumen: *"Backend Engineer (Python, FastAPI, Redis, Postgres)"* |

---

## 2. Prinsip Penting Bagi Penilai (Annotator)
1. **Blind Evaluation:** Penilai tidak diberitahu sistem mana yang menghasilkan dokumen (apakah *baseline keyword* atau *TF-IDF*).
2. **Tidak Melihat Profil Pengguna:** Penilaian murni berbasis kesesuaian teks kueri dan teks lowongan, tidak dipengaruhi riwayat atau preferensi personal penilai.
3. **Penanganan Kasus Batas (Edge Cases):**
   - Jika judul pekerjaan cocok tetapi teknologi wajib tidak disebutkan sama sekali $\rightarrow$ berikan Grade **1**.
   - Jika sinonim formal digunakan (misal kueri: *"Software Engineer"*, lowongan: *"Programmer"* dengan tech stack yang cocok) $\rightarrow$ berikan Grade **2**.
