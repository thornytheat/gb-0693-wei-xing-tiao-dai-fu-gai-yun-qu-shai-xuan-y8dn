from app.domain import length
from app.numeric import number
from app.modules.m7_delivery.rules import apply
from copy import deepcopy
def test_delivery_balanced(ctx):assert ctx['balanced'] is True
def test_delivery_complete(ctx):assert ctx['stages']['7']['rows'][0]['结论']=='完整'
def test_missing_delivery(ctx):
    c=deepcopy(ctx);c['purchase_coverage']=[];assert apply(c)['rows'][0]['差异_度']=='20'
def test_budget_left(ctx):assert ctx['stages']['7']['metrics'][1][1]==str(1000-number(ctx['purchase_cost']))
def test_manifest_sha(ctx):assert len(ctx['manifest']['sha256'])==64
def test_no_alias_double_payment(ctx):assert len({r['canonical'] for r in ctx['selected']})==len(ctx['selected'])
def test_gap_coverage_evidence(ctx):assert ctx['stages']['7']['rows'][0]['目标_度']=='20'

