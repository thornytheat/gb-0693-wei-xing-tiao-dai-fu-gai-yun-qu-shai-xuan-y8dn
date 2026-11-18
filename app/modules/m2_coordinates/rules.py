from app.domain import split,aliases
from app.numeric import number
from app.errors import DomainError
from app.reasons import isolate
def apply(ctx):
    groups={};duplicates=0;valid=[];candidates=[]
    for r in ctx['rows']:
        try:
            spans=split(r['west'],r['east'])
            if not r['scene']: raise DomainError('MISSING','场景编号为空')
            if bool(r['cloud_w'])!=bool(r['cloud_e']): raise DomainError('CLOUD','云区端点缺失')
            cloud=split(r['cloud_w'],r['cloud_e']) if r['cloud_w'] else []
            price=number(r['price'])
            if price<0:raise DomainError('RANGE','价格不能为负')
            version=int(r['version'])
            if version<1:raise ValueError()
            candidates.append({**r,'spans':spans,'cloud':cloud,'price_n':price,'version_n':version})
        except DomainError as e:isolate(ctx,r,e.code,e.message)
        except ValueError:isolate(ctx,r,'VERSION','版本必须为正整数')
    names=aliases(candidates)
    for r in candidates:
        canonical=names[r['scene']]
        groups.setdefault(canonical,[]).append({**r,'canonical':canonical})
    for key,items in sorted(groups.items()):
        version=max(r['version_n'] for r in items);top=[r for r in items if r['version_n']==version]
        fingerprints={(tuple(r['spans']),tuple(r['cloud']),r['price_n'],r['quality']) for r in top}
        if len(fingerprints)>1:
            for r in items:isolate(ctx,r,'CONFLICT','同版本影像元数据冲突')
            continue
        winner=min(top,key=lambda r:r['行号']);valid.append(winner)
        for r in items:
            if r is winner:continue
            if r['version_n']==version:duplicates+=1
            else:isolate(ctx,r,'SUPERSEDED','存在更新影像版本')
    ctx.update(scenes=valid,duplicates=duplicates)
    return {'rows':[{k:v for k,v in r.items() if k not in ('spans','cloud')} for r in valid],'metrics':[['有效场景',len(valid),'幅'],['别名',sum(k!=v for k,v in names.items()),'个'],['重复',duplicates,'条']]}

