import csv
from pathlib import Path

p = Path('resultados_scan.csv')
if not p.exists():
    print('Arquivo resultados_scan.csv não encontrado')
    raise SystemExit(1)

rows = []
with p.open(encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        try:
            cnt = int(row.get('count') or 0)
        except Exception:
            cnt = 0
        if cnt > 0:
            rows.append((row.get('codigo'), cnt))

rows.sort(key=lambda x: -x[1])
print(f'Total códigos com paradas: {len(rows)}')
for codigo, cnt in rows:
    print(f'{codigo}: {cnt}')
