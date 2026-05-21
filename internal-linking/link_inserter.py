#!/usr/bin/env python3
"""
Internal Link Inserter: inserts approved links into WordPress posts.

Usage (from Google Sheet):
    python link_inserter.py --from-sheet [--dry-run]

Usage (from CSV):
    python link_inserter.py --input internal_links.csv [--dry-run]

Required env vars:
    WORDPRESS_SITE_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD
Optional:
    GOOGLE_SERVICE_ACCOUNT_JSON, SEO_SHEET_ID (for --from-sheet)
"""
import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import SHEET_ID
from utils import wp_request, find_post_by_url, insert_link_in_content


def load_approved_csv(path: str) -> list:
    with open(path, encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r.get("Status", "").strip().lower() == "approved"]


def load_approved_sheet(sheet_id: str) -> list:
    from sheets_client import read_tab
    return [r for r in read_tab(sheet_id, "Internal Links") if r.get("Status", "").strip().lower() == "approved"]


def _save_csv_statuses(path: str, updates: dict):
    rows = []
    fieldnames = None
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    for row in rows:
        key = (row.get("Source URL", ""), row.get("Target URL", ""))
        if key in updates:
            row["Status"] = updates[key]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def process(links: list, dry_run: bool) -> dict:
    updates = {}
    post_cache = {}

    for link in links:
        src_url = link["Source URL"]
        tgt_url = link["Target URL"]
        anchor = link["Anchor Text"]
        key = (src_url, tgt_url)

        label = "[DRY RUN] " if dry_run else ""
        print(f"\n{label}{src_url}")
        print(f"  → {tgt_url}  (anchor: '{anchor}')")

        if src_url not in post_cache:
            post_cache[src_url] = find_post_by_url(src_url)

        found = post_cache[src_url]
        if not found:
            print(f"  ✗ Post not found")
            updates[key] = "error: post not found"
            continue

        post = found["post"]
        post_type = found["type"]
        post_id = post["id"]
        content = post.get("content", {}).get("raw", "")
        if not content:
            # rendered HTML fallback (less ideal for inserting)
            content = post.get("content", {}).get("rendered", "")

        new_content, inserted = insert_link_in_content(content, anchor, tgt_url)

        if not inserted:
            print(f"  ✗ Anchor text not found in content (may already be linked)")
            updates[key] = "skipped: anchor not found"
            continue

        if dry_run:
            print(f"  ✓ Would insert link in post ID {post_id}")
            updates[key] = "dry-run"
        else:
            wp_request("POST", f"{post_type}/{post_id}", {"content": new_content})
            print(f"  ✓ Inserted — post ID {post_id} updated")
            updates[key] = "inserted"

    return updates


def main():
    parser = argparse.ArgumentParser(description="Insert approved internal links into WordPress")
    parser.add_argument("--input", help="Path to internal_links.csv")
    parser.add_argument("--from-sheet", action="store_true")
    parser.add_argument("--sheet-id", default=SHEET_ID)
    parser.add_argument("--dry-run", action="store_true", help="Preview without making changes")
    args = parser.parse_args()

    if args.from_sheet:
        print("Loading approved links from Google Sheet...")
        links = load_approved_sheet(args.sheet_id)
    elif args.input:
        print(f"Loading approved links from: {args.input}")
        links = load_approved_csv(args.input)
    else:
        parser.error("Provide --input FILE or --from-sheet")

    if not links:
        print("No rows with Status='approved' found. Đổi Status trong Sheet/CSV thành 'approved' trước.")
        sys.exit(0)

    print(f"Processing {len(links)} approved links...")
    if args.dry_run:
        print("[DRY RUN — no WordPress changes will be made]")

    updates = process(links, dry_run=args.dry_run)

    if not args.dry_run:
        if args.input:
            _save_csv_statuses(args.input, updates)
            print(f"\nUpdated statuses in {args.input}")
        if args.from_sheet:
            from sheets_client import update_statuses
            update_statuses(args.sheet_id, "Internal Links", updates)
            print("\nUpdated statuses in Google Sheet")

    inserted = sum(1 for v in updates.values() if v == "inserted" or v == "dry-run")
    skipped = sum(1 for v in updates.values() if "skipped" in v)
    errors = sum(1 for v in updates.values() if "error" in v)
    print(f"\nSummary: {inserted} inserted, {skipped} skipped, {errors} errors")


if __name__ == "__main__":
    main()
