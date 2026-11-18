"""Guide 2.85 (from 2.84). Health Visiting team finder (David, 18 Nov) - Section 4 "Contact your team"
and the same finder on Section 8 "Your Health Visiting team":
 1. The instruction at the top stays on screen after a team is chosen (someone may pick the wrong team).
 2. More space between the instruction and the selectors, and between the selectors and the team card.
 3. The Contact details / Map switch is always shown on the team card; a newly chosen team opens on
    Contact details (existing script). Switching fades smoothly.
 4. "Tap the contact number to call." is inside the card, under the opening hours (was a separate note
    under the card, with a map line that the switch now makes unnecessary).
 5. One phone number per team (Cheadle Hulme and Bramhall, Heatons had two; the first is kept).
 6. Card polish: soft shadow, clock icon on the hours line (matching the address pin), a thin divider
    above the tap note, more room under the team name.
usage: python3 make285.py v2.84.html v2.85.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def page(pid):
    m = re.search(r'<section class="screen" id="%s".*?</section>' % re.escape(pid), s, re.S); assert m, pid; return m

# one phone number per team (David): the two teams with two numbers keep the first one listed
for tel in ('01618354354', '01618356453'):
    k = s.count('<a class="hv-call" href="tel:%s">' % tel); assert k == 2, (tel, k)
    s = re.sub(r'<a class="hv-call" href="tel:%s">.*?</a>' % tel, '', s, flags=re.S)
assert s.count('0161 835 4354') == 0 and s.count('0161 835 6453') == 0

CLOCK = ('<svg aria-hidden="true" viewBox="0 0 20 20" width="18" height="18"><circle cx="10" cy="10" r="7.2" fill="none" stroke="currentColor" stroke-width="1.8"/>'
         '<path d="M10 6v4.3l2.8 1.8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')
HOURS = '<p class="hv-hours">Monday to Friday, office hours</p>'
n_cards = 0
for pid in ('hv', 's5-hv'):
    m = page(pid); blk = m.group(0)
    def card(mm):
        global n_cards
        c = mm.group(0); n_cards += 1
        two = c.count('class="hv-call"') > 1
        tap = '<p class="hv-tap">Tap %s contact number to call.</p>' % ('a' if two else 'the')
        assert c.count(HOURS) == 1
        return c.replace(HOURS, '<p class="hv-hours">%s<span>Monday to Friday, office hours</span></p>\n%s' % (CLOCK, tap))
    blk2 = re.sub(r'<div class="hv-card hv-c-[^"]+">.*?<div class="hv-map">', card, blk, flags=re.S)
    s = s[:m.start()] + blk2 + s[m.end():]
assert n_cards == 46, n_cards
# the separate note under the card goes (its call line is now in the card; the switch shows the map)
rep('<div class="hv-tips"><p>To view on a map, tap the address.</p><p>To call, tap the contact number.</p></div>\n', '')
# keep the instruction on screen after a team is chosen (Section 4)
for town in ('Bury', 'Rochdale', 'Stockport'):
    rep('#hv:has(#hvs-loc option[value="%s"]:checked):has(#hvs-team-%s option:not([value=""]):checked) .hv-how{display:none}' % (town, town), '')

CSS = '''/* 2.85 Health Visiting team finder: instruction stays, more space, switch always shown, call note in the card */
@media screen{
#app :is(#hv,#s5-hv) .hv-how{display:block}
#app :is(#hv,#s5-hv) .hv-card{border-radius:14px;box-shadow:0 1px 2px rgba(0,48,135,.10),0 6px 18px rgba(0,48,135,.09)}
#app :is(#hv,#s5-hv) .hv-seg{display:flex!important}
#app :is(#hv,#s5-hv) .hv-hours{display:flex;gap:8px;align-items:flex-start;color:var(--ink)}
#app :is(#hv,#s5-hv) .hv-hours svg{flex:0 0 18px;color:var(--accent);margin-top:1px}
#app :is(#hv,#s5-hv) .hv-tap{border-top:1px solid rgba(0,48,135,.14);font-size:15px;line-height:1.35;color:var(--sub)}
#app :is(#hv,#s5-hv) .hv-v-c:checked~.hv-det,#app :is(#hv,#s5-hv) .hv-v-m:checked~.hv-map{animation:hvFade .25s ease-out}
#app :is(#hv,#s5-hv) .hv-seg label{transition:background-color .2s ease,color .2s ease}
}
/* spacing, tested on every team at every iPhone size; on shorter screens the Locality / team labels are hidden
   from view (the instruction above names both fields; screen readers still hear the labels) */
@media screen{
#app :is(#hv,#s5-hv) .hv-how{margin-bottom:12px!important}
#app :is(#hv,#s5-hv) .hv-card{margin-top:14px!important;padding:11px 13px 10px 14px!important}
#app :is(#hv,#s5-hv) .hv-card h3{margin-bottom:8px!important}
#app :is(#hv,#s5-hv) .hv-seg{margin:0 0 10px}
#app :is(#hv,#s5-hv) .hv-seg label{min-height:30px;padding:3px 6px}
#app :is(#hv,#s5-hv) .hv-tel{margin-top:9px!important;gap:6px!important}
#app :is(#hv,#s5-hv) .hv-call{font-size:16px!important;padding:5px 10px!important;min-height:36px!important;gap:6px!important}
#app :is(#hv,#s5-hv) .hv-hours{margin-top:8px!important}
#app :is(#hv,#s5-hv) .hv-tap{margin-top:7px;padding-top:6px}
}
@media screen and (max-height:700px){
@media screen and (max-height:700px){
#app :is(#hv,#s5-hv) .hv-f>label{position:absolute!important;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
}
@media screen and (max-height:640px){
#app :is(#hv,#s5-hv) .hv-card{margin-top:12px!important;padding:10px 12px 9px 13px!important}
#app :is(#hv,#s5-hv) .hv-card h3{margin-bottom:7px!important}
#app :is(#hv,#s5-hv) .hv-seg{margin-bottom:9px}
#app :is(#hv,#s5-hv) .hv-tel{margin-top:8px!important}
#app :is(#hv,#s5-hv) .hv-hours{margin-top:7px!important}
#app :is(#hv,#s5-hv) .hv-tap{margin-top:6px;padding-top:6px}
}
@media screen and (max-height:600px),screen and (max-width:369px){
#app :is(#hv,#s5-hv) .hv-how{margin-bottom:10px!important}
#app :is(#hv,#s5-hv) .hv-sel select{min-height:40px!important}
#app :is(#hv,#s5-hv) .hv-card{margin-top:10px!important;padding:9px 11px 8px 12px!important}
#app :is(#hv,#s5-hv) .hv-card h3{font-size:16px!important;margin-bottom:6px!important}
#app :is(#hv,#s5-hv) .hv-seg{margin-bottom:8px}
#app :is(#hv,#s5-hv) .hv-seg label{min-height:28px}
#app :is(#hv,#s5-hv) .hv-tel{margin-top:7px!important}
#app :is(#hv,#s5-hv) .hv-hours{margin-top:5px!important}
#app :is(#hv,#s5-hv) .hv-tap{margin-top:5px;padding-top:5px}
}
@media screen and (max-height:600px){
#app :is(#hv,#s5-hv) .hv-seg label{min-height:26px}
#app :is(#hv,#s5-hv) .hv-sel select{min-height:38px!important}
#app :is(#hv,#s5-hv) .hv-card{padding-bottom:7px!important}
#app :is(#hv,#s5-hv) .hv-tap{margin-top:4px;padding-top:4px}
}
@media screen and (max-width:369px){
#app :is(#hv,#s5-hv) .hv-how{font-size:15px!important}
#app :is(#hv,#s5-hv) .hv-card{border-left-width:4px}
#app :is(#hv,#s5-hv) .hv-tel{gap:4px!important}
#app :is(#hv,#s5-hv) .hv-call{min-height:32px!important;padding:3px 8px!important;font-size:15px!important}
}
@keyframes hvFade{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){#app :is(#hv,#s5-hv) .hv-det,#app :is(#hv,#s5-hv) .hv-map{animation:none!important}}
.hv-tap{display:none}
@media screen{#app :is(#hv,#s5-hv) .hv-tap{display:block}}
'''
rep('@media print{', CSS + '@media print{')
# the Locality menu's prompt says what it is (its label is hidden on shorter screens)
for sid in ('hvs-loc', 'hv-loc'):
    rep('<select id="%s"><option value="" selected>Choose</option>' % sid, '<select id="%s"><option value="" selected>Locality</option>' % sid)
# map: smallest height 100 px (was 130) so the map view fits on iPhone SE with the instruction kept
rep('Math.max(130,260-over-2)', 'Math.max(100,260-over-2)')

# version
rep('Carer role v2.84', 'Carer role v2.85'); rep('Version 2.84 iPhone', 'Version 2.85 iPhone')
rep('<div>Version 2.84</div>', '<div>Version 2.85</div>'); rep('>2.84 – REVIEW DRAFT', '>2.85 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.82</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.84</span>', '<div class="rr"><span class="rv">2.85</span><span class="rd">18 Nov 2026</span><p>Health Visiting team finder: instruction stays, more space, Contact details / Map switch always shown, call note in the card</p></div>\n<div class="rr"><span class="rv">2.84</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
