"""Design review 3: one job per colour (magenta brand, blue actions, green success only). usage: cs.py src out"""
import sys
s = open(sys.argv[1], encoding='utf-8').read()
css = '''
/* design review 3: blue for every action button; green only means "done / all good" */
#app .screen:not(#cover) .nav-start,#app .screen:not(#cover) .nav-start:hover,#app .screen:not(#cover) .nav-start:active,
#app .screen:has(.ans-yes:checked) .go-yes{background:#1d6fb8!important;border-color:#1d6fb8!important;color:#fff!important;box-shadow:0 2px 6px rgba(15,76,138,.25)!important;animation:none!important}
#app .screen .stuck a.stuck-a{background:#1d6fb8!important;background-image:none!important}
'''
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
