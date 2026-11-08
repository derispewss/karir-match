# Finalisasi RQ, Hipotesis, dan Rencana Statistik — KarirMatch

Dokumen ini memfinalisasi definisi operasional dari Research Questions (RQ1–RQ5), hipotesis kerja yang dapat diuji (falsifiable), metrik, serta uji statistik yang akan diterapkan pada Fase 7.

---

## 1. Matriks RQ, Hipotesis, dan Uji Statistik

| ID | Research Question (RQ) | Hipotesis Kerja ($H_1$) | Metrik Evaluasi | Eksperimen Terkait | Uji Statistik & Ambang Batas |
|---|---|---|---|---|---|
| **RQ1** | Seberapa baik ranking TF-IDF + Cosine dibanding baseline keyword matching? | Ranking TF-IDF + Cosine menghasilkan nilai P@10, MAP, dan nDCG@10 yang secara statistik signifikan lebih tinggi dibandingkan baseline Boolean/keyword matching. | P@5, P@10, MAP, nDCG@10, MRR | E1 (TF-IDF vs Keyword Baseline) | Paired t-test (jika data terdistribusi normal) atau Wilcoxon signed-rank test; $\alpha = 0.05$; Effect size (Cohen's $d$). |
| **RQ2** | Bagaimana variasi preprocessing (stopword, stemming, normalisasi, bobot field, n-gram) memengaruhi kualitas retrieval? | Penerapan field weighting dan normalisasi kata/istilah meningkatkan nDCG@10 dan MAP secara signifikan, sedangkan stemming agresif pada teks lowongan kerja IT (bilingual) berpotensi menurunkan presisi. | P@10, MAP, nDCG@10, Index build time | E2 (Ablation Preprocessing & Field Weighting) | One-way ANOVA atau Friedman test untuk multi-variasi, dilanjutkan post-hoc Tukey/Nemenyi; $\alpha = 0.05$. |
| **RQ3** | Bagaimana pengaruh personalisasi berbasis profil terhadap kualitas rekomendasi lowongan? | Re-ranking feed menggunakan profil vektor interaksi pengguna menghasilkan relevansi (P@10, nDCG@10) yang lebih tinggi dibandingkan feed acak/kronologis non-personalisasi. | P@5, P@10, nDCG@10, Catalog Coverage, Category Diversity | E3 (Personalisasi vs Non-Personalisasi) | Wilcoxon signed-rank test per profil pengguna simulasi; $\alpha = 0.05$. |
| **RQ4** | Seberapa besar kontribusi komponen profil, dan bagaimana sensitivitas bobot $\alpha$ terhadap kualitas rekomendasi? | Terdapat nilai optimal parameter $\alpha \in [0.4, 0.7]$ yang memaksimalkan nDCG@10 tanpa menyebabkan feedback loop berlebih (category collapse). | nDCG@10, Intra-list diversity, Serendipity | E4 (Sensitivitas Parameter $\alpha$ & Ablation Profil) | Analisis kurva sensitivitas parameter & Repeated Measures ANOVA; $\alpha = 0.05$. |
| **RQ5** | Apakah latensi kueri dan ukuran indeks yang dihasilkan layak untuk skala operasional prototipe? | P95 latency retrieval tetap berada di bawah ambang batas interaktif ($\le 200$ ms) dan ukuran memori indeks $\le 150$ MB untuk korpus $\ge 1.000$ lowongan. | P50 Latency (ms), P95 Latency (ms), Throughput (req/s), Index RAM size (MB) | E5 (Benchmarking Efisiensi & Latensi) | Summary statistics (Mean, P50, P95, P99); evaluasi terhadap SLA sistem. |

---

## 2. Prinsip Kebijakan Klaim (Claim Policy)
1. **Tidak Ada Klaim Superioritas Tanpa Data:** Pernyataan bahwa "TF-IDF lebih baik dari keyword" atau "personalisasi meningkatkan kepuasan" tetap berstatus hipotesis sampai data Fase 7 selesai dihitung.
2. **Pelaporan Terpisah Per Bahasa:** Mengingat korpus lowongan mengandung istilah bilingual (ID/EN), metrik RQ1 dan RQ2 wajib dilaporkan dalam 3 subset: Bahasa Indonesia (`id`), Bahasa Inggris (`en`), dan Campuran (`mixed`).
3. **Unit Analisis:** Unit analisis pada RQ1 dan RQ2 adalah kueri ($N \approx 40\text{--}60$ kueri), sedangkan unit analisis pada RQ3 dan RQ4 adalah profil interaksi pengguna simulasi ($N \approx 20\text{--}30$ profil).
