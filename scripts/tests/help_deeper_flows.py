import asyncio,sys
from playwright.async_api import async_playwright
sys.argv=[sys.argv[0],sys.argv[1]]
exec(open(__import__('os').path.join(__import__('os').path.dirname(__file__),'results_flows.py')).read().split('async def m():')[0])
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':390,'height':797})
        await answer(pg,[1]*6)
        helps=await pg.evaluate("()=>[...document.querySelectorAll('#tsum .sum-help')].filter(e=>e.offsetParent!==null).map(e=>e.getAttribute('href'))")
        for hh in helps:
            await answer(pg,[1]*6)
            await pg.evaluate("h=>{[...document.querySelectorAll('#tsum .sum-help')].find(e=>e.offsetParent!==null&&e.getAttribute('href')==h).click()}",hh); await pg.wait_for_timeout(520)
            links=await pg.evaluate("()=>[...document.querySelectorAll('.screen.on .scroll a[href^=\"#\"]')].filter(e=>e.offsetParent!==null).map(e=>e.getAttribute('href'))")
            for L in links:
                await answer(pg,[1]*6)
                await pg.evaluate("h=>{[...document.querySelectorAll('#tsum .sum-help')].find(e=>e.offsetParent!==null&&e.getAttribute('href')==h).click()}",hh); await pg.wait_for_timeout(520)
                await pg.evaluate("h=>{[...document.querySelectorAll('.screen.on .scroll a')].find(e=>e.offsetParent!==null&&e.getAttribute('href')==h).click()}",L); await pg.wait_for_timeout(520)
                path=[hh[1:],await cur(pg)]
                for i in range(12):
                    t=await tap(pg,'.bnav .nav-next'); c=await cur(pg); path.append(f'{c}({t})')
                    if c=='tsum' or t is None: break
                ok='OK' if path[-1].startswith('tsum') else 'DOES NOT RETURN'
                print(ok,' > '.join(path))
        await b.close()
asyncio.run(m())
