from app.domain import merge,length
def apply(ctx):
    union=merge([span for r in ctx['usable'] for span in r['clear']]);ctx['coverage']=union
    rows=[{'起始经度':str(a),'结束经度':str(z),'有效宽度_度':str(z-a)} for a,z in union]
    return {'rows':rows,'metrics':[['并集宽度',str(length(union)),'度'],['独立区间',len(union),'段'],['场景数',len(ctx['usable']),'幅']]}

