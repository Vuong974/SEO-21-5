# Tự động đăng bài WordPress từ Google Sheet

## File đã tạo

- `templates/wordpress-auto-post-template.csv`: template để import vào Google Sheets.
- `google-sheet-wordpress-autopost.gs`: Apps Script tự động đăng hoặc cập nhật bài qua WordPress REST API.

## Cách thiết lập

1. Mở Google Sheets và import file `templates/wordpress-auto-post-template.csv`.
2. Đổi tên tab thành `wordpress-auto-post-template` nếu Google Sheets đặt tên khác.
3. Vào `Extensions > Apps Script`.
4. Dán toàn bộ nội dung file `google-sheet-wordpress-autopost.gs`.
5. Trong hàm `setWordPressConfig()`, thay:
   - `YOUR_WORDPRESS_USERNAME`
   - `YOUR_WORDPRESS_APPLICATION_PASSWORD`
6. Chạy `setWordPressConfig()` một lần để lưu cấu hình vào Script Properties.
7. Chạy `setupSheetFormatting()` một lần để đổi tên tab, đóng băng tiêu đề và tạo dropdown.
8. Chạy `installAutoPostTrigger()` một lần để tạo trigger tự động.

## Cách nhập bài

Nhập dữ liệu từ dòng 3 trở xuống. Các cột quan trọng:

| Cột | Tên cột | Cách dùng |
| --- | --- | --- |
| B | Publish Action | `create`, `pending`, `update`, hoặc `skip` |
| C | WP Status | Nên dùng `draft`; chỉ dùng `publish` khi đã chắc chắn |
| D | Post Type | `posts` cho bài viết thường, `pages` cho trang, hoặc REST base khác |
| E | Post ID | Để trống khi tạo mới; nhập ID khi cập nhật |
| F | Title | Tiêu đề bài viết |
| G | Slug | Đường dẫn URL, có thể để trống |
| H | Content HTML | Nội dung bài viết dạng HTML |
| I | Excerpt | Mô tả ngắn |
| J | Categories | Tên chuyên mục; nhiều mục phân cách bằng dấu phẩy |
| K | Tags | Tên tag; nhiều tag phân cách bằng dấu phẩy |
| L | Featured Media ID | ID ảnh trong Media Library nếu có |
| O-R | Kết quả | Script tự ghi URL, trạng thái, lỗi, thời gian chạy |

## Quy tắc tự động đăng

- Sau khi nhập xong bài, đặt `Publish Action = create` hoặc `pending`.
- Script sẽ tự đổi tên/slug Categories và Tags sang ID rồi đăng bài lên `https://knacert.com.vn/wp-json/wp/v2/posts`.
- Nếu Tag chưa tồn tại trên WordPress, script sẽ tự tạo tag mới rồi gắn vào bài. Category vẫn cần tồn tại sẵn để tránh tạo sai danh mục.
- Không nhập ID trong giao diện Sheet; chỉ nhập/chọn tên trong dropdown. Việc đổi sang ID là trách nhiệm của Apps Script.
- Khi thành công, script ghi `WP URL`, `Post ID`, `Publish Status = success`, rồi đổi `Publish Action` về `skip` để tránh đăng trùng.
- Nếu lỗi, script ghi `Publish Status = error` và nội dung lỗi vào cột `Error`.

## Lưu ý an toàn

- Mặc định nên để `WP Status = draft`.
- Không nhập mật khẩu hoặc Application Password vào Google Sheet.
- Dùng WordPress Application Password, không dùng mật khẩu đăng nhập chính.
- Với bài cập nhật, bắt buộc nhập `Post ID` và đặt `Publish Action = update`.
