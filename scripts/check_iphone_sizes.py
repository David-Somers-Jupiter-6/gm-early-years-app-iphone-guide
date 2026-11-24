"""Every page on every iPhone size: cut off, scrolling, too-wide, truncated text, plus answered states.
usage: multi.py file.html out.json [sizes-filter]"""
import asyncio, sys, json, re
from playwright.async_api import async_playwright
F = sys.argv[1]; OUT = sys.argv[2]
SIZES = [  # name, W, H  (Safari = with toolbars; Home = added to Home Screen)
 ('SE Safari', 375, 548), ('SE Home', 375, 647),
 ('mini/Zoomed Safari', 375, 635), ('mini/Zoomed Home', 375, 768),
 ('12-14 Safari', 390, 664), ('12-14 Home', 390, 797),
 ('15/16 Safari', 393, 659), ('15/16 Home', 393, 793),
 ('16 Pro Safari', 402, 681), ('16 Pro Home', 402, 814),
 ('11/XR Safari', 414, 715), ('11/XR Home', 414, 848),
 ('Pro Max Safari', 430, 740), ('Pro Max Home', 430, 873),
 ('16 Pro Max Safari', 440, 763), ('16 Pro Max Home', 440, 896)]
if len(sys.argv) > 3: SIZES = [s for s in SIZES if re.search(sys.argv[3], s[0])]
h = open(F, encoding='utf-8').read()
IDS = re.findall(r'<section class="screen[^"]*" id="([^"]+)"', h)
SKIP = {'revisions'}
MEASURE = """(id)=>{const s=document.getElementById(id);if(!s)return null;const navE=s.querySelector('.bnav');const W=innerWidth;
 const nav=navE?navE.getBoundingClientRect().top:innerHeight;const sc=s.querySelector('.scroll');
 const vis=e=>{if(!e.getClientRects().length)return false;const cs=getComputedStyle(e);if(cs.visibility=='hidden'||+cs.opacity==0)return false;return !e.closest('[hidden],.vh,.hv-map iframe')};
 const els=[...s.querySelectorAll('.scroll *')].filter(e=>vis(e)&&!e.closest('.bnav')&&(e.children.length==0||e.tagName=='IMG'||e.tagName=='LABEL'||e.tagName=='A'||e.tagName=='P'));
 const cls=e=>(e.getAttribute('class')||e.tagName);const box=e=>{const c=e.tagName=='IMG'&&e.closest('.shot,.crop,.ex-peek');return (c||e).getBoundingClientRect()};
 let cut=0,cutWhat='';for(const e of els){const b=box(e).bottom-nav;if(b>cut+0.5){cut=b;cutWhat=cls(e)+':'+(e.textContent||'').trim().slice(0,30)}}
 let wide=[];for(const e of els){if(e.closest('svg'))continue;const r=box(e);if(r.right>W+1||r.left<-1)wide.push(cls(e)+':'+(e.textContent||'').trim().slice(0,20))}
 let ell=[];for(const e of s.querySelectorAll('.scroll *')){if(!vis(e))continue;const cs=getComputedStyle(e);if(cs.textOverflow=='ellipsis'&&e.scrollWidth>e.clientWidth+1)ell.push((e.textContent||'').trim().slice(0,40))}
 for(const e of s.querySelectorAll('.scroll select')){if(!vis(e))continue;const o=e.options[e.selectedIndex];if(!o)continue;const c=document.createElement('canvas').getContext('2d');const cs=getComputedStyle(e);c.font=cs.fontWeight+' '+cs.fontSize+' '+cs.fontFamily;const tw=c.measureText(o.text).width;const room=e.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);if(tw>room+1)ell.push('select: '+o.text)}
 return {cut:Math.round(cut),cutWhat,scroll:sc?sc.scrollHeight-sc.clientHeight:0,wide:wide.slice(0,3),ell:ell.slice(0,4),sy:Math.round(scrollY),tight:document.documentElement.className.includes('tight')||s.className.includes('tight')}}"""
async def go(pg, id):
    await pg.evaluate("s=>{location.hash=s}", id); await pg.wait_for_timeout(200)
async def size_run(b, name, W, H):
    ctx = await b.new_context(viewport={'width': W, 'height': H})
    pg = await ctx.new_page()
    await pg.goto('file://' + F + '#cover'); await pg.wait_for_timeout(600)
    res = []
    async def rec(id, state):
        r = await pg.evaluate(MEASURE, id)
        if r: res.append(dict(size=name, W=W, H=H, page=id, state=state, **r))
    for id in IDS:
        if id in SKIP: continue
        await go(pg, id); await rec(id, '')
    # Sign-in check question states
    for q in ['ts1', 'ts1b', 'ts2', 'ts3', 'ts4', 'ts5']:
        await go(pg, q)
        await pg.evaluate("q=>{const l=document.querySelector('#'+q+' .bnav label.nav-next, #'+q+' .bnav .go-wait');l&&l.click()}", q); await pg.wait_for_timeout(200)
        await rec(q, 'Next before answering')
        for k, st in [(0, 'answered Yes'), (1, 'answered No')]:
            await pg.evaluate("([q,k])=>{const r=document.querySelectorAll('#'+q+' input.ans');r[k]&&r[k].click()}", [q, k]); await pg.wait_for_timeout(200)
            await rec(q, st)
    for nm, which in [('all Yes', [0]*6), ('all No', [1]*6), ('mixed', [0, 1, 0, 1, 0, 1])]:
        for k, q in enumerate(['ts1', 'ts1b', 'ts2', 'ts3', 'ts4', 'ts5']):
            await go(pg, q); await pg.evaluate("([q,k])=>{document.querySelectorAll('#'+q+' input.ans')[k].click()}", [q, which[k]]); await pg.wait_for_timeout(80)
        await go(pg, 'tsum'); await pg.wait_for_timeout(150); await rec('tsum', nm)
    # Health Visiting team finder
    for page in ['hv', 's5-hv']:
        for area, team in [('Bury', '4'), ('Stockport', '3'), ('Rochdale', '0')]:
            await go(pg, page)
            await pg.select_option(f'#{page} .hv-f-loc select', area); await pg.wait_for_timeout(150)
            await pg.select_option(f'#{page} .hv-ts-{area} select', team); await pg.wait_for_timeout(250)
            await rec(page, f'{area} team {team} contact')
            await pg.evaluate("p=>{const l=[...document.querySelectorAll('#'+p+' .hv-seg label')].find(x=>x.offsetParent&&x.textContent.trim()=='Map');l&&l.click()}", page); await pg.wait_for_timeout(250)
            await rec(page, f'{area} team {team} map')
    await ctx.close(); return res
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        allr = []
        for i in range(0, len(SIZES), 4):
            rs = await asyncio.gather(*[size_run(b, *s) for s in SIZES[i:i+4]])
            for r in rs: allr += r
        await b.close()
    json.dump(allr, open(OUT, 'w'), indent=0)
    bad = [r for r in allr if r['cut'] > 0 or r['scroll'] > 1 or r['wide'] or r['ell']]
    print(len(allr), 'checks;', len(bad), 'with problems')
asyncio.run(main())
