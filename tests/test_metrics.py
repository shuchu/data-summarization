# -*- coding: utf-8 -*-


import math
from summ.metrics import Metric
from summ.kv_stores.dict_store import DictStore


def test_update_states_once():
    # Test function call
    key = 'A'
    val = 1
    metrics = ['min']
    metric_buf = {}
    kv_store = DictStore()

    mymetrc = Metric(kv_store)
    mymetrc._update_stats_once(key, val, metrics, metric_buf)

    assert len(metric_buf.keys()) == 1
    assert key in metric_buf
    assert 'min' in metric_buf[key]
    assert 'max' not in metric_buf[key] 

    # Test metric calculation
    metrics = ['min', 'max', 'mean', 'hist10']
    metric_buf = {}

    mymetrc = Metric(kv_store)
    mymetrc._update_stats_once(key, 1, metrics, metric_buf)

    assert 'min' in metric_buf[key]
    assert 'max' in metric_buf[key]
    assert 'mean' in metric_buf[key]
    assert 'hist10' in metric_buf[key]
    assert metric_buf[key]['cnt'] == 1

    mymetrc._update_stats_once(key, 2, metrics, metric_buf)
    assert metric_buf[key]['cnt'] == 2
    assert metric_buf[key]['min'] == 1
    assert metric_buf[key]['max'] == 2
    assert math.fabs(metric_buf[key]['mean'] - 1.5) < 1e-5
    assert metric_buf[key]['hist10'][0] == 2


    mymetrc._update_stats_once(key, 27, metrics, metric_buf)
    assert metric_buf[key]['cnt'] == 3
    assert metric_buf[key]['min'] == 1
    assert metric_buf[key]['max'] == 27
    assert math.fabs(metric_buf[key]['mean'] - 10.0) < 1e-5
    assert metric_buf[key]['hist10'][0] == 2
    assert metric_buf[key]['hist10'][2] == 1


def test_calc_stats():
    kv_store = DictStore()
    mymetric = Metric(kv_store)

    # Test function
    device_id = '0123ABCD'
    kv_store.set('{}|A'.format(device_id), 10)
    kv_store.set('{}|B'.format(device_id), 30)

    res = mymetric.calc_stats(eval_key=device_id)
    assert device_id in res
    assert res[device_id]['min'] == 10
    assert res[device_id]['max'] == 30
    assert math.fabs(res[device_id]['mean'] - 20.0) < 1e-5
    assert res[device_id]['cnt'] == 2

    # Test eval_key is *
    res = mymetric.calc_stats()
    assert device_id in res
    assert res[device_id]['min'] == 10
    assert res[device_id]['max'] == 30
    assert math.fabs(res[device_id]['mean'] - 20.0) < 1e-5
    assert res[device_id]['cnt'] == 2

    # Test eval_key is not correct
    res = mymetric.calc_stats(eval_key='BAD')
    assert not res
    res = mymetric.calc_stats(eval_key='')
    assert not res

    # Test event_type is not correct
    res = mymetric.calc_stats(eval_key=device_id, eval_type='event_type')
    assert not res
    res = mymetric.calc_stats(eval_key=device_id, eval_type='I_do_not_want_to_tell')
    assert not res

    # Test select metrics
    for m in {'min', 'max', 'mean'}:
        res = mymetric.calc_stats(eval_key=device_id, metrics=[m])
        assert device_id in res
        assert m in res[device_id]
        assert len(res[device_id].keys()) == 2  # has key "cnt" by default

    m = 'hist10'
    res = mymetric.calc_stats(eval_key=device_id, metrics=[m])
    assert not res

    res = mymetric.calc_stats(eval_key='A', eval_type='event_type', metrics=[m])
    print(res)
    assert 'A' in res
    assert m in res['A']

    # Test mix metrics

    metrics = ['min', 'micky', 'Musky', 'Mermaid']
    res = mymetric.calc_stats(eval_key=device_id, metrics=metrics)
    assert 'min' in res[device_id]
    assert len(res[device_id].keys()) == 2  # has key 'cnt' by default
    assert 'Mermaid' not in res[device_id]