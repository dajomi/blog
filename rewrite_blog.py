import pathlib,re
root=pathlib.Path(r'C:\Users\admin\Documents\blog\content')
files=[p for p in root.rglob('*.md') if p.name.startswith(('2025 ','2026 '))]
repl=[
('네가 ','연구자가 '),('너가 ','연구자가 '),('너의 ','연구자의 '),('네 관점에서는','실무 관점에서는'),('네 실무와','실무와'),('네 프로젝트','프로젝트'),('네 관심사','관심 분야'),('네 커리어','관련 커리어'),('네 질문','이 질문'),
('이번 브리핑','이번 글'),('다음 브리핑','후속 글'),('이번 회차','이번 글'),('지난 대화','앞선 논의'),
('꼽겠어','선정했다'),('추천해.','추천한다.'),('읽어봐.','읽어볼 수 있다.'),('볼게.','살펴본다.'),
('골랐어.','선정했다.'),('있어.','있다.'),('없어.','없다.'),('같아.','보인다.'),('좋아.','적절하다.'),('보여줘.','보여준다.'),('했어.','했다.'),('이야.','이다.'),('거야.','것이다.'),('할게.','하겠다.'),('해봐.','시도할 수 있다.'),('거든.','때문이다.')
]
for p in files:
 s=p.read_text(encoding='utf-8')
 s=s.replace('\\*\\*','').replace('**','')
 for a,b in repl:s=s.replace(a,b)
 p.write_text(s,encoding='utf-8',newline='')
print('EDITED',len(files))
print('REMAINING',[(p.name,len(re.findall(r'너가|네가|\*\*',p.read_text(encoding='utf-8')))) for p in files if re.search(r'너가|네가|\*\*',p.read_text(encoding='utf-8'))])