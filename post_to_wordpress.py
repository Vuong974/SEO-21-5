import argparse
import base64
import json
import os
import sys
from typing import Any, Dict, Optional
from urllib import error, parse, request


def required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def wp_request(method: str, path: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    site_url = required_env("WORDPRESS_SITE_URL").rstrip("/")
    username = required_env("WORDPRESS_USERNAME")
    app_password = required_env("WORDPRESS_APP_PASSWORD")

    token = base64.b64encode(f"{username}:{app_password}".encode("utf-8")).decode("ascii")
    data = None
    headers = {
        "Authorization": f"Basic {token}",
        "Accept": "application/json",
        "User-Agent": "Codex-WordPress-Workflow/1.0",
    }

    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"

    req = request.Request(f"{site_url}{path}", data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"WordPress API error {exc.code}: {body}") from exc


def find_term(taxonomy: str, name: str) -> Optional[int]:
    query = parse.urlencode({"search": name, "per_page": 20})
    items = wp_request("GET", f"/wp-json/wp/v2/{taxonomy}?{query}")
    wanted = name.strip().casefold()
    for item in items:
        if item.get("name", "").strip().casefold() == wanted:
            return int(item["id"])
    return None


def create_term(taxonomy: str, name: str) -> int:
    item = wp_request("POST", f"/wp-json/wp/v2/{taxonomy}", {"name": name.strip()})
    return int(item["id"])


def resolve_terms(taxonomy: str, raw_value: str, create_missing: bool) -> list[int]:
    ids: list[int] = []
    for part in [p.strip() for p in raw_value.split(",") if p.strip()]:
        if part.isdigit():
            ids.append(int(part))
            continue
        term_id = find_term(taxonomy, part)
        if term_id is None and create_missing:
            term_id = create_term(taxonomy, part)
        if term_id is not None:
            ids.append(term_id)
    return ids


def build_payload(args: argparse.Namespace) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "title": args.title,
        "content": args.content,
        "status": args.status,
    }
    if args.slug:
        payload["slug"] = args.slug
    if args.excerpt:
        payload["excerpt"] = args.excerpt
    if args.categories:
        payload["categories"] = resolve_terms("categories", args.categories, args.create_missing_terms)
    if args.tags:
        payload["tags"] = resolve_terms("tags", args.tags, args.create_missing_terms)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or update a WordPress post.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--content", required=True)
    parser.add_argument("--status", default="draft", choices=["draft", "pending", "publish", "private", "future"])
    parser.add_argument("--slug", default="")
    parser.add_argument("--excerpt", default="")
    parser.add_argument("--categories", default="")
    parser.add_argument("--tags", default="")
    parser.add_argument("--post-id", default="")
    parser.add_argument("--create-missing-terms", action="store_true")
    args = parser.parse_args()

    payload = build_payload(args)
    if args.post_id:
        result = wp_request("POST", f"/wp-json/wp/v2/posts/{args.post_id}", payload)
    else:
        result = wp_request("POST", "/wp-json/wp/v2/posts", payload)

    print(json.dumps({
        "id": result.get("id"),
        "link": result.get("link"),
        "status": result.get("status"),
        "slug": result.get("slug"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
