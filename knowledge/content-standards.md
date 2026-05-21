# Content Standards

## Brand voice

Giọng viết của KNA CERT cần chuyên nghiệp, rõ ràng, có chiều sâu và trung lập. Nội dung nên thể hiện vai trò chuyên gia đồng hành, không dùng giọng bán hàng áp lực.

Nên dùng:

- “đào tạo”, “chứng nhận”, “hướng dẫn áp dụng”, “hỗ trợ”, “đồng hành”
- “chuẩn quốc tế”, “thực chất”, “minh bạch”, “năng lực chuyên môn”
- “đối tác EcoVadis được công nhận”

Không dùng:

- “giá rẻ”, “rẻ”, “chi phí rẻ”, “giá cạnh tranh”
- “nhanh gọn”, “trọn gói”, “thời gian ngắn”
- “mua bán chứng chỉ”
- “cấp chứng chỉ trong vài ngày/vài tuần”
- “ủy quyền EcoVadis”
- Cụm “tư vấn và chứng nhận” để mô tả KNA.

## Cấu trúc bài SEO

Mỗi bài SEO nên có:

- Title chứa keyword chính, tự nhiên, 50-80 ký tự khi phù hợp.
- Mở bài trả lời trực tiếp nhu cầu tìm kiếm trong 100-150 từ đầu.
- H2 theo các intent phụ: định nghĩa, đối tượng áp dụng, quy trình, lợi ích, chi phí/yếu tố ảnh hưởng, FAQ.
- H3 chỉ dùng khi cần chia nhỏ ý dưới H2.
- Bảng khi so sánh tiêu chí, quy trình hoặc loại chứng nhận.
- CTA tự nhiên, không gây áp lực.
- 2-5 internal links cho bài khoảng 2.000 từ.

## Chuẩn WordPress HTML

Khi chuyển bài sang HTML:

- Không đưa `<h1>` vào body; WordPress dùng title làm H1.
- Dùng inline style theo `bai-viet-kna/SKILL.md`.
- Không thêm style vào `<li>` hoặc `<strong>`.
- Giữ nguyên nội dung nguồn, không rút gọn nếu nhiệm vụ là format/tối ưu.
- Ảnh cần có `alt`, `width`, `height`, `loading="lazy"` và nên bọc trong `<figure>`.
- Shortcode `[kna_link]` phải đứng riêng, không nằm trong paragraph, list item, heading hoặc link.

## Meta SEO

| Trường | Quy tắc |
| --- | --- |
| Meta title | 55-60 ký tự khi khả thi, chứa keyword chính và brand nếu còn chỗ |
| Meta description | 140-160 ký tự, chứa keyword, nêu giá trị và CTA nhẹ |
| Slug | Viết thường, bỏ dấu, nối bằng dấu gạch ngang |
| Focus keyword | Bám sát intent chính, không chọn keyword quá rộng nếu trang BOFU |

## E-E-A-T

Nội dung nên bổ sung:

- Tên tiêu chuẩn, phiên bản, tổ chức ban hành hoặc phạm vi áp dụng khi có.
- Dẫn chứng từ tiêu chuẩn, cơ quan công nhận, quy định hoặc nguồn chính thức.
- Ngày cập nhật.
- Tác giả hoặc chuyên gia rà soát nếu nội dung có tính chuyên môn cao.
- Phân biệt rõ KNA trực tiếp chứng nhận trong phạm vi nào và dịch vụ nào là đào tạo/hướng dẫn/hỗ trợ.

## Checklist trước xuất bản

- Không có từ/cụm từ cấm.
- Không có claim vượt quá năng lực thật.
- Không có H1 trong body.
- Keyword chính xuất hiện tự nhiên trong title, mở bài, ít nhất một H2 và meta.
- Internal link không trùng lặp, anchor tự nhiên.
- CTA phù hợp intent.
- FAQ trả lời ngắn, rõ và có thể dùng cho schema nếu cần.
- Thông tin hotline đúng: `093.2211.786`.

## Chuẩn content brief trước khi viết

Mỗi bài hoặc trang SEO cần có brief trước khi sản xuất. Không bắt đầu viết nếu chưa rõ các trường sau:

| Trường | Yêu cầu |
| --- | --- |
| Keyword chính | Một keyword đại diện intent chính, không chọn quá rộng |
| Keyword phụ | 5-15 biến thể, câu hỏi hoặc thực thể liên quan |
| Search intent | Thông tin, thương mại, giao dịch, điều hướng, địa phương hoặc hỗ trợ |
| Funnel | TOFU, MOFU, BOFU hoặc Retention |
| Loại trang | Blog, pillar, trang dịch vụ, FAQ, comparison, địa phương |
| Cụm dịch vụ | Gắn với một service cluster trong Brand Framework |
| Persona chính | Giám đốc nhà máy, QA Manager, chủ doanh nghiệp, ESG Manager hoặc nhóm cụ thể khác |
| Mục tiêu chuyển đổi | Gọi hotline, gửi form, tải tài liệu, đăng ký đánh giá, đọc trang dịch vụ |
| URL đích | URL hiện có hoặc URL đề xuất |
| Internal links bắt buộc | Trang pillar, trang dịch vụ, bài hỗ trợ |
| Nguồn cần tham khảo | Tiêu chuẩn, cơ quan công nhận, Google Search Central, nguồn pháp lý hoặc nguồn ngành |
| Claim cần kiểm tra | Năng lực chứng nhận, con số credentials, partnership, thời gian, chi phí |

## Kiểm tra SERP và intent

Trước khi viết, cần kiểm tra SERP thủ công hoặc bằng dữ liệu có sẵn:

- Google đang ưu tiên loại trang nào: blog, service page, video, PDF, trang nhà nước, glossary hay forum.
- Các kết quả top 5 trả lời intent gì và còn thiếu góc nào.
- Có SERP feature nào quan trọng: People Also Ask, featured snippet, video, image pack, local pack, AI Overview.
- Keyword có rủi ro nhiều nghĩa hoặc không phù hợp dịch vụ KNA không.
- Có trang KNA hiện có đang rank cho keyword này không để tránh cannibalization.

Nếu SERP chủ yếu là tài liệu pháp lý/chính phủ, nội dung KNA cần đóng vai trò giải thích ứng dụng thực tế cho doanh nghiệp, không cố thay thế nguồn gốc pháp lý.

## Chuẩn theo loại nội dung

### Bài blog TOFU

Dùng cho truy vấn "là gì", "quy trình", "cách", "tiêu chuẩn", "đối tượng áp dụng".

Bắt buộc có:

- Định nghĩa ngắn ở đầu bài.
- Giải thích theo ngôn ngữ dễ hiểu cho người không chuyên.
- Bảng tóm tắt nếu chủ đề có nhiều tiêu chí.
- FAQ cuối bài.
- Internal link về pillar hoặc trang dịch vụ phù hợp.
- CTA nhẹ: tìm hiểu thêm, kiểm tra doanh nghiệp có phù hợp không, liên hệ hỗ trợ.

### Bài MOFU

Dùng cho truy vấn so sánh, lựa chọn, chuẩn bị audit, buyer requirement.

Bắt buộc có:

- Bối cảnh ra quyết định của doanh nghiệp.
- Tiêu chí so sánh rõ.
- Lợi ích, rủi ro, điều kiện áp dụng.
- Case hoặc ví dụ ngành nếu có.
- Link về trang dịch vụ BOFU.

### Trang dịch vụ BOFU

Dùng cho keyword giao dịch như dịch vụ, chứng nhận, đào tạo, đăng ký, báo giá.

Bắt buộc có:

- Offer rõ: KNA cung cấp gì, trong phạm vi nào.
- Đối tượng phù hợp.
- Quy trình triển khai.
- Hồ sơ/thông tin doanh nghiệp cần chuẩn bị nếu có.
- Năng lực và credentials liên quan.
- CTA rõ nhưng không gây áp lực.
- FAQ xử lý phản đối: chi phí, thời gian, phạm vi, chứng chỉ, sau chứng nhận.

### Pillar page

Dùng cho chủ đề rộng cần gom cluster.

Bắt buộc có:

- Tổng quan chủ đề.
- Các nhánh nội dung con.
- Bảng điều hướng tới bài con/trang dịch vụ.
- Internal link mạnh hai chiều.
- Cập nhật định kỳ khi có bài con mới.

## Chuẩn nguồn và trích dẫn

Khi bài nói về tiêu chuẩn, quy định, ESG, carbon, chứng nhận hoặc chính sách Google:

- Ưu tiên nguồn chính thức: ISO, IAF, BoA, APAC, cơ quan nhà nước, EU, Google Search Central, web.dev.
- Không dùng blog đối thủ làm nguồn duy nhất cho claim chuyên môn.
- Không copy dài từ nguồn; diễn giải lại bằng ngôn ngữ KNA.
- Ghi nguồn ở cuối bài hoặc trong phần tham khảo nếu nội dung có tính chuyên môn cao.
- Với thông tin có thể thay đổi theo thời gian, thêm ngày cập nhật.

## Quy tắc claim cho KNA

Luôn kiểm tra claim trước khi xuất bản:

- Chỉ nói KNA trực tiếp chứng nhận khi nằm trong phạm vi năng lực đã được xác nhận.
- Các dịch vụ ngoài phạm vi chứng nhận trực tiếp phải dùng "đào tạo", "hướng dẫn áp dụng", "hỗ trợ" hoặc mô tả tương đương đã được duyệt.
- EcoVadis dùng "đối tác được công nhận", không dùng "ủy quyền".
- Không cam kết kết quả audit, thời gian cấp chứng chỉ hoặc chi phí nếu chưa có căn cứ.
- Không dùng "đảm bảo đạt", "bao đậu", "cấp nhanh", "giá rẻ".

## Chuẩn chống thin content và scaled content

Không xuất bản bài nếu:

- Nội dung chỉ thay tên tiêu chuẩn từ một template cũ.
- Không có thông tin riêng cho ngành, đối tượng hoặc quy trình áp dụng.
- Không trả lời thêm điều gì so với các kết quả top SERP.
- Không có internal link hoặc bước tiếp theo rõ.
- Nội dung AI chưa được rà soát bởi người hiểu chủ đề.

Mỗi bài mới cần có ít nhất một trong các giá trị riêng:

- Checklist thực tế.
- Bảng so sánh rõ.
- Quy trình KNA.
- Lỗi doanh nghiệp thường gặp.
- Ví dụ theo ngành.
- Giải thích khác biệt giữa các tiêu chuẩn/chứng nhận liên quan.
- Câu hỏi khách hàng thật.

## Chuẩn hình ảnh

- Ảnh đầu bài nên liên quan trực tiếp đến chủ đề, không dùng ảnh minh họa chung chung nếu có lựa chọn tốt hơn.
- Alt text mô tả ảnh bằng 5-15 từ và chứa keyword khi tự nhiên.
- Không nhồi keyword trong alt.
- Ảnh cần có kích thước rõ để giảm CLS.
- Nếu ảnh là sơ đồ/quy trình, caption cần giải thích giá trị của hình.
- Tên file ảnh nên viết thường, bỏ dấu, có keyword hoặc mô tả ngắn.

## Chuẩn schema

Schema không thay thế nội dung tốt, nhưng giúp Google hiểu rõ trang.

Ưu tiên:

- `Organization` cho thông tin KNA.
- `BreadcrumbList` cho đường dẫn điều hướng.
- `Article` hoặc `BlogPosting` cho bài kiến thức.
- `FAQPage` khi FAQ hiển thị thật trên trang.
- `Service` cho trang dịch vụ nếu phù hợp với cấu trúc website.

Quy tắc:

- Structured data phải khớp nội dung hiển thị.
- Không markup nội dung ẩn hoặc không có trên trang.
- Test bằng Rich Results Test nếu có khả năng triển khai.

## Workflow sản xuất content

1. Chọn keyword và lập brief.
2. Kiểm tra SERP, intent và trang KNA hiện có.
3. Chọn loại trang và cluster.
4. Lập outline theo intent, persona và mục tiêu chuyển đổi.
5. Viết nháp theo brand voice và people-first content.
6. Bổ sung nguồn, bảng, FAQ, internal links, CTA.
7. Kiểm tra claim, từ cấm, E-E-A-T và thin content.
8. Chuyển sang WordPress HTML nếu cần.
9. Tạo meta title, meta description, slug.
10. Rà soát cuối bằng checklist và ghi ngày cập nhật.

## Definition of Done

Một bài/trang SEO KNA chỉ được xem là hoàn tất khi:

- Brief đầy đủ và intent rõ.
- Không cannibalize URL hiện có.
- Nội dung khớp loại trang và funnel.
- Có thông tin riêng của KNA hoặc insight thực tế.
- Không vi phạm brand rules hoặc spam policies.
- Có nguồn chính thức khi nói về tiêu chuẩn/quy định.
- Có title, meta description, slug, heading structure.
- Có internal links vào/ra phù hợp.
- Có CTA đúng giai đoạn funnel.
- Có ảnh, alt text và kích thước ảnh nếu bài dùng hình.
- Có FAQ nếu intent cần.
- Có author/reviewer hoặc ngày cập nhật cho chủ đề chuyên môn cao.
- Sẵn sàng paste vào WordPress hoặc xuất bản theo workflow hiện hành.
