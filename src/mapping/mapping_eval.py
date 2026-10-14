"""
Evaluate VI→EN matcher using external queries.json (no templates)
=================================================================

- Đọc catalog từ JSON: [{"course_id": "...", "name_en": "..."}]
- Đọc queries từ JSON: ["câu hỏi 1 ...", "câu hỏi 2 ...", ...]
- Với mỗi câu hỏi:
    + LLM trích xuất 1..N tên môn tiếng Việt (vi_terms)
    + Cho từng vi_term: LLM sinh candidates EN, chấm điểm với catalog
    + Luôn lấy top-1; nếu score >= threshold → retrieved=True
- Thống kê:
    + retrieval_percent: % (trên tổng số cặp query×vi_term) có score_top1 >= threshold
- Ghi chi tiết ra evaluation_report.json

Chạy:
   python HCMUS-RAG-main\mapping_eval.py --catalog HCMUS-RAG-main\catalog.json --queries HCMUS-RAG-main\catalog_queries_vi.json --sleep 12
   python HCMUS-RAG-main\mapping_eval.py --catalog HCMUS-RAG-main\catalog.json --queries HCMUS-RAG-main\queries_2.json 
"""

from __future__ import annotations
import json
import argparse
import time
from typing import List, Dict, Any

# Dùng lại toàn bộ pipeline/hàm từ mapping_LLm.py
from mapping_LLm import (
    CatalogItem,
    THRESHOLD,
    extract_vi_terms_llm,
    generate_en_candidates_llm,
    HybridScorer,
)

# ---------- IO helpers ----------
def load_catalog_from_json(path: str) -> List[CatalogItem]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    items: List[CatalogItem] = []
    for row in raw:
        cid = str(row.get("course_id", "")).strip()
        name = str(row.get("name_en", "")).strip()
        if cid and name:
            items.append(CatalogItem(cid, name))
    if not items:
        raise ValueError("Catalog JSON rỗng hoặc sai định dạng. Cần list các object có course_id và name_en.")
    return items


def load_queries_from_json(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list) or not all(isinstance(x, str) for x in data):
        raise ValueError("queries.json phải là mảng các chuỗi (list[str]).")
    return data


# ---------- Evaluation ----------
def evaluate_from_queries(
    catalog: List[CatalogItem],
    queries: List[str],
    threshold: float = THRESHOLD,
    sleep: float = 0.0,
) -> Dict[str, Any]:
    """
    Trả về:
    {
      "summary": {...},
      "rows": [...]
    }
    """
    scorer = HybridScorer(catalog)

    rows: List[Dict[str, Any]] = []
    total_pairs = 0
    retrieved_pairs = 0

    for idx, query_vi in enumerate(queries, start=1):
        # GĐ1: trích xuất các tên môn VI từ câu
        try:
            vi_terms = extract_vi_terms_llm(query_vi)
        except Exception as e:
            rows.append({
                "query_vi": query_vi,
                "vi_term": None,
                "predicted_en_top1": None,
                "score": None,
                "retrieved": False,
                "error": f"extract_vi_terms_llm: {e}",
            })
            continue

        # Nếu không có term nào, log lại
        if not vi_terms:
            rows.append({
                "query_vi": query_vi,
                "vi_term": None,
                "predicted_en_top1": None,
                "score": None,
                "retrieved": False,
                "error": "no_vi_term_extracted",
            })
            continue

        # GĐ2/GĐ3/GĐ4: xử lý từng vi_term
        for vi_term in vi_terms:
            total_pairs += 1
            try:
                candidates = generate_en_candidates_llm(vi_term)
                best_idx, best_score, _ = scorer.score_candidates(candidates)
                if best_idx >= 0:
                    en_top1 = catalog[best_idx].name_en
                    sc = float(round(best_score, 4))
                else:
                    en_top1 = None
                    sc = None
            except Exception as e:
                rows.append({
                    "query_vi": query_vi,
                    "vi_term": vi_term,
                    "predicted_en_top1": None,
                    "score": None,
                    "retrieved": False,
                    "error": f"score_candidates: {e}",
                })
                continue

            retrieved = (sc is not None) and (sc >= threshold)
            if retrieved:
                retrieved_pairs += 1

            rows.append({
                "query_vi": query_vi,
                "vi_term": vi_term,
                "predicted_en_top1": en_top1,
                "score": sc,
                "retrieved": retrieved,
            })

        # Thêm delay để tránh vượt quota API
        if sleep > 0:
            print(f"[{idx}/{len(queries)}] Sleeping {sleep}s to respect API rate limits...")
            time.sleep(sleep)

    # Tổng hợp kết quả
    retrieval_percent = round((100.0 * retrieved_pairs / total_pairs), 2) if total_pairs else 0.0
    return {
        "summary": {
            "total_pairs": total_pairs,
            "retrieved": retrieved_pairs,
            "retrieval_percent": retrieval_percent,
            "threshold": threshold,
        },
        "rows": rows,
    }


# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser(description="Evaluate VI→EN matcher using external queries.json")
    ap.add_argument("--catalog", required=True, help="Đường dẫn catalog.json (list {course_id,name_en})")
    ap.add_argument("--queries", required=True, help="Đường dẫn queries.json (list[str] các câu hỏi)")
    ap.add_argument("--out", default="evaluation_report_4.json", help="Đường dẫn file kết quả JSON")
    ap.add_argument("--sleep", type=float, default=12.0, help="Thời gian nghỉ giữa các query (giây)")
    args = ap.parse_args()

    catalog = load_catalog_from_json(args.catalog)
    queries = load_queries_from_json(args.queries)

    print(f"Loaded {len(catalog)} catalog items.")
    print(f"Loaded {len(queries)} queries.")
    print(f"Sleep between requests: {args.sleep}s")

    report = evaluate_from_queries(catalog, queries, threshold=THRESHOLD, sleep=args.sleep)

    print("\n=== SUMMARY ===")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\nFull report saved to: {args.out}")


if __name__ == "__main__":
    main()
