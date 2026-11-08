"""Unit test untuk pipeline pembersihan, penghapusan PII, dan deduplikasi."""

from research.clean_corpus import clean_text, compute_dedup_hash

def test_clean_text_removes_html():
    raw = "<p>Lowongan Kerja <b>Software Engineer</b></p>"
    assert clean_text(raw) == "Lowongan Kerja Software Engineer"

def test_clean_text_removes_urls():
    raw = "Lamar di https://careers.example.com/apply sekarang!"
    assert clean_text(raw) == "Lamar di sekarang!"

def test_clean_text_strips_pii_email_and_phone():
    raw = "Hubungi HRD kami di hrd@company.com atau wa +6281234567890 untuk info."
    cleaned = clean_text(raw)
    assert "hrd@company.com" not in cleaned
    assert "+6281234567890" not in cleaned

def test_compute_dedup_hash_identical():
    h1 = compute_dedup_hash("Backend Dev", "PT Tech", "Membangun API")
    h2 = compute_dedup_hash("backend dev  ", "PT Tech", "  Membangun API ")
    assert h1 == h2
