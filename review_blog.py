import pathlib,re
r=pathlib.Path(r'C:\Users\admin\Documents\blog\content')
pat=re.compile('네 |너|했어|했지|있지|않아|거야|할까|좋아|해보|읽어|해줘|보자|겠어|이다\?')
out=[]
for p in r.rglob('*.md'):
 if p.name.startswith(('2025 ','2026 ')):
  for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
   if pat.search(line):out.append(f'{p.name}:{i}: {line[:300]}')
pathlib.Path(r'C:\Users\admin\Documents\blog\review_hits.txt').write_text('\n'.join(out),encoding='utf-8')