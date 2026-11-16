import re, json, sys, html
s=open(sys.argv[1]).read()
secs=list(re.finditer(r'<section class="screen[^"]*" id="([^"]+)"([^>]*)>(.*?)</section>',s,re.S))
pages=[]; edges=[]
for m in secs:
    pid=m.group(1); attrs=m.group(2); body=m.group(3)
    sec=html.unescape(re.search(r'data-sec="([^"]*)"',attrs).group(1))
    title=html.unescape(re.search(r'data-title="([^"]*)"',attrs).group(1))
    pages.append({'id':pid,'sec':sec,'title':title})
    navm=re.search(r'<nav class="bnav".*?</nav>',body,re.S); nav=navm.group(0) if navm else ''
    content=body.replace(nav,'')
    for a in re.finditer(r'<a ([^>]*)href="#([^"]+)"([^>]*)>',nav):
        cls=a.group(1)+a.group(3); t=a.group(2)
        if 'menu-btn' in cls or ' off' in cls+' ' and 'nav-next' in cls and t==pid: continue
        kind='back' if 'nav-back' in cls else 'next'
        if 'go-yes' in cls: kind='yes'
        elif 'go-no' in cls: kind='no'
        elif 'go-wait' in cls: continue
        edges.append((pid,t,kind))
    for a in re.finditer(r'<a ([^>]*)href="#([^"]+)"([^>]*)>(.*?)</a>',content,re.S):
        cls=a.group(1)+a.group(3); t=a.group(2)
        if t==pid: continue
        txt=re.sub(r'<[^>]+>',' ',a.group(4)); txt=re.sub(r'\s+',' ',html.unescape(txt)).strip()
        kind='link'
        if 'go-yes' in cls: kind='yes'
        elif 'go-no' in cls: kind='no'
        elif 'go-wait' in cls: continue
        elif 'toc-row' in cls: kind='list'
        edges.append((pid,t,kind+':'+txt[:40]))
ids={p['id'] for p in pages}
edges=[e for e in edges if e[1] in ids]
# dedupe
seen=set(); E=[]
for e in edges:
    k=(e[0],e[1],e[2].split(':')[0])
    if k in seen: continue
    seen.add(k); E.append(e)
json.dump({'pages':pages,'edges':E},open('graph.json','w'),indent=0)
print(len(pages),'pages',len(E),'edges')
for p in pages: print(p['id'],'|',p['sec'],'|',p['title'])
