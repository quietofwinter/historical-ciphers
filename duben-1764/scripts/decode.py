import json,sys,re
k={a:b[0] for a,b in json.load(open('key/key_c01_base.json')).items()}
k.update(json.load(open("key/corrections.json")))
for fn in sys.argv[1:]:
  print('==',fn)
  for i,line in enumerate(open(fn),1):
    out=[]
    for tok in re.split(r'([./|\s]+)',line.strip()):
        if re.fullmatch(r'\d+',tok):
            v=k.get(tok)
            out.append(v if v else ('' if tok in k else f'[{tok}]'))
        elif '/' in tok: out.append('|')
    print(f'{i:2} '+''.join(out))
