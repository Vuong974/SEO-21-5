# Workflow: Upload content -> bai-viet-kna -> Google Sheet WordPress

## Mục tiêu

Khi người dùng tải file content lên Codex, Codex dùng skill `bai-viet-kna` để chuẩn hóa bài viết thành HTML WordPress SEO, sau đó tự điền một dòng mới vào Google Sheet đăng bài WordPress.

Google Sheet mặc định:

https://docs.google.com/spreadsheets/d/1RKKodccAYToZeUzzsd24Z5WsNOK4bnUORPoBWy6t578/edit

Tab nhập bài:

`wordpress-auto-post-template`

## Câu lệnh sử dụng

Sau khi upload file content, dùng một trong các câu lệnh sau:

```text
Chạy workflow bai-viet-kna cho file tôi vừa upload và cập nhật vào Google Sheet.
Từ khóa chính: [keyword]
Categories: [tên danh mục]
Tags: [tag 1, tag 2]
```

Hoặc nếu file đã nằm trong workspace:

```text
Chạy workflow bai-viet-kna cho file: [đường dẫn file]
Từ khóa chính: [keyword]
Categories: [tên danh mục]
Tags: [tag 1, tag 2]
Cập nhật vào Google Sheet đăng bài.
```

## Quy tắc an toàn

- Mặc định ghi `Publish Action = skip`.
- Mặc định ghi `WP Status = draft`.
- Không tự đặt `Publish Action = pending/create` trừ khi người dùng yêu cầu rõ là đăng thử hoặc tạo bản nháp ngay.
- Không ghi đè dòng đã có `Post ID`, `WP URL`, hoặc `Publish Status = success`.
- Nếu chưa có `Categories`, dùng `Tin Tức Tiêu Chuẩn` cho bài kiến thức/tiêu chuẩn.
- Nếu chưa có `Tags`, suy luận từ từ khóa chính hoặc để trống.
- Không lưu WordPress username/password/Application Password vào Sheet.

## Input cần có

Tối thiểu:

- File content: `.txt`, `.md`, `.html`, hoặc nội dung người dùng paste trực tiếp.
- Từ khóa chính.

Tùy chọn:

- Từ khóa phụ/LSI.
- Internal URLs.
- Categories.
- Tags.
- Featured Media ID.

Nếu thiếu từ khóa chính, Codex được phép suy luận từ tiêu đề bài viết nhưng phải ghi vào `Notes`.

## Luồng xử lý của Codex

1. Đọc file content người dùng upload hoặc file trong workspace.
2. Dùng skill `bai-viet-kna`:
   - Nếu input là raw text: chạy workflow raw text.
   - Nếu input là HTML WordPress cũ: chạy workflow old WordPress HTML.
3. Bảo toàn đầy đủ nội dung nguồn, không tóm tắt, không bỏ đoạn.
4. Tạo đủ 4 phần output theo skill:
   - ARTICLE TITLE.
   - HTML body.
   - META SEO.
   - CHECKLIST ON-PAGE.
   - CÁC ĐIỀU CHỈNH NGÔN NGỮ.
5. Trích dữ liệu để điền Sheet.
6. Mở Google Sheet bằng Google Drive connector.
7. Tìm dòng trống đầu tiên từ hàng 3 trở xuống.
8. Ghi dữ liệu vào dòng trống.
9. Đọc lại dòng vừa ghi để xác nhận.

## Mapping sang Google Sheet

| Cột | Tên cột | Giá trị ghi |
| --- | --- | --- |
| A | Row | Số thứ tự tiếp theo |
| B | Publish Action | `skip` mặc định |
| C | WP Status | `draft` mặc định |
| D | Post Type | `posts` |
| E | Post ID | để trống |
| F | Title | `ARTICLE TITLE` từ skill, không có thẻ HTML |
| G | Slug | `Slug đề xuất` trong META SEO, bỏ dấu `/` đầu/cuối |
| H | Content HTML | Toàn bộ HTML body từ skill `bai-viet-kna`, không chứa `<h1>` |
| I | Excerpt | Meta Desc hoặc mô tả ngắn 140-160 ký tự |
| J | Categories | Tên category, ví dụ `Tin Tức Tiêu Chuẩn` |
| K | Tags | Tên tag, phân cách bằng dấu phẩy |
| L | Featured Media ID | nếu người dùng cung cấp |
| M | Meta Title | `Meta Title` trong META SEO |
| N | Meta Description | `Meta Desc` trong META SEO |
| O | WP URL | để trống |
| P | Publish Status | để trống |
| Q | Error | để trống |
| R | Last Run | để trống |
| S | Notes | Ghi nguồn file, từ khóa chính, checklist tóm tắt |

## Quy tắc điền Categories và Tags

Sheet đang dùng tên category/tag, không dùng ID ở giao diện nhập.

Ví dụ hợp lệ:

```text
Categories = Tin Tức Tiêu Chuẩn
Tags = ISO 9001, ISO
```

Apps Script `google-sheet-wordpress-autopost.gs` sẽ tự đổi tên/slug/ID sang ID khi đăng lên WordPress.

## Kiểm tra trước khi ghi Sheet

Trước khi ghi, Codex phải kiểm tra:

- `ARTICLE TITLE` có nội dung.
- `Content HTML` không chứa thẻ `<h1>`.
- HTML không bị rút gọn bằng placeholder.
- Meta Title có nội dung.
- Meta Description có nội dung.
- Slug có nội dung.
- `Content HTML` không rỗng.
- `Categories` là tên danh mục có trong tab `WP Categories` nếu connector đọc được tab này.
- `Tags` là tên tag có trong tab `WP Tags` nếu connector đọc được tab này.

Nếu thiếu dữ liệu quan trọng, vẫn ghi dòng nhưng để `Publish Action = skip` và ghi rõ lỗi/cảnh báo vào `Notes`.

## Sau khi cập nhật Sheet

Codex trả lời ngắn gọn:

- Link Google Sheet.
- Dòng đã ghi.
- Title.
- Slug.
- Categories.
- Tags.
- Trạng thái an toàn: `skip/draft`.

Người dùng chỉ đổi `Publish Action` sang `pending` khi đã kiểm tra xong và muốn tạo bản nháp WordPress.

## Prompt mẫu cho Codex

```text
Chạy workflow upload content -> bai-viet-kna -> Google Sheet.
File: [đường dẫn hoặc file vừa upload]
Từ khóa chính: [keyword]
Từ khóa phụ: [keyword phụ, nếu có]
Internal URLs:
- [url 1]
- [url 2]
Categories: Tin Tức Tiêu Chuẩn
Tags: [tag 1, tag 2]
Giữ Publish Action = skip để tôi kiểm tra trước.
```
