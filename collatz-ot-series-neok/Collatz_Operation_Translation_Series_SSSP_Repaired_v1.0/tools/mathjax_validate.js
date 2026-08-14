#!/usr/bin/env node
const fs=require('fs');
const path=require('path');
const {mathjax}=require('/opt/nvm/versions/node/v22.16.0/lib/node_modules/mathjax-full/js/mathjax.js');
const {TeX}=require('/opt/nvm/versions/node/v22.16.0/lib/node_modules/mathjax-full/js/input/tex.js');
const {SVG}=require('/opt/nvm/versions/node/v22.16.0/lib/node_modules/mathjax-full/js/output/svg.js');
const {liteAdaptor}=require('/opt/nvm/versions/node/v22.16.0/lib/node_modules/mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler}=require('/opt/nvm/versions/node/v22.16.0/lib/node_modules/mathjax-full/js/handlers/html.js');
const {AllPackages}=require('/opt/nvm/versions/node/v22.16.0/lib/node_modules/mathjax-full/js/input/tex/AllPackages.js');

function extractMath(text) {
  const lines=text.split(/\r?\n/);
  const items=[];
  let inDisplay=false, buf=[], start=0;
  for (let i=0;i<lines.length;i++) {
    const line=lines[i];
    if (line.trim()==='$$') {
      if (!inDisplay) { inDisplay=true; buf=[]; start=i+1; }
      else { items.push({kind:'display', line_start:start, line_end:i+1, latex:buf.join('\n')}); inDisplay=false; buf=[]; }
      continue;
    }
    if (inDisplay) { buf.push(line); continue; }
    // Inline $...$ spans; source convention disallows multiline inline math.
    let j=0;
    while (j<line.length) {
      if (line[j]==='$' && line[j-1] !== '\\' && line[j+1] !== '$') {
        let k=j+1, found=-1;
        while (k<line.length) {
          if (line[k]==='$' && line[k-1] !== '\\' && line[k+1] !== '$') { found=k; break; }
          k++;
        }
        if (found<0) throw new Error(`Unclosed inline math at line ${i+1}`);
        items.push({kind:'inline', line_start:i+1, line_end:i+1, latex:line.slice(j+1,found)});
        j=found+1;
      } else j++;
    }
  }
  if (inDisplay) throw new Error(`Unclosed display math starting line ${start}`);
  return items;
}

const root=process.argv[2];
if (!root) { console.error('usage: mathjax_validate.js <package-root>'); process.exit(2); }
const files=[];
for (const dir of ['core_series','research_program']) {
  const d=path.join(root,dir);
  for (const f of fs.readdirSync(d).filter(x=>x.endsWith('.md')).sort()) files.push(path.join(d,f));
}
const adaptor=liteAdaptor(); RegisterHTMLHandler(adaptor);
let currentErr=null;
const tex=new TeX({packages:AllPackages, formatError:(jax,err)=>{currentErr=err; throw err;}});
const svg=new SVG({fontCache:'none'});
const html=mathjax.document('',{InputJax:tex,OutputJax:svg});
const result={renderer:'MathJax mathjax-full',files:[],total_formulas:0,total_display:0,total_inline:0,errors:[]};
for (const f of files) {
  const text=fs.readFileSync(f,'utf8');
  let items;
  try { items=extractMath(text); }
  catch(e){ result.errors.push({file:path.relative(root,f),stage:'extract',error:e.message}); continue; }
  let ok=0;
  for (let idx=0;idx<items.length;idx++) {
    const it=items[idx]; currentErr=null;
    try { html.convert(it.latex,{display:it.kind==='display'}); ok++; }
    catch(e) { result.errors.push({file:path.relative(root,f),index:idx,kind:it.kind,line_start:it.line_start,line_end:it.line_end,latex:it.latex,error:e.message}); }
  }
  const display=items.filter(x=>x.kind==='display').length, inline=items.length-display;
  result.files.push({file:path.relative(root,f),formulas:items.length,display,inline,rendered_ok:ok});
  result.total_formulas+=items.length; result.total_display+=display; result.total_inline+=inline;
}
result.status=result.errors.length===0?'PASS':'FAIL';
console.log(JSON.stringify(result,null,2));
process.exit(result.errors.length?1:0);
