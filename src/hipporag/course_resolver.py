
import json
import re
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

import numpy as np
from rapidfuzz import fuzz

try:
    from unidecode import unidecode
except Exception:
    unidecode = None

try:
    from transformers import AutoTokenizer, AutoModel
    import torch
except Exception:
    AutoTokenizer = AutoModel = torch = None


# ----------------------------
# Utils
# ----------------------------
_VI_STOPWORDS = {
    "mon", "hoc", "hocphan", "hoc_phan", "chuandaura", "chuan", "dau", "ra",
    "do", "ai", "day", "giang", "vien", "thay", "co", "theo", "cho", "minh", "xin",
    "can", "biet", "trinh", "bay", "hoi", "ve", "cua", "va", "voi", "la", "nhu"
}

def _strip_accents(s: str) -> str:
    if unidecode is None:
        # fallback: naive, keep as-is
        return s
    return unidecode(s)

def normalize_keep(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s

def normalize_canon(s: str) -> str:
    s = s.lower()
    s = _strip_accents(s)
    s = re.sub(r"[\(\)\[\]\{\}\.\,\:\;\!\?\-_/\\]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


# ----------------------------
# Mention extraction (Rule #1)
# ----------------------------
@dataclass
class Mention:
    raw: str
    span: Optional[Tuple[int, int]] = None  # char span in original text if known


class HCMUSCourseMentionExtractor:
    """
    Rule-based mention extractor tuned for HCMUS-like Vietnamese queries.

    Goal: extract course name strings (often VN) reliably, including:
    - patterns: "môn <X>", "học phần <X>", "chuẩn đầu ra của <X>", "CLO môn <X>"
    - multiple courses: separated by "và", ",", ";", "&"
    - keep important suffixes: "thực hành", "đồ án", "1A/1B/2/II", "lab"
    - also capture short abbreviations like "xlsltk", "oop", "ml" if present
    """

    # keyword triggers that often precede a course list
    TRIGGERS = [
        r"chuẩn\s+đầu\s+ra\s+của",
        r"chuan\s+dau\s+ra\s+cua",
        r"(?:c|clo)\s*(?:môn|mon)",
        r"(?:môn|mon)",
        r"(?:học\s+phần|hoc\s+phan)",
        r"(?:học\s+phần|hoc\s+phan)\s*(?:là|la)?",
        r"(?:đề\s+cương|de\s+cuong)\s*(?:môn|mon)?",
        r"(?:tài\s+liệu|tai\s+lieu)\s*(?:môn|mon)?",
        r"(?:do\s+ai\s+dạy|do\s+ai\s+day|ai\s+dạy|ai\s+day)"
    ]

    SPLIT_RE = re.compile(r"\s*(?:,|;|&| và | va |\/|\+|\||\n)\s*", re.IGNORECASE)

    ABBR_RE = re.compile(r"\b[a-z]{2,10}\b", re.IGNORECASE)

    def __init__(self, abbreviations: Optional[Dict[str, str]] = None):
        self.abbreviations = {normalize_canon(k): v for k, v in (abbreviations or {}).items()}

    def extract(self, query: str) -> List[Mention]:
        q_keep = normalize_keep(query)
        q_canon = normalize_canon(query)

        mentions: List[Mention] = []

        # 1) Trigger-based extraction: grab substring after trigger, stop at punctuation end
        # We'll work on canon text for robust matching, but slice in keep-text approximately.
        for trig in self.TRIGGERS:
            m = re.search(trig, q_canon, flags=re.IGNORECASE)
            if not m:
                continue
            # Take text after trigger
            after = q_keep[m.end():] if m.end() < len(q_keep) else ""
            after = after.strip()
            if not after:
                continue
            # Stop at common sentence boundary
            after = re.split(r"[\.!\?]\s*", after)[0].strip()
            # If the trigger was "do ai day", course name often precedes it instead.
            if re.search(r"do\s+ai\s+(?:day|dạy)", trig, re.IGNORECASE):
                continue
            # Split into candidates
            parts = [p.strip() for p in self.SPLIT_RE.split(after) if p.strip()]
            for p in parts:
                # Avoid capturing teacher names etc by stripping leading stopwords
                mentions.append(Mention(raw=p))

        # 2) If query contains explicit "môn X" patterns multiple times, capture each X
        for mm in re.finditer(r"(?:môn|mon)\s+([^\.\!\?\n]+)", q_canon, flags=re.IGNORECASE):
            seg = q_keep[mm.end(0):]
            seg = re.split(r"[\.!\?]\s*", seg)[0].strip()
            parts = [p.strip() for p in self.SPLIT_RE.split(seg) if p.strip()]
            for p in parts:
                mentions.append(Mention(raw=p))

        # 3) Abbreviation capture (only if present in abbreviation dict)
        for token in self.ABBR_RE.findall(q_canon):
            t = normalize_canon(token)
            if t in self.abbreviations:
                mentions.append(Mention(raw=self.abbreviations[t]))

        # 4) Cleanup / dedup
        cleaned = []
        seen = set()
        for ment in mentions:
            raw = ment.raw.strip()
            if not raw:
                continue
            # remove leading filler words
            raw_c = normalize_canon(raw)
            raw_tokens = [t for t in raw_c.split() if t not in _VI_STOPWORDS]
            raw2 = " ".join(raw_tokens).strip()
            if not raw2:
                continue
            # revert to original-ish by using tokens from keep
            final = raw if len(raw) <= 120 else raw[:120]
            key = normalize_canon(final)
            if key in seen:
                continue
            seen.add(key)
            cleaned.append(Mention(raw=final))
        return cleaned


# ----------------------------
# E5 embedder (default)
# ----------------------------
class MultilingualE5Embedder:
    """
    Uses intfloat/multilingual-e5-large by default.
    Embedding is mean pooled last hidden state and L2 normalized.

    For E5, it's recommended to prefix inputs:
      query: "query: ..."
      passage: "passage: ..."
    """
    def __init__(self, model_name: str = "intfloat/multilingual-e5-large", device: Optional[str] = None):
        if AutoTokenizer is None or AutoModel is None or torch is None:
            raise ImportError("transformers/torch not available. Please install them to use MultilingualE5Embedder.")
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.model.to(self.device)

    @staticmethod
    def _mean_pooling(last_hidden_state, attention_mask):
        mask = attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float()
        summed = (last_hidden_state * mask).sum(1)
        counts = mask.sum(1).clamp(min=1e-9)
        return summed / counts

    def encode(self, texts: List[str], prefix: str = "passage: ", batch_size: int = 32) -> np.ndarray:
        vecs = []
        with torch.no_grad():
            for i in range(0, len(texts), batch_size):
                batch = [prefix + t for t in texts[i:i+batch_size]]
                tok = self.tokenizer(batch, padding=True, truncation=True, return_tensors="pt")
                tok = {k: v.to(self.device) for k, v in tok.items()}
                out = self.model(**tok)
                emb = self._mean_pooling(out.last_hidden_state, tok["attention_mask"])
                emb = torch.nn.functional.normalize(emb, p=2, dim=1)
                vecs.append(emb.cpu().numpy())
        return np.vstack(vecs) if vecs else np.zeros((0, 1024), dtype=np.float32)

    def encode_query(self, query: str) -> np.ndarray:
        return self.encode([query], prefix="query: ", batch_size=1)[0]


# ----------------------------
# Catalog resolver (Rule #2 + logging)
# ----------------------------
@dataclass
class Candidate:
    ma_mon_hoc: str
    tieng_viet: str
    tieng_anh: str
    score: float


@dataclass
class ResolvedCourse:
    ma_mon_hoc: str
    tieng_viet: str
    tieng_anh: str
    score: float
    status: str  # CONFIDENT | AMBIGUOUS


class CourseResolver:
    def __init__(
        self,
        catalog_path: str,
        embed_model_name: str = "intfloat/multilingual-e5-large",
        threshold: float = 0.80,
        margin: float = 0.02,
        top_k_debug: int = 5,
        enable_debug_log: bool = True,
        abbreviations: Optional[Dict[str, str]] = None,
    ):
        self.catalog_path = str(catalog_path)
        self.threshold = float(threshold)
        self.margin = float(margin)
        self.top_k_debug = int(top_k_debug)
        self.enable_debug_log = bool(enable_debug_log)

        self.extractor = HCMUSCourseMentionExtractor(abbreviations=abbreviations or {})

        with open(self.catalog_path, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

        self.names_vi = [c["tieng_viet"] for c in self.catalog]
        self.names_vi_no = [normalize_canon(c["tieng_viet"]) for c in self.catalog]

        self.embedder = MultilingualE5Embedder(model_name=embed_model_name)

        # Precompute catalog embeddings using "passage:" prefix
        self.catalog_emb = self.embedder.encode(self.names_vi, prefix="passage: ", batch_size=64)
        self.catalog_emb_no = self.embedder.encode(self.names_vi_no, prefix="passage: ", batch_size=64)

    def _score_candidates(self, mention: str) -> List[Candidate]:
        q1 = normalize_keep(mention)
        q2 = normalize_canon(mention)

        q_emb = self.embedder.encode([q1], prefix="query: ", batch_size=1)[0]
        q_emb_no = self.embedder.encode([q2], prefix="query: ", batch_size=1)[0]

        sim = self.catalog_emb @ q_emb
        sim_no = self.catalog_emb_no @ q_emb_no

        # fuzzy compares against canonicalized text
        fuzzy_scores = np.array([fuzz.token_sort_ratio(q2, name_no) / 100.0 for name_no in self.names_vi_no], dtype=np.float32)

        final = np.maximum.reduce([sim, sim_no, fuzzy_scores])
        idxs = np.argsort(-final)

        cands: List[Candidate] = []
        for i in idxs[: max(self.top_k_debug, 10)]:
            rec = self.catalog[i]
            cands.append(Candidate(
                ma_mon_hoc=rec["ma_mon_hoc"],
                tieng_viet=rec["tieng_viet"],
                tieng_anh=rec["tieng_anh"],
                score=float(final[i])
            ))
        return cands

    def resolve(self, query: str) -> Dict[str, Any]:
        mentions = self.extractor.extract(query)

        resolved: List[ResolvedCourse] = []
        debug_blocks: List[str] = []

        for ment in mentions:
            cands = self._score_candidates(ment.raw)
            if not cands:
                continue
            top1 = cands[0]
            top2 = cands[1] if len(cands) > 1 else None
            margin = (top1.score - top2.score) if top2 else top1.score

            status = "CONFIDENT" if (top1.score >= self.threshold and margin >= self.margin) else "AMBIGUOUS"
            resolved.append(ResolvedCourse(
                ma_mon_hoc=top1.ma_mon_hoc,
                tieng_viet=top1.tieng_viet,
                tieng_anh=top1.tieng_anh,
                score=top1.score,
                status=status
            ))

            if self.enable_debug_log:
                lines = [f'[CourseResolver] mention="{ment.raw}" canon="{normalize_canon(ment.raw)}" decision={status} top1={top1.score:.3f} margin={margin:.3f}']
                for j, c in enumerate(cands[:self.top_k_debug], 1):
                    lines.append(f"  {j}) {c.ma_mon_hoc} | {c.tieng_viet} -> {c.tieng_anh} | score={c.score:.3f}")
                debug_blocks.append("\n".join(lines))

        # dedup by course code
        uniq = {}
        for r in resolved:
            uniq[r.ma_mon_hoc] = r
        resolved = list(uniq.values())

        canonical_note = ""
        if resolved:
            canonical_note = "Canonical courses (from catalog): " + "; ".join([f'{r.ma_mon_hoc} — {r.tieng_anh}' for r in resolved])

        return {
            "mentions": [m.raw for m in mentions],
            "resolved_courses": [r.__dict__ for r in resolved],
            "canonical_note": canonical_note,
            "debug_log": "\n\n".join(debug_blocks)
        }
