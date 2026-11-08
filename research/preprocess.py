"""Pre‑processing pipeline for KarirMatch documents & queries.

All steps are controlled by config/preprocess.yaml.
"""
import re
import json
import yaml
from pathlib import Path
from typing import List, Dict, Tuple

def load_config() -> dict:
    with open("config/preprocess.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def read_stopwords(path: Path) -> set:
    if not path.exists():
        return set()
    return {line.strip().lower() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}

def load_stopword_lists(cfg: dict) -> Dict[str, set]:
    base = Path(".")
    return {
        "id": read_stopwords(base / cfg["stopwords"]["id"]),
        "en": read_stopwords(base / cfg["stopwords"]["en"]),
        "domain": read_stopwords(base / cfg["stopwords"]["domain"]) if "domain" in cfg["stopwords"] else set(),
    }

def detect_language(text: str) -> str:
    ind_tokens = {"dan", "di", "yang", "dengan", "untuk", "pada", "adalah", "pekerjaan", "kandidat", "posisi"}
    eng_tokens = {"the", "and", "for", "with", "job", "position", "company", "skills", "experience"}
    tokens = set(text.lower().split())
    ind = len(tokens & ind_tokens)
    eng = len(tokens & eng_tokens)
    if ind > eng:
        return "id"
    if eng > ind:
        return "en"
    return "mixed"

def case_folding(text: str) -> str:
    return text.lower()

def strip_html_and_urls(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    return text

def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

TOKEN_PATTERN = re.compile(r"\b[\w\.+/-]+\b", re.UNICODE)

def tokenize(text: str) -> List[str]:
    return TOKEN_PATTERN.findall(text)

def normalize_abbreviations(tokens: List[str], abbr_dict: dict) -> List[str]:
    result = []
    for tok in tokens:
        lower = tok.lower()
        if lower in abbr_dict:
            result.extend(abbr_dict[lower].split())
        else:
            result.append(tok)
    return result

def preprocess_text(text: str, cfg: dict, stoplists: dict, abbr: dict, lang: str = "id") -> str:
    if not text:
        return ""
    pipeline = cfg["pipeline"]
    if pipeline.get("case_folding", True):
        text = case_folding(text)
    if pipeline.get("html_url_removal", True):
        text = strip_html_and_urls(text)
    if pipeline.get("whitespace_normalization", True):
        text = normalize_whitespace(text)
    if pipeline.get("tokenization", True):
        tokens = tokenize(text)
    else:
        tokens = text.split()
    if pipeline.get("abbreviation_normalization", True):
        tokens = normalize_abbreviations(tokens, abbr)
    if pipeline.get("stopword_removal", True):
        sw = stoplists.get(lang, set()) | stoplists.get("domain", set())
        tokens = [t for t in tokens if t not in sw]
    return " ".join(tokens)

def preprocess_corpus(input_path: Path, output_path: Path) -> None:
    cfg = load_config()
    stoplists = load_stopword_lists(cfg)
    abbr = cfg.get("abbreviations", {})

    with open(input_path, "r", encoding="utf-8") as f:
        docs = json.load(f)

    cleaned = []
    for doc in docs:
        lang = doc.get("language", "id")
        cleaned_doc = dict(doc)
        for field in ("title", "skills", "description"):
            if field in doc:
                cleaned_doc[field] = preprocess_text(doc[field], cfg, stoplists, abbr, lang=lang)
        cleaned.append(cleaned_doc)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    print(f"Preprocessed {len(cleaned)} documents -> {output_path}")

def preprocess_queries(query_path: Path, output_path: Path) -> None:
    cfg = load_config()
    stoplists = load_stopword_lists(cfg)
    abbr = cfg.get("abbreviations", {})

    with open(query_path, "r", encoding="utf-8") as f:
        queries = json.load(f)

    cleaned = []
    for q in queries:
        lang = q.get("language", "id")
        cleaned_q = dict(q)
        cleaned_q["query"] = preprocess_text(q["query"], cfg, stoplists, abbr, lang=lang)
        cleaned.append(cleaned_q)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    print(f"Preprocessed {len(cleaned)} queries -> {output_path}")

if __name__ == "__main__":
    preprocess_corpus(Path("data/processed/corpus_id_v1.json"), Path("data/processed/corpus_id_v1.json"))
    preprocess_queries(Path("research/query_set_v1.json"), Path("research/queries_clean.json"))
