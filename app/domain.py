from decimal import Decimal
from app.numeric import number
from app.errors import DomainError
TARGET=[(Decimal('-180'),Decimal('-170')),(Decimal('170'),Decimal('180'))]
def split(west,east):
    west=number(west);east=number(east)
    if not -180<=west<=180 or not -180<=east<=180 or west==east: raise DomainError('COORD','经度范围无效')
    return [(west,east)] if west<east else [(Decimal(-180),east),(west,Decimal(180))]
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
