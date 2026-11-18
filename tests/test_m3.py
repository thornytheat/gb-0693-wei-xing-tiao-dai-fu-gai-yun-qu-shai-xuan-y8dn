from app.domain import subtract,length
from decimal import Decimal
def test_cloud_subtract(): assert subtract([(0,10)],[(3,7)])==[(0,3),(7,10)]
def test_cloud_outside(): assert subtract([(0,10)],[(11,12)])==[(0,10)]
def test_full_cloud(): assert subtract([(0,10)],[(0,10)])==[]
def test_dateline_cloud_sample(ctx): assert next(r for r in ctx['stages']['3']['rows'] if r['场景']=='DATELINE')['有效宽度_度']=='5'
def test_missing_cloud_endpoint(ctx): assert any(q['原因码']=='CLOUD' for q in ctx['quarantine'])
def test_not_negative(ctx): assert all(Decimal(r['有效宽度_度'])>=0 for r in ctx['stages']['3']['rows'])
def test_quality_priority(raw): # TRAP-19
    from app.pipeline import calculate
    c=calculate(raw.replace('pass','fail'));assert not c['usable']

