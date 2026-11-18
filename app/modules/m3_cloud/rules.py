from app.domain import subtract,intersect,TARGET,length
from app.reasons import isolate
def apply(ctx):
    usable=[];rows=[]
    for r in ctx['scenes']:
        if r['quality']!='pass':isolate(ctx,r,'QUALITY','影像质量未通过');continue
        spans=intersect(subtract(r['spans'],r['cloud']),TARGET);area=length(spans)
        usable.append({**r,'clear':spans})
        rows.append({'场景':r['canonical'],'有效宽度_度':str(area),'云区段数':len(r['cloud']),'有效段数':len(spans),'价格_CNY':str(r['price_n']),'行号':r['行号']})
    ctx['usable']=usable
    return {'rows':rows,'metrics':[['可用场景',len(usable),'幅'],['带云场景',sum(bool(r['cloud']) for r in usable),'幅'],['总目标',20,'度']]}

