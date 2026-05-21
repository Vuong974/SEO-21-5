# Bao cao cong viec website KNA Cert ngay 18/05/2026

## 1. Thong tin chung

- Website: https://knacert.com.vn
- Ngay thuc hien: 18/05/2026
- Pham vi: chinh sua noi dung WordPress, doi soat CTA, so dien thoai/email, link noi dung va nhom trang dich vu.
- Thu muc luu log/backup: `reports/2026-05-18/`

## 2. Cac viec da xu ly

### 2.1. Xu ly CTA va tai nguyen quang cao trong bai viet

- Quet cac bai viet co CTA/hinh nut/asset cu can go.
- Cap nhat 18 bai viet WordPress.
- Go tong cong 69 asset refs CTA/quang cao.
- Da tao backup truoc khi sua: `wordpress-cta-delete-18-backup-20260518-110706.json`.
- Da xac minh sau khi sua: 18/18 bai con `remaining_count = 0`.

File ket qua:

- `reports/2026-05-18/wordpress/cta/wordpress-cta-delete-18-result-20260518-110706.csv`
- `reports/2026-05-18/wordpress/cta/wordpress-cta-delete-18-verify-20260518-110842.csv`

### 2.2. Doi soat block khuyen mai/lien quan

- Quet cac block CTA mau cam va block khuyen mai/lien quan tren bai viet.
- Ghi nhan 163 noi dung co block CTA mau cam de doi soat.
- Ghi nhan 24 noi dung co nut CTA trong bao cao su dung.
- Tao backup cho 19 bai lien quan den block promo truoc khi xu ly.

File doi soat/backup:

- `reports/2026-05-18/wordpress/cta/wordpress-cta-orange-blocks-report.json`
- `reports/2026-05-18/wordpress/cta/wordpress-nut-cta-usage-report.json`
- `reports/2026-05-18/wordpress/cta/wordpress-related-promo-delete-19-backup-20260518-111340.json`

### 2.3. Xu ly so dien thoai va email cu

- Thuc hien cac dot thay/xoa so dien thoai, email cu tren cac loai noi dung WordPress.
- Tao backup cho 2 dot thay so dien thoai:
  - Dot 1: 684 ban ghi.
  - Dot 2: 198 ban ghi.
- Tao backup cho cac dot xoa phone/email:
  - Dot 1: 7 ban ghi.
  - Dot 2: 10 ban ghi.
  - Full scan: 18 ban ghi.
- Xu ly rieng 3 noi dung con sot:
  - 1 trang service.
  - 2 trang course.
- Ket qua rieng: xoa 2 lan so `306`, xoa 1 lan so `679`, khong phat sinh thay email.
- File verify sau cung cho nhom public types khong con ban ghi can xu ly.

File ket qua:

- `reports/2026-05-18/wordpress/phone-email/wordpress-custom-phone-email-result-20260518-115214.csv`
- `reports/2026-05-18/wordpress/phone-email/wordpress-all-public-types-phone-email-verify-20260518-115431.csv`

### 2.4. Xu ly link anchor "tai day"

- Quet cac bai viet co anchor/link dang "tai day".
- Xu ly 166 bai trong danh sach ket qua.
- Ket qua: 165 bai OK, 1 bai SKIP.
- Da luu backup truoc khi thao tac.

File ket qua:

- `reports/2026-05-18/wordpress/tai-day/tai-day-removal-result.csv`
- `reports/2026-05-18/wordpress/tai-day/backup-before-tai-day-removal.csv`

### 2.5. Xu ly nhom trang dich vu/service

- Lay index API cua 242 trang service de doi soat.
- Backup truoc khi xu ly cac nhom service:
  - 131 service co CTA can go/doi soat.
  - 119 service co bang lien he trong/noi dung thua.
  - 95 service co leftover lien he trong.
  - 95 service backup truoc khi sua HTML.
  - 1 service rieng ID 15047 lien quan phone/email.
- Quet rieng chuoi/so `679`; ket qua scan sau cung khong con ban ghi trong `service-679-scan-result.csv`.
- Co log debug rieng cho service ID 14966 de kiem tra HTML, table va asset lien quan BRC TOC.

File lien quan:

- `reports/2026-05-18/wordpress/service/wordpress-service-api-index-20260518.csv`
- `reports/2026-05-18/wordpress/service/wordpress-service-cta-delete-backup-20260518.json`
- `reports/2026-05-18/wordpress/service/wordpress-service-empty-contact-table-delete-backup-20260518.json`
- `reports/2026-05-18/wordpress/service/wordpress-service-empty-contact-leftover-delete-backup-20260518.json`
- `reports/2026-05-18/wordpress/service/wordpress-service-html-repair-prerepair-backup-20260518.json`
- `reports/2026-05-18/wordpress/service/service-679-scan-result.csv`

## 3. Tong hop so lieu

| Hang muc | So luong |
| --- | ---: |
| Bai viet da cap nhat go CTA | 18 |
| Asset refs CTA da go | 69 |
| Bai verify CTA con loi | 0 |
| Bai trong danh sach xu ly link "tai day" | 166 |
| Bai link "tai day" OK | 165 |
| Bai link "tai day" SKIP | 1 |
| Service duoc lap index API | 242 |
| Service co backup CTA | 131 |
| Service co backup bang lien he trong | 119 |
| Service co backup leftover lien he | 95 |
| Ban ghi backup thay so dien thoai dot 1 | 684 |
| Ban ghi backup thay so dien thoai dot 2 | 198 |
| Noi dung phone/email xu ly rieng | 3 |

## 4. Ket qua va ghi chu

- Cac thao tac chinh deu co file backup truoc khi cap nhat noi dung.
- Nhom CTA da duoc verify sau sua, ket qua khong con asset CTA trong 18 bai da xu ly.
- Nhom link "tai day" da co ket qua doi soat ro rang: 165 OK, 1 SKIP.
- Nhom service da duoc tach log rieng de de kiem tra lai khi can rollback hoac doi chieu.
- Can tiep tuc kiem tra thu cong bai co trang thai SKIP trong file `tai-day-removal-result.csv` neu muon xu ly not 100%.

