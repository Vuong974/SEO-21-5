# Kiểm tra cấu trúc gắn chuyên gia KNA CERT

Ngày kiểm tra: 2026-05-25

## Kết luận

Website không nên gắn chuyên gia bằng cách chèn HTML vào nội dung bài viết. Cấu trúc hiện tại có post type riêng tên `expert`, và theme có component hiển thị chuyên gia dạng `author-expert`.

Tuy nhiên, field liên kết giữa `post` và `expert` chưa được expose qua WordPress REST API hiện tại, nên chưa thể cập nhật đúng cơ chế chọn chuyên gia bằng REST nếu chưa biết meta key hoặc chưa có endpoint riêng.

## Bằng chứng kỹ thuật

- REST namespace có post type `expert`: `/wp-json/wp/v2/expert`
- 5 chuyên gia hiện có là các item thuộc custom post type `expert`
- Cao Thế Hiệp có ID `657`, URL `https://knacert.com.vn/chuyen-gia/cao-the-hiep/`
- Post type `post` có `supports.custom-fields = true`
- REST `wp/v2/posts/{id}?context=edit` chỉ expose:
  - `meta._acf_changed`
  - `meta.footnotes`
  - `acf: []`
- ACF REST endpoint `/wp-json/acf/v3/...` không tồn tại hoặc chưa bật
- XML-RPC `/xmlrpc.php` bị chặn `403 Forbidden`
- Admin edit screen không truy cập được bằng Application Password; request bị trả về trang chủ

## Điều này có nghĩa gì

Muốn tự động gắn chuyên gia đúng như thao tác chọn trong admin, cần một trong các điều kiện sau:

1. Biết chính xác meta key lưu chuyên gia trong database.
2. Bật `show_in_rest` cho field/meta chuyên gia.
3. Có custom REST endpoint để set expert cho post.
4. Có quyền SSH/WP-CLI/database để đọc và cập nhật post meta.
5. Có một bài mẫu đã gắn chuyên gia đúng trong admin để đối chiếu cấu trúc render và nếu có quyền DB/WP-CLI thì truy ra meta.

## Không nên làm

- Không chèn block chuyên gia trực tiếp vào `post_content`.
- Không đổi WordPress author sang chuyên gia, vì expert là custom post type riêng, không phải user author.
- Không cập nhật `meta` qua REST khi field chưa được register, vì WordPress sẽ bỏ qua hoặc từ chối field không expose.

