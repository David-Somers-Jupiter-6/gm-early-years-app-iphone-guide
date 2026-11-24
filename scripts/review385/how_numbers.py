"""How this guide works numbers as pink tinted squares. usage: how_numbers.py src out"""
import sys
s = open(sys.argv[1], encoding='utf-8').read()
css = '''
/* How this guide works: numbers as pink tinted squares, like Contents */
#app :is(#how,#roadmap) :is(.hw-n,.rm-dot){width:28px!important;height:28px!important;border-radius:8px!important;border:0!important;background:var(--tp-bg)!important;color:var(--tp-fg)!important}
'''
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
