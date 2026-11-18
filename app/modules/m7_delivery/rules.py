from app.domain import subtract,TARGET,length
from app.numeric import number
def apply(ctx):
    gaps=subtract(TARGET,ctx['purchase_coverage']);gap=length(gaps);ctx['balanced']=length(ctx['coverage'])+length(ctx['gaps'])==20
    rows=[{'核验项':'目标覆盖','目标_度':'20','已交付_度':str(length(ctx['purchase_coverage'])),'差异_度':str(gap),'结论':'完整' if not gap else '缺影像'},{'核验项':'目录与交付','目标_度':str(length(ctx['coverage'])),'已交付_度':str(length(ctx['purchase_coverage'])),'差异_度':str(length(ctx['coverage'])-length(ctx['purchase_coverage'])),'结论':'预算内选择'}]
    return {'rows':rows,'metrics':[['交付缺口',str(gap),'度'],['预算结余',str(1000-number(ctx['purchase_cost'])),'CNY'],['区间守恒','相符' if ctx['balanced'] else '差异','']]}

