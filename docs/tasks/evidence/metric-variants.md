# Metric Variant Documentation – Phase 3

Dokumen ini mencatat pilihan varian metrik yang akan dipakai dalam evaluasi **KarirMatch**.

## 1. Gain untuk DCG / nDCG
- **Linear gain** – nilai relevansi (grade) digunakan secara linear (0, 1, 2).
- **Eksponensial gain** – `gain = 2^grade - 1` (sering dipakai pada TREC). 

**Keputusan:** Untuk semua eksperimen pada fase ini kami menggunakan **linear gain** karena grade hanya memiliki tiga nilai dan interpretasi linier lebih mudah dipahami.

## 2. Penanganan kueri tanpa dokumen relevan
- Jika tidak ada dokumen relevan dalam qrels, **nDCG = 0** dan **MAP = 0**. 
- Recall di‑definisikan sebagai 0 karena denominator (`|rel|`) = 0; hal ini di‑catat dalam laporan sehingga tidak menimbulkan pembagian oleh nol.

## 3. Normalisasi skor
- Semua skor (Precision, MAP, nDCG) berada pada rentang **[0, 1]**. 
- Tidak ada scaling tambahan; nilai yang dihasilkan langsung dibandingkan.

## 4. K‑fold pooling (tidak dipakai pada fase ini)
- Pooling dilakukan hanya sekali (Top‑15) dari semua sistem (baseline & TF‑IDF) – tidak ada stratifikasi K‑fold.

---

*Dokumen ini disimpan di* `docs/tasks/evidence/metric-variants.md` *dan dirujuk di* `docs/tasks/03-baseline-dan-query-set.md` *pada poin P3‑03.*