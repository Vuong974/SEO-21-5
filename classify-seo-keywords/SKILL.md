---
name: classify-seo-keywords
description: Phân loại danh sách từ khóa SEO theo ý định tìm kiếm, giai đoạn phễu, cụm chủ đề, loại SERP, nhóm người dùng, loại nội dung, giả định độ khó và mức ưu tiên kinh doanh. Dùng khi Codex cần phân nhóm từ khóa tiếng Việt hoặc tiếng Anh cho kế hoạch SEO, keyword mapping, topical clustering, content brief, chiến lược pillar-cluster, ecommerce category planning hoặc bảng phân loại từ khóa có thể đưa vào spreadsheet.
---

# Phân Loại Từ Khóa SEO

## Tổng Quan

Dùng skill này để biến danh sách từ khóa thô thành bảng phân loại SEO có thể triển khai cho content planning, cấu trúc website và keyword-to-page mapping. Ưu tiên các nhãn giúp ra quyết định thực tế thay vì chỉ phân loại học thuật.

Khi cần phân loại nhiều từ khóa nhất quán hoặc cần schema dạng spreadsheet, đọc thêm [taxonomy.md](references/taxonomy.md).

## Quy Trình

1. Chuẩn hóa danh sách từ khóa:
   - Loại trùng lặp, nhiễu viết hoa, tham số tracking, dấu câu thừa và biến thể sai chính tả rõ ràng.
   - Giữ dấu tiếng Việt khi dấu có ý nghĩa.
   - Giữ các từ khóa gần giống nhau nếu chúng khác ý định, modifier, loại sản phẩm, địa điểm, nhóm người dùng hoặc giai đoạn phễu.

2. Suy luận bối cảnh ngành:
   - Xác định niche, sản phẩm hoặc dịch vụ, địa lý, ngôn ngữ, đối tượng mục tiêu và đường chuyển đổi từ prompt hoặc từ chính danh sách keyword.
   - Nếu thiếu bối cảnh, đưa ra giả định thận trọng và đánh dấu các trường chưa chắc là `Cần rà soát`.

3. Phân loại từng từ khóa với các trường cốt lõi:
   - `tu_khoa`
   - `y_dinh_chinh`: Thông tin, Thương mại, Giao dịch, Điều hướng, Địa phương, Hỗ trợ
   - `giai_doan_pheu`: TOFU, MOFU, BOFU, Retention
   - `cum_chu_de`
   - `loai_trang`: Bài blog, Trang pillar, Trang danh mục, Trang sản phẩm/dịch vụ, Landing page, Trang so sánh, FAQ/hỗ trợ, Trang địa phương, Trang chủ/brand
   - `goc_noi_dung`
   - `gia_dinh_serp`
   - `gia_tri_kinh_doanh`: Cao, Trung bình, Thấp
   - `uu_tien_seo`: Cao, Trung bình, Thấp
   - `ghi_chu`

4. Nhóm và mapping từ khóa:
   - Gán một `tu_khoa_chinh` cho mỗi trang dự kiến.
   - Gộp biến thể gần và long-tail hỗ trợ vào cùng một trang khi ý định tìm kiếm giống nhau.
   - Tách thành trang riêng khi ý định SERP, danh mục sản phẩm, nhóm người dùng, địa điểm hoặc hành động chuyển đổi khác nhau.

5. Ưu tiên triển khai:
   - Ưu tiên từ khóa có intent rõ, liên quan mạnh đến kinh doanh và có loại trang mà website có thể đáp ứng.
   - Không mặc định volume cao là ưu tiên cao.
   - Đánh dấu từ khóa cần kiểm tra SERP, đặc biệt là head term mơ hồ và keyword có mixed intent.

## Quy Tắc Phân Loại

- Xem `mua`, `giá`, `báo giá`, `dịch vụ`, `đặt`, `tư vấn`, `gần đây`, `ở đâu`, tên brand/model sản phẩm và modifier địa điểm là tín hiệu chuyển đổi.
- Xem `là gì`, `cách`, `hướng dẫn`, `kinh nghiệm`, `mẹo`, `review`, `so sánh`, `tốt nhất`, `nên chọn` là tín hiệu thông tin hoặc thương mại tùy mức độ gần với hành vi mua.
- Phân loại keyword so sánh là Thương mại, trừ khi câu chữ thể hiện ý định mua ngay.
- Phân loại keyword chỉ có brand là Điều hướng; brand + sản phẩm/dịch vụ có thể là Giao dịch hoặc Thương mại.
- Phân loại modifier địa phương như thành phố, quận, `gần tôi`, `near me`, `tại Hà Nội`, `TPHCM` là Địa phương cộng với intent nền.
- Dùng Hỗ trợ cho truy vấn lỗi, bảo hành, tài liệu hướng dẫn, đăng nhập, chính sách, cài đặt và hậu mãi.
- Ưu tiên intent của trang hơn cấu trúc ngữ pháp của keyword. Ví dụ: `máy lọc nước kangaroo giá` nên map vào trang sản phẩm/danh mục hoặc landing page thương mại, không phải bài blog.

## Định Dạng Đầu Ra

Mặc định dùng bảng Markdown cho danh sách ngắn. Với danh sách lớn hoặc khi người dùng nhắc Excel, CSV, Google Sheets hoặc spreadsheet, xuất bảng có cột thân thiện CSV và tránh ô nhiều dòng.

Bảng rút gọn khuyến nghị:

```text
tu_khoa | y_dinh_chinh | giai_doan_pheu | cum_chu_de | loai_trang | goc_noi_dung | gia_tri_kinh_doanh | uu_tien_seo | ghi_chu
```

Bảng mở rộng khuyến nghị:

```text
tu_khoa | tu_khoa_chuan_hoa | y_dinh_chinh | y_dinh_phu | giai_doan_pheu | cum_chu_de | chu_de_con | loai_trang | tu_khoa_chinh | vai_tro_tu_khoa | goc_noi_dung | gia_dinh_serp | gia_tri_kinh_doanh | uu_tien_seo | do_tin_cay | ghi_chu
```

Dùng `do_tin_cay` là Cao, Trung bình hoặc Thấp. Đặt Thấp khi intent phụ thuộc nhiều vào SERP thực tế, quyền sở hữu brand, phạm vi địa phương hoặc mô hình kinh doanh chưa rõ.

## Kiểm Tra Chất Lượng

Trước khi hoàn tất:

- Kiểm tra các từ khóa được gán vào cùng một trang có cùng intent chính.
- Kiểm tra keyword BOFU không bị map vào bài blog thông tin chung chung.
- Kiểm tra một keyword không bị gán làm từ khóa chính cho nhiều trang, trừ khi chiến lược trang cố ý tách theo địa điểm, nhóm người dùng hoặc danh mục sản phẩm.
- Đánh dấu rủi ro cannibalization khi hai trang dự kiến sẽ cạnh tranh cùng một truy vấn.
- Thêm tóm tắt ngắn về các cụm chủ đề, trang ưu tiên và giả định chưa chắc chắn sau bảng.
