# Workflow thu cong trong Codex: dang bai WordPress tu Google Sheet

## Muc tieu

Khi ban dien noi dung vao Google Sheet, Codex se doc tung dong, tao bai viet WordPress qua REST API, va ghi lai ket qua dang bai vao sheet.

Workflow nay chay thu cong trong Codex khi ban ra lenh. No khong tu dong chay nen.

## Dieu kien can co

Can co thong tin WordPress:

```text
WORDPRESS_SITE_URL=https://knacert.com.vn
WORDPRESS_USERNAME=admin@knacert.com
WORDPRESS_APP_PASSWORD=...
```

Khuyen nghi dung WordPress Application Password, khong dung mat khau dang nhap chinh.
Khong ghi `WORDPRESS_APP_PASSWORD` vao Google Sheet hoac file workflow.

## Thiet lap trong PowerShell

Chay lenh sau trong PowerShell truoc khi dang bai:

```powershell
$env:WORDPRESS_SITE_URL = "https://knacert.com.vn"
$env:WORDPRESS_USERNAME = "admin@knacert.com"
$env:WORDPRESS_APP_PASSWORD = "application-password-cua-ban"
```

Sau do moi ra lenh cho Codex chay workflow dang bai.

## Cau truc Google Sheet

Google Sheet mac dinh:

```text
https://docs.google.com/spreadsheets/d/1wwhKA8qatXaenBe1Mxd5IZi2tAbw8jgxL7u3QjsUeIw/edit
```

Tab mac dinh:

```text
WordPress Posts
```

| Cot | Ten cot | Vai tro |
| --- | --- | --- |
| A | Title | Tieu de bai viet |
| B | Slug | Duong dan bai viet, co the de trong de WordPress tu tao |
| C | Content | Noi dung bai viet dang HTML hoac Markdown |
| D | Excerpt | Mo ta ngan |
| E | Category | Ten hoac ID chuyen muc |
| F | Tags | Danh sach tag, cach nhau bang dau phay |
| G | Status | `draft`, `pending`, hoac `publish` |
| H | Featured Image URL | URL anh dai dien, neu co |
| I | WordPress URL | Link bai viet sau khi dang |
| J | WordPress ID | ID bai viet WordPress |
| K | Publish Status | Trang thai xu ly: `pending`, `posted`, `error` |
| L | Error | Loi neu co |

## Quy tac nhan dien dong can dang

Codex se xu ly cac dong thoa dieu kien:

1. Cot `Title` co du lieu.
2. Cot `Content` co du lieu.
3. Cot `Publish Status` dang trong hoac bang `pending`.
4. Cot `WordPress ID` dang trong.

Neu cot `WordPress ID` da co du lieu, Codex se bo qua de tranh dang trung bai, tru khi ban yeu cau cap nhat lai bai.

## Cau lenh mau

```text
Chay workflow dang bai WordPress tu Google Sheet.
```

Hoac:

```text
Dang cac bai co Publish Status pending len WordPress.
```

Neu co nhieu Google Sheet, can chi ro link sheet:

```text
Chay workflow dang bai WordPress tu Google Sheet: [link sheet]
```

## Quy trinh Codex se thuc hien

1. Mo Google Sheet bang connector.
2. Doc header de xac dinh dung cot.
3. Tim cac dong can dang bai.
4. Kiem tra bien moi truong WordPress trong may.
5. Chuyen noi dung Markdown sang HTML neu cot `Content` la Markdown.
6. Tao payload cho WordPress REST API.
7. Goi API:

```text
POST /wp-json/wp/v2/posts
```

8. Ghi ket qua ve Google Sheet:
   - `WordPress URL`
   - `WordPress ID`
   - `Publish Status = posted`
   - xoa cot `Error` neu dang thanh cong
9. Neu loi, ghi:
   - `Publish Status = error`
   - noi dung loi vao cot `Error`

## Payload WordPress mau

```json
{
  "title": "Tieu de bai viet",
  "slug": "duong-dan-bai-viet",
  "content": "<h1>...</h1><p>...</p>",
  "excerpt": "Mo ta ngan",
  "status": "draft",
  "categories": [1],
  "tags": [2, 3]
}
```

## Trang thai dang bai

Nen dung `draft` mac dinh de kiem tra tren WordPress truoc khi public.

Gia tri hop le:

- `draft`: tao ban nhap.
- `pending`: cho duyet.
- `publish`: dang cong khai ngay.

## Luu y ve Category va Tags

WordPress REST API can ID cho `categories` va `tags`.

Neu Google Sheet nhap ten chuyen muc/tag, Codex can:

1. Goi API tim category/tag theo ten.
2. Neu tim thay, dung ID do.
3. Neu khong tim thay, tao moi category/tag neu ban cho phep.

## Bien the cap nhat bai da dang

Neu cot `WordPress ID` da co gia tri va ban yeu cau cap nhat, Codex se goi:

```text
POST /wp-json/wp/v2/posts/{id}
```

Sau do ghi lai ket qua moi vao sheet.

## An toan van hanh

- Mac dinh nen dang o trang thai `draft`.
- Khong dang lai dong da co `WordPress ID`.
- Khong luu username/password truc tiep trong Google Sheet.
- Khong dua Application Password vao file workflow.
- Truoc khi `publish`, nen kiem tra title, slug, internal link, anh va category.
