#!/usr/bin/env python3
"""
Keyword Mapper: maps GSC keywords to the best matching article.

Usage (articles from Google Sheet):
    python keyword_mapper.py --articles-from-sheet --push-to-sheet

Usage (articles from CSV):
    python keyword_mapper.py --articles articles.csv
"""
import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import SHEET_ID, ARTICLES_TAB, KEYWORD_MAPPING_TAB, GSC_REPORT_PATH, KEYWORD_MATCH_THRESHOLD
from utils import normalize, overlap_coefficient

_HEADERS = [
    "Keyword", "Clicks", "Impressions", "CTR", "Position",
    "Cluster", "Intent", "Funnel", "Page Type", "SEO Priority",
    "Mapped URL", "Mapped Title", "Confidence", "Note",
]


def load_keywords(tsv_path: str) -> list:
    with open(tsv_path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def load_articles_csv(path: str) -> list:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_articles_sheet(sheet_id: str) -> list:
    from sheets_client import read_tab
    return read_tab(sheet_id, ARTICLES_TAB)


def _score(article: dict, keyword: dict) -> float:
    article_tokens = normalize(
        article.get("Title", "") + " " + article.get("Target Keywords", "")
    )
    cluster_score = overlap_coefficient(normalize(keyword.get("cum_chu_de", "")), article_tokens)
    query_score = overlap_coefficient(normalize(keyword.get("truy_van", "")), article_tokens)
    return 0.4 * cluster_score + 0.6 * query_score


def _confidence(score: float) -> str:
    if score >= 0.4:
        return "Cao"
    if score >= 0.15:
        return "Trung bình"
    if score >= KEYWORD_MATCH_THRESHOLD:
        return "Thấp"
    return "Không khớp"


def map_keywords(keywords: list, articles: list) -> list:
    results = []
    for kw in keywords:
        best, best_score = None, 0.0
        for art in articles:
            s = _score(art, kw)
            if s > best_score:
                best_score, best = s, art
        mapped = best_score >= KEYWORD_MATCH_THRESHOLD
        results.append({
            "Keyword": kw.get("truy_van", ""),
            "Clicks": kw.get("luot_nhap", ""),
            "Impressions": kw.get("hien_thi", ""),
            "CTR": kw.get("ctr", ""),
            "Position": kw.get("vi_tri", ""),
            "Cluster": kw.get("cum_chu_de", ""),
            "Intent": kw.get("y_dinh_chinh", ""),
            "Funnel": kw.get("giai_doan_pheu", ""),
            "Page Type": kw.get("loai_trang", ""),
            "SEO Priority": kw.get("uu_tien_seo", ""),
            "Mapped URL": best["URL"] if mapped and best else "",
            "Mapped Title": best["Title"] if mapped and best else "",
            "Confidence": _confidence(best_score),
            "Note": kw.get("ghi_chu", ""),
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="Map GSC keywords to articles")
    parser.add_argument("--articles", help="Path to articles CSV")
    parser.add_argument("--articles-from-sheet", action="store_true", help="Load articles from Google Sheet")
    parser.add_argument("--sheet-id", default=SHEET_ID)
    parser.add_argument("--gsc", default=GSC_REPORT_PATH, help="Path to GSC TSV report")
    parser.add_argument("--output", default="keyword_mapping.csv")
    parser.add_argument("--push-to-sheet", action="store_true", help="Push results to Google Sheet")
    args = parser.parse_args()

    print(f"Loading keywords from: {args.gsc}")
    keywords = load_keywords(args.gsc)
    print(f"  {len(keywords)} keywords loaded.")

    if args.articles_from_sheet:
        print(f"Loading articles from Google Sheet ({args.sheet_id})...")
        articles = load_articles_sheet(args.sheet_id)
    elif args.articles:
        print(f"Loading articles from: {args.articles}")
        articles = load_articles_csv(args.articles)
    else:
        parser.error("Provide --articles FILE or --articles-from-sheet")

    print(f"  {len(articles)} articles loaded.")

    print("Mapping keywords...")
    results = map_keywords(keywords, articles)

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_HEADERS)
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved: {args.output}")

    if args.push_to_sheet:
        from sheets_client import overwrite_tab
        rows = [[r[h] for h in _HEADERS] for r in results]
        overwrite_tab(args.sheet_id, KEYWORD_MAPPING_TAB, _HEADERS, rows)
        print(f"Pushed to Sheet tab '{KEYWORD_MAPPING_TAB}'")

    mapped = sum(1 for r in results if r["Mapped URL"])
    print(f"\nResult: {mapped}/{len(results)} keywords mapped")
    unmapped = [r["Keyword"] for r in results if not r["Mapped URL"]]
    if unmapped:
        preview = ", ".join(unmapped[:8])
        more = f" (+{len(unmapped) - 8} more)" if len(unmapped) > 8 else ""
        print(f"  Unmapped: {preview}{more}")
        print("  → Thêm bài viết vào tab Articles để tăng tỉ lệ mapping.")


if __name__ == "__main__":
    main()
