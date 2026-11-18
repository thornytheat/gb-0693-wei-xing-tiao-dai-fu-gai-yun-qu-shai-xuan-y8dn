from app.domain import subtract,merge,length
from app.numeric import number
from decimal import Decimal
def apply(ctx):
    candidates=[{**r,'price_n':number(r['price_n'])} for r in ctx['usable']];selected=[];covered=[];cost=Decimal(0)
    while candidates:
        ranked=[]
        for r in candidates:
            gain=length(subtract(r['clear'],covered));score=gain/r['price_n'] if r['price_n'] else gain*1000000
            ranked.append((score,gain,r['canonical'],r))
        score,gain,_,best=sorted(ranked,key=lambda x:(-x[0],-x[1],x[2]))[0]
        if gain<=0:break
        candidates.remove(best)
        if cost+best['price_n']>1000:continue
        cost+=best['price_n'];covered=merge(covered+best['clear']);selected.append({**best,'gain':gain})
    ctx.update(selected=selected,purchase_coverage=covered,purchase_cost=cost)
    rows=[{'场景':r['canonical'],'新增覆盖_度':str(r['gain']),'价格_CNY':str(r['price_n']),'性价比':str(r['gain']/r['price_n']) if r['price_n'] else '免费'} for r in selected]
    return {'rows':rows,'metrics':[['采购场景',len(rows),'幅'],['采购额',str(cost),'CNY'],['采购覆盖',str(length(covered)),'度']]}

