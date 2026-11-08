"""Generator Korpus Lowongan Pekerjaan Sintetis Bahasa Indonesia.

Menghasilkan 250 dokumen lowongan realistis dengan variasi level, tipe kerja,
lokasi kota di Indonesia, istilah bilingual (IT/Software/Data), serta format teks.
Bebas dari PII (Personally Identifiable Information).
"""

import json
import random
from pathlib import Path

# Seed agar reprodusibel
random.seed(42)

TITLES_ID = [
    ("Backend Engineer", "Teknologi Informasi", "Python, FastAPI, PostgreSQL, Docker, Redis", "Pengembangan API dan microservices."),
    ("Frontend Developer", "Teknologi Informasi", "React, TypeScript, Tailwind CSS, REST API", "Membangun tampilan antarmuka web modern dan responsif."),
    ("Fullstack Developer", "Teknologi Informasi", "Node.js, React, MongoDB, Next.js", "Pengembangan end-to-end aplikasi web."),
    ("Data Analyst", "Data & Analitik", "SQL, Python, Tableau, Excel, PowerBI", "Menganalisis tren data bisnis dan membuat dashboard visual."),
    ("Machine Learning Engineer", "Data & Analitik", "PyTorch, Scikit-Learn, MLOps, Python, Docker", "Merancang model AI/ML dan deployment ke produksi."),
    ("DevOps Engineer", "Teknologi Informasi", "Kubernetes, CI/CD, AWS, Terraform, Linux", "Mengelola infrastruktur cloud dan otomatisasi deployment."),
    ("QA Automation Engineer", "Quality Assurance", "Selenium, Cypress, Python, Postman, Jest", "Melakukan automated testing dan penjaminan mutu software."),
    ("Product Manager", "Manajemen Produk", "Agile, Scrum, Jira, Product Roadmap, PRD", "Mengelola lifecycle produk dan berkolaborasi dengan engineer."),
    ("UI/UX Designer", "Desain Kreatif", "Figma, Wireframing, Usability Testing, Prototyping", "Merancang pengalaman pengguna dan antarmuka produk digital."),
    ("Mobile Developer (Flutter)", "Teknologi Informasi", "Flutter, Dart, Bloc, REST API, Git", "Mengembangkan aplikasi mobile cross-platform Android dan iOS."),
    ("Digital Marketing Specialist", "Pemasaran", "SEO, SEM, Google Analytics, Copywriting", "Menjalankan kampanye digital dan optimasi trafik website."),
    ("HR Generalist", "Sumber Daya Manusia", "Recruitment, BPJS, Payroll, Hubungan Industrial", "Menangani proses rekrutmen karyawan dan administrasi personalia."),
]

COMPANIES = [
    "PT Teknologi Nusantara Digital",
    "PT Solusi Inovasi Gemilang",
    "PT Maju Jaya Bersama",
    "PT Siber Kreatif Utama",
    "PT Bintang Cipta Asia",
    "PT Fintek Mandiri Canggih",
    "PT Media Digital Pratama",
    "PT Nusantara Cloud Services",
]

LOCATIONS = ["Jakarta Selatan", "Bandung", "Surabaya", "Yogyakarta", "Semarang", "Remote"]
EXPERIENCE_LEVELS = ["Entry Level / Fresh Graduate", "Junior (1-2 tahun)", "Mid-Level (3-4 tahun)", "Senior (5+ tahun)"]
EMPLOYMENT_TYPES = ["Full-time", "Contract", "Internship", "Part-time"]

def generate_synthetic_corpus(output_path: Path, count: int = 250):
    corpus = []
    
    for i in range(1, count + 1):
        job_def = random.choice(TITLES_ID)
        title, category, skills, core_task = job_def
        company = random.choice(COMPANIES)
        loc = random.choice(LOCATIONS)
        exp = random.choice(EXPERIENCE_LEVELS)
        emp_type = random.choice(EMPLOYMENT_TYPES)
        
        # Variasi gaya teks dan kualifikasi
        desc = (
            f"{company} sedang membuka kesempatan berkarier sebagai {title}. "
            f"Tanggung jawab utama: {core_task} Kandidat diharapkan memiliki etos kerja yang tinggi, "
            f"mampu bekerja dalam tim Scrum/Agile, dan memiliki keahlian teknis terkait: {skills}. "
            f"Kandidat ideal memiliki pengalaman setingkat {exp} dan siap ditempatkan di {loc} ({emp_type})."
        )
        
        doc = {
            "id": f"syn-id-{i:04d}",
            "title": title,
            "company": company,
            "job_category": category,
            "location": loc,
            "experience_level": exp,
            "employment_type": emp_type,
            "skills": skills,
            "description": desc,
            "language": "id" if random.random() > 0.3 else "mixed",
            "is_simulated": True,
            "is_active": True,
            "source": "KarirMatch-Synthetic-v1"
        }
        corpus.append(doc)
        
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
        
    print(f"Berhasil menghasilkan {len(corpus)} dokumen lowongan sintetis ke {output_path}")

if __name__ == "__main__":
    out_file = Path("data/raw/synthetic_jobs_id.json")
    generate_synthetic_corpus(out_file, count=250)
