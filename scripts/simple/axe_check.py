"""Automated accessibility check (axe-core, WCAG 2.2 AA + best practice) of every Simple guide page, Light and Dark Mode.
usage: axe_check.py /abs/path/file.html [path/to/axe.min.js]"""
import asyncio, sys, json
from playwright.async_api import async_playwright
F=sys.argv[1]
AXE=open(sys.argv[2] if len(sys.argv)>2 else 'node_modules/axe-core/axe.min.js').read()  # npm install axe-core@4
PAGES=['cover','before']+[f'step-{i}' for i in range(1,9)]+['help','contacts','a11y']
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        found={}
        for dark in (False,True):
            ctx=await b.new_context(viewport={'width':414,'height':715},color_scheme='dark' if dark else 'light'); pg=await ctx.new_page()
            await pg.goto('file://'+F); await pg.wait_for_timeout(400); await pg.add_script_tag(content=AXE)
            states=[(x,None) for x in PAGES]+[('help','p-code'),('help','p-app'),('contacts','team')]
            for pid,st in states:
                await pg.evaluate(f"location.hash='{pid}'"); await pg.wait_for_timeout(150)
                if st and st.startswith('p-'): await pg.evaluate(f"document.getElementById('{st}').open=true")
                if st=='team': await pg.click('.area[data-area="Bury"]'); await pg.select_option('#team','4')
                await pg.wait_for_timeout(150)
                r=await pg.evaluate("""async (pid)=>{const res=await axe.run(document.getElementById(pid),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}});
                   return res.violations.map(v=>({id:v.id,impact:v.impact,help:v.help,nodes:v.nodes.slice(0,12).map(n=>(n.target.join(' ')+' | '+(n.failureSummary||'').split('\\n').slice(1,3).join(' ')).slice(0,240))}))}""",pid)
                for v in r:
                    key=(v['id'],'dark' if dark else 'light')
                    found.setdefault(key,{'impact':v['impact'],'help':v['help'],'where':set()})
                    found[key]['where'].add(pid+(f'+{st}' if st else ''))
                    found[key].setdefault('nodes',[])
                    for n in v['nodes']:
                        sig=n.split(' | ')[1][:120] if ' | ' in n else n
                        if all(sig not in m for m in found[key]['nodes']): found[key]['nodes'].append(n)
            await ctx.close()
        await b.close()
    if not found: print('axe: no violations'); return
    for (i,mode),v in sorted(found.items()):
        print(f"[{v['impact']}] {i} ({mode}): {v['help']}\n   pages: {sorted(v['where'])}")
        for n in v['nodes']: print('   -',n)
asyncio.run(main())
