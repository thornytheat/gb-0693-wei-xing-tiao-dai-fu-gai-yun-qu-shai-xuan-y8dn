from app.domain import length
from app.numeric import number
from app.modules.m6_purchase.rules import apply
from copy import deepcopy
def test_budget_not_exceeded(ctx):assert number(ctx['purchase_cost'])<=1000
def test_positive_marginal_gain(ctx):assert all(number(r['gain'])>0 for r in ctx['selected'])
def test_selected_unique(ctx):assert len({r['canonical'] for r in ctx['selected']})==len(ctx['selected'])
def test_sample_complete(ctx):assert length(ctx['purchase_coverage'])==20
def test_purchase_order_deterministic(ctx):
    c=deepcopy(ctx);c['usable'].reverse();apply(c);assert [r['canonical'] for r in c['selected']]==[r['canonical'] for r in ctx['selected']]
def test_free_scene(ctx):
    c=deepcopy(ctx);c['usable']=[{**c['usable'][0],'price_n':0}];apply(c);assert c['purchase_cost']==0
def test_empty_catalogue():assert apply({'usable':[]})['rows']==[]

