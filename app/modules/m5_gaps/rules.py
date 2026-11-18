from app.domain import subtract,TARGET,length
def apply(ctx):
    gaps=subtract(TARGET,ctx['coverage']);ctx['gaps']=gaps
    return {'rows':[{'缺口起点':str(a),'缺口终点':str(z),'缺口宽度_度':str(z-a)} for a,z in gaps],'metrics':[['缺口',str(length(gaps)),'度'],['缺口段数',len(gaps),'段'],['覆盖率',str((20-length(gaps))*5),'%']]}

