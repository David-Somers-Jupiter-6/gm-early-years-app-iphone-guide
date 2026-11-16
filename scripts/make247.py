import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a, s.count(a)); s = s.replace(a, b)
# 1. reading text at 17
sels = '''.scroll small,.hv-lead,.hv-how,.hv-how strong,.hv-f label,.hv-card h3,.hv-card .hv-addr,.hv-card .hv-addr span,.hv-card .hv-note,.hv-card .hv-hours,.hv-card .sp-warn,.hv-card .sp-warn strong,.sp-lead,.sum-s,.sum-msg p,.sum-msg p strong,.intro-need p,.intro-need p strong,.parts li>span:not([class]),.step-tip p,.step-tip p strong,.scroll>.tip p,.scroll>.tip p strong,.ts-small'''.split(',')
P = 'html .screen:not(#x) '
hide = '\n'.join(f'#s5-hv:has(#hv-loc option[value="{l}"]:checked):has(#hv-team-{l} option:not([value=""]):checked) .hv-how{{display:none}}' for l in ['Bury','Rochdale','Stockport'])
block = ("/* 2.47 reading text at Apple's default size (17) everywhere a carer reads (the GMDP email button stays 15 so the address fits) */\n"
         + ','.join(P + x for x in sels) + ',html #s4-nhs:not(#x) .lead,html #s4-problems:not(#x) .lead{font-size:17px!important}\n'
         + '/* 2.47 fits at 17: Contact & support team page also hides the "To see your team" line once a team is chosen */\n' + hide + '\n'
         + '#sum .st,:where(html:not(.jsnav)) #sum .st{padding:4px 2px}\n#sum .sum-msg,:where(html:not(.jsnav)) #sum .sum-msg{margin-top:8px;padding-top:7px;padding-bottom:7px}\n'
         + '#s4-activation .scroll>.tip{margin-top:4px!important}\n#hv .hv-card h3{margin-bottom:3px!important}\n#hv .hv-card .hv-tel{margin-top:4px!important}\n')
rep('@media print{', block + '@media print{')
# long web addresses: break after a slash, never at a hyphen
s = re.sub(r'(<a[^>]*class="sp-link"[^>]*>.*?<small>)([^<]+)(</small>)',
           lambda m: m.group(1) + m.group(2).replace('/', '/<wbr>').replace('-', '&#8209;') + m.group(3), s, flags=re.S)
# 2. shorter wording so pages still fit
rep('<p class="info-lead hv-lead">Your Health Visiting team can check the account holder, correct App contact details and help with a missing Activation Link.</p>',
    '<p class="info-lead hv-lead">Your team can check your account and link.</p>', 2)
rep('<p class="info-lead sp-lead">For setting up NHS login, getting back into your account, or changing your NHS login details. GMDP Support cannot access NHS login accounts.</p>',
    '<p class="info-lead sp-lead">For NHS login problems. GMDP Support cannot access NHS login accounts.</p>')
rep('<p class="ts-small">NHS login is run by the NHS. GMDP Support cannot access NHS login accounts or help with NHS login problems.</p>',
    '<p class="ts-small">GMDP Support cannot access NHS login accounts.</p>', 8)
rep('<p>Please answer every question. Select <strong>Answer</strong> next to any item with a dash.</p>',
    '<p>Select <strong>Answer</strong> next to any item with a dash.</p>')
rep('<p>Select <strong>Get help</strong> next to each item with a cross. Select <strong>Next</strong> for more troubleshooting help.</p>',
    '<p>Select <strong>Get help</strong> next to each cross, or <strong>Next</strong> for more help.</p>')
# version
rep('Carer role v2.46', 'Carer role v2.47'); rep('Version 2.46 iPhone', 'Version 2.47 iPhone')
rep('<div>Version 2.46</div>', '<div>Version 2.47</div>'); rep('>2.46 – REVIEW DRAFT', '>2.47 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.44</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.46</span>', '<div class="rr"><span class="rv">2.47</span><span class="rd">16 Nov 2026</span><p>Reading text at 17 throughout; some wording shortened so pages still fit</p></div>\n<div class="rr"><span class="rv">2.46</span>')
open(dst, 'w', encoding='utf-8').write(s)
