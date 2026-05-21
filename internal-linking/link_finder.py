#!/usr/bin/env python3
"""
Internal Link Finder: scores article pairs and suggests internal links.

Usage (from Google Sheet):
    python link_finder.py --articles-from-sheet --push-to-sheet

Usage (from CSV):
    python link_finder.py --articles articles.csv
"""
import argparse
import csv
import os
import sys
from itertools import permutations

sys.path.insert(0, os.path.dirname(__file__))
from config import SHEET_ID, ARTICLES_TAB, LINK_RELEVANCE_THRESHOLD, MAX_LINKS_PER_SOURCE
from utils import normalize, overlap_coefficient

_HEADERS = [
    "Source URL", "Source Title", "Target URL", "Target Title",
    "Anchor Text", "Relevance Score", "Status",
]


def load_articles_csv(path: str) -> list:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_articles_sheet(sheet_id: str) -> list:
    from sheets_client import read_tab
    return read_tab(sheet_id, ARTICLES_TAB)


def _build_tokens(article: dict) -> set:
    return normalize(
        article.get("Title", "") + " "
        + article.get("Target Keywords", "") + " "
        + article.get("Excerpt", "")
    )


def _best_anchor(source: dict, target: dict) -> str:
    """Pick the best anchor text: a target keyword that appears in source content."""
    source_text = (
        source.get("Title", "") + " "
        + source.get("Target Keywords", "") + " "
        + source.get("Excerpt", "")
    ).lower()
    target_keywords = [kw.strip() for kw in target.get("Target Keywords", "").split(",") if kw.strip()]
    # Prefer longer phrases that actually appear in source text
    for kw in sorted(target_keywords, key=len, reverse=True):
        if kw.lower() in source_text:
            return kw
    # Fallback: primary target keyword or title
    if target_keywords:
        return target_keywords[0]
    return target.get("Title", "")


def find_opportunities(articles: list) -> list:
    token_map = {art["URL"]: _build_tokens(art) for art in articles}
    outgoing = {}  # source_url → count
    opportunities = []

    # Sort pairs by score descending so we fill best links first
    pairs = []
    for src, tgt in permutations(articles, 2):
        score = overlap_coefficient(token_map[src["URL"]], token_map[tgt["URL"]])
        if score >= LINK_RELEVANCE_THRESHOLD:
            pairs.append((score, src, tgt))
    pairs.sort(key=lambda x: -x[0])

    for score, src, tgt in pairs:
        src_url = src["URL"]
        if outgoing.get(src_url, 0) >= MAX_LINKS_PER_SOURCE:
            continue
        anchor = _best_anchor(src, tgt)
        if not anchor:
            continue
        opportunities.append({
            "Source URL": src_url,
            "Source Title": src.get("Title", ""),
            "Target URL": tgt["URL"],
            "Target Title": tgt.get("Title", ""),
            "Anchor Text": anchor,
            "Relevance Score": round(score, 3),
            "Status": "pending",
        })
        outgoing[src_url] = outgoing.get(src_url, 0) + 1

    opportunities.sort(key=lambda x: (x["Source URL"], -x["Relevance Score"]))
    return opportunities


def main():
    parser = argparse.ArgumentParser(description="Find internal link opportunities")
    parser.add_argument("--articles", help="Path to articles CSV")
    parser.add_argument("--articles-from-sheet", action="store_true")
    parser.add_argument("--sheet-id", default=SHEET_ID)
    parser.add_argument("--output", default="internal_links.csv")
    parser.add_argument("--push-to-sheet", action="store_true")
    args = parser.parse_args()

    if args.articles_from_sheet:
        print(f"Loading articles from Google Sheet ({args.sheet_id})...")
        articles = load_articles_sheet(args.sheet_id)
    elif args.articles:
        print(f"Loading articles from: {args.articles}")
        articles = load_articles_csv(args.articles)
    else:
        parser.error("Provide --articles FILE or --articles-from-sheet")

    if len(articles) < 2:
        print(f"Need at least 2 articles, got {len(articles)}. Thêm bài vào tab Articles.")
        sys.exit(1)

    print(f"  {len(articles)} articles loaded.")
    print("Finding link opportunities...")
    opps = find_opportunities(articles)
    print(f"  Found {len(opps)} opportunities.")

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_HEADERS)
        writer.writeheader()
        writer.writerows(opps)
    print(f"Saved: {args.output}")

    if args.push_to_sheet:
        from sheets_client import upsert_internal_links
        added = upsert_internal_links(args.sheet_id, opps)
        print(f"Added {added} new rows to Sheet tab 'Internal Links'")

    # Summary
    by_source = {}
    for o in opps:
        by_source.setdefault(o["Source URL"], []).append(o)
    if by_source:
        print("\nTop articles (most link opportunities):")
        for url, items in sorted(by_source.items(), key=lambda x: -len(x[1]))[:5]:
            print(f"  {len(items):2d}  {url}")


if __name__ == "__main__":
    main()
