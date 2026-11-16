import re
def strip_comments(c): return re.sub(r'/\*.*?\*/','',c,flags=re.S)
def parse(css):
    """yield (media or None, selector, decls_text) for rules at top level and one level inside @media"""
    css=strip_comments(css); i=0; n=len(css); out=[]
    def block_end(k):
        depth=0
        while k<n:
            if css[k]=='{': depth+=1
            elif css[k]=='}':
                depth-=1
                if depth==0: return k
            k+=1
        return n
    while i<n:
        j=css.find('{',i)
        if j<0: break
        head=css[i:j].strip(); e=block_end(j)
        if head.startswith('@media'):
            inner=css[j+1:e]; k=0
            while True:
                a=inner.find('{',k)
                if a<0: break
                b=inner.find('}',a)
                out.append((head[6:].strip(),inner[k:a].strip(),inner[a+1:b]))
                k=b+1
        elif head.startswith('@'):
            pass
        else:
            out.append((None,head,css[j+1:e]))
        i=e+1
    return out
