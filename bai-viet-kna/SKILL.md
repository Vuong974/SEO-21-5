---
name: bai-viet-kna
description: Format and optimize Vietnamese KNA CERT blog articles for WordPress SEO. Use when Codex receives raw Vietnamese article text, Google Docs text, or old WordPress Text/HTML content and must convert or clean it into paste-ready WordPress HTML with KNA typography, internal links, image alt text, [kna_link] CTA shortcodes, Yoast/RankMath meta fields, on-page checklist, and a language-edit report.
---

# Bài Viết KNA

## Core Rule

Preserve the source article completely. Do not shorten, summarize, omit, paraphrase, or insert placeholders such as `[nội dung tiếp theo...]`, `[...]`, or `[phần còn lại giữ nguyên]`.

Only change wording when fixing a clear language issue, and record every wording change in the language-edit report. Before final output, check that all source paragraphs, especially the ending and CTA section, are present.

## Input Modes

Choose the workflow by input type:

- **Raw text / Google Docs text**: Convert structure into WordPress HTML.
- **Old WordPress HTML**: Clean existing HTML, remove junk markup, normalize structure, preserve working media URLs, and reapply KNA styles.

Expected user inputs:

- Article content: raw text or WordPress HTML.
- Main keyword.
- Secondary/LSI keywords, optional.
- Internal URLs, optional, one URL per line.

If a useful field is missing, proceed with the content available and mark uncertain checklist items with `o`.

## Typography

Apply these inline styles after structure and language checks:

```html
<h2 style="font-family: Inter, sans-serif; font-size: 26px; color: #1e3255;">
<h3 style="font-family: Inter, sans-serif; font-size: 20px; color: #1e3255;">
<p style="font-family: Inter, sans-serif; font-size: 16px; color: #020b27;">
<ul style="font-family: Inter, sans-serif; font-size: 16px; color: #020b27;">
<ol style="font-family: Inter, sans-serif; font-size: 16px; color: #020b27;">
<a style="color: #1e3255; text-decoration: underline;">
```

Do not add inline style to `<h1>`, `<li>`, or `<strong>`.

## Workflow For Raw Text

1. Map the article into HTML:
   - Main title -> exactly one `<h1>`.
   - Major sections -> `<h2>`.
   - Subsections inside an H2 -> `<h3>` only when useful.
   - Paragraphs -> `<p>`.
   - Bullet or numbered lists -> `<ul>/<ol><li>`.
   - Data tables -> `<table>`.
   - `[ẢNH: mô tả]` markers -> `<figure>`.

2. Optimize headings:
   - H1 contains the main keyword, is 50-80 characters when feasible, and has no final punctuation.
   - H2 represents major topics, ideally contains the main keyword or LSI keyword, is 5+ words and <= 70 characters.
   - Use H3 only for supporting ideas under an H2.

3. Add internal links:
   - Infer each URL topic from its slug.
   - Insert each URL at most once into a natural anchor inside `<p>`, never inside headings.
   - Aim for 2-5 internal links per article around 2,000 words.
   - Use:

```html
<a href="https://knacert.com.vn/trang/" style="color: #1e3255; text-decoration: underline;" title="Tên trang">anchor text</a>
```

If no suitable URL is supplied but a link opportunity is important, use:

```html
<a href="#" style="color: #1e3255; text-decoration: underline;" title="[GỢI Ý: từ khóa cần link]">anchor text</a>
<!-- TODO: Thay # bằng URL phù hợp -->
```

4. Check and fix language:
   - Correct Vietnamese spelling, dấu hỏi/ngã, obvious consonant mistakes, punctuation, and capitalization of standards such as ISO, IEC, GDPR, EUDR, CBAM.
   - Split sentences over 50 words when they contain tangled clauses.
   - Reduce repeated words and awkward passive phrasing when it improves clarity.
   - Keep KNA CERT voice professional, clear, neutral.
   - Avoid empty phrases such as "trong bối cảnh hiện nay", "ngày càng phát triển", "không thể phủ nhận".
   - Do not use "tư vấn"; replace with context-appropriate words such as "hỗ trợ", "đồng hành", "đánh giá", or "chứng nhận".

5. Apply KNA typography.

6. Optimize images:
   - For `[ẢNH: mô tả]`, create:

```html
<figure>
  <img src="[URL ảnh]" alt="[từ khóa chính] - [mô tả ngắn]" width="800" height="450" loading="lazy" />
  <figcaption>Mô tả ảnh hiển thị bên dưới</figcaption>
</figure>
```

   - Alt text must describe the image in 5-15 words.
   - The first image alt should include the main keyword when natural.

7. Add `[kna_link]` CTA shortcode:
   - Add 1-2 shortcodes per article.
   - Always add one near the end after the final CTA paragraph.
   - Optionally add one after an important H2 about process, benefits, eligibility, cost, or timeline.
   - Put shortcode on its own line, outside `<p>`, `<li>`, headings, and links.

Use labels by context:

| Context | Label |
|---|---|
| Introduction / standard overview | `Tìm hiểu thêm về [Tên tiêu chuẩn]` |
| Certification process / steps | `Nhận hỗ trợ lộ trình chứng nhận` |
| Benefits / reasons to apply | `Đăng ký đánh giá miễn phí` |
| Applicable organizations | `Kiểm tra doanh nghiệp có phù hợp không` |
| Cost / timeline | `Nhận báo giá chi tiết` |
| Final CTA | `Liên hệ KNA CERT ngay hôm nay` |

Shortcode format:

```text
[kna_link href="#popup" style="style-1" label="Liên hệ KNA CERT ngay hôm nay"]
```

## Workflow For Old WordPress HTML

Perform the raw-text workflow after this cleanup pass:

1. Remove old styles and junk markup:
   - Remove existing `style="..."` from all tags before applying KNA styles.
   - Remove meaningless wrapper spans, extra `&nbsp;`, stray `<br>` inside paragraphs, Gutenberg `data-*`, auto-generated IDs, `contenteditable`, `data-block`, and `data-type`.
   - Preserve required attributes: `src`, `alt`, `href`, `title`, `width`, `height`, `loading`.

2. Normalize structure:
   - Ensure exactly one H1.
   - Use H2 for major sections and H3 for smaller subsections.
   - Merge fragmented `<p>` elements only when clearly the same paragraph.
   - Convert `<p>• item</p>` or `<p>- item</p>` patterns into proper lists.
   - If `[kna_link ...]` already exists, keep its position and update only the label when needed.

3. Preserve and improve images:
   - Never change existing working `src` values.
   - Add or improve `alt`, add `loading="lazy"` if missing, and wrap image in `<figure>` if missing.
   - Verify image `src` values are unchanged before final output.

4. Update existing internal links:
   - Keep relevant existing links.
   - Add the KNA `<a>` style when missing.
   - Do not duplicate internal URLs.

## SEO Meta

After HTML, output:

```text
━━━━━━━━━━━━━━━━━━━━━━
📌 META SEO (dán vào Yoast / RankMath)
━━━━━━━━━━━━━━━━━━━━━━
Meta Title    : [≤ 60 ký tự, chứa từ khóa chính]
Meta Desc     : [140-160 ký tự, chứa từ khóa, có CTA]
Slug đề xuất  : /[tu-khoa-chinh-viet-thuong-bo-dau]/
Focus Keyword : [từ khóa chính]
━━━━━━━━━━━━━━━━━━━━━━
```

Generate the slug from the main keyword: lowercase, Vietnamese accents removed, words joined by hyphens.

## Final Output

Return exactly these four parts in order:

1. **HTML body**: complete cleaned/formatted HTML, including `[kna_link]`.
2. **META SEO** block.
3. **CHECKLIST ON-PAGE** with `[x/o]` marks:
   - H1 contains main keyword.
   - H1 appears once.
   - Main keyword appears in the first 100 words.
   - Main keyword appears in at least one H2.
   - Keyword density is about 1-2%.
   - Internal link count.
   - Image alt text is complete.
   - All images have `loading="lazy"`.
   - Images are wrapped in `<figure>`.
   - Old WordPress styles/junk tags removed, when relevant.
   - Gutenberg `data-*` removed, when relevant.
   - Meta title is <= 60 characters.
   - Meta description is 140-160 characters.
   - No extra H1 tags.
   - `[kna_link]` count and positions.
   - Shortcode labels fit context.
   - Shortcodes are not inside paragraphs, list items, headings, or links.
4. **CÁC ĐIỀU CHỈNH NGÔN NGỮ**:
   - For each edit, show position, original text, revised text, and reason.
   - If there are no edits, write: `✅ Không phát hiện lỗi ngôn ngữ cần sửa`.

## KNA Preferences

- Avoid the word "tư vấn" in final copy and CTA labels.
- Prefer anchor text based on standard names when relevant: ISO 9001, EcoVadis, BSCI, ISO 14001, ISO 45001, SMETA, RBA, EUDR, CBAM.
- Keep the tone professional, specific, and neutral.
