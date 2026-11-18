from app.pipeline import calculate
from app.errors import DomainError
import pytest
def test_sample_scene_rows(ctx): assert ctx['input_count']==46
def test_bom_strip(raw): # TRAP-02
    assert calculate('\ufeff'+raw)['input_count']==46
def test_quarantine_orig_line(ctx): assert all('行号' in q for q in ctx['quarantine'])
def test_empty_rejected():
    with pytest.raises(DomainError):calculate('')
def test_sample_latband(ctx):assert ctx['stages']['1']['metrics'][2][1]==20
def test_columns_failure(raw):assert any(r['原因码']=='COLUMNS' for r in calculate(raw+'x,y\n')['quarantine'])
def test_sample_keeps_alias(ctx):assert any(r['alias']=='DL-A' for r in ctx['rows'])

