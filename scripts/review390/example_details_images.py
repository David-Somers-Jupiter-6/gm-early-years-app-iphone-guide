import re,base64,io,sys
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from img_edit import replace
from PIL import Image
JOBS={  # section id: list of (box, old, new, kw)
 'step-5':[((25,292,425,334),'charlotte.somers@hotmail.co.uk','c.somers@example.com',dict(thr=100,fill=[24,293,425,333]))],
 'step-c':[((25,416,425,464),'charlotte.somers@hotmail.co.uk','c.somers@example.com',dict(thr=100,fill='C'))],
 'step-6':[((343,327,404,350),'9985.','0123.',dict(bold=True,thr=150,pad=3))],
 'step-7':[((343,48,404,71),'9985.','0123.',dict(bold=True,thr=150,pad=3))],
 'step-d':[((343,392,404,415),'9985.','0123.',dict(bold=True,thr=150,pad=3))],
 'step-e':[((343,392,404,415),'9985.','0123.',dict(bold=True,thr=150,pad=3))],
 'step-f':[((343,392,404,415),'9985.','0123.',dict(bold=True,thr=150,pad=3))],
 'step-10':[((165,638,295,657),'XXX-XXX-29985','XXX-XXX-00123',dict(center=True,thr=160,pad=2))],
 'step-11':[((165,617,295,636),'XXX-XXX-29985','XXX-XXX-00123',dict(center=True,thr=160,pad=2))],
 'step-12':[((199,164,350,186),'XXX-XXX-29985','XXX-XXX-00123',dict(center=True,thr=160,pad=2))],
}
def run(html_in, html_out, preview_dir=None):
    s=open(html_in,encoding='utf-8').read()
    for sid,jobs in JOBS.items():
        i=s.index(f'<section class="screen" id="{sid}"'); j=s.index('</section>',i)
        m=re.search(r'src="data:image/(\w+);base64,([^"]+)"',s[i:j]); assert m,sid
        fmt=m.group(1); im=Image.open(io.BytesIO(base64.b64decode(m.group(2)))).convert('RGB')
        for box,old,new,kw in jobs:
            kw=dict(kw)
            if kw.get('fill')=='C': kw['fill']=CFILL
            replace(im,box,old,new,**kw)
        if preview_dir: im.save(f'{preview_dir}/{sid}.png')
        buf=io.BytesIO()
        if fmt in ('jpeg','jpg'): im.save(buf,'JPEG',quality=90,optimize=True)
        else: im.save(buf,'PNG',optimize=True)
        new='src="data:image/%s;base64,%s"'%(fmt,base64.b64encode(buf.getvalue()).decode())
        s=s[:i]+s[i:j].replace(m.group(0),new,1)+s[j:]
    open(html_out,'w',encoding='utf-8').write(s)
CFILL=[22,415,427,465]
if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2]); print('images ok')
