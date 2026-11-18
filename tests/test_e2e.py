def test_all_pages_render(client):
    for n in range(1,8): assert client.get('/work/'+str(n)).status_code==200
def test_end_to_end_idempotence(client):
    first=client.post('/api/run',json={}).get_json();again=client.post('/api/run',json={}).get_json()
    assert first['manifest']['run_id']==again['manifest']['run_id'];assert again['reused'] is True
    assert len(client.get('/api/history').get_json())==1
def test_review_rejects_stale_version(client):
    run=client.post('/api/run',json={}).get_json();payload={'id':run['manifest']['run_id'],'revision':1,'decision':'通过'}
    assert client.post('/api/review',json=payload).status_code==200
    assert client.post('/api/review',json=payload).status_code==409
def test_empty_input_is_recoverable(client):
    assert client.post('/api/run',json={'csv':''}).status_code==422
    assert client.post('/api/run',json={}).status_code==200
def test_evidence_has_manifest_and_reason(client):
    text=client.get('/api/evidence.csv').data.decode('utf-8-sig')
    assert 'run_id' in text and '规则版本' in text and '原因码' in text
def test_independent_module_endpoints(client):
    for n in range(1,8):
        response=client.post('/api/m'+str(n),json={})
        assert response.status_code==200;assert response.get_json()['stage']==n
def test_selected_batch_survives_interleaved_rerun(client,raw):
    first=client.post('/api/run',json={'csv':raw}).get_json();other=client.post('/api/run',json={'csv':raw+'\n'}).get_json();again=client.post('/api/run',json={'csv':raw}).get_json()
    assert first['manifest']['run_id']==again['manifest']['run_id']!=other['manifest']['run_id']
    ident=first['manifest']['run_id'];page=client.get('/work/4?run_id='+ident).data.decode();evidence=client.get('/api/evidence.csv?run_id='+ident).data.decode('utf-8-sig')
    assert ident in page and ident in evidence and other['manifest']['run_id'] not in evidence
def test_unknown_batch_is_404(client):
    assert client.get('/work/1?run_id=absent').status_code==404
    assert client.get('/api/evidence.csv?run_id=absent').status_code==404
def test_invalid_review_action(client):
    run=client.post('/api/run',json={}).get_json()
    assert client.post('/api/review',json={'id':run['manifest']['run_id'],'revision':1,'decision':'其他'}).status_code==422

def test_non_object_json_never_runs_default_sample(client):
    for endpoint in ['/api/run','/api/review']+['/api/m'+str(n) for n in range(1,8)]:
        for value in ([],[1],'text',7,True,None):
            response=client.post(endpoint,json=value) if value is not None else client.post(endpoint,data='null',content_type='application/json')
            assert response.status_code==400 and response.get_json()['code']=='REQUEST'
    assert client.get('/api/history').get_json()==[]

def test_malformed_or_non_json_is_bad_request(client):
    assert client.post('/api/run',data='{',content_type='application/json').status_code==400
    assert client.post('/api/run',data='csv=text').status_code==400

def test_wrong_upload_field_is_bad_request(client):
    import io
    assert client.post('/api/run',data={'wrong':(io.BytesIO(b'a,b'),'wrong.csv')}).status_code==400

def test_rule_version_is_part_of_batch_identity(monkeypatch):
    import app.manifest as manifest
    first=manifest.make('same content')
    monkeypatch.setattr(manifest,'RULE_VERSION','future-rules')
    second=manifest.make('same content')
    assert first['sha256']==second['sha256'] and first['run_id']!=second['run_id']

def test_multi_cloud_format_switch_keeps_legacy_batch(client,raw,monkeypatch):
    # 旧契约批次先签核落库；随后目录升级为多离散云区
    legacy_text=raw.replace('179;-180,180;-179','179,-179')
    monkeypatch.setattr('app.manifest.RULE_VERSION','2026.11.18.2')
    legacy=client.post('/api/run',json={'csv':legacy_text}).get_json()
    legacy_id=legacy['manifest']['run_id']
    client.post('/api/review',json={'id':legacy_id,'revision':1,'decision':'通过'})
    monkeypatch.setattr('app.manifest.RULE_VERSION','2026.11.18.3')
    upgraded=client.post('/api/run',json={'csv':raw}).get_json()
    assert upgraded['manifest']['rule_version']=='2026.11.18.3' and legacy['manifest']['rule_version']=='2026.11.18.2'
    assert upgraded['manifest']['run_id']!=legacy_id
    # 旧批次按原契约版本重放：复核身份、决定、覆盖结果均不改写
    fetched=client.get('/api/runs/'+legacy_id)
    assert fetched.status_code==200, fetched.get_json()
    replayed=fetched.get_json()
    assert replayed['manifest']['run_id']==legacy_id and replayed['decision']=='通过' and replayed['revision']==2
    old_row={r['场景']:r for r in replayed['stages']['3']['rows']}['DATELINE']
    new_row={r['场景']:r for r in upgraded['stages']['3']['rows']}['DATELINE']
    assert old_row['有效宽度_度']==new_row['有效宽度_度']=='5'

def test_failed_switch_keeps_previous_batch_and_retry_is_same_batch(client,raw):
    good=client.post('/api/run',json={'csv':raw}).get_json()
    # 结构性失败：422 且不产生批次，上一版候选保留
    blocked=client.post('/api/run',json={'csv':''})
    assert blocked.status_code==422
    assert [h['id'] for h in client.get('/api/history').get_json()]==[good['manifest']['run_id']]
    # 行级裁决失败：批次保留隔离证据，不动旧候选；同一目录重试不新增批次
    bad_rows=raw.replace('179;-180,180;-179','179;-180,180')  # 端点数不一致
    quarantined=client.post('/api/run',json={'csv':bad_rows}).get_json()
    assert any(q['原因码']=='CLOUD' for q in quarantined['quarantine'])
    assert client.post('/api/run',json={'csv':bad_rows}).get_json()['manifest']['run_id']==quarantined['manifest']['run_id']
    # 修正后重试回到原候选批次
    fixed=client.post('/api/run',json={'csv':raw}).get_json()
    assert fixed['manifest']['run_id']==good['manifest']['run_id'] and fixed['reused'] is True
    history=client.get('/api/history').get_json()
    assert len(history)==2 and good['manifest']['run_id'] in [h['id'] for h in history]

def test_multi_cloud_pages_and_evidence_compare_both_batches(client,raw,monkeypatch):
    legacy_text=raw.replace('179;-180,180;-179','179,-179')
    monkeypatch.setattr('app.manifest.RULE_VERSION','2026.11.18.2')
    legacy=client.post('/api/run',json={'csv':legacy_text}).get_json()
    monkeypatch.setattr('app.manifest.RULE_VERSION','2026.11.18.3')
    current=client.post('/api/run',json={'csv':raw}).get_json()
    for ident in (legacy['manifest']['run_id'],current['manifest']['run_id']):
        page=client.get('/work/3?run_id='+ident).data.decode()
        evidence=client.get('/api/evidence.csv?run_id='+ident).data.decode('utf-8-sig')
        assert ident in page and ident in evidence and 'DATELINE' in evidence
    current_evidence=client.get('/api/evidence.csv?run_id='+current['manifest']['run_id']).data.decode('utf-8-sig')
    assert '-180--179' in current_evidence and '179-180' in current_evidence

def test_multi_cloud_idempotent_retry_no_new_batch(client):
    text=open('sample_data/multi-cloud.csv',encoding='utf-8').read()
    first=client.post('/api/run',json={'csv':text}).get_json()
    again=client.post('/api/run',json={'csv':text}).get_json()
    assert first['manifest']['run_id']==again['manifest']['run_id'] and again['reused'] is True
    assert len(client.get('/api/history').get_json())==1

