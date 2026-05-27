import base64
import json
import os
import re
import sys
from html import unescape
from urllib import error, request


SITE_URL = os.environ.get("WORDPRESS_SITE_URL", "https://knacert.com.vn").rstrip("/")
USERNAME = os.environ.get("WORDPRESS_USERNAME", "").strip()
APP_PASSWORD = os.environ.get("WORDPRESS_APP_PASSWORD", "").strip()

EXPERT_ID = 657
EXPERT_NAME = "Cao Thế Hiệp"
EXPERT_URL = "https://knacert.com.vn/chuyen-gia/cao-the-hiep/"

POST_IDS = [
    13829,  # Chứng nhận EUDR
]

POST_SLUGS = [
    "7-uu-diem-cua-san-pham-go-duoc-chung-nhan-fsc",
    "chung-chi-xanh-ty-usd-cho-nganh-go-viet-nam",
    "chung-nhan-eudr-xac-minh-tuan-thu-quy-dinh-chong-pha-rung-eu",
    "co-che-hap-thu-khi-nha-kinh-tu-lam-nghiep-cac-yeu-to-anh-huong",
    "danh-sach-ho-so-tai-lieu-eutr-ve-go-va-san-pham-go-can-chuan-bi",
    "danh-sach-san-pham-duoc-mien-tru-eutr-eutr-exemptions",
    "eudr-la-gi-tat-tan-tat-quy-dinh-chong-pha-rung-eu-moi-nhat-20231115",
    "hang-go-xuat-khau-can-chung-chi-rung",
    "hang-hoa-san-xuat-tren-dat-chat-pha-rung-se-khong-duoc-phep-vao-chau-au",
    "kna-hop-tac-voi-tuv-danh-gia-tieu-chuan-fsc-tai-viet-nam",
]

EXPERT_BLOCK = f"""
<div class="kna-expert-review" data-expert-id="{EXPERT_ID}">
  <p><strong>Cố vấn chuyên môn:</strong> <a href="{EXPERT_URL}">{EXPERT_NAME}</a> - Giảng viên cao cấp và Chuyên gia đánh giá trưởng của KNA CERT, có 17 năm kinh nghiệm trong lĩnh vực lâm nghiệp, đánh giá chứng nhận các tiêu chuẩn bền vững và tiêu chuẩn rừng.</p>
</div>
""".strip()


def wp_request(method, path, payload=None):
    if not USERNAME or not APP_PASSWORD:
        raise RuntimeError("Missing WORDPRESS_USERNAME or WORDPRESS_APP_PASSWORD")

    token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode("utf-8")).decode("ascii")
    headers = {
        "Authorization": f"Basic {token}",
        "Accept": "application/json",
        "User-Agent": "Codex-KNA-Expert-Mapping/1.0",
    }
    data = None
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"

    req = request.Request(f"{SITE_URL}{path}", data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=45) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"WordPress API error {exc.code}: {body}") from exc


def get_post_by_slug(slug):
    items = wp_request("GET", f"/wp-json/wp/v2/posts?slug={slug}&context=edit")
    if not items:
        raise RuntimeError(f"Post not found for slug: {slug}")
    return items[0]


def insert_expert_block(raw_content):
    if "data-expert-id=\"657\"" in raw_content or EXPERT_URL in raw_content:
        return raw_content, False

    # Put the review box after the first paragraph, where readers and crawlers see it early.
    match = re.search(r"</p>", raw_content, flags=re.IGNORECASE)
    if not match:
        return f"{EXPERT_BLOCK}\n\n{raw_content}", True
    insert_at = match.end()
    return raw_content[:insert_at] + "\n\n" + EXPERT_BLOCK + raw_content[insert_at:], True


def main():
    updated = []
    skipped = []
    for slug in POST_SLUGS:
        post = get_post_by_slug(slug)
        post_id = int(post["id"])
        title = unescape(post["title"]["rendered"])
        raw_content = post["content"]["raw"]
        new_content, changed = insert_expert_block(raw_content)
        if not changed:
            skipped.append((post_id, title, "already_has_expert_block"))
            continue

        result = wp_request("POST", f"/wp-json/wp/v2/posts/{post_id}", {"content": new_content})
        updated.append((post_id, title, result.get("link")))

    print(json.dumps({"updated": updated, "skipped": skipped}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
