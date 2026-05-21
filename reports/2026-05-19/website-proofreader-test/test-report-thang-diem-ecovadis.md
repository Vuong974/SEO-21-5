# Test skill website-proofreader

## Thong tin bai test

- Skill: `website-proofreader`
- Website: https://knacert.com.vn
- Post ID: 28795
- Tieu de: Thang diem EcoVadis va co che tinh diem
- URL: https://knacert.com.vn/tin-tuc-tieu-chuan/thang-diem-ecovadis-co-che-tinh-diem/
- Ngay test: 19/05/2026

## File dau vao va dau ra

- Text trich xuat ban dau: `reports/2026-05-19/website-proofreader-test/post-text.txt`
- Text trich xuat co giu xuong dong: `reports/2026-05-19/website-proofreader-test/post-text-lines.txt`
- Candidate CSV tu script: `reports/2026-05-19/website-proofreader-test/proofread-candidates-lines.csv`

## Ket qua chay script

- Script da chay thanh cong.
- Tong so candidate findings: 6
- Nhom candidate:
  - `Lap tu`: 2 candidate
  - `Dau cau/khoang trang`: 4 candidate

## Danh gia candidate

| Vi tri | Loai | Noi dung hien tai | Danh gia | De xuat |
| --- | --- | --- | --- | --- |
| Doan noi ve POLI | Lap tu | `tuyen bo chung chung` | False positive. Day la cach dien dat hop le, khong phai lap tu loi. | Khong sua. |
| Doan 360 Watch | Lap tu | `muc phat nang. 25: Co su co lon...` | False positive do regex bat nham chu cuoi va so tiep theo. | Khong sua. Can cai tien script. |
| Cac cau hoi co dau ngoac kep | Dau cau/khoang trang | `khong?” POLI`, `thuc te?” MESU`, `khong?” REPO` | False positive do script chua xu ly dau ngoac kep tieng Viet. | Khong sua noi dung. Can cai tien script. |
| Cuoi bai | Dau cau/khoang trang | `Hotline: 0983.246.419` | False positive do script nham dau cham trong so dien thoai. | Khong sua. Can cai tien script. |

## Loi noi dung that dang chu y

| URL/Page | Vi tri | Loai loi | Noi dung hien tai | De xuat sua | Muc do |
| --- | --- | --- | --- | --- | --- |
| Post 28795 | Dong 27 | Dien dat/Thuat ngu | `COVE: Nhan to nhan, phan anh muc do trien khai...` | `COVE: He so nhan, phan anh muc do trien khai...` | Medium |
| Post 28795 | Dong 31 va 76 | Loi hien thi/CTA | `Nhan Lo Trinh Chi Tiet` xuat hien trong dong text noi dung | Kiem tra day co phai CTA chen giua bai. Neu la nut CTA thi nen tach khoi noi dung bai/heading de khong bi doc nhu mot cau trong noi dung. | Low |
| Post 28795 | Dong 53-54 | Dien dat | `Co mot so tiep can ben vung...`; `Co tiep can ben vung...` | `Co cach tiep can ben vung...` hoac `Da co phuong phap tiep can ben vung...` | Low |
| Post 28795 | Dong 72 | Dien dat/nhat quan ngon ngu | `coverage tu 66% tieu chi...` | `muc do bao phu tu 66% tieu chi...` neu muon Viet hoa thuat ngu; giu `coverage` neu day la thuat ngu noi bo. | Low |

## Ket luan test

- Skill dung duoc cho quy trinh kiem tra mot bai post that tren website.
- Script `check_text_report.py` hoat dong, tao duoc CSV candidate.
- Can cai tien script de giam false positive voi:
  - Tu lap co chu y nghia hop le nhu `chung chung`.
  - Dau cau nam truoc dau ngoac kep tieng Viet.
  - So dien thoai co dau cham.
  - Danh sach diem dang `25:`, `50:`, `75:`.
- Phan editorial pass van can thiet, dung nhu huong dan trong skill: script chi nen coi la buoc loc ung vien ban dau.
