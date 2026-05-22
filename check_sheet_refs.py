import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import openpyxl, pathlib

src = pathlib.Path(__file__).parent / 'Phân Loại Page KNA CERT (1).xlsx'
wb = openpyxl.load_workbook(str(src))
ws = wb['Báo Cáo Tháng 5']

print('=== Toàn bộ nội dung sheet Báo Cáo Tháng 5 ===')
for row in ws.iter_rows(min_row=1, values_only=False):
    for cell in row:
        if cell.value is not None:
            print(f'  {cell.coordinate}: {repr(cell.value)}')
