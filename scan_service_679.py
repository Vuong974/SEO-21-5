"""
Scan all WordPress 'service' posts for phone numbers ending in 679.
Outputs a CSV report with post ID, title, URL, and matched phone snippets.
"""
import base64
import json
import os
import re
import csv
import sys
from urllib import error, request as urllib_request

PHONE_679_PATTERN = re.compile(
    r'(?<!\d)'                        # no digit before
    r'(?:0|\+84|84)?'                 # optional country code
    r'[\s.\-]?'
    r'(?:\d[\s.\-]?){6,10}'          # middle digits (flexible separators)
    r'679'                            # must end in 679
    r'(?!\d)',                        # no digit after
    re.UNICODE
)

def wp_get(path: str) -> list:
    site_url = os.environ["WORDPRESS_SITE_URL"].rstrip("/")
    username = os.environ["WORDPRESS_USERNAME"]
    app_password = os.environ["WORDPRESS_APP_PASSWORD"]
    token = base64.b64encode(f"{username}:{app_password}".encode()).decode("ascii")
    headers = {
        "Authorization": f"Basic {token}",
        "Accept": "application/json",
        "User-Agent": "KNA-Scanner/1.0",
    }
    req = urllib_request.Request(f"{site_url}{path}", headers=headers, method="GET")
    try:
        with urllib_request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"API error {exc.code}: {body}") from exc

def strip_html(html: str) -> str:
    return re.sub(r'<[^>]+>', ' ', html)

def get_context(text: str, match) -> str:
    start = max(0, match.start() - 60)
    end = min(len(text), match.end() + 60)
    return text[start:end].strip()

def scan_all_services():
    results = []
    page = 1
    total_pages = 1

    print("Scanning service posts...", flush=True)

    while page <= total_pages:
        path = f"/wp-json/wp/v2/service?per_page=100&page={page}&status=publish&_fields=id,title,link,content"
        try:
            posts = wp_get(path)
        except RuntimeError as e:
            print(f"  Error page {page}: {e}", flush=True)
            break

        if not posts:
            break

        print(f"  Page {page}: {len(posts)} posts", flush=True)

        for post in posts:
            post_id = post.get("id")
            title = post.get("title", {}).get("rendered", "")
            link = post.get("link", "")
            raw_content = post.get("content", {}).get("rendered", "")
            plain_text = strip_html(raw_content)

            matches = list(PHONE_679_PATTERN.finditer(plain_text))
            if matches:
                for m in matches:
                    ctx = get_context(plain_text, m)
                    results.append({
                        "post_id": post_id,
                        "title": re.sub(r'<[^>]+>', '', title),
                        "link": link,
                        "phone_matched": m.group().strip(),
                        "context": ctx,
                    })
                print(f"    FOUND 679: ID={post_id} | {title[:60]} | matches={len(matches)}", flush=True)

        page += 1

    return results

def main():
    results = scan_all_services()

    out_path = os.path.join(os.path.dirname(__file__), "service-679-scan-result.csv")
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["post_id", "title", "link", "phone_matched", "context"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nDone. Found {len(results)} match(es) in {len({r['post_id'] for r in results})} post(s).")
    print(f"Report saved: {out_path}")

    # Print summary table
    seen = set()
    for r in results:
        if r["post_id"] not in seen:
            seen.add(r["post_id"])
            print(f"  ID={r['post_id']} | {r['title'][:60]} | {r['link']}")

if __name__ == "__main__":
    main()
