# SEO Research Report: Thiết lập SEO Research Agent cho KNA

## 1. Tóm Tắt

- **Ngày nghiên cứu:** 2026-05-20
- **Người/agent thực hiện:** Codex
- **Mục tiêu:** Tạo một agent chuyên nghiên cứu SEO trước khi triển khai công việc cho KNA.
- **Đầu ra cần tạo sau research:** Bộ hướng dẫn agent, workflow, template report và thư mục lưu kết quả research.
- **Phạm vi:** Project local `SEO-KNA-main`.

## 2. Nguồn Nội Bộ Đã Đọc

| Nguồn | Phần liên quan | Insight lấy ra |
| --- | --- | --- |
| `Brand KNA/KNA_Brand_Framework_v1.1.md` | Brand positioning, service clusters, SEO content framework | Agent phải map mọi nghiên cứu về cụm dịch vụ, persona, funnel, CTA và brand voice của KNA. |
| `classify-seo-keywords/SKILL.md` | Quy trình phân loại keyword | Agent cần phân loại intent, funnel, loại trang, business value và ưu tiên SEO trước khi đề xuất hành động. |
| `classify-seo-keywords/references/taxonomy.md` | Taxonomy intent/funnel | Dùng nhãn thống nhất cho keyword research và content planning. |
| `internal-linking/README.md` | Workflow internal link | Research nên tạo được input cho keyword mapping và internal link plan. |
| `bai-viet-kna/SKILL.md` | Quy tắc bài viết KNA | Khi chuyển sang viết brief/bài, phải giữ giọng chuyên nghiệp, tránh claim yếu và gắn author/expert. |

## 3. Nguồn Ngoài Đã Kiểm Tra

Không cần nguồn ngoài cho nhiệm vụ thiết lập agent. Đây là thay đổi cấu trúc workflow nội bộ.

## 4. Bối Cảnh SEO

- **Dịch vụ/cụm chủ đề KNA:** Toàn bộ 9 cụm dịch vụ.
- **Persona chính:** SEO/content team nội bộ.
- **Funnel:** Research trước triển khai.
- **Search intent chính:** Không áp dụng.
- **Loại trang phù hợp:** Không áp dụng.
- **CTA phù hợp:** Không áp dụng.

## 5. Khuyến Nghị Hành Động

| STT | Hành động | Lý do | Output | Ưu tiên |
| --- | --- | --- | --- | --- |
| 1 | Dùng `AGENT.md` làm prompt chuẩn khi yêu cầu research SEO | Giữ quy trình research-first nhất quán | Agent instruction | Cao |
| 2 | Lưu mọi research vào `research-output/YYYY-MM-DD/` | Tránh mất insight trong chat | Research report | Cao |
| 3 | Dùng `templates/research-report.md` cho mọi nhiệm vụ | Chuẩn hóa output và dễ tái sử dụng | Template report | Cao |
| 4 | Dùng kết quả research làm đầu vào cho Google Sheet, content brief, internal link hoặc WordPress workflow | Tách rõ nghiên cứu và triển khai | Workflow sạch | Cao |

## 6. Rủi Ro & Giả Định

- Agent này là bộ hướng dẫn local trong project, không phải một service tự chạy nền.
- Khi cần dữ liệu SERP/current SEO, agent vẫn phải truy cập web hoặc đọc nguồn được cung cấp.
- Không tự bịa volume, traffic hoặc số liệu chuyển đổi.

## 7. Kết Luận

Đã tạo cấu trúc agent research-first cho SEO KNA. Việc nên làm tiếp theo:

1. Khi có task SEO mới, mở `agents/seo-research-agent/AGENT.md`.
2. Tạo report research trong `research-output/YYYY-MM-DD/`.
3. Chỉ sau đó mới triển khai output cuối như brief, sheet, keyword map hoặc audit.
