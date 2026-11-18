from app.reader import read_rows
def apply(ctx):
    rows=read_rows(ctx)
    return {'rows':rows,'metrics':[['目录记录',len(rows),'条'],['输入',ctx['input_count'],'条'],['目标宽度',20,'度']]}

