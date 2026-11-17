"""Guide 2.67 (from 2.66). Troubleshooting pages in the The issue / Who can help / What to do layout
(David, 17 Nov, approved mockups):
- NHS login account issues pages 3-8 (s4-pw, s4-code, s4-email, s4-pwchange, s4-mobile, s4-name):
  NHS login Support team with the bracketed GMDP note; help link + Contact NHS login Support buttons.
  Email, mobile and name pages: step 2 "Ask your Health Visiting team to update your App account."
- s4-reasons becomes a contents page "Common sign-in problems"; the "What stopped you signing in?"
  pages (s4-problems, s4-1b, s4-2) are replaced by "Details do not match", "Partner's details used",
  "A partner is signing in" (Health Visiting team, button to s5-hv). Troubleshooting contents row 3 renamed.
- s4-help "Still need help?": GMDP Support team; email us with the step that failed and any error
  message; never send passwords or security codes; email button shows the address.
usage: python3 make267.py v2.66.html v2.67.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
EXT='<svg aria-hidden="true" viewBox="0 0 20 20" width="18" height="18"><path d="M11 3h6v6M17 3l-8 8M14 11v5a1 1 0 01-1 1H4a1 1 0 01-1-1V7a1 1 0 011-1h5" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARR='<svg aria-hidden="true" viewBox="0 0 20 20" width="18" height="18"><path d="M4 10h11M11 5l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
MAIL='<svg aria-hidden="true" viewBox="0 0 20 20" width="18" height="18"><rect x="2.5" y="4.5" width="15" height="11" rx="1.6" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M3 5.5l7 5.2 7-5.2" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/></svg>'
CHEV='<svg class="chev" aria-hidden="true" viewBox="0 0 20 20" width="18" height="18"><path d="M7 4l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
IC_ISSUE='<span class="abc-ic ic-issue" aria-hidden="true">!</span>'
IC_WHO='<span class="abc-ic ic-who" aria-hidden="true"><svg viewBox="0 0 20 20" width="16" height="16"><circle cx="10" cy="6.5" r="3.2" fill="currentColor"/><path d="M3.5 17.5c.6-3.6 3.3-5.6 6.5-5.6s5.9 2 6.5 5.6z" fill="currentColor"/></svg></span>'
IC_DO='<span class="abc-ic ic-do" aria-hidden="true"><svg viewBox="0 0 20 20" width="16" height="16"><path d="M4 10h11M11 5l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
def row(ic,k,body): return f'<div class="abc-row">{ic}<div><p class="abc-k">{k}</p>{body}</div></div>'
def abc(issue,who,do): return '<div class="abc">'+row(IC_ISSUE,'The issue',issue)+row(IC_WHO,'Who can help',who)+row(IC_DO,'What to do',do)+'</div>'
def ext(href,label): return f'<a class="sp-link abc-btn" href="{href}" rel="noopener" target="_blank">{EXT}<span><strong>{label}</strong></span></a>'
def intl(href,label): return f'<a class="sp-link abc-btn" href="{href}">{ARR}<span><strong>{label}</strong></span></a>'
def links(*a): return '<div class="hv-card sp-card abc-links">'+''.join(a)+'</div>'
def note(k,p): return f'<div class="tip abc-ask"><span class="k">{k}</span><p>{p}</p></div>'
P=lambda t:f'<p>{t}</p>'
NHS_WHO='<p><strong>NHS login Support team</strong></p><p class="abc-sub">(The GMDP Support team cannot assist with NHS login account issues, as they do not have access to NHS login accounts.)</p>'
HV_WHO='<p><strong>Your Health Visiting team</strong></p>'
CONTACT=ext('https://help.login.nhs.uk/contact','Contact NHS login Support')
HVBTN=intl('#s5-hv','Find your Health Visiting team')
pages={
's4-pw':('Forgotten your password',
  abc(P('You have forgotten your NHS login password, so you cannot sign in.'),NHS_WHO,
      P('Reset your password using the NHS login guide. If that does not work, contact NHS login Support.'))+
  links(ext('https://help.login.nhs.uk/manage/passwords/','Reset your password'),CONTACT)),
's4-code':('Security code not arriving',
  abc(P('Your NHS login security code has not arrived.'),NHS_WHO,
      P('Follow the NHS login guide on security codes. If the code still does not arrive, contact NHS login Support.'))+
  links(ext('https://help.login.nhs.uk/error-messages-support','Security code help'),CONTACT)),
's4-email':('Cannot get into your email',
  abc(P('You cannot get into the email account you use for NHS login.'),NHS_WHO,
      '<ol class="abc-steps"><li>Update your email with NHS login.</li><li>Ask your Health Visiting team to update your App account.</li></ol>')+
  links(ext('https://help.login.nhs.uk/manage/emailaddresses/','Email address help'),CONTACT)),
's4-pwchange':('Change your password',
  abc(P('You want to change the password for your NHS login.'),NHS_WHO,
      P('Follow the NHS login guide to change your password. If you need help, contact NHS login Support.'))+
  links(ext('https://help.login.nhs.uk/manage/passwords/','Change your password'),CONTACT)),
's4-mobile':('Mobile number problems',
  abc(P('Your mobile number has changed, or you no longer have that phone.'),NHS_WHO,
      '<ol class="abc-steps"><li>Update your number with NHS login.</li><li>Ask your Health Visiting team to update your App account.</li></ol>')+
  links(ext('https://help.login.nhs.uk/manage/mobile-phone','Mobile number help'),CONTACT)),
's4-name':('My name has changed',
  abc(P('Your name has changed and needs updating on your NHS login.'),NHS_WHO,
      '<ol class="abc-steps"><li>Ask NHS login Support to update your name.</li><li>Ask your Health Visiting team to update your App account.</li></ol>')+
  links(CONTACT)),
# Common reasons: contents + three reason pages
's4-problems':('Details do not match',
  abc(P('Your App account was set up with an email address or mobile number that does not match your NHS login.'),HV_WHO,
      P('Ask the team to update your App account so it matches your NHS login details.'))+
  links(HVBTN)),
's4-1b':("Partner's details used",
  abc(P("Your App account was set up with your partner's email address or mobile number, not your own."),HV_WHO,
      P('Ask the team to change your App account to your own email address and mobile number.'))+
  links(HVBTN)),
's4-2':('A partner is signing in',
  abc(P("The App account is for the child's mother or primary carer. A partner cannot sign in to it."),HV_WHO,
      P('The person named on the account must sign in with their own NHS login. If the account is for the wrong person, ask the team.'))+
  links(HVBTN)),
's4-help':('Still need help?',
  abc(P('You have followed this guide but still cannot sign in to the App.'),
      '<p><strong>GMDP Support team</strong></p>',
      '<ul class="abc-list"><li>Email us with the step that failed and any error message.</li><li>Never send passwords or security codes.</li></ul>')+
  '<div class="hv-card sp-card abc-links"><a class="sp-link abc-btn abc-mail" href="mailto:gmdp.support@greatermanchester-ca.gov.uk">'+MAIL+'<span><strong>Email GMDP Support</strong><span class="abc-addr">gmdp.support@<wbr><span class="nw">greatermanchester-ca.gov.uk</span></span></span></a></div>'),
}
def toc_row(n,href,t,sub): return f'<a class="toc-row" href="{href}"><span class="gb">{n}</span><span class="tt">{t}<small>{sub}</small></span>{CHEV}</a>'
reasons=('<p class="info-lead abc-toc-lead">Choose the reason that matches your situation.</p>\n<nav aria-label="Common reasons for sign-in problems" class="toc toc-sm">'+
  toc_row(1,'#s4-problems','Details do not match','App account and NHS login are different')+
  toc_row(2,'#s4-1b',"Partner's details used","Set up with a partner's email or mobile")+
  toc_row(3,'#s4-2','A partner is signing in','Only the named carer can sign in')+'</nav>')
CSS='''
/* 2.67 more Troubleshooting pages in the issue / who can help / what to do layout */
.abc-mail .abc-addr{display:block;font-size:15px;font-weight:700;color:var(--accent);overflow-wrap:anywhere;line-height:1.3}
.abc-mail .nw{white-space:nowrap}
.abc-mail{align-items:flex-start!important}.abc-mail svg{margin-top:3px}
.abc-toc-lead{margin-bottom:10px!important}
#s4-reasons .toc-row .tt small{display:block;font-size:15px;font-weight:400;color:var(--sub);line-height:1.35;margin-top:1px}
.abc-steps{list-style:none;counter-reset:st;padding:0;margin:0;display:flex;flex-direction:column;gap:3px}
#app .screen .abc-steps li{counter-increment:st;position:relative;padding-left:24px;font-size:17px!important;line-height:1.36!important;color:var(--ink)}
.abc-steps li::before{content:counter(st);position:absolute;left:0;top:3px;width:17px;height:17px;border-radius:50%;background:var(--accentSoft);color:var(--accent2);font:800 12px/17px var(--font-head);text-align:center}
'''
def put(pid,title,content):
    global s
    m=re.search(r'<section class="screen" id="%s".*?</section>'%re.escape(pid),s,re.S); sec=m.group(0)
    a=sec.find('</div></div>',sec.find('<div class="strip"'))+len('</div></div>')
    b=sec.find('</div>\n<nav class="bnav"'); assert a>20 and b>a,pid
    new=sec[:a]+'\n'+content+'\n'+sec[b:]
    new=re.sub(r'(<h2 class="h2" tabindex="-1">)[^<]*',lambda x:x.group(1)+title,new,count=1)
    new=re.sub(r'data-title="[^"]*" aria-label="[^"]*"',f'data-title="{title}" aria-label="{title}"',new,count=1)
    s=s[:m.start()]+new+s[m.end():]
for pid,(t,c) in pages.items(): put(pid,t,c)
put('s4-reasons','Common sign-in problems',reasons)
rep('@media print{',CSS.strip()+'\n@media print{')

rep('<span class="tt">Common reasons for sign-in problems<small>The usual causes and what to check</small></span>',
    '<span class="tt">Common sign-in problems<small>Details that do not match, or a partner&#8217;s details</small></span>')
rep('Carer role v2.66', 'Carer role v2.67'); rep('Version 2.66 iPhone', 'Version 2.67 iPhone')
rep('<div>Version 2.66</div>', '<div>Version 2.67</div>'); rep('>2.66 – REVIEW DRAFT', '>2.67 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.64</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.66</span>', '<div class="rr"><span class="rv">2.67</span><span class="rd">17 Nov 2026</span><p>More Troubleshooting pages show the issue, who can help and what to do; new Common sign-in problems pages</p></div>\n<div class="rr"><span class="rv">2.66</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
