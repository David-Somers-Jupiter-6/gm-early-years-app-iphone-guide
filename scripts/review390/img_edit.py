import numpy as np
from PIL import Image,ImageDraw,ImageFont
IN='/usr/share/fonts/truetype/inter/'
import glob
def font(bold,size):
    pats=glob.glob('/usr/share/fonts/**/Inter*.tt[fc]',recursive=True)+glob.glob('/usr/share/fonts/**/Inter*.otf',recursive=True)
    want='Bold' if bold else 'Regular'
    c=[p for p in pats if p.endswith(f'Inter-{want}.ttf') or p.endswith(f'Inter-{want}.otf')] or [p for p in pats if want in p and 'Display' not in p and 'Italic' not in p]
    return ImageFont.truetype(c[0],size)
def fit_size(text,width,bold):
    for s in [x/2 for x in range(10,80)]:
        f=font(bold,s)
        if f.getlength(text)>=width: return s
    return 40
def text_bbox(a,x0,y0,x1,y1,thr):
    sub=a[y0:y1,x0:x1].mean(axis=2); ys,xs=np.where(sub<thr)
    return x0+xs.min(),y0+ys.min(),x0+xs.max()+1,y0+ys.max()+1
def replace(im,box,old,new,bold=False,center=False,thr=110,pad=2,fill=None,bgpad=5):
    a=np.asarray(im.convert('RGB')).astype(int)
    x0,y0,x1,y1=box
    tx0,ty0,tx1,ty1=text_bbox(a,x0,y0,x1,y1,thr)
    ring=np.concatenate([a[ty0-bgpad,tx0:tx1],a[ty1+bgpad-1,tx0:tx1],a[ty0:ty1,max(0,tx0-bgpad)],a[ty0:ty1,min(a.shape[1]-1,tx1+bgpad-1)]])
    bg=tuple(int(v) for v in np.median(ring,axis=0))
    sub=a[ty0:ty1,tx0:tx1].reshape(-1,3); fg=tuple(int(v) for v in sub[sub.sum(1).argmin()])
    s=fit_size(old,tx1-tx0,bold); f=font(bold,s)
    d=ImageDraw.Draw(im)
    fx0,fy0,fx1,fy1 = fill if fill else [tx0-pad,ty0-pad,tx1+pad,ty1+pad]
    if fill: d.rectangle([fx0,fy0,fx1,fy1],fill=bg)
    for yy in ([] if fill else range(fy0,fy1+1)):   # row-by-row fill: matches gradients
        l=a[yy,max(0,fx0-bgpad):max(1,fx0-1)]; r=a[yy,fx1+2:fx1+bgpad+1]
        c=np.median(np.concatenate([l,r]),axis=0) if len(l)+len(r) else bg
        d.line([(fx0,yy),(fx1,yy)],fill=tuple(int(v) for v in c))
    # align: top of rendered old-string ink to ty0
    ob=f.getbbox(old); nb=f.getbbox(new)
    x = (tx0+tx1)/2-(nb[2]-nb[0])/2-nb[0] if center else tx0-ob[0]
    d.text((x,ty0-ob[1]),new,font=f,fill=fg)
    return (tx0,ty0,tx1,ty1),s,bg,fg
