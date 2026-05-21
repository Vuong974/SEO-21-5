import base64
import json
import os
import re
import unicodedata
from typing import Any, Dict, Optional, Tuple
from urllib import error, request as urlrequest

# Common Vietnamese stop words (normalized, no diacritics)
_STOP_WORDS = {
    "la", "va", "cua", "trong", "co", "khong", "voi", "cho", "de", "tren",
    "theo", "khi", "nhu", "duoc", "tu", "boi", "dang", "se", "da", "cac",
    "nhung", "mot", "hai", "ba", "nam", "gi", "nay", "do", "hay", "hoac",
    "rat", "ve", "tai", "sau", "truoc", "neu", "vi", "nen", "the", "thi",
    "moi", "cung", "deu", "nao", "ay", "o", "a", "i", "to", "va", "an",
}


def normalize(text: str) -> set:
    if not text:
        return set()
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[^\w\s]", " ", text)
    tokens = set(text.split())
    return tokens - _STOP_WORDS - {""}


def overlap_coefficient(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing env var: {name}")
    return value


def wp_request(method: str, path: str, payload: Optional[Dict[str, Any]] = None) -> Any:
    site_url = required_env("WORDPRESS_SITE_URL").rstrip("/")
    username = required_env("WORDPRESS_USERNAME")
    app_password = required_env("WORDPRESS_APP_PASSWORD")
    token = base64.b64encode(f"{username}:{app_password}".encode()).decode("ascii")
    data = None
    headers = {
        "Authorization": f"Basic {token}",
        "Accept": "application/json",
        "User-Agent": "SEO-KNA-Internal-Link/1.0",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    url = f"{site_url}/wp-json/wp/v2/{path}"
    req = urlrequest.Request(url, data=data, headers=headers, method=method)
    try:
        with urlrequest.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"WordPress {method} {path} → {e.code}: {body}") from e


def find_post_by_url(post_url: str) -> Optional[Dict[str, Any]]:
    """Find a WordPress post or page by its public URL. Returns {type, post} or None."""
    slug = post_url.rstrip("/").split("/")[-1]
    for post_type in ("posts", "pages"):
        results = wp_request("GET", f"{post_type}?slug={slug}&context=edit&_fields=id,link,content,title")
        if isinstance(results, list) and results:
            return {"type": post_type, "post": results[0]}
    return None


def insert_link_in_content(content: str, anchor: str, target_url: str) -> Tuple[str, bool]:
    """Wrap the first unlinked occurrence of anchor in content with a link."""
    linked_ranges = [
        (m.start(), m.end())
        for m in re.finditer(r"<a\b[^>]*>.*?</a>", content, re.IGNORECASE | re.DOTALL)
    ]
    for m in re.finditer(re.escape(anchor), content, re.IGNORECASE):
        if not any(start <= m.start() < end for start, end in linked_ranges):
            new_content = (
                content[: m.start()]
                + f'<a href="{target_url}">{m.group()}</a>'
                + content[m.end() :]
            )
            return new_content, True
    return content, False
