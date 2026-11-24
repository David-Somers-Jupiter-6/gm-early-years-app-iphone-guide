import asyncio,sys,json
from playwright.async_api import async_playwright
F=sys.argv[1]
Q=['ts1','ts1b','ts2','ts3','ts4','ts5']
async def cur(pg): return await pg.evaluate("()=>document.querySelector('.screen.on').id")
async def tap(pg,sel):
    ok=await pg.evaluate("""s=>{const c=document.querySelector('.screen.on');const e=[...c.querySelectorAll(s)].find(x=>x.offsetParent!==null&&!x.classList.contains('off'));if(!e)return null;e.click();return (e.textContent||'').trim()}""",sel)
    await pg.wait_for_timeout(520); return ok
async def answer(pg,ans):
    await pg.goto('file://'+F+'#cover'); await pg.wait_for_timeout(500)
    await pg.evaluate("()=>{location.hash='ts'}"); await pg.wait_for_timeout(500)
    await tap(pg,'.bnav .nav-next')  # Begin
    for k,q in enumerate(Q):
        assert await cur(pg)==q,(await cur(pg),q)
        await pg.evaluate("([q,k])=>document.querySelectorAll('#'+q+' input.ans')[k].click()",[q,ans[k]]); await pg.wait_for_timeout(150)
        await tap(pg,'.bnav .nav-next')
    return await cur(pg)
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':390,'height':797})
        for name,ans in [('all yes',[0]*6),('one no (link)',[0,0,0,0,0,1]),('mixed',[0,1,0,1,0,1]),('all no',[1]*6)]:
            at=await answer(pg,ans); t=await tap(pg,'.bnav .nav-next'); a=await cur(pg); await tap(pg,'.bnav .nav-back'); bk=await cur(pg)
            print(f'{name}: results={at} | bottom button "{t}" -> {a} | then Back -> {bk}')
        # help links
        at=await answer(pg,[1]*6)
        helps=await pg.evaluate("()=>[...document.querySelectorAll('#tsum .sum-help')].filter(e=>e.offsetParent!==null).map(e=>e.getAttribute('href'))")
        print('help links (all no):',helps)
        for hh in helps:
            await answer(pg,[1]*6)
            await pg.evaluate("h=>{[...document.querySelectorAll('#tsum .sum-help')].find(e=>e.offsetParent!==null&&e.getAttribute('href')==h).click()}",hh); await pg.wait_for_timeout(520)
            first=await cur(pg); await tap(pg,'.bnav .nav-back'); back=await cur(pg)
            # forward path
            await answer(pg,[1]*6)
            await pg.evaluate("h=>{[...document.querySelectorAll('#tsum .sum-help')].find(e=>e.offsetParent!==null&&e.getAttribute('href')==h).click()}",hh); await pg.wait_for_timeout(520)
            path=[await cur(pg)]
            for i in range(12):
                t=await tap(pg,'.bnav .nav-next'); c=await cur(pg); path.append(f'{c}({t})')
                if c=='tsum' or t is None: break
            print(f'  {hh}: Back -> {back} | Next path: {" > ".join(path)}')
        await b.close()
asyncio.run(m())
