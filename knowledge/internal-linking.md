# Internal Linking

## Mục tiêu

Internal linking giúp Google hiểu cấu trúc topic cluster, phân phối authority về trang dịch vụ quan trọng và dẫn người đọc tới bước tiếp theo phù hợp.

## Nguyên tắc

- Mỗi bài blog nên có 2-5 internal links nếu độ dài khoảng 2.000 từ.
- Ưu tiên link về trang pillar, trang dịch vụ và bài hỗ trợ trong cùng cluster.
- Không nhồi link trong đoạn mở bài nếu không tự nhiên.
- Anchor text phải mô tả đích đến, không dùng chung chung như “xem thêm” quá nhiều.
- Một URL chỉ nên xuất hiện một lần trong cùng bài, trừ trường hợp CTA hoặc navigation có lý do rõ.
- Không đặt internal link trong heading.

## Luồng link theo funnel

| Trang nguồn | Trang đích nên link |
| --- | --- |
| TOFU blog | Pillar, bài giải thích liên quan, trang dịch vụ nhẹ |
| MOFU guide/comparison | Trang dịch vụ, case study, checklist, FAQ |
| BOFU service page | Bài hỗ trợ niềm tin, FAQ, tiêu chuẩn liên quan |
| Pillar page | Các bài con và trang dịch vụ trọng điểm |

## Anchor text

Anchor tốt:

- Có tên tiêu chuẩn hoặc chủ đề cụ thể: “ISO 9001”, “đánh giá EcoVadis”, “kiểm kê khí nhà kính ISO 14064-1”.
- Phù hợp ngữ cảnh câu.
- Không lặp chính xác keyword quá nhiều trên toàn site.

Tránh:

- Anchor quá tối ưu kiểu spam.
- Anchor không nói rõ đích đến.
- Link vào trang không giải quyết nhu cầu được nhắc trong câu.

## Quy trình tối ưu internal link

1. Xác định cluster và URL mục tiêu cần đẩy.
2. Tìm bài liên quan trong cùng cluster.
3. Chọn đoạn có ngữ cảnh tự nhiên.
4. Thêm link một lần bằng anchor mô tả rõ.
5. Kiểm tra không phá vỡ HTML WordPress.
6. Ghi nhận URL nguồn, URL đích, anchor và ngày cập nhật.

## Khi dùng script

Tham khảo `internal-linking/README.md` và các script:

- `keyword_mapper.py`: map keyword với URL.
- `link_finder.py`: tìm cơ hội link.
- `link_inserter.py`: chèn link.
- `seo-kna-apps-script.gs`: hỗ trợ workflow Google Sheets.

Sau khi chạy tự động, luôn rà soát thủ công các điểm:

- Anchor có tự nhiên không.
- Link có đúng intent không.
- Có bị trùng link hoặc link vào trang sai cluster không.
- HTML có bị lỗi thẻ không.

