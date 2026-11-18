from decimal import Decimal
import unicodedata
from app.numeric import number
from app.errors import DomainError
TARGET=[(Decimal('-180'),Decimal('-170')),(Decimal('170'),Decimal('180'))]
def split(west,east):
    west=number(west);east=number(east)
    if not -180<=west<=180 or not -180<=east<=180 or west==east: raise DomainError('COORD','经度范围无效')
    return [(west,east)] if west<east else [(Decimal(-180),east),(west,Decimal(180))]
def _cloud_parts(value):
    text=unicodedata.normalize('NFKC',str(value)).strip()
    if not text:return []
    return [part.strip() for part in text.replace('；',';').split(';')]
def cloud_spans(cloud_w,cloud_e):
    # 云区契约 v3：cloud_w/cloud_e 均支持分号分隔的多区间端点；单区间（v2）写法保持兼容
    left=_cloud_parts(cloud_w);right=_cloud_parts(cloud_e)
    if not left and not right:return []
    if bool(left)!=bool(right) or len(left)!=len(right):
        raise DomainError('CLOUD','云区端点缺失或多区间端点数不一致')
    spans=[]
    for west,east in zip(left,right):
        spans.extend(split(west,east))
    return merge(spans)
def merge(intervals):
    answer=[]
    for start,end in sorted((number(a),number(z)) for a,z in intervals):
        if end<=start: continue
        if answer and start<=answer[-1][1]: answer[-1]=(answer[-1][0],max(end,answer[-1][1]))
        else: answer.append((start,end))
    return answer
def intersect(left,right):
    return merge([(max(a,c),min(z,d)) for a,z in left for c,d in right if max(a,c)<min(z,d)])
def subtract(intervals,mask):
    result=merge(intervals)
    for c,d in merge(mask):
        new=[]
        for a,z in result:
            if z<=c or a>=d:new.append((a,z));continue
            if a<c:new.append((a,c))
            if z>d:new.append((d,z))
        result=new
    return result
def length(intervals): return sum((z-a for a,z in merge(intervals)),Decimal(0))
def aliases(rows):
    parent={}
    def find(x):
        parent.setdefault(x,x)
        if parent[x]!=x:parent[x]=find(parent[x])
        return parent[x]
    for r in rows:
        a=r['scene'];other=r['alias'] or a;ra,rb=find(a),find(other);parent[max(ra,rb)]=min(ra,rb)
    return {x:find(x) for x in list(parent)}
