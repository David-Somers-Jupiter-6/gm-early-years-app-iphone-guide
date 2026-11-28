from PIL import Image, ImageDraw
G=(181,229,29); LW=7; S=417/750
def arrow(d, cx, top, sl=46):
    hh,hw,sw=40,94,54   # head height, head width, shaft width, shaft length (750 scale)
    d.polygon([(cx,top),(cx-hw/2,top+hh),(cx+hw/2,top+hh)],fill=G)
    d.rectangle([cx-sw/2,top+hh-1,cx+sw/2,top+hh+sl],fill=G)
    return top+hh+sl
J={  # n: frame, box (750 scale), arrow centre x or None
 '06':('f_1.png',(42,110,189,294),None),
 '10':('f_3.png',(32,96,600,210),(230,22)),
 '13':('f_4.png',(552,284,719,369),636),
 '15':('f_5.png',(636,281,724,369),680),
 '17':('f_6.png',(552,284,719,369),636),
 '18':('f_7.png',(40,694,709,826),None)}
out={}
for n,(fn,(x0,y0,x1,y1),ax) in J.items():
    im=Image.open(fn).convert('RGB'); d=ImageDraw.Draw(im)
    d.rectangle([x0,y0,x1,y1],outline=G,width=LW)
    bot=y1
    if ax: bot=arrow(d,ax[0],y1+8,ax[1]) if isinstance(ax,tuple) else arrow(d,ax,y1+10)
    im=im.resize((417,902),Image.LANCZOS); im.save(f'shot{n}c.png')
    out[n]=(round(y0*S),round(bot*S))
print(out)
ims=[Image.open(f'shot{n}c.png') for n in J]
s=Image.new('RGB',(427*6,902),'white')
for i,im in enumerate(ims): s.paste(im,(i*427,0))
s.resize((s.width//2,451)).save('newsheet.png')
