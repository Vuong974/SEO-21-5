#!/usr/bin/env python3
"""Generate candidate proofreading findings from website text exports.

Input:
  - Plain text file, or
  - CSV with columns such as url,title,text/content/body.

Output:
  CSV rows: source, location, issue_type, current_text, suggestion, severity, note
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


TEXT_COLUMNS = ("text", "content", "body", "description", "excerpt")
SOURCE_COLUMNS = ("url", "link", "permalink", "title", "id")


TYPO_HINTS = {
    "chung nhan": "chứng nhận",
    "danh gia": "đánh giá",
    "dao tao": "đào tạo",
    "he thong": "hệ thống",
    "quan ly": "quản lý",
    "chat luong": "chất lượng",
    "an toan": "an toàn",
    "doanh nghiep": "doanh nghiệp",
    "tieu chuan": "tiêu chuẩn",
}


def rows_from_input(path: Path):
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, start=2):
                text = ""
                for col in TEXT_COLUMNS:
                    if row.get(col):
                        text = row[col]
                        break
                if not text:
                    text = " ".join(v for v in row.values() if v)
                source_parts = [row.get(c, "") for c in SOURCE_COLUMNS if row.get(c)]
                yield " | ".join(source_parts) or f"row {i}", f"row {i}", text
    else:
        text = path.read_text(encoding="utf-8-sig")
        yield str(path), "file", text


def context(text: str, start: int, end: int, radius: int = 55) -> str:
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    snippet = text[left:right].replace("\n", " ")
    return re.sub(r"\s+", " ", snippet).strip()


def find_issues(source: str, location: str, text: str):
    patterns = [
        (r"\b(\w{2,})\s+\1\b", "Lap tu", "Remove the repeated word.", "Medium"),
        (r"[ \t]{2,}", "Khoang trang", "Use a single space.", "Low"),
        (r"\s+[,.;:!?]", "Dau cau/khoang trang", "Remove the space before punctuation.", "Low"),
        (r"[,.;:!?](?=[^\s\d])", "Dau cau/khoang trang", "Add a space after punctuation if this is prose.", "Low"),
        (r"[!?.,;:]{2,}", "Dau cau", "Use one punctuation mark unless emphasis is intentional.", "Low"),
        (r"&(?:nbsp|amp|quot|lt|gt);", "Loi hien thi", "Decode or remove the visible HTML entity.", "Medium"),
        (r"\[[A-Za-z0-9_-]+(?:\s+[^\]]*)?\]", "Loi hien thi", "Check whether this shortcode is visible on the page.", "Medium"),
    ]
    for pattern, issue_type, suggestion, severity in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            yield {
                "source": source,
                "location": location,
                "issue_type": issue_type,
                "current_text": context(text, match.start(), match.end()),
                "suggestion": suggestion,
                "severity": severity,
                "note": f"Matched pattern: {pattern}",
            }

    lowered = text.lower()
    for raw, fixed in TYPO_HINTS.items():
        for match in re.finditer(rf"\b{re.escape(raw)}\b", lowered):
            yield {
                "source": source,
                "location": location,
                "issue_type": "Chinh ta/dau tieng Viet",
                "current_text": context(text, match.start(), match.end()),
                "suggestion": f"Consider: {fixed}",
                "severity": "Medium",
                "note": "Candidate missing Vietnamese diacritics; verify in context.",
            }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("proofread-candidates.csv"))
    args = parser.parse_args()

    fieldnames = ["source", "location", "issue_type", "current_text", "suggestion", "severity", "note"]
    count = 0
    with args.output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for source, location, text in rows_from_input(args.input):
            for issue in find_issues(source, location, text):
                writer.writerow(issue)
                count += 1
    print(f"Wrote {count} candidate findings to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
