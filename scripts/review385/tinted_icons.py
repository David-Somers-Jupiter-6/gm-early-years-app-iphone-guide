"""List icons as soft tints (pale pink + deep magenta; pale blue + NHS blue). Run on the list-style mock-up. usage: tint.py src out"""
import re, sys
s = open(sys.argv[1], encoding='utf-8').read()
def url_from(rule_start):
    i = s.index(rule_start); m = re.compile(r'url\(([^)]*)\)').search(s, i); return m.group(1)
NHS = url_from('#app #s4 .tc-nhsmark{background:#005eb8 url(')
GM = url_from('#app #s5 .wc-gm .wc-tile{background:url(')
HV = url_from('#app #s5 .wc-hv .wc-tile{background:#005eb8 url(')
L = ':is(.toc-g,.toc.toc-sm,.tc-list,.tr-list,.wc-list,.tsp-list,.toc-tiles)'
T = ':is(.gb,.tc-tile,.tr-i,.wc-tile,.tsp-n)'
css = '''
/* soft tinted icon tiles */
html{--tp-bg:#f6e3ec;--tp-fg:#a3124d;--tb-bg:#e1edf9;--tb-fg:#005eb8;--tg-bg:#e6eaee;--tg-fg:#4e5d6c}
@media (prefers-color-scheme:dark){html{--tp-bg:#3d1b2e;--tp-fg:#ff9ec4;--tb-bg:#142f4b;--tb-fg:#8cc4ff;--tg-bg:#27323b;--tg-fg:#b7c4ce}}
#app .screen L T{background:var(--tp-bg)!important;background-image:none!important;color:var(--tp-fg)!important;position:relative}
#app .screen L T svg{color:var(--tp-fg)!important}
#app .screen L :is(.tc-nhs .tc-tile,.wc-nhs .wc-tile,.wc-hv .wc-tile,.tr-i){background:var(--tb-bg)!important;color:var(--tb-fg)!important}
#app .screen L :is(.tc-nhs .tc-tile,.wc-nhs .wc-tile,.wc-hv .wc-tile,.tr-i) svg{color:var(--tb-fg)!important}
#app .screen L .wc-tile.ls-a11y,#app #contents :is(.toc-row,.toc-tile)[aria-current="page"] .gb{background:var(--tg-bg)!important;color:var(--tg-fg)!important}
#app .screen L .wc-tile.ls-a11y svg,#app #contents :is(.toc-row,.toc-tile)[aria-current="page"] .gb svg{color:var(--tg-fg)!important}
/* picture icons drawn in the tint colour */
#app .screen L :is(.tc-nhsmark,.wc-nhs .wc-tile,.wc-hv .wc-tile,.wc-gm .wc-tile)::after{content:"";position:absolute;inset:0;-webkit-mask-position:center;mask-position:center;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat}
#app .screen L :is(.tc-nhsmark,.wc-nhs .wc-tile)::after{background:var(--tb-fg);-webkit-mask-image:url(NHS);mask-image:url(NHS);-webkit-mask-size:24px auto;mask-size:24px auto}
#app .screen L .wc-hv .wc-tile::after{background:var(--tb-fg);-webkit-mask-image:url(HV);mask-image:url(HV);-webkit-mask-size:20px 20px;mask-size:20px 20px}
#app .screen L .wc-gm .wc-tile::after{background:var(--tp-fg);-webkit-mask-image:url(GM);mask-image:url(GM);-webkit-mask-size:20px 20px;mask-size:20px 20px}
'''.replace('L', L).replace('T', T).replace('url(NHS)', 'url(%s)' % NHS).replace('url(HV)', 'url(%s)' % HV).replace('url(GM)', 'url(%s)' % GM)
BLOCKS = ('<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.7">'
          '<rect x="7.6" y="1.8" width="8.8" height="8.8" rx="1.6"/><rect x="2.2" y="12.6" width="8.8" height="8.8" rx="1.6"/><rect x="13" y="12.6" width="8.8" height="8.8" rx="1.6"/></g>'
          '<g fill="currentColor" font-family="Arial,sans-serif" font-weight="700" font-size="6.6" text-anchor="middle">'
          '<text x="12" y="8.7">A</text><text x="6.6" y="19.5">B</text><text x="17.4" y="19.5">C</text></g></svg>')
old = '<a class="wc wc-gm" href="#s5-gmdp"><span class="wc-tile" aria-hidden="true"></span>'
assert s.count(old) == 1
s = s.replace(old, '<a class="wc wc-gm" href="#s5-gmdp"><span class="wc-tile ls-gm" aria-hidden="true">%s</span>' % BLOCKS)
css += '''
#app .screen .wc-gm .wc-tile.ls-gm::after{display:none!important}
#app #s5 .wc-hv .wc-tile,#app #s5 .wc-nhs .wc-tile,#app #s4 .tc-nhsmark{background:var(--tb-bg)!important;background-image:none!important}
#app #s5 .wc-gm .wc-tile{background:var(--tp-bg)!important;background-image:none!important}
#app .screen .wc-gm .wc-tile.ls-gm svg{width:21px!important;height:21px!important}
#app #ts .tsp-list .tsp-n{background:var(--tp-bg)!important;color:var(--tp-fg)!important}
#app #contents .toc-tile .gb{background:var(--tp-bg)!important;color:var(--tp-fg)!important}
#app #contents .toc-tile .gb svg{color:var(--tp-fg)!important}
#app #contents .toc-tile[aria-current="page"] .gb{background:var(--tg-bg)!important;color:var(--tg-fg)!important}
#app #contents .toc-tile[aria-current="page"] .gb svg{color:var(--tg-fg)!important}
'''
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
