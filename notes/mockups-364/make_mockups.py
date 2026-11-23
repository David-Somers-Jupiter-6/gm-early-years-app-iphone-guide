import re
base = open('/home/claude/repo/releases/GM_Early_Years_App_iPhone_v3.64.html', encoding='utf-8').read()
TIGHT = '''
#app :is(#ts1,#ts1b,#ts2,#ts3) .ts-card .abc-row{padding:6px 10px 7px!important;margin-bottom:6px!important}
#app :is(#ts1,#ts1b,#ts2,#ts3) .ts-card .abc-row:last-child{margin-bottom:0!important}
#app :is(#ts1,#ts1b,#ts2,#ts3) .ts-ask{margin-top:8px!important;padding:6px 10px 8px!important}
#app :is(#ts1,#ts1b,#ts2,#ts3) .ts-ask .ts-ask-k{margin:0 0 2px!important}
#app :is(#ts1,#ts1b,#ts2,#ts3) .ts-ask .q-hint{margin:4px 0 6px!important}
#app :is(#ts1,#ts1b,#ts2,#ts3) .ts-ask .ans-msg{margin-top:8px!important;padding-top:8px!important;padding-bottom:8px!important}
'''
HELP_ICON = '<span class="abc-ic ic-who who-nhs ts-hi" aria-hidden="true"></span>'
def sec(s, i):
    return re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % i, s, re.S)
def edit(s, i, f):
    m = sec(s, i); return s[:m.start()] + f(m.group(0)) + s[m.end():]
WHO_ROW = re.compile(r'<div class="abc-row"><span class="abc-ic ic-who who-nhs" aria-hidden="true"></span><div><p class="abc-k">Who can help</p><p><strong>([^<]*)</strong></p></div></div>')
def variant(name, css, f=None):
    s = base.replace('/* 2.95 A. Troubleshooting help pages as three blocks */', TIGHT + css + '\n/* 2.95 A. Troubleshooting help pages as three blocks */', 1)
    if f:
        for i in ['ts1', 'ts1b', 'ts2', 'ts3']: s = edit(s, i, f)
    s = s.replace('Version 3.64</span>', 'Mock-up %s</span>' % name)
    open('/home/claude/mock/%s.html' % name, 'w', encoding='utf-8').write(s)

# A – keep the Who can help card; give it its own colour (pale grey, grey edge); question stays white with slate edge
variant('A', '''
#app .screen .ts-card .abc-row:nth-child(2){background:#f1f3f4!important;border-color:#d8dde0!important;border-left-color:#768692!important}
''')

# B – Who can help moves into the reply (shown only after an answer)
def fB(b):
    m = WHO_ROW.search(b); who = m.group(1); b = b.replace(m.group(0), '')
    line = '<p class="ok-more ts-help">%s<span>Who can help: <strong>%s</strong></span></p>' % (HELP_ICON, who)
    # put it at the end of the No reply
    i = b.find('msg-no'); j = b.find('</div>\n', b.find('ok-more', i)) if 'stop-msg' in b[i:i+60] else b.find('</div>\n', i)
    return b[:j] + line + b[j:]
variant('B', '''
#app .screen .ts-help{display:flex!important;align-items:center;gap:8px;margin-top:6px!important;padding-top:6px;border-top:1px solid rgba(0,0,0,.1)}
#app .screen .ts-help .ts-hi{position:static!important;flex:0 0 22px;width:22px!important;height:22px!important;border-radius:6px}
''', fB)

# C – Who can help becomes one line at the foot of the information card
def fC(b):
    m = WHO_ROW.search(b); who = m.group(1); b = b.replace(m.group(0), '')
    line = '<p class="ts-help">%s<span>Who can help: <strong>%s</strong></span></p>' % (HELP_ICON, who)
    k = b.find('<div class="abc ts-card">'); end = b.find('</div></div></div>', k)
    return b[:end] + line + b[end:]
variant('C', '''
#app .screen .ts-card .ts-help{display:flex!important;align-items:center;gap:8px;margin-top:7px!important;padding-top:6px;border-top:1px solid rgba(0,94,184,.18);font-size:16px!important}
#app .screen .ts-help .ts-hi{position:static!important;flex:0 0 22px;width:22px!important;height:22px!important;border-radius:6px}
''', fC)
print('ok')
