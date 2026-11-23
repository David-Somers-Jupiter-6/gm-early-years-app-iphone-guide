"""Guide 3.79 (from 3.78) – TRIAL. David, 23 Nov:
 - Section 5 "Troubleshooting" renamed "Support"; Section 6 "Contact & support" renamed "Contacts"
   (Contents, page titles, section labels and strips, aria labels, Done buttons, search shortcuts, in-text mentions);
 - fixes the Signing in step 13 mention that still said "Section 6 · Troubleshooting" (now "Section 5 · Support").
usage: python3 make379.py v3.78.html v3.79.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
i = s.index('<body'); head, body = s[:i], s[i:]
parts = re.split(r'(<script.*?</script>|<style.*?</style>)', body, flags=re.S)
R = [('Section 5 · Troubleshooting', 'Section 5 · Support'),
     ('Section 6 · Troubleshooting', 'Section 5 · Support'),
     ('Section 6 · Contact &amp; support', 'Section 6 · Contacts'),
     ('Section 6, Contact &amp; support', 'Section 6, Contacts'),
     ('aria-label="Section 5: Troubleshooting"', 'aria-label="Section 5: Support"'),
     ('aria-label="Troubleshooting contents"', 'aria-label="Support contents"'),
     ('Done – back to Troubleshooting', 'Done – back to Support'),
     ('data-title="Troubleshooting"', 'data-title="Support"'),
     ('data-title="Contact &amp; support"', 'data-title="Contacts"'),
     ('>Troubleshooting<', '>Support<'),
     ('>Contact &amp; support<', '>Contacts<')]
counts = {a: 0 for a, b in R}
for n in range(0, len(parts), 2):
    for a, b in R:
        counts[a] += parts[n].count(a); parts[n] = parts[n].replace(a, b)
s = head + ''.join(parts)
print({k: v for k, v in counts.items()})
text = re.sub(r'<script.*?</script>|<style.*?</style>', '', s[s.index('<body'):], flags=re.S)
left = [text[m.start()-60:m.end()+20] for m in re.finditer(r'Troubleshooting|Contact &amp; support|Contact & support', text)]
assert not left, left
rep('Carer role v3.78', 'Carer role v3.79'); rep('Version 3.78 iPhone', 'Version 3.79 iPhone')
rep('>3.78 – REVIEW DRAFT', '>3.79 – REVIEW DRAFT')
rep('<span class="cv-ver">Version 3.78</span>', '<span class="cv-ver">Version 3.79</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.74</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.78</span>', '<div class="rr"><span class="rv">3.79</span><span class="rd">23 Nov 2026</span><p>Section 5 renamed Support; Section 6 renamed Contacts</p></div>\n<div class="rr"><span class="rv">3.78</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
