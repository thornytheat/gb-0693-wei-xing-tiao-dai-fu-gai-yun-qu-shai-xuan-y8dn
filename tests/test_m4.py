from app.domain import merge,length
from decimal import Decimal
def test_union_not_sum():assert length([(0,10),(5,15)])==15
def test_adjacent_merge():assert merge([(0,5),(5,10)])==[(0,10)]
def test_union_empty():assert merge([])==[]
def test_sample_coverage(ctx):assert length(ctx['coverage'])==20
def test_union_order_independent():assert merge([(5,15),(0,10)])==merge([(0,10),(5,15)])
def test_no_zero_span():assert merge([(5,5)])==[]
def test_capped_target(ctx):assert length(ctx['coverage'])<=20

