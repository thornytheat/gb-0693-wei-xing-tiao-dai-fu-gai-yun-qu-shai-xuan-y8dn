from app.domain import split,aliases
from decimal import Decimal
def test_dateline_split(): # TRAP-23
    assert split('178','-175')==[(Decimal('-180'),Decimal('-175')),(Decimal('178'),Decimal('180'))]
def test_number_fullwidth(): # TRAP-06
    assert split('１７０','１８０')==[(Decimal(170),Decimal(180))]
def test_missing_coordinate(ctx): # TRAP-07
    assert any(r['原因码']=='MISSING' for r in ctx['quarantine'])
def test_duplicate_does_not_cover_twice(ctx): # TRAP-14
    assert ctx['duplicates']==1
def test_alias_equivalence(): # TRAP-22
    rows=[{'scene':'B','alias':'A'},{'scene':'C','alias':'B'}];assert aliases(rows)==aliases(list(reversed(rows)))
def test_bad_coordinate(ctx): assert any(q['原因码']=='COORD' for q in ctx['quarantine'])
def test_newest_version_rules(raw): # TRAP-25
    from app.pipeline import calculate
    tail='SC0000,,165,167,,,pass,20,2026-11-17T00:00:00Z,2\n';result=calculate(raw+tail);assert any(q['原因码']=='SUPERSEDED' for q in result['quarantine'])


def test_quarantined_alias_cannot_merge_good_scenes(raw):
    import csv,io
    from app.pipeline import calculate
    records=list(csv.DictReader(io.StringIO(raw)));bad={**records[0],'alias':'SOUTH','west':'N/A'}
    out=io.StringIO();writer=csv.DictWriter(out,fieldnames=list(bad));writer.writeheader();writer.writerows(records+[bad])
    baseline=calculate(raw);result=calculate(out.getvalue())
    assert {r['canonical'] for r in baseline['scenes']}=={r['canonical'] for r in result['scenes']}
    assert len(result['scenes'])==42 and sum(q['原因码']=='MISSING' for q in result['quarantine'])==2
