import json
g=json.load(open('graph.json')); P=g['pages']; order=[p['id'] for p in P]; num={p['id']:i+1 for i,p in enumerate(P)}
secs=[]; 
for p in P:
    if not secs or secs[-1][0]!=p['sec']: secs.append([p['sec'],[]])
    secs[-1][1].append(p['id'])
names={'Welcome':'Welcome','Section 1 · Health Visiting team':'Section 1 · Your Health Visiting team'}
W,H,PX,GUT=200,96,264,88; PY=H+GUT; X0=0
els=[]; eid=[0]
def nid(): eid[0]+=1; return 'e%d'%eid[0]
pos={}; bid={}
y=300
conts=[]
# Welcome + S1 share a band
bands=[[secs[0],secs[1]]]+[[s] for s in secs[2:]]
for band in bands:
    col=0; maxrows=1
    for sec,ids in band:
        rows=[ids[i:i+8] for i in range(0,len(ids),8)]
        c0=col; ncol=min(8,len(ids))
        cx=X0+c0*PX-24; cy=y-40; cw=(ncol-1)*PX+W+48; ch=(len(rows)-1)*PY+H+80
        conts.append({'type':'container','x':cx,'y':cy,'w':cw,'h':ch,'text':names.get(sec,sec).replace('&','&')})
        for r,row in enumerate(rows):
            for c,pid in enumerate(row):
                pos[pid]=(X0+(c0+c)*PX, y+r*PY, r, c0+c)
        maxrows=max(maxrows,len(rows)); col=c0+ncol+1
    y+= (maxrows-1)*PY+H+80+40+100
board_h=y
for c in conts: c['id']=nid(); els.append(c)
for pid in order:
    x,yy,r,c=pos[pid]; t=[p for p in P if p['id']==pid][0]['title']
    t=t.replace('Introduction and viewing the guide','Introduction')
    e={'id':nid(),'type':'shape','kind':'rounded','x':x,'y':yy,'w':W,'h':H,'color':'white','size':'small','text':'**%d** · %s\n`%s`'%(num[pid],t,pid)}
    if pid=='sum': e['color']='yellow'
    bid[pid]=e['id']; els.append(e)
# edges: priority
pri={'yes':3,'no':3,'list':2,'link':2,'next':1}
best={}
for a,b,k in g['edges']:
    kk=k.split(':')[0]
    if kk=='back' or a==b: continue
    if a in ('contents','how') and kk in ('list','link'): continue
    if kk in('yes','no') and a!='sum': kk='next'   # question pages: both answers go on to the next page
    key=(a,b)
    if key not in best or pri[kk]>pri[best[key][0]]: best[key]=(kk,k)
arrows=[]; lane=[0]
for (a,b),(kk,k) in best.items():
    xa,ya,ra,ca=pos[a]; xb,yb,rb,cb=pos[b]
    e={'id':nid(),'type':'arrow','from':bid[a],'to':bid[b]}
    if kk=='next':
        if not (ya==yb and cb==ca+1): continue
        e.update(fromSide='right',toSide='left',color='#9aa7b8')
    else:
        lane[0]+=1; j=((lane[0]%7)-3)*9
        e['color']={'yes':'green','no':'terracotta','list':'blue','link':'blue'}[kk]
        if kk=='link': e['dash']=True
        if a=='sum' and k.startswith('link:Get help'): e['color']='terracotta'; e['dash']=True
        if kk=='yes': e['label']='All Yes'
        if kk=='no': e['label']='Any No'
        fcx,fcy=xa+W/2,ya+H/2; tcx,tcy=xb+W/2,yb+H/2
        half=H/2+GUT/2
        if ya==yb:
            if abs(cb-ca)==1:
                e.update(fromSide='right' if cb>ca else 'left',toSide='left' if cb>ca else 'right')
            else:
                e['bends']=['v',round(half+j)]
        else:
            down=yb>ya
            # vertical lane in the column gap next to the target, on the side facing the source
            gapx = xb-32 if ca<=cb else xb+W+32
            if cb==0 and ca<=cb: gapx=xb-56
            a1=round((half if down else -half)+j)
            b1=round(gapx+j*0.6-fcx)
            c1=round((-half if down else half)+j)
            e['bends']=['v',a1,b1,c1]
    arrows.append(e)
els+=arrows
# title, take-away, key
els.append({'id':nid(),'type':'text','x':0,'y':0,'text':'GM Early Years App iPhone guide: sitemap','size':'title'})
els.append({'id':nid(),'type':'text','x':0,'y':84,'text':'Every page and link in guide v2.52','size':'large'})
els.append({'id':nid(),'type':'shape','kind':'rounded','x':1180,'y':0,'w':920,'h':230,'color':'white','size':'small','textAlign':'left','text':
 '**How to read this map**\n- Each box is one page, numbered as in the guide (1 to 72), with its page id.\n- Grey arrows: **Next**, along each row, then on to the start of the row below. **Back** goes the other way. Questions show Next once an answer is chosen.\n- Blue: menu rows (Contents and section menus). Dashed blue: links in the page text.\n- Green: all checklist answers Yes. Terracotta: any answer No; dashed terracotta: Get help on the summary (yellow).\n- Contents (page 2) links to the first page of each section and to Accessibility (68), and How this guide works (70) links to each section; those links are not drawn.\n- Not drawn: the Contents button on every page, links to NHS login, phone, email and maps.'})
order_ids=[e['id'] for e in els]
docs=[{'op':'set','path':'board/meta','data':{'v':1,'title':'GM Early Years App guide – sitemap (v2.52)','order':order_ids}}]
for e in els:
    d=dict(e); i=d.pop('id'); docs.append({'op':'set','path':'elements/'+i,'data':d})
batches=[docs[i:i+50] for i in range(0,len(docs),50)]
for n,bt in enumerate(batches): json.dump(bt,open('batch%d.json'%n,'w'),separators=(',',':'),ensure_ascii=False)
print(len(els),'elements',len(arrows),'arrows',len(batches),'batches',[len(json.dumps(b,ensure_ascii=False)) for b in batches],'height',board_h)
