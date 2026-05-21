---
name: website-proofreader
description: Check website copy for spelling mistakes, Vietnamese grammar issues, punctuation errors, awkward sentences, inconsistent terminology, and broken-looking text. Use when Codex is asked to review, audit, proofread, or report language errors on website pages, WordPress posts, HTML exports, URL lists, CSV crawls, Google Sheets content, or copied page text.
---

# Website Proofreader

## Workflow

1. Collect source content from the safest available input:
   - URL list, sitemap, WordPress export/API result, crawl CSV, Google Sheet, HTML file, Markdown file, or pasted text.
   - Preserve page title, URL, content type, and section heading when available.
2. Extract readable page text before reviewing:
   - Ignore menus, footer boilerplate, cookie notices, tracking scripts, hidden text, and repeated CTA blocks unless the user asks to check all text.
   - Keep enough context around each finding so the user can locate it.
3. Run deterministic checks first when many pages are involved:
   - Use `scripts/check_text_report.py` on text/CSV exports to catch repeated words, punctuation spacing, double spaces, suspect casing, and common Vietnamese typo patterns.
   - Treat script output as candidates, not final truth.
4. Do an editorial pass:
   - Check spelling, diacritics, grammar, punctuation, sentence flow, repeated words, wrong word choice, inconsistent terms, and SEO-title/meta wording if present.
   - For Vietnamese, prefer natural business Vietnamese, clear subject-verb structure, correct accent marks, and concise sentences.
5. Report findings in a table:
   - URL/page
   - Location or nearby text
   - Error type
   - Current text
   - Suggested correction
   - Severity: `High`, `Medium`, or `Low`
   - Notes
6. If the user asks to fix live website content, create backups before editing and verify the changed pages after update.

## Severity

- `High`: Meaning changes, broken sentence, wrong legal/technical term, misleading certification/service wording, or visible headline/title error.
- `Medium`: Clear spelling/grammar/punctuation issue in body copy.
- `Low`: Style, wording, mild repetition, spacing, or readability improvement.

## Vietnamese Review Rules

- Check diacritics carefully: missing or wrong tone marks can change meaning.
- Do not modernize technical standards or certification names unless clearly wrong. Preserve names like `ISO 9001:2015`, `ISO 14001:2015`, `HACCP`, `BRC`, `FSC`, `FDA`, `GRS`, `RCS`.
- Keep brand terms consistent: `KNA CERT`, `KNA Cert`, or the user's chosen house style. Flag inconsistency instead of silently normalizing.
- Distinguish typo fixes from rewrite suggestions. Do not rewrite marketing copy heavily unless asked.
- Avoid over-correcting SEO keywords when the phrase is intentionally repeated for search relevance; flag repetition only when it harms readability or looks accidental.

## Output Formats

For a quick audit, use:

| URL/Page | Vi tri | Loai loi | Noi dung hien tai | De xuat sua | Muc do |
| --- | --- | --- | --- | --- | --- |

For a handoff report, add:

- `ID` if available from WordPress.
- `Post type` such as `post`, `page`, `service`, `course`.
- `Trang thai xu ly` such as `Can sua`, `Da sua`, `Can xac minh`.

## Resources

- Read `references/vietnamese-style-checklist.md` when doing a Vietnamese-language review or when deciding whether something is a typo, grammar issue, or style suggestion.
- Use `scripts/check_text_report.py` for bulk text/CSV checks before the editorial pass.
