import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import openpyxl, pathlib

src = pathlib.Path(__file__).parent / 'Phân Loại Page KNA CERT (1).xlsx'
wb = openpyxl.load_workbook(str(src))
ws4 = wb['Page-Thang-4']
ws5 = wb['Page Thang 5']

def aggregate(ws, group_col, click_col=12, ht_col=13, sq_col=14):
    result = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        key = row[group_col - 1]
        if not key:
            continue
        key = str(key).strip()
        c = row[click_col - 1] or 0
        h = row[ht_col - 1] or 0
        s = row[sq_col - 1] or 0
        if key not in result:
            result[key] = {'pages': 0, 'click': 0, 'hien_thi': 0, 'sq': 0}
        result[key]['pages'] += 1
        result[key]['click'] += c
        result[key]['hien_thi'] += h
        result[key]['sq'] += s
    return result

nhom4 = aggregate(ws4, 6)
nhom5 = aggregate(ws5, 6)
loai4 = aggregate(ws4, 5)
loai5 = aggregate(ws5, 5)

def pct(a, b):
    return (b - a) / a * 100 if a else 0

print('=== NHÓM TRANG ===')
all_nhom = sorted(set(list(nhom4.keys()) + list(nhom5.keys())))
for k in all_nhom:
    d4 = nhom4.get(k, {'pages': 0, 'click': 0, 'hien_thi': 0, 'sq': 0})
    d5 = nhom5.get(k, {'pages': 0, 'click': 0, 'hien_thi': 0, 'sq': 0})
    print(f"{k}")
    print(f"  pages  T4={d4['pages']}  T5={d5['pages']}")
    print(f"  click  T4={d4['click']:,}  T5={d5['click']:,}  ({pct(d4['click'], d5['click']):+.1f}%)")
    print(f"  HT     T4={d4['hien_thi']:,}  T5={d5['hien_thi']:,}  ({pct(d4['hien_thi'], d5['hien_thi']):+.1f}%)")
    print(f"  SQ     T4={d4['sq']}  T5={d5['sq']}  ({pct(d4['sq'], d5['sq']):+.1f}%)")

print()
print('=== LOẠI TRANG ===')
all_loai = sorted(set(list(loai4.keys()) + list(loai5.keys())))
for k in all_loai:
    d4 = loai4.get(k, {'pages': 0, 'click': 0, 'hien_thi': 0, 'sq': 0})
    d5 = loai5.get(k, {'pages': 0, 'click': 0, 'hien_thi': 0, 'sq': 0})
    print(f"{k}")
    print(f"  pages  T4={d4['pages']}  T5={d5['pages']}")
    print(f"  click  T4={d4['click']:,}  T5={d5['click']:,}  ({pct(d4['click'], d5['click']):+.1f}%)")
    print(f"  HT     T4={d4['hien_thi']:,}  T5={d5['hien_thi']:,}  ({pct(d4['hien_thi'], d5['hien_thi']):+.1f}%)")
    print(f"  SQ     T4={d4['sq']}  T5={d5['sq']}  ({pct(d4['sq'], d5['sq']):+.1f}%)")

print()
t4c = sum(v['click'] for v in nhom4.values())
t5c = sum(v['click'] for v in nhom5.values())
t4h = sum(v['hien_thi'] for v in nhom4.values())
t5h = sum(v['hien_thi'] for v in nhom5.values())
t4s = sum(v['sq'] for v in nhom4.values())
t5s = sum(v['sq'] for v in nhom5.values())
print(f"TỔNG WEBSITE:")
print(f"  click  T4={t4c:,}  T5={t5c:,}  ({pct(t4c, t5c):+.1f}%)")
print(f"  HT     T4={t4h:,}  T5={t5h:,}  ({pct(t4h, t5h):+.1f}%)")
print(f"  SQ     T4={t4s}  T5={t5s}  ({pct(t4s, t5s):+.1f}%)")
