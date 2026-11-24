"""Design review 2: one iOS-style grouped list everywhere. usage: ls.py src out"""
import re, sys
s = open(sys.argv[1], encoding='utf-8').read()
A11Y = '<span class="wc-tile ls-a11y" aria-hidden="true"><svg viewBox="0 0 24 24" width="18" height="18"><circle cx="12" cy="4.5" r="2" fill="currentColor"/><path d="M5 8.5l7 1.5 7-1.5M12 10v5l-3 6M12 15l3 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
m = re.search(r'<a class="wc-a11y" href="#a11y"><span>([^<]*)</span>', s)
s = s.replace(m.group(0), '<a class="wc-a11y" href="#a11y">%s<span class="wc-t"><b>%s</b></span>' % (A11Y, m.group(1)), 1)
L = ':is(.toc-g,.toc.toc-sm,.tc-list,.tr-list,.wc-list,.tsp-list)'
R = ':is(.toc-row,.tc,.tr,.wc,.wc-a11y,.tsp-list>li)'
css = '''
/* design review 2: one grouped list style (iOS Settings) */
#app .screen L{background:var(--surface)!important;border:0!important;border-radius:12px!important;box-shadow:0 1px 2px rgba(16,40,70,.07)!important;padding:0!important;overflow:hidden;display:block!important}
#app .screen L>R{display:flex!important;align-items:center!important;gap:12px!important;min-height:52px!important;margin:0!important;padding:9px 14px!important;border:0!important;border-radius:0!important;box-shadow:none!important;background:transparent!important;text-decoration:none;color:var(--ink)}
#app .screen L>R+R{background:linear-gradient(var(--line),var(--line)) 56px 0/calc(100% - 56px) 1px no-repeat!important}
/* icon tiles: 30pt rounded squares */
#app .screen L :is(.gb,.tc-tile,.tr-i,.wc-tile,.tsp-n){flex:0 0 30px!important;width:30px!important;height:30px!important;border-radius:8px!important;border:0!important;display:grid!important;place-items:center!important;background-color:#b0175b;background-image:linear-gradient(135deg,#7a1660,#cf1747);color:#fff!important;font:700 15px/1 var(--font-head)!important;box-shadow:none!important}
#app .screen L :is(.gb,.tc-tile,.tr-i,.wc-tile) svg{width:18px!important;height:18px!important;color:#fff!important;stroke:currentColor}
#app .screen L :is(.tc-nhs .tc-tile,.wc-nhs .wc-tile,.wc-hv .wc-tile){background-image:none;background-color:#005eb8}
#app .screen L .tc-tile.tc-nhsmark,#app .screen L :is(.wc-nhs,.wc-hv) .wc-tile{background-size:22px auto!important}
#app .screen .tr-list .tr-i{background-image:none!important;background-color:#005eb8!important}
#app .screen L .wc-tile.ls-a11y{background-image:linear-gradient(135deg,#4e5d6c,#6b7b8a)!important}
/* text: title 17 semibold, second line 15 grey */
#app .screen L :is(.tt,.tc-t>b,.tr-t,.wc-t>b,.tsp-t){font-family:var(--font-body)!important;font-size:17px!important;font-weight:600!important;line-height:1.25!important;color:var(--ink)!important}
#app .screen L :is(.tt small,.toc-sub,.tc-s,.wc-f){display:block;font-family:var(--font-body)!important;font-size:15px!important;font-weight:400!important;line-height:1.3!important;color:var(--sub)!important;margin-top:1px!important}
#app .screen L .wc-f em{font-style:normal;font-weight:400}
#app .screen L :is(.tt,.tc-t,.tr-t,.wc-t,.tsp-t){flex:1;min-width:0}
#app #ts .tsp-list>li .tsp-t{font-weight:400!important}
#app #ts .tsp-list .tsp-n{background:linear-gradient(135deg,#7a1660,#cf1747)!important;color:#fff!important}
/* chevrons: quiet grey */
#app .screen L>R>svg:last-child,#app .screen L :is(.tc-c,.wc-c) svg{color:#a7b1bb!important;stroke:#a7b1bb}
#app .screen L :is(.tc-c,.wc-c){display:flex;color:#a7b1bb}
/* Contents: welcome tiles use the same icon tile */
#app #contents .toc-tiles{background:var(--surface)!important}
#app #contents .toc-tile .gb{width:30px!important;height:30px!important;border-radius:8px!important;border:0!important;background:linear-gradient(135deg,#7a1660,#cf1747)!important;color:#fff!important}
#app #contents .toc-tile .gb svg{color:#fff!important;width:18px;height:18px}
#app #contents .toc-tile[aria-current="page"]{color:var(--ink)}
#app #contents .toc-tile[aria-current="page"] .gb{background:#4e5d6c!important}
#app #contents .toc-row[aria-current="page"] .gb{background:#4e5d6c!important}
#app #contents.tight :is(.toc-row){min-height:42px!important;padding-top:5px!important;padding-bottom:5px!important}
#app #contents.tight .toc-row .gb{flex-basis:26px!important;width:26px!important;height:26px!important;font-size:13px!important}
/* Sign-in check start page rows are not links: no chevron, slightly shorter */
#app #ts .tsp-list>li{min-height:46px!important}
@media screen and (max-height:700px){#app .screen L>R{min-height:44px!important;padding-top:5px!important;padding-bottom:5px!important}#app #ts .tsp-list>li{min-height:40px!important;padding-top:4px!important;padding-bottom:4px!important}#app #contents.tight :is(.toc-row){min-height:40px!important;padding-top:4px!important;padding-bottom:4px!important}}
@media (prefers-color-scheme:dark){#app .screen L{box-shadow:none!important}#app .screen L>R>svg:last-child,#app .screen L :is(.tc-c,.wc-c) svg{color:#6c7a88!important;stroke:#6c7a88}}
'''.replace('L', L).replace('R', R)
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
