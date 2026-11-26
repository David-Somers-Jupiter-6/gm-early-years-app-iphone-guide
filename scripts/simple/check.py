"""Every page of the Simple guide on all 16 iPhone sizes (light) + Dark Mode on two sizes.
Measures: page scrolls (how much), anything wider than the screen, console errors. Saves screenshots for chosen sizes.
usage: check.py file.html outdir [shot-size-regex]"""
import asyncio, sys, json, re
from playwright.async_api import async_playwright
F, OUT = sys.argv[1], sys.argv[2]
SHOT = re.compile(sys.argv[3]) if len(sys.argv) > 3 else re.compile('^(SE Safari|11/XR Safari)$')
SIZES = [('SE Safari', 375, 548), ('SE Home', 375, 647), ('mini/Zoomed Safari', 375, 635), ('mini/Zoomed Home', 375, 768),
         ('12-14 Safari', 390, 664), ('12-14 Home', 390, 797), ('15/16 Safari', 393, 659), ('15/16 Home', 393, 793),
         ('16 Pro Safari', 402, 681), ('16 Pro Home', 402, 814), ('11/XR Safari', 414, 715), ('11/XR Home', 414, 848),
         ('Pro Max Safari', 430, 740), ('Pro Max Home', 430, 873), ('16 Pro Max Safari', 440, 763), ('16 Pro Max Home', 440, 896)]
PAGES = ['cover', 'before'] + [f'step-{i}' for i in range(1, 9)] + ['help', 'contacts', 'a11y']
M = """(id)=>{const s=document.getElementById(id);const sc=s.querySelector('.scroll');
 const wide=[...s.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect();return r.width&&(r.right>innerWidth+0.5||r.left<-0.5)}).map(e=>(e.className&&e.className.baseVal===undefined?e.className:e.tagName)).slice(0,3);
 const shot=s.querySelector('.shot');
 const small=[...s.querySelectorAll('.scroll p,.scroll li,.scroll span,.scroll a,.scroll h2,.scroll h3,.scroll strong,.scroll button,.scroll select')].filter(e=>e.offsetParent&&!e.closest('.cv-gmca,.kicker,.vh,.ti,.cv-band')&&e.textContent.trim()&&parseFloat(getComputedStyle(e).fontSize)<13).map(e=>e.textContent.trim().slice(0,20));
 const tgt=[...s.querySelectorAll('a,button,select,summary')].filter(e=>e.offsetParent&&!e.closest('.vh')).filter(e=>{const r=e.getBoundingClientRect();return r.height<44&&!e.closest('p,li')}).map(e=>e.textContent.trim().slice(0,20));
 return {scroll:sc.scrollHeight-sc.clientHeight,wide,shotH:shot?Math.round(shot.getBoundingClientRect().height):null,small:small.slice(0,3),tgt:tgt.slice(0,3)}}"""
async def main():
    res, errs = [], []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        runs = [(n, W, H, False) for n, W, H in SIZES] + [(n, W, H, True) for n, W, H in SIZES if n in ('SE Safari', '11/XR Safari')]
        for name, W, H, dark in runs:
            ctx = await b.new_context(viewport={'width': W, 'height': H}, device_scale_factor=2, color_scheme='dark' if dark else 'light')
            pg = await ctx.new_page()
            pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto('file://' + F + '#cover'); await pg.wait_for_timeout(500)
            states = [(pid, '') for pid in PAGES] + [('help', 'open p-code'), ('help', 'open p-open'), ('contacts', 'Bury team 4'), ('contacts', 'Stockport team 9')]
            for pid, st in states:
                await pg.evaluate("s=>{location.hash=s}", pid); await pg.wait_for_timeout(120)
                if st.startswith('open'):
                    await pg.evaluate("o=>{document.getElementById(o).open=true}", st.split()[1]); await pg.wait_for_timeout(120)
                if st.startswith(('Bury', 'Stockport')):
                    a, _, i = st.split()
                    await pg.click(f'.area[data-area="{a}"]'); await pg.select_option('#team', i); await pg.wait_for_timeout(400)
                r = await pg.evaluate(M, pid)
                res.append(dict(size=name, dark=dark, page=pid, state=st, **r))
                if SHOT.search(name):
                    tag = f"{name.replace('/', '-').replace(' ', '_')}{'_dark' if dark else ''}_{pid}{'_' + st.replace(' ', '-') if st else ''}"
                    await pg.screenshot(path=f'{OUT}/{tag}.png')
                if st.startswith(('Bury', 'Stockport')):
                    await pg.evaluate("()=>{document.querySelector('#contacts .scroll').scrollTop=1e5}"); await pg.wait_for_timeout(80)
                    if SHOT.search(name): await pg.screenshot(path=f'{OUT}/{tag}_bottom.png')
            await ctx.close()
        await b.close()
    json.dump(res, open(f'{OUT}/results.json', 'w'), indent=0)
    for r in res:
        flag = r['scroll'] > 0 or r['wide'] or r['small'] or r['tgt']
        if flag: print(r)
    print('console errors:', sorted(set(errs)) or 'none')
    print(len(res), 'page states measured')
asyncio.run(main())
