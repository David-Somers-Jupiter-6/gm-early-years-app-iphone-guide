import asyncio,sys
from playwright.async_api import async_playwright
sys.argv=[sys.argv[0],sys.argv[1]]
exec(open(__import__('os').path.join(__import__('os').path.dirname(__file__),'results_flows.py')).read().split('async def m():')[0])
async def goto(pg,i): await pg.goto('file://'+F+'#'+i); await pg.wait_for_timeout(500)
async def clicklink(pg,href,inbnav=False):
    r=await pg.evaluate("([h,b])=>{const c=document.querySelector('.screen.on');const e=[...c.querySelectorAll((b?'.bnav ':'.scroll ')+'a')].find(x=>x.offsetParent!==null&&x.getAttribute('href')==h);if(!e)return false;e.click();return true}",[href,inbnav]); await pg.wait_for_timeout(520); return r
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':390,'height':797})
        # normal order through Contacts
        await goto(pg,'s5'); p_=['s5']
        for i in range(4): t=await tap(pg,'.bnav .nav-next'); p_.append(f'{await cur(pg)}({t})')
        print('Contacts in order:',' > '.join(p_))
        # Contents -> s5-hv -> Next
        await goto(pg,'contents'); await clicklink(pg,'#s5'); 
        await goto(pg,'contents'); ok=await clicklink(pg,'#hv'); t=await tap(pg,'.bnav .nav-next'); print('Contents > hv > Next:',ok,await cur(pg),t)
        # question reply link to hv, then Done
        for q in ['ts1','ts1b','ts2','ts3','ts4','ts5']:
            await goto(pg,q)
            for k in [0,1]:
                await goto(pg,q); await pg.evaluate("([q,k])=>document.querySelectorAll('#'+q+' input.ans')[k].click()",[q,k]); await pg.wait_for_timeout(200)
                links=await pg.evaluate("q=>[...document.querySelectorAll('#'+q+' .ts-replies a')].filter(e=>e.offsetParent!==null).map(e=>e.getAttribute('href'))",q)
                for L in links:
                    await goto(pg,q); await pg.evaluate("([q,k])=>document.querySelectorAll('#'+q+' input.ans')[k].click()",[q,k]); await pg.wait_for_timeout(200)
                    await pg.evaluate("([q,h])=>[...document.querySelectorAll('#'+q+' .ts-replies a')].find(e=>e.offsetParent!==null&&e.getAttribute('href')==h).click()",[q,L]); await pg.wait_for_timeout(520)
                    at=await cur(pg); t=await tap(pg,'.bnav .nav-next'); n=await cur(pg)
                    await goto(pg,q); await pg.evaluate("([q,k])=>document.querySelectorAll('#'+q+' input.ans')[k].click()",[q,k]); await pg.wait_for_timeout(200)
                    await pg.evaluate("([q,h])=>[...document.querySelectorAll('#'+q+' .ts-replies a')].find(e=>e.offsetParent!==null&&e.getAttribute('href')==h).click()",[q,L]); await pg.wait_for_timeout(520)
                    await tap(pg,'.bnav .nav-back'); bk=await cur(pg)
                    print(f'{q} {"Yes" if k==0 else "No"} > {L} = {at}: right button "{t}" -> {n}; Back -> {bk}', 'OK' if n==q and bk==q else 'CHECK')
        await b.close()
asyncio.run(m())
