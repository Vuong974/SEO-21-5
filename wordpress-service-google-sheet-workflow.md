# Workflow đăng bài Service KNA từ Google Sheet

## Mục tiêu

Đọc dữ liệu từ Google Sheet template, tạo HTML content cho custom post type `service`, đăng lên WordPress KNA Cert ở trạng thái `draft`/`pending`/`publish`, và ghi kết quả lại vào sheet.

**Google Sheet:**
```
https://docs.google.com/spreadsheets/d/1nDk557AjRnOa1q9X2gYYSu1R-_3elXldAqGVWKDPu2g/edit
```

**Tab nhập liệu (landing service mẫu ISO 9001):**
```
Service Landing ISO9001
```

---

## Cấu trúc cột (82 cột: A → CC)

### Nhóm A: Điều khiển (A–E)

| Cột | Tên | Giá trị hợp lệ |
|-----|-----|----------------|
| A | # | Số thứ tự (tự động) |
| B | Publish Action | `pending` / `create` / `update` / `skip` |
| C | WP Status | `draft` / `pending` / `publish` / `private` |
| D | Post ID | ID WordPress khi update; để trống khi tạo mới |
| E | Notes | Ghi chú nội bộ |

### Nhóm B: Metadata (F–K)

| Cột | Tên | Mô tả |
|-----|-----|-------|
| F | Title | Tiêu đề WordPress (hiện tab trình duyệt) |
| G | Slug | Đường dẫn URL, vd: `chung-nhan-iso-9001` |
| H | Excerpt | Mô tả ngắn ~150 ký tự (hiện ở listing) |
| I | Meta Title | SEO title ~60 ký tự |
| J | Meta Desc | SEO description ~160 ký tự |
| K | Featured Image URL | URL ảnh đại diện |

### Nhóm C: Hero Section (L–T)

| Cột | Tên | Mô tả |
|-----|-----|-------|
| L | Hero H1 | Tiêu đề lớn nhất đầu trang |
| M | Hero Subline | Dòng phụ bên dưới H1 |
| N | Hero Bullet 1 | Điểm mạnh #1 |
| O | Hero Bullet 2 | Điểm mạnh #2 |
| P | Hero Bullet 3 | Điểm mạnh #3 |
| Q | Hero Bullet 4 | Điểm mạnh #4 |
| R | Hero Bullet 5 | Điểm mạnh #5 (tuỳ chọn) |
| S | CTA 1 | Nút CTA 1, mặc định: `NHẬN BÁO GIÁ` |
| T | CTA 2 | Nút CTA 2, mặc định: `LIÊN HỆ NGAY` |

### Nhóm D: Quick Info Block (U–AB)

| Cột | Tên | Ví dụ |
|-----|-----|-------|
| U | QI Label 1 | `Thời gian giám sát` |
| V | QI Value 1 | `12 tháng/chu kỳ` |
| W | QI Label 2 | `Áp dụng` |
| X | QI Value 2 | `Mọi ngành, lĩnh vực, quy mô` |
| Y | QI Label 3 | `Hiệu lực chứng chỉ` |
| Z | QI Value 3 | `3 năm` |
| AA | QI Label 4 | `Công nhận` |
| AB | QI Value 4 | `170+ quốc gia` |

### Nhóm E: Nội dung chính (AC–AR)

| Cột | Tên | Mô tả |
|-----|-----|-------|
| AC | Intro | Đoạn mở đầu in đậm (~2–3 câu) |
| AD | H2 Là gì | Tiêu đề section, vd: `TIÊU CHUẨN ISO 9001 LÀ GÌ?` |
| AE | Là gì Content | Nội dung giải thích tiêu chuẩn |
| AF | H2 Áp dụng | Tiêu đề, vd: `DOANH NGHIỆP NÀO NÊN ÁP DỤNG?` |
| AG | Áp dụng Content | Mô tả đối tượng áp dụng |
| AH | H2 Lợi ích | Tiêu đề section lợi ích |
| AI | LI 1 Title | Lợi ích #1 – tiêu đề |
| AJ | LI 1 Content | Lợi ích #1 – nội dung |
| AK | LI 2 Title | Lợi ích #2 – tiêu đề |
| AL | LI 2 Content | Lợi ích #2 – nội dung |
| AM | LI 3 Title | Lợi ích #3 – tiêu đề |
| AN | LI 3 Content | Lợi ích #3 – nội dung |
| AO | LI 4 Title | Lợi ích #4 – tiêu đề |
| AP | LI 4 Content | Lợi ích #4 – nội dung |
| AQ | LI 5 Title | Lợi ích #5 – tiêu đề |
| AR | LI 5 Content | Lợi ích #5 – nội dung |

### Nhóm F: Quy trình (AS–AZ)

| Cột | Tên | Ghi chú |
|-----|-----|---------|
| AS | H2 Quy trình | Tiêu đề section |
| AT | Bước 1 | Gộp tiêu đề + mô tả vào 1 ô |
| AU | Bước 2 | — |
| AV | Bước 3 | — |
| AW | Bước 4 | — |
| AX | Bước 5 | — |
| AY | Bước 6 | Tuỳ chọn |
| AZ | Bước 7 | Tuỳ chọn |

### Nhóm G: Chứng nhận, Tại sao KNA, Chuẩn bị (BA–BG)

| Cột | Tên | Mô tả |
|-----|-----|-------|
| BA | (trống) | — |
| BB | H2 Chứng nhận | Tiêu đề section chứng chỉ |
| BC | Chứng nhận Content | Mô tả về giấy chứng nhận |
| BD | H2 Tại sao KNA | `TẠI SAO CHỌN KNA CERT?` |
| BE | Tại sao KNA Content | Các lý do chọn KNA (1–2 đoạn) |
| BF | H2 Chuẩn bị | `HỒ SƠ DOANH NGHIỆP CẦN CHUẨN BỊ` |
| BG | Chuẩn bị Items | Mỗi mục một dòng (Enter để ngắt) → tự động thành danh sách `<ul>` |

### Nhóm H: FAQ (BH–BR)

| Cột | Tên |
|-----|-----|
| BH | H2 FAQ |
| BI | FAQ 1 Câu hỏi |
| BJ | FAQ 1 Trả lời |
| BK | FAQ 2 Câu hỏi |
| BL | FAQ 2 Trả lời |
| BM | FAQ 3 Câu hỏi |
| BN | FAQ 3 Trả lời |
| BO | FAQ 4 Câu hỏi (tuỳ chọn) |
| BP | FAQ 4 Trả lời (tuỳ chọn) |
| BQ | FAQ 5 Câu hỏi (tuỳ chọn) |
| BR | FAQ 5 Trả lời (tuỳ chọn) |

### Nhóm I: CTA & Contact (BS–BT)

| Cột | Tên | Ví dụ |
|-----|-----|-------|
| BS | CTA Footer Text | `Liên hệ KNA CERT để được tư vấn...` |
| BT | Hotline | `0983.246.419` |

### Nhóm J: Taxonomy (BU–BY)

| Cột | Tên | Ghi chú |
|-----|-----|---------|
| BU | Service Type | Taxonomy `service-type` (tên hoặc slug) |
| BV | Industry | Taxonomy `industry` |
| BW | Cost | Taxonomy `service-cost` |
| BX | Time | Taxonomy `service-time` |
| BY | Tags | Phân cách bằng dấu phẩy |

### Nhóm K: Kết quả (BZ–CC) — tự động điền

| Cột | Tên |
|-----|-----|
| BZ | WP URL |
| CA | Publish Status |
| CB | Error |
| CC | Last Run |

---

## HTML được tạo ra

Script `service_landing_publisher.py` tự động tạo HTML theo cấu trúc sau:

```
<p><strong>[INTRO]</strong></p>
<h2>THÔNG TIN NHANH</h2>
<ul><li>QI Label 1: QI Value 1</li>...</ul>
<h2>[H2 LÀ GÌ]</h2>
<p>[Nội dung]</p>
<h2>[H2 ÁP DỤNG]</h2>
<p>[Nội dung]</p>
<h2>[H2 LỢI ÍCH]</h2>
<h3>[LI 1 Title]</h3><p>[LI 1 Content]</p> × 5
<h2>[H2 QUY TRÌNH]</h2>
<p>Bước 1: ... Bước 2: ... </p>
<h2>[H2 CHỨNG NHẬN]</h2>
<p>[Nội dung]</p>
<h2>[H2 CHUẨN BỊ]</h2>
<ul><li>Mục 1</li>...</ul>
<h2>[H2 TẠI SAO KNA]</h2>
<p>[Nội dung]</p>
<h2>[H2 FAQ]</h2>
<h3>[Câu hỏi 1]</h3><p>[Trả lời]</p> × 5
<p><strong>[CTA Footer]</strong></p>
<p>Hotline: ...</p>
```

---

## Điều kiện xử lý một dòng

**Xử lý khi:**
- `Title` có dữ liệu
- `Publish Action` = `pending`, `create`, hoặc `update`

**Bỏ qua khi:**
- `Publish Action` = `skip` hoặc trống
- `Title` trống
- `Action=create` nhưng `Post ID` đã có → báo lỗi
- `Action=update` nhưng `Post ID` trống → báo lỗi

---

## Cách setup sheet lần đầu

1. Mở Google Sheet: [link](https://docs.google.com/spreadsheets/d/1nDk557AjRnOa1q9X2gYYSu1R-_3elXldAqGVWKDPu2g/edit)
2. Vào **Extensions > Apps Script**
3. Paste toàn bộ nội dung file `service-landing-setup.gs`
4. Chạy hàm `setupTemplate()`
5. Tab `Service Landing ISO9001` sẽ được tạo tự động với:
   - Headers màu sắc theo nhóm
   - Dropdown validation cho các cột điều khiển
   - Dòng mẫu ISO 9001 ở hàng 4

---

## Cách dùng khi ra lệnh cho Claude

### Đăng bài mới (draft):
```
Đăng các bài trong tab "Service Landing ISO9001" có Publish Action = pending
lên WordPress https://knacert.com.vn ở trạng thái draft.
Sheet: https://docs.google.com/spreadsheets/d/1nDk557AjRnOa1q9X2gYYSu1R-_3elXldAqGVWKDPu2g/edit
Dùng script service_landing_publisher.py với --dry-run trước, sau đó hỏi xác nhận.
```

### Chạy bằng script Python (nếu sheet public view):
```bash
# Dry run trước
python service_landing_publisher.py \
  --sheet-id 1nDk557AjRnOa1q9X2gYYSu1R-_3elXldAqGVWKDPu2g \
  --dry-run

# Đăng thực tế
python service_landing_publisher.py \
  --sheet-id 1nDk557AjRnOa1q9X2gYYSu1R-_3elXldAqGVWKDPu2g \
  --output reports/service-publish-result.json
```

### Chạy từ file CSV đã export:
```bash
# Export sheet → File > Download > CSV
python service_landing_publisher.py \
  --csv "Service Landing ISO9001.csv" \
  --dry-run
```

---

## Biến môi trường cần thiết

```bash
WORDPRESS_SITE_URL=https://knacert.com.vn
WORDPRESS_USERNAME=<username>
WORDPRESS_APP_PASSWORD=<app password>
```

---

## Nguyên tắc an toàn

- Mặc định dùng `draft`, không `publish` hàng loạt nếu chưa duyệt.
- Luôn chạy `--dry-run` trước để preview HTML.
- Tạo/cập nhật từng dòng và ghi kết quả ngay sau mỗi dòng.
- Không lưu WordPress username/app password trong sheet.
- Nếu update bài cũ, backup content cũ trước khi gọi API.
- Nếu taxonomy không map được theo tên, ghi warning vào `Error` thay vì tạo mới tự động.

---

## Custom post type & taxonomy

```
Post type:    service
REST:         /wp-json/wp/v2/service
Taxonomies:   post_tag | industry | service-cost | service-time | service-type
```
