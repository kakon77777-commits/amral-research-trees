#!/usr/bin/env python3
from pathlib import Path
import sys, hashlib, json, difflib, subprocess, shutil, os

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def fail(msg): print('FAIL:',msg); raise SystemExit(1)
def ok(msg): print('PASS:',msg)

def canonical_source_files(root):
    return sorted(list((root/'core_series').glob('*.md'))+list((root/'research_program').glob('*.md')), key=lambda p:p.as_posix())

def main():
    root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
    req=['README.md','SERIES_INDEX.md','AUDIT_AND_CORRECTIONS.md','AI_HANDOFF.md','manifest.json','validation.json','CHECKSUMS.sha256','provenance/source_hashes.json','provenance/corrections.json','provenance/repair.diff','provenance/mathjax_validation.json','provenance/math_inventory.json','provenance/theorem_regression.json','provenance/sssp_repair_audit_export.md','tools/verify_math_claims.py','tools/generate_math_inventory.py','tools/mathjax_validate.js']
    for r in req:
        if not (root/r).is_file(): fail(f'missing required file {r}')
    ok('required package files present')

    # Checksum manifest and full payload coverage.
    listed={}
    for line in (root/'CHECKSUMS.sha256').read_text('utf-8').splitlines():
        if not line.strip(): continue
        h,rel=line.split('  ',1); listed[rel]=h
    actual=set()
    for p in root.rglob('*'):
        if p.is_file() and p.name!='CHECKSUMS.sha256': actual.add(p.relative_to(root).as_posix())
    if set(listed)!=actual:
        fail(f'checksum coverage mismatch: missing={sorted(actual-set(listed))}, extra={sorted(set(listed)-actual)}')
    for rel,h in listed.items():
        if sha(root/rel)!=h: fail(f'checksum mismatch {rel}')
    ok(f'checksums verified for complete payload ({len(listed)} files)')

    # Strict UTF-8 and canonical delimiter policy for scholarly sources.
    srcs=canonical_source_files(root)
    if len(srcs)!=10: fail(f'expected 10 scholarly source files, found {len(srcs)}')
    for p in srcs:
        try: s=p.read_bytes().decode('utf-8','strict')
        except UnicodeDecodeError as e: fail(f'UTF-8 decode error {p.relative_to(root)}: {e}')
        if '\ufffd' in s: fail(f'Unicode replacement character in {p.relative_to(root)}')
        if r'\(' in s or r'\)' in s: fail(f'legacy inline math delimiter in {p.relative_to(root)}')
        if any(line.strip() in (r'\[',r'\]') for line in s.splitlines()): fail(f'legacy display math delimiter in {p.relative_to(root)}')
    ok('strict UTF-8 and canonical $ / $$ delimiter policy verified for 10 sources')

    # Source-set aggregate identity.
    shmeta=json.loads((root/'provenance/source_hashes.json').read_text('utf-8'))
    entries=[]
    for p in srcs:
        rel=p.relative_to(root).as_posix(); entries.append({'path':rel,'sha256':sha(p),'bytes':len(p.read_bytes())})
    obj={'files':entries}
    canon=json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
    agg=hashlib.sha256(canon).hexdigest()
    if entries!=shmeta['files'] or agg!=shmeta['aggregate_sha256']:
        fail('source-set hash inventory/aggregate mismatch')
    if agg!='96b1b9ccb64a62a0d4fc3942d6cdf7af63c5ffe2ae3369799b7c20d1fe24f155':
        fail('source-set aggregate differs from committed SSSP anchor')
    ok('source-set aggregate matches SSSP-anchored digest')

    # Mechanical per-file diff regeneration.
    corr=json.loads((root/'provenance/corrections.json').read_text('utf-8'))
    agg_parts=[]
    for ent in sorted(corr['files'], key=lambda x:(x['key']!='HZ', x['key']) if False else x['key']):
        key=ent['key']
        orig=(root/ent['original_path']).read_text('utf-8')
        cur=(root/ent['corrected_path']).read_text('utf-8')
        d=''.join(difflib.unified_diff(orig.splitlines(True),cur.splitlines(True),fromfile=f"original/{key}__{Path(ent['original_path']).name.split('__',1)[-1]}",tofile=f'corrected/{key}',lineterm='\n'))
        stored=(root/ent['diff_path']).read_text('utf-8')
        if d!=stored: fail(f'diff regeneration mismatch for {key}')
    # Aggregate uses fixed semantic order.
    for key in ['01','02','03','04','05','06','07','08','09','HZ']:
        d=(root/'provenance/diffs'/f'{key}.diff').read_text('utf-8')
        agg_parts.append(f'### BEGIN DIFF {key} ###\n{d}### END DIFF {key} ###\n')
    aggdiff='\n'.join(agg_parts)
    if aggdiff!=(root/'provenance/repair.diff').read_text('utf-8'):
        fail('aggregate repair.diff regeneration mismatch')
    ok('all per-file diffs and aggregate repair.diff reproduce byte-for-byte')

    # Re-run finite/algebraic regressions and compare exact JSON.
    proc=subprocess.run([sys.executable,str(root/'tools/verify_math_claims.py')],capture_output=True,text=True,check=False)
    if proc.returncode!=0: fail('finite theorem regression script failed: '+proc.stderr)
    got=json.loads(proc.stdout); expected=json.loads((root/'provenance/theorem_regression.json').read_text('utf-8'))
    if got!=expected: fail('finite theorem regression output differs from stored evidence')
    ok('finite/algebraic theorem regression evidence reproduced exactly')

    # Rebuild source-derived math inventory independently of renderer metadata.
    proc=subprocess.run([sys.executable,str(root/'tools/generate_math_inventory.py'),str(root)],capture_output=True,text=True,check=False)
    if proc.returncode!=0: fail('math inventory generation failed: '+proc.stderr)
    got=json.loads(proc.stdout); expected=json.loads((root/'provenance/math_inventory.json').read_text('utf-8'))
    if got!=expected: fail('math inventory differs from stored evidence')
    if got['totals']!={'display_math_blocks':2204,'inline_math_spans':823,'all_math_spans':3027}: fail('math inventory totals differ from committed validation counts')
    ok('source-derived math inventory reproduced exactly (3027 formula hashes)')

    # Re-run MathJax if the packaged environment has the dependency. Missing renderer is an explicit skip, not a fake PASS.
    node=shutil.which('node')
    mj='/opt/nvm/versions/node/v22.16.0/lib/node_modules/mathjax-full/js/mathjax.js'
    if node and Path(mj).exists():
        proc=subprocess.run([node,str(root/'tools/mathjax_validate.js'),str(root)],capture_output=True,text=True,check=False)
        if proc.returncode!=0: fail('MathJax validation failed: '+proc.stderr+'\n'+proc.stdout[:2000])
        got=json.loads(proc.stdout); expected=json.loads((root/'provenance/mathjax_validation.json').read_text('utf-8'))
        if got!=expected: fail('MathJax inventory/output differs from stored evidence')
        ok(f"MathJax evidence reproduced exactly ({got['total_formulas']} formulas, 0 errors)")
    else:
        print('SKIP: local Node mathjax-full dependency unavailable; stored renderer evidence remains checksum-protected')

    # Manifest / validation semantic scope consistency.
    manifest=json.loads((root/'manifest.json').read_text('utf-8'))
    validation=json.loads((root/'validation.json').read_text('utf-8'))
    if manifest['source_set']['aggregate_sha256']!=agg: fail('manifest source aggregate mismatch')
    if validation['renderer_validation']['formulas_rendered']!=3027: fail('renderer validation formula count mismatch')
    if validation['renderer_validation']['errors']!=0: fail('stored renderer validation not PASS')
    if manifest['sssp']['revision']!=8 or manifest['sssp']['validation_status']!='PASS': fail('SSSP manifest mismatch')
    ok('manifest and validation scopes consistent')

    print('PASS: PACKAGE VERIFIED')

if __name__=='__main__': main()
