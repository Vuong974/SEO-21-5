# KNA Work Workspace

Workspace nay chua script, workflow, du lieu va bao cao cho cac nhom cong viec KNA.

Nguyen tac hien tai: giu cac file dang co o vi tri cu de khong lam hong duong dan script, nhung cong viec moi nen dua vao `workstreams/` theo dung muc dich.

## Cau truc

- `workstreams/`: noi quan ly cac nhom cong viec moi theo muc dich.
  - `seo/`: SEO, GSC, tu khoa, internal linking, WordPress SEO.
  - `general-reports/`: bao cao tong hop, KPI, dashboard, bao cao lien phong ban.
  - `content/`: bai viet, outline, brand/content standard.
  - `automation/`: workflow tu dong hoa, Google Sheet, WordPress posting.
  - `shared/`: template, quy uoc, tai nguyen dung chung.
- `bai-viet-kna/`: skill va huong dan format bai viet KNA.
- `classify-seo-keywords/`: cong cu/du lieu phan loai tu khoa.
- `cta-candidates/`: du lieu ung vien CTA.
- `data/gsc/`: file nguon va bao cao GSC.
- `templates/`: template Excel dung cho workflow.
- `reports/2026-05-18/`: toan bo file scan, result, verify va backup phat sinh trong ngay 2026-05-18.
  - `wordpress/service/`: cac bao cao va backup lien quan service pages.
  - `wordpress/cta/`: scan/xoa CTA va promo blocks.
  - `wordpress/phone-email/`: scan/xoa/thay so dien thoai va email.
  - `wordpress/tai-day/`: bao cao va backup xoa link "Tai day".
  - `debug/brc-toc/`: file HTML/CSS/JS debug loi muc luc trang BRC.
  - `debug/assets/`: asset JS tai ve khi debug.

## File chinh o root

- `post_to_wordpress.py`: dang/cap nhat bai WordPress.
- `build_gsc_keyword_report.py`: tao bao cao tu du lieu GSC.
- `create_keyword_template.py`: tao template phan loai tu khoa.
- `scan_service_679.py`: script scan service da dung trong dot kiem tra.
- `*-workflow.md`: tai lieu workflow van hanh.

## Cach dat cong viec moi

- Viec thuoc SEO: tao thu muc/ngay trong `workstreams/seo/`.
- Viec la bao cao chung: tao thu muc/ngay trong `workstreams/general-reports/`.
- Viec viet bai/noi dung: tao thu muc/ngay trong `workstreams/content/`.
- Viec tu dong hoa: tao thu muc/ngay trong `workstreams/automation/`.
- File co the dung lai cho nhieu viec: dua vao `workstreams/shared/`.

Neu file dang duoc script cu tham chieu, giu nguyen vi tri cu va ghi link/ghi chu trong README cua workstream tuong ung.

## Luu y

- Backup WordPress truoc khi xoa/sua noi dung nam trong `reports/2026-05-18/wordpress/**`.
- File `reports/2026-05-18/move-log.csv` ghi lai cac file da duoc chuyen vao cau truc moi.
