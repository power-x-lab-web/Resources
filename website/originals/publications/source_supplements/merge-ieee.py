from pathlib import Path
import json,re,unicodedata,html,hashlib,csv,copy,collections,shutil
P=Path(r'D:\Ravenclaw\Ollivanders\InTsingHua\PowerXLab_Web\Publications');O=P/'website_ready';O.mkdir(exist_ok=True)
def clean(s):return html.unescape(str(s or '')).replace('$\\pm$','±').replace('\\&','&').replace('\\%','%').replace('\\_','_').replace('{','').replace('}','').replace('\u00a0',' ').strip()
def norm(s):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',clean(s)).lower())
def doi(s):return re.sub(r'^https?://(?:dx\.)?doi.org/','',s.strip(),flags=re.I).lower()
def year(s):return int(s) if str(s).isdigit() else None
old=json.loads((P/'publications.json').read_text(encoding='utf-8'))['records'];inp=json.loads(Path('work/ieee-input.json').read_text(encoding='utf-8'))
rows=[];changes=[];excluded=[];matches=[]
for x in inp:
 e={'id':'','category':x['category'],'type':x['entry_type'],'title':clean(x['title']),'author':clean(x.get('author','')),'editor':clean(x.get('editor','')),'year':year(x.get('year','')),'journal':clean(x.get('journal','')),'booktitle':clean(x.get('booktitle','')),'publisher':clean(x.get('publisher','')),'volume':clean(x.get('volume','')),'number':clean(x.get('number','')),'pages':clean(x.get('pages','')),'doi':doi(x.get('doi','')),'url':clean(x.get('url','')),'isbn':clean(x.get('isbn','')),'sources':[{'type':'user_supplied_bibtex','file':'IEEE_Xplore/'+x['source_file'],'key':x['key']}],'scholar_urls':[],'notes':[]}
 if e['doi']:e['url']='https://doi.org/'+e['doi']
 elif not e['url'] and x['key'].isdigit():e['url']='https://ieeexplore.ieee.org/document/'+x['key']
 rows.append(e)
# Resolve missing metadata for supplemental records against DOI registration records.
extra=[]
for p in Path('work/extra-dois').glob('*.json'):extra.append(json.loads(p.read_text(encoding='utf-8')))
for e in old:
 match=next((r for r in rows if (e['doi'] and e['doi'].lower()==r['doi']) or norm(e['title'])==norm(r['title'])),None)
 if not match and 'Theoretical Minimum' in e['title'] and e['title'].rstrip().endswith('…'):
  prefix=norm(e['title'].rstrip(' …'));match=next((r for r in rows if r['category']==e['category'] and r['year']==e['year'] and norm(r['title']).startswith(prefix)),None)
 if match:
  match['sources']+=e['sources'];match['scholar_urls']+=e['scholar_urls'];match['notes']+=e.get('notes',[])
  if not match['doi'] and e['doi']:match['doi']=e['doi'];match['url']='https://doi.org/'+e['doi']
  for field,new in [('title',match['title']),('year',match['year']),('category',match['category'])]:
   if e[field]!=new:changes.append({'id':match['doi'] or match['title'],'field':field,'previous':e[field],'selected':new,'rule':'Prefer user-provided IEEE_Xplore export'})
  if e['subtype']=='edited-book':match['notes'].append('Editors are credited as editors, not authors.')
  matches.append({'old_id':e['id'],'selected_doi':match['doi'],'method':'doi' if e['doi'] and e['doi']==match['doi'] else 'normalized_title_or_truncated_title'})
  continue
 if e['category']=='Review Required':excluded.append({'reason':'Book chapter: outside the requested three categories; retained for review.','record':e});continue
 m=next((m for m in extra if norm(' '.join(m.get('title',[])))==norm(e['title'])),None)
 if m and not any(re.search(r'\b(?:yan|y\.?)\s+lu\b',a.get('given','')+' '+a.get('family',''),re.I) for a in m.get('author',[])):
  excluded.append({'reason':'Crossref and institutional record list no Yan Lu among authors; do not publish without confirmation.','evidence':'https://doi.org/'+m['DOI'],'record':e});continue
 r={'id':'','category':e['category'],'type':{'Books':'book','Journal Articles':'article','Conference Articles':'inproceedings'}[e['category']],'title':clean(e['title']),'author':' and '.join(e['authors']),'editor':' and '.join(e['editors']),'year':e['year'],'journal':e['venue'] if e['category']=='Journal Articles' else '', 'booktitle':e['venue'] if e['category']=='Conference Articles' else '', 'publisher':e['publisher'],'volume':e['volume'],'number':e['issue'],'pages':e['pages'],'doi':e['doi'],'url':e['url'],'isbn':'; '.join(e['isbn']),'sources':e['sources'],'scholar_urls':e['scholar_urls'],'notes':e.get('notes',[])}
 if m:
  r.update(title=clean(' '.join(m['title'])),author=' and '.join((a.get('family','')+', '+a['given']) if a.get('given') else a.get('family','') for a in m.get('author',[])),doi=m['DOI'].lower(),url='https://doi.org/'+m['DOI'].lower(),volume=m.get('volume',r['volume']),number=m.get('issue',r['number']),pages=m.get('page',r['pages']))
  r['sources'].append({'type':'crossref','url':'https://api.crossref.org/works/'+m['DOI'],'accessed':'2026-10-27'})
  if r['category']=='Journal Articles':r['journal']=clean(' '.join(m.get('container-title',[])))
  else:r['booktitle']=clean(' '.join(m.get('container-title',[])))
 r['notes'].append('Supplemental record not present in supplied IEEE_Xplore lists.')
 rows.append(r)
for e in rows:
 e['id']='yan-lu-'+hashlib.sha256((e['doi'] or norm(e['title'])).encode()).hexdigest()[:12]
 e['authors']=[s.strip() for s in e['author'].split(' and ') if s.strip()];e['editors']=[s.strip() for s in e['editor'].split(' and ') if s.strip()]
 e['notes']=list(dict.fromkeys(e['notes']));e['scholar_urls']=list(dict.fromkeys(e['scholar_urls']))
 e['date_precision']='year';e['link_type']='doi' if e['doi'] else 'publisher' if e['url'] else 'none'
rows.sort(key=lambda e:({'Books':0,'Journal Articles':1,'Conference Articles':2}[e['category']],-(e['year'] or 0),e['title'].lower()))
counts=dict(collections.Counter(e['category'] for e in rows))
meta={'schema_version':'2.0','prepared_on':'2026-10-27','status':'merged_for_website','coverage_note':'Merged supplied IEEE_Xplore lists with prior sourced draft. Not certified as complete/current Google Scholar profile. Excluded uncertain author attribution and book chapter are retained separately.','sort_order':'Books / Journal Articles / Conference Articles; year descending; title ascending within year','counts':counts,'records':rows}
(O/'publications.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
for c,n in [('Books','books'),('Journal Articles','journal_articles'),('Conference Articles','conference_articles')]: (O/(n+'.json')).write_text(json.dumps([e for e in rows if e['category']==c],ensure_ascii=False,indent=2),encoding='utf-8')
# Brace-free UTF-8 field values work with the site's simple BibTeX parser.
fields=['title','author','editor','year','journal','booktitle','publisher','volume','number','pages','doi','url','isbn']
bib='\n\n'.join('@'+e['type']+'{'+e['id']+',\n'+',\n'.join('  '+k+' = {'+str(e[k]).replace('{','').replace('}','')+'}' for k in fields if e.get(k))+'\n}' for e in rows)+'\n'
(O/'publications.bib').write_text(bib,encoding='utf-8');(O/'ExPub.txt').write_text(bib,encoding='utf-8')
with (O/'publications.csv').open('w',encoding='utf-8-sig',newline='') as f:
 cw=csv.DictWriter(f,fieldnames=['id','category']+fields);cw.writeheader();cw.writerows({k:e.get(k,'') for k in cw.fieldnames} for e in rows)
(O/'excluded_needs_review.json').write_text(json.dumps(excluded,ensure_ascii=False,indent=2),encoding='utf-8')
report={'input_counts':dict(collections.Counter(e['category'] for e in inp)),'old_count':len(old),'matched_old_records':len(matches),'added_supplemental_records':len(rows)-len(inp),'output_counts':counts,'output_count':len(rows),'doi_count':sum(bool(e['doi']) for e in rows),'excluded_count':len(excluded),'field_differences':changes,'matches':matches}
(O/'merge_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
assert len({e['id'] for e in rows})==len(rows);assert len({e['doi'] for e in rows if e['doi']})==sum(bool(e['doi']) for e in rows)
assert all(e['title'] and e['year'] and (e['author'] or e['editor']) and e['url'] for e in rows)
assert all(not re.search(r'\ufffd|\$|\\(?:pm|mu|times)',e['title']) for e in rows)
print(json.dumps({k:v for k,v in report.items() if k not in ['field_differences','matches']},ensure_ascii=False));print('Differences',len(changes));print('Excluded',[x['record']['title'] for x in excluded])
