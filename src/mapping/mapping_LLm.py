"""
LLM-only Course Matcher VI→EN (Gemini) — Python 3.9 compatible
==============================================================

- Input: 1 câu truy vấn tiếng Việt có thể chứa 1+ tên môn học.
- Catalog: danh sách học phần tiếng Anh (course_id, name_en).
- Pipeline:
  GĐ1) Gemini trích xuất tên môn VI  -> ["cấu trúc dữ liệu", ...]
  GĐ2) Gemini sinh EN candidates     -> ["data structures", "data structure"]
  GĐ3) So khớp hybrid (FTS proxy + Fuzzy + Semantic)
  GĐ4) Trả kết quả: chỉ top-1 nếu score ≥ 0.85; kèm danh sách candidates_en.

Chạy:
    python HCMUS-RAG-main\mapping_LLm.py
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
from functools import lru_cache
import os
import re
import json


# ===== Python 3.9 compatibility shim =====
# Bổ sung importlib.metadata.packages_distributions khi chạy trên 3.9
try:
    import importlib.metadata as _md
    _ = _md.packages_distributions  
except Exception:
    import importlib_metadata as _md_backport  
    import sys as _sys
    _sys.modules["importlib.metadata"] = _md_backport  # monkeypatch stdlib alias

# ===== Load .env =====
try:
    from dotenv import load_dotenv  # pip install python-dotenv
    load_dotenv()
except Exception:
    pass


# ===== Cấu hình Gemini =====
MODEL_NAME = "gemini-2.5-flash" 

_GEMINI_READY = False
try:
    import google.generativeai as genai
    if os.getenv("GEMINI_API_KEY"):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        _GEMINI_READY = True
except Exception as _e:
    _GEMINI_READY = False

# ===== Thư viện NLP/Vector =====
try:
    from rapidfuzz import fuzz
except Exception:
    # Fallback thô nếu thiếu rapidfuzz
    class _Fuzz:  #Mô phỏng lại (fallback) chức năng của fuzz nếu thư viện thật bị thiếu.
        @staticmethod
        def token_sort_ratio(a, b):     # input là 2 chuỗi a,b 
            def toks(s):                # nhận một chuỗi s
                return tuple(sorted(re.findall(r"[\w]+", s.lower())))   # chuyển chuỗi s về lowercase, lấy tất cả từ (\w+), sắp xếp và trả về tuple
            ta, tb = set(toks(a)), set(toks(b))     # lấy set token từ a và b để so sánh
            if not ta or not tb:        # nếu 1 trong 2 set rỗng thì trả về 0
                return 0
            inter = len(ta & tb)        # tính số token chung giữa a và b
                                        # ta = {"data", "structures"}
                                        # tb = {"data", "algorithms"}
                                        # ta & tb  # kết quả: {"data"}
                                        
            union = len(ta | tb)        # số token tổng hợp, tức số token duy nhất có trong cả hai chuỗi.
            return int(100 * inter / union)  
    fuzz = _Fuzz()

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    _HAVE_ST = True
except Exception:
    import numpy as np
    _HAVE_ST = False

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ===== Hyper-params =====
W_FTS = 0.35
W_FUZZY = 0.25
W_SEM = 0.40
THRESHOLD = 0.85  # chỉ nhận top-1 nếu score >= 0.85

# ===== Tuning flags =====
EXACT_MATCH_BONUS = True  # #NEW: nếu candidate == tên catalog (sau normalize) -> score=1.0 cho cặp đó
ADD_VI_HEURISTIC_CANDIDATES = True  # #NEW: bổ sung vài biến thể EN hay gặp từ một số hậu tố VI (đại cương, nhập môn,...)

# ===== Utils =====
def normalize(text: str) -> str:   # Chuẩn hóa văn bản 
    text = text.lower().strip()
    text = re.sub(r"[’'`]+", "'", text)
    text = re.sub(r"[^\w\s\-&/']", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

# Đo độ chồng lấp từ (token overlap) giữa hai chuỗi, tức đo mức độ giống nhau theo token.
def token_overlap(a: str, b: str) -> float:     # nhận hai chuỗi a, b kiểu str và trả về một số thực float
    aa = set(normalize(a).split())              # {"cấu", "trúc", "dữ", "liệu"}
    bb = set(normalize(b).split())              # {"dữ", "liệu", "và", "cấu", "trúc"}
    if not aa or not bb:
        return 0.0
    inter = len(aa & bb)                        # aa & bb -> {"cấu", "trúc", "dữ", "liệu"}  -> len = 4
    return inter / max(len(aa), len(bb))  # ∈ [0,1]   , max(4,5) = 5 -> result = 4/5


# ===== Data model =====
@dataclass
class CatalogItem:
    course_id: str
    name_en: str


# ===== Gemini helpers (LLM-only) =====
def _ensure_gemini_ready():
    if not _GEMINI_READY:
        raise RuntimeError(
            "Gemini chưa được cấu hình. Hãy set GEMINI_API_KEY trong .env hoặc biến môi trường."
        )


def _call_gemini_json(model_name: str, system_msg: str, user_msg: str) -> Dict[str, Any]:
    model = genai.GenerativeModel(model_name)
    resp = model.generate_content([system_msg, user_msg])
    txt = resp.text or "{}"
    try:
        return json.loads(txt)
    except Exception:
        # Thử bóc JSON khi SDK trả thêm text
        m = re.search(r"\{[\s\S]*\}", txt)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
        return {}


def extract_vi_terms_llm(query_vi: str) -> List[str]:
    """
    Dùng Gemini trích xuất tên môn học tiếng Việt từ câu truy vấn.
    Output: ["cấu trúc dữ liệu", "toán rời rạc", ...]
    """
    _ensure_gemini_ready()
    system = (
        "Bạn là hệ trích xuất tên học phần từ tiếng Việt một cách kỹ lưỡng."
        "Chú ý đến vấn đề từ 'thực hành', 'thực tập' nếu đứng trước tên môn học thì cũng thuộc tên môn học, ví dụ thực hành đại số tuyến tính thì 'thực hành đại số tuyến tính' được xem là tên một môn học. Nếu đứng riêng lẻ không trước tên môn học thì chỉ xem là động từ"
        "Nếu có các số thứ tự 1, 2, 3, 1B, 2B, 1A, 2A,... ngay sau tên môn học thì cũng là một phần nằm trong tên môn học"
        "Chỉ trả về JSON đúng schema: {\"courses_vi\": [{\"text\": \"...\"}]}. "
        "Không thêm trường nào khác, không bình luận."
    )
    prompt = f"Văn bản: {query_vi}\nTrích xuất đúng schema."
    data = _call_gemini_json(MODEL_NAME, system, prompt)
    items = data.get("courses_vi", []) or []
    out: List[str] = []
    for it in items:
        t = (it.get("text") or "").strip()
        if t:
            out.append(t)
    return out


@lru_cache(maxsize=4096)
def generate_en_candidates_llm(vi_term: str) -> List[str]:
    """
    Dùng Gemini sinh ứng viên tiếng Anh từ một tên môn tiếng Việt.
    Output: ["data structures", "data structure", ...]
    """
    _ensure_gemini_ready()
    system = (
        "Bạn là chuyên gia dịch thuật chương trình đào tạo đại học từ tiếng Việt sang tiếng Anh."
        "Cho trước tên một học phần bằng tiếng Việt, hãy sinh ra 8 tên tiếng Anh của môn học đó một cách chính xác, tự nhiên và hợp lý nhất, theo chuẩn đặt tên môn học của các trường đại học nói tiếng Anh."
        "Các tên có từ như 'thực hành' thì hãy dịch đúng thành 'Practice', 'Laboratory'; 'thực tập' dịch thành 'Lab work', tương ứng sao cho phù hợp. Hoán đổi vị trí trước sau của chúng trong tên để phù hợp theo ngữ cảnh."
        "Hãy giữ nguyên, xác định đúng các số 1, 2, 3, 1B, 2B, 1A, 2A,... ngay sau tên môn học Tiếng Việt vào trong tên tiếng Anh vì nó cũng thuộc tên môn học"
        "Tên tiếng Anh phải nghe tự nhiên, trang trọng và xuất hiện trong danh mục học phần của các trường đại học."
        "Trả kết quả ở dạng mảng JSON gồm các lựa chọn, sắp xếp theo mức độ tự nhiên giảm dần."
        "Chỉ trả về JSON: {\"en\": [\"...\"]}. Không ghi chú thêm."
    )
    prompt = f"Tên môn: {vi_term}"
    data = _call_gemini_json(MODEL_NAME, system, prompt)
    ens = data.get("en", []) or []
    out = [e.strip() for e in ens if isinstance(e, str) and e.strip()]
    # dedupe giữ thứ tự
    seen = set()
    dedup = []
    for e in out:
        k = e.lower()
        if k not in seen:
            seen.add(k)
            dedup.append(e)
    return dedup


# ===== Scorer (hybrid) =====
class HybridScorer:
    def __init__(
        self,
        catalog: List[CatalogItem],
        w_fts=W_FTS,
        w_fuzzy=W_FUZZY,
        w_sem=W_SEM,
        sem_model_name: str = "distiluse-base-multilingual-cased-v2",
    ):
        assert abs((w_fts + w_fuzzy + w_sem) - 1.0) < 1e-6, "Weights must sum to 1"
        self.catalog = catalog
        self.w_fts, self.w_fuzzy, self.w_sem = w_fts, w_fuzzy, w_sem
        self.names = [c.name_en for c in catalog]   # danh sách tên tiếng anh các môn học trong datalog
        # Semantic backend
        self.use_st = False  # Khởi tạo cờ để biết có sử dụng sentence-transformer hay không
        try:
            if _HAVE_ST:
                self.model = SentenceTransformer(sem_model_name)
                self.name_embs = self.model.encode(self.names, normalize_embeddings=True)
                self.use_st = True
        except Exception:
            self.use_st = False
        if not self.use_st:
            self.tfidf = TfidfVectorizer()
            self.name_embs = self.tfidf.fit_transform(self.names)

    def _semantic(self, s: str) -> np.ndarray:
        if self.use_st:
            v = self.model.encode([s], normalize_embeddings=True)       # encode chuỗi s thành vector v
            sims = (v @ self.name_embs.T).ravel()           # nhân ma trận v với self.name_embs.T để tính cosine similarity với tất cả tên trong catalog.
                                                            # .ravel() chuyển kết quả sang 1D array.
            return sims
        else:
            vec = self.tfidf.transform([s])                 # nếu không có sentence- transformer thì dùng TF-IDF
            sims = cosine_similarity(vec, self.name_embs).ravel()
            return sims

    # Nhận danh sách tên candidates en các môn học vi trong query do LLM sinh ra
    def score_candidates(self, candidates: List[str]) -> Tuple[int, float, Dict[str, float]]:
        if not candidates:
            return -1, -1.0, {"fts": 0.0, "fuzzy": 0.0, "semantic": 0.0}
        sem_mats = [self._semantic(c) for c in candidates]      # tính vector similarity với tất cả các môn học cho từng candidate
        sem_max = np.max(np.vstack(sem_mats), axis=0)           # list ma trận similarity của từng candidate
        sem_max = np.clip(sem_max, 0.0, 1.0)                    # Gộp các similarity matrices lại (vstack) và lấy giá trị max trên từng cột (tương ứng với từng môn học).

        best_idx, best_score = -1, -1.0     #Khởi tạo biến lưu môn học tốt nhất, score tốt nhất, breakdown score (FTS, Fuzzy, Semantic).
        best_breakdown = {"fts": 0.0, "fuzzy": 0.0, "semantic": 0.0}
        for i, name in enumerate(self.names):   # lặp qua từng môn học trong danh sách
            fts_i = 0.0
            fuzzy_i = 0.0
            exact_hit = False  # #NEW: cờ exact-match
            name_norm = name.strip().lower()
            for c in candidates:                # lặp qua từng candidate
                fts_i = max(fts_i, token_overlap(c, name))
                fuzzy_i = max(fuzzy_i, fuzz.token_sort_ratio(c, name) / 100.0)
                # exact match bonus trigger
                if EXACT_MATCH_BONUS and c.strip().lower() == name_norm:
                    exact_hit = True
                    
            sem_i = float(sem_max[i])           # Lấy semantic similarity cho môn học i từ sem_max
            
            # nếu exact match -> đẩy các thành phần lên 1.0 để score = 1.0
            if exact_hit:
                fts_i, fuzzy_i, sem_i = 1.0, 1.0, 1.0
                
            score = self.w_fts * fts_i + self.w_fuzzy * fuzzy_i + self.w_sem * sem_i        # Tính hybrid score
            if score > best_score:
                best_idx, best_score = i, score
                best_breakdown = {"fts": round(fts_i, 3), "fuzzy": round(fuzzy_i, 3), "semantic": round(sem_i, 3)}
        return best_idx, float(best_score), best_breakdown  # (index_môn_tốt_nhất, score_tốt_nhất, breakdown_score).


# ===== Public API =====
def map_query_vi_to_en(query_vi: str, catalog: List[CatalogItem], threshold: float = THRESHOLD) -> List[Dict[str, Any]]:

    vi_terms = extract_vi_terms_llm(query_vi)
    scorer = HybridScorer(catalog)
    results: List[Dict[str, Any]] = []
    for vi in vi_terms:
        candidates = generate_en_candidates_llm(vi)
        best_idx, best_score, breakdown = scorer.score_candidates(candidates)

        if best_idx >= 0 and best_score >= threshold:
            item = catalog[best_idx]
            results.append({
                "vi_term": vi,
                "candidates_en": candidates,  # danh sách ứng viên do LLM sinh
                "en_name": item.name_en,
                "course_id": item.course_id,
                "score": round(best_score, 4),
                "breakdown": breakdown,
            })
        else:
            results.append({
                "vi_term": vi,
                "candidates_en": candidates,  # vẫn trả về để bạn kiểm tra
                "en_name": None,
                "course_id": None,
                "score": None,
                "breakdown": None,
                "status": "không có trong database",
            })
    return results


# ===== Demo =====
if __name__ == "__main__":
    # Kiểm tra key
    if not _GEMINI_READY:
        raise SystemExit("GEMINI_API_KEY chưa được thiết lập. Hãy đặt trong .env hoặc export rồi chạy lại.")
    
    # Catalog ví dụ; thực tế bạn nạp từ DB/CSV
    catalog = [
        CatalogItem("CS101", "Data Structures & Algorithms"),
        CatalogItem("MATH201", "Recommender System"),
        CatalogItem("MATH101", "Discrete Mathematics Practice"),
        CatalogItem("MATH202", "Linear Algebra"),
        CatalogItem("CS301", "Lab work on General Physics"),
        CatalogItem("CS302", "Seminar on Data Science"),
        CatalogItem("CS401", "Computational Software Laboratory"),
        CatalogItem("SE201", "General Chemistry Laboratory 2"),
        CatalogItem("STAT201", "General Chemistry Laboratory 1"),
    ]

    query = "Em cần đăng ký hệ thống tư vấn và thực tập vật lý đại cương, còn seminar cho khoa học dữ liệu để kỳ sau."
    try:
        out = map_query_vi_to_en(query, catalog, threshold=THRESHOLD)
        print(json.dumps(out, ensure_ascii=False, indent=2))
    except Exception as e:
        print("An error occurred:", e)
