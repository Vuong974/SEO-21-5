# Internal Linking & Keyword Mapping

Bộ công cụ tìm cơ hội internal link và map từ khóa GSC cho knacert.com.vn.

## Cài đặt

```powershell
pip install -r requirements.txt
```

---

## Chuẩn bị Google Sheet

Mở Google Sheet và tạo tab **Articles** với 4 cột sau:

| URL | Title | Target Keywords | Excerpt |
|-----|-------|-----------------|---------|
| https://knacert.com.vn/ma-tran-swot/ | Ma Trận SWOT Là Gì | ma trận swot, swot, phân tích swot | Hướng dẫn phân tích ma trận SWOT chi tiết |
| https://knacert.com.vn/iso-9001/ | ISO 9001 Là Gì | iso 9001, chứng nhận iso 9001, tiêu chuẩn iso | Tiêu chuẩn quản lý chất lượng ISO 9001:2015 |

- **URL** — URL đầy đủ của bài viết trên WordPress
- **Title** — Tiêu đề bài viết
- **Target Keywords** — Các từ khóa mục tiêu, cách nhau bằng dấu phẩy
- **Excerpt** — Mô tả ngắn hoặc meta description

---

## Cài đặt xác thực Google Sheets (một lần)

1. Vào [Google Cloud Console](https://console.cloud.google.com) → tạo project mới
2. **APIs & Services → Enable APIs** → bật **Google Sheets API**
3. **IAM & Admin → Service Accounts** → tạo service account → **Create Key → JSON** → lưu file về máy
4. Mở Google Sheet → **Share** → nhập email của service account (Editor)
5. Set env vars:

```powershell
$env:GOOGLE_SERVICE_ACCOUNT_JSON = "C:\path\to\service-account.json"
$env:SEO_SHEET_ID = "ID_CUA_GOOGLE_SHEET"   # phần ID trong URL spreadsheet
```

---

## Workflow

### Bước 1 — Keyword Mapping

Map 100 từ khóa GSC vào từng bài viết phù hợp nhất.

```powershell
cd internal-linking
python keyword_mapper.py --articles-from-sheet --push-to-sheet
```

Kết quả:
- File `keyword_mapping.csv` lưu local
- Tab **Keyword Mapping** tự tạo trong Google Sheet

Cột quan trọng trong output:
- **Mapped URL** — bài viết được gán cho từ khóa này
- **Confidence** — Cao / Trung bình / Thấp / Không khớp
- Nếu nhiều từ khóa "Không khớp" → thêm bài viết vào tab Articles

---

### Bước 2 — Tìm Internal Link

Tìm cơ hội link giữa các bài dựa trên độ tương đồng từ khóa.

```powershell
python link_finder.py --articles-from-sheet --push-to-sheet
```

Kết quả:
- File `internal_links.csv` lưu local
- Tab **Internal Links** tự tạo trong Google Sheet (không ghi đè dữ liệu cũ)

---

### Bước 3 — Review và duyệt link

Trong tab **Internal Links** của Google Sheet:

| Cột Status | Ý nghĩa |
|------------|---------|
| `pending` | Chưa review |
| `approved` | Duyệt — sẽ được chèn vào WordPress |
| `rejected` | Bỏ qua |

Đổi các link muốn chèn sang `approved`.

---

### Bước 4 — Chèn link vào WordPress

Set env vars WordPress trước:

```powershell
$env:WORDPRESS_SITE_URL    = "https://knacert.com.vn"
$env:WORDPRESS_USERNAME    = "admin@knacert.com"
$env:WORDPRESS_APP_PASSWORD = "xxxx xxxx xxxx xxxx"
```

Thử trước với `--dry-run` (không thay đổi gì):

```powershell
python link_inserter.py --from-sheet --dry-run
```

Chèn thật:

```powershell
python link_inserter.py --from-sheet
```

Script tự động:
- Tìm bài WordPress theo slug từ URL
- Chèn `<a href="target">anchor</a>` tại lần xuất hiện đầu tiên của anchor text (chưa được link)
- Cập nhật Status thành `inserted` trong Sheet

---

## Cấu hình nâng cao

Sửa `config.py`:

| Biến | Mặc định | Ý nghĩa |
|------|----------|---------|
| `LINK_RELEVANCE_THRESHOLD` | `0.08` | Giảm để có nhiều gợi ý hơn, tăng để chặt hơn |
| `MAX_LINKS_PER_SOURCE` | `8` | Số link tối đa mỗi bài nguồn |
| `KEYWORD_MATCH_THRESHOLD` | `0.05` | Ngưỡng tối thiểu để map từ khóa |

---

## Dùng với CSV thay vì Google Sheet

Nếu chưa setup Google Sheets API, export tab Articles ra CSV và dùng:

```powershell
python keyword_mapper.py --articles articles.csv
python link_finder.py --articles articles.csv
python link_inserter.py --input internal_links.csv --dry-run
```
