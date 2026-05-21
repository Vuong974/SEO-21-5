# SEO Research Agent

Agent này dùng cho các việc SEO cần nghiên cứu trước khi triển khai: lập kế hoạch nội dung, phân loại từ khóa, tối ưu money page, refresh bài cũ, xây topic cluster, internal linking, phân tích đối thủ, hoặc viết content brief.

Nguyên tắc chính: **research trước, làm sau**. Không viết bài, không sửa sheet, không đề xuất kế hoạch lớn nếu chưa có phần nghiên cứu được lưu lại trong project.

## Khi Nào Dùng

- Cần hiểu một chủ đề SEO mới trước khi tạo bài hoặc template.
- Cần kiểm tra SERP, intent, đối thủ, keyword, persona, dịch vụ KNA.
- Cần tạo brief bài SEO, topic cluster, content plan, keyword map.
- Cần tối ưu trang dịch vụ nhưng chưa rõ vấn đề hiện tại.
- Cần quyết định nên tạo mới, refresh, gộp bài hay internal link.

## Quy Trình Bắt Buộc

1. Xác định yêu cầu:
   - Mục tiêu SEO là gì?
   - Trang/dịch vụ/cụm chủ đề nào?
   - Output cuối cùng cần tạo là gì?

2. Đọc nguồn nội bộ:
   - `Brand KNA/KNA_Brand_Framework_v1.1.md`
   - `classify-seo-keywords/SKILL.md`
   - `classify-seo-keywords/references/taxonomy.md`
   - `internal-linking/README.md`
   - Workflow liên quan nếu có.

3. Nghiên cứu nguồn ngoài khi cần:
   - SERP thực tế.
   - Website đối thủ.
   - Tài liệu tiêu chuẩn/quy định chính thức.
   - Website KNA hiện tại.

4. Lưu kết quả research:
   - Tạo file trong `research-output/YYYY-MM-DD/`.
   - Dùng template `templates/research-report.md`.
   - Nếu có nhiều URL/nguồn, thêm bảng nguồn hoặc `source-log.csv`.

5. Chốt insight:
   - Intent chính.
   - Persona.
   - Funnel.
   - Cụm dịch vụ KNA.
   - Content gap.
   - Rủi ro cannibalization.
   - Hành động SEO đề xuất.

6. Chỉ sau đó mới triển khai:
   - Viết brief.
   - Tạo Google Sheet.
   - Tối ưu bài/trang.
   - Lập internal link.
   - Phân loại keyword.

## Cấu Trúc Thư Mục

```text
agents/seo-research-agent/
  README.md
  AGENT.md
  templates/
    research-report.md
    source-log.csv
  research-output/
    README.md
```

## Quy Ước Đặt Tên Report

```text
YYYY-MM-DD--chu-de-ngan.md
```

Ví dụ:

```text
2026-05-20--ecovadis-topic-cluster.md
2026-05-20--iso-9001-money-page-audit.md
2026-05-20--phan-loai-tu-khoa-esg.md
```

## Tiêu Chuẩn Hoàn Thành

Một nhiệm vụ research chỉ được xem là xong khi có:

- File report trong `research-output/YYYY-MM-DD/`.
- Tóm tắt insight chính.
- Danh sách nguồn đã dùng.
- Khuyến nghị hành động rõ ràng.
- Output triển khai nếu người dùng yêu cầu.
