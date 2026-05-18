# Workflow xử lý bài viết KNA từ Google Sheet

## Mục tiêu

Khi người dùng điền link nội dung vào cột `Link Nội dung`, Codex đọc nội dung đó, dùng skill `$bai-viet-kna` để xử lý bài viết, tạo Google Doc chứa kết quả, rồi ghi link Google Doc vào cột `Link Xử Lý`.

## Sheet nguồn

- Spreadsheet: `Fomat Bài Viết`
- Tab nhập liệu: `Trang tính1`
- Cột A: `STT`
- Cột B: `Title`
- Cột C: `Link Nội dung`
- Cột D: `Link Xử Lý`

## Điều kiện xử lý một dòng

Chỉ xử lý dòng khi:

- `Link Nội dung` có link Google Doc hoặc file nội dung đọc được.
- `Link Xử Lý` đang trống.

Bỏ qua dòng khi:

- `Link Nội dung` trống.
- `Link Xử Lý` đã có link.
- Link nội dung không truy cập được.

## Quy trình cho mỗi dòng

1. Đọc dòng cần xử lý trong `Trang tính1`.
2. Mở link ở cột `Link Nội dung` bằng Google Drive connector.
3. Lấy toàn bộ nội dung bài viết.
4. Xác định dữ liệu đầu vào cho `$bai-viet-kna`:
   - Nội dung bài viết: lấy từ link.
   - Từ khóa chính: ưu tiên dòng `TỪ KHÓA CHÍNH` nếu có trong nội dung; nếu không có, suy luận từ `Title`.
   - Từ khóa phụ: lấy từ nội dung nếu có dòng `TỪ KHÓA PHỤ`; nếu không có thì để trống.
   - Internal links: lấy từ nội dung nếu có phần `INTERNAL LINKS`; nếu không có thì để trống.
5. Dùng `$bai-viet-kna` để tạo đủ 4 phần:
   - HTML body.
   - META SEO.
   - CHECKLIST ON-PAGE.
   - CÁC ĐIỀU CHỈNH NGÔN NGỮ.
6. Tạo Google Doc mới, đặt tên theo mẫu:
   - `Xử lý - [Title]`
7. Ghi toàn bộ kết quả xử lý vào Google Doc.
8. Ghi link Google Doc mới vào cột `Link Xử Lý`.

## Prompt vận hành

Khi cần chạy workflow, dùng yêu cầu:

```text
Chạy workflow bài viết KNA cho sheet này: https://docs.google.com/spreadsheets/d/1BWNaL7gdGfB4HXbc-UIvmYqahYgcgTTwnFIf-s98AD0/edit

Hãy xử lý tất cả dòng có Link Nội dung nhưng chưa có Link Xử Lý. Dùng $bai-viet-kna, tạo Google Doc kết quả, rồi ghi link Google Doc vào cột Link Xử Lý.
```

## Ghi chú

- Workflow này chạy bằng Codex và Google Drive connector, không phải công thức Google Sheets.
- Nếu muốn tự động chạy ngay khi nhập link mà không cần gọi Codex, cần tạo thêm Google Apps Script hoặc dịch vụ webhook có OpenAI API key.
