from app.domain import subtract,length,cloud_spans
from decimal import Decimal
import pytest
from app.errors import DomainError
def test_cloud_subtract(): assert subtract([(0,10)],[(3,7)])==[(0,3),(7,10)]
def test_cloud_outside(): assert subtract([(0,10)],[(11,12)])==[(0,10)]
def test_full_cloud(): assert subtract([(0,10)],[(0,10)])==[]
def test_dateline_cloud_sample(ctx): assert next(r for r in ctx['stages']['3']['rows'] if r['场景']=='DATELINE')['有效宽度_度']=='5'
def test_missing_cloud_endpoint(ctx): assert any(q['原因码']=='CLOUD' for q in ctx['quarantine'])
def test_not_negative(ctx): assert all(Decimal(r['有效宽度_度'])>=0 for r in ctx['stages']['3']['rows'])
def test_quality_priority(raw): # TRAP-19
    from app.pipeline import calculate
    c=calculate(raw.replace('pass','fail'));assert not c['usable']

# ---- 多离散云区契约（v3）----
def test_legacy_single_pair_still_parses():
    assert cloud_spans('172','176')==[(Decimal('172'),Decimal('176'))]
def test_multi_cloud_discrete_spans():
    assert cloud_spans('171;175','173;178')==[(Decimal('171'),Decimal('173')),(Decimal('175'),Decimal('178'))]
def test_multi_cloud_fullwidth_semicolon():
    assert cloud_spans('171；175','173；178')==[(Decimal('171'),Decimal('173')),(Decimal('175'),Decimal('178'))]
def test_overlapping_cloud_pieces_are_merged():
    # 重叠条带不得把云洞重新算成可用覆盖：先并再扣
    assert cloud_spans('172;174;173','176;179;178')==[(Decimal('172'),Decimal('179'))]
def test_cloud_endpoint_count_mismatch_isolated():
    with pytest.raises(DomainError) as info: cloud_spans('171;175','173')
    assert info.value.code=='CLOUD'
def test_cloud_bad_endpoint_coord():
    with pytest.raises(DomainError) as info: cloud_spans('190','195')
    assert info.value.code=='COORD'
def test_empty_cloud_spans(): assert cloud_spans('','')==[]
def test_subtract_all_discrete_cloud_intervals():
    mask=cloud_spans('171;175','173;178')
    assert subtract([(Decimal('170'),Decimal('180'))],mask)==[(Decimal('170'),Decimal('171')),(Decimal('173'),Decimal('175')),(Decimal('178'),Decimal('180'))]
def test_multi_cloud_sample_rows():
    from app.pipeline import calculate
    text=open('sample_data/multi-cloud.csv',encoding='utf-8').read()
    r=calculate(text);rows={row['场景']:row for row in r['stages']['3']['rows']}
    assert rows['MULTI-A']['有效宽度_度']=='5' and rows['MULTI-A']['云区段数']==2
    # 三段重叠云合并为一段，云洞不会被重复条带重新计为覆盖
    assert rows['OVERLAP']['有效宽度_度']=='3' and rows['OVERLAP']['云区段数']==1
    assert rows['LEGACY-ONE']['云区段数']==1
    reasons={q['scene']:q['原因码'] for q in r['quarantine']}
    assert reasons=={'BADMULTI':'CLOUD','BADCOORD':'COORD'}
def test_multi_cloud_evidence_column(ctx):
    row=next(r for r in ctx['stages']['3']['rows'] if r['场景']=='DATELINE')
    assert '云区间' in row and row['云区段数']==2 and ';' in row['云区间']
def test_sample_dateline_uses_discrete_format(raw):
    assert '179;-180' in raw and '180;-179' in raw
