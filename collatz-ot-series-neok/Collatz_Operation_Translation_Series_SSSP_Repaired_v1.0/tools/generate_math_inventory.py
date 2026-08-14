#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,sys

def sha_text(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
def extract(text):
    lines=text.splitlines()
    out=[]; in_display=False; buf=[]; start=None
    for i,line in enumerate(lines,1):
        if line.strip()=='$$':
            if not in_display:
                in_display=True; buf=[]; start=i
            else:
                latex='\n'.join(buf)
                out.append({'kind':'display','line_start':start,'line_end':i,'sha256':sha_text(latex),'latex':latex})
                in_display=False; buf=[]; start=None
            continue
        if in_display:
            buf.append(line); continue
        j=0
        while j<len(line):
            if line[j]=='$' and (j==0 or line[j-1]!='\\') and not (j+1<len(line) and line[j+1]=='$'):
                k=j+1
                while k<len(line):
                    if line[k]=='$' and line[k-1]!='\\' and not (k+1<len(line) and line[k+1]=='$'):
                        latex=line[j+1:k]
                        out.append({'kind':'inline','line_start':i,'line_end':i,'sha256':sha_text(latex),'latex':latex})
                        j=k+1; break
                    k+=1
                else: raise ValueError(f'unclosed inline math line {i}')
            else: j+=1
    if in_display: raise ValueError(f'unclosed display math line {start}')
    return out

def generate(root):
    paths=sorted(list((root/'core_series').glob('*.md'))+list((root/'research_program').glob('*.md')),key=lambda p:p.as_posix())
    files=[]; td=ti=0
    for p in paths:
        items=extract(p.read_text('utf-8'))
        d=sum(x['kind']=='display' for x in items); i=len(items)-d; td+=d;ti+=i
        files.append({'path':p.relative_to(root).as_posix(),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'display_math_blocks':d,'inline_math_spans':i,'formulas':items})
    return {'schema':'sssp-math-inventory/1.0','files':files,'totals':{'display_math_blocks':td,'inline_math_spans':ti,'all_math_spans':td+ti}}

def main():
    root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
    print(json.dumps(generate(root),ensure_ascii=False,indent=2))
if __name__=='__main__': main()
