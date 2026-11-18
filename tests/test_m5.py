from app.domain import subtract,length,TARGET
def test_no_sample_gap(ctx):assert ctx['gaps']==[]
def test_partial_gap():assert subtract([(0,10)],[(2,8)])==[(0,2),(8,10)]
def test_whole_target_missing():assert length(subtract(TARGET,[]))==20
def test_gap_conservation(ctx):assert length(ctx['coverage'])+length(ctx['gaps'])==20
def test_boundaries_not_duplicated():assert subtract([(0,5),(5,10)],[(0,5)])==[(5,10)]
def test_sample_percentage(ctx):assert ctx['stages']['5']['metrics'][2][1]=='100'
def test_nested_mask():assert subtract([(0,10)],[(1,9),(2,8)])==[(0,1),(9,10)]

