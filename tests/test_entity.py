# -*- coding: utf-8 -*-


from summ.entity import Entity

def test_is_device_id():
    id = '1234ABCD'
    assert Entity.is_device_id(id)

    id = 'ABCDEFGH'
    assert not Entity.is_device_id(id)

    id = '123456789ABCD'
    assert not Entity.is_device_id(id)

    id = '00000000'
    assert Entity.is_device_id(id)

    id = ''
    assert not Entity.is_device_id(id)

def test_is_event_type():
    et = ''
    assert not Entity.is_event_type(et)

    et = 'Squirrel'
    assert Entity.is_event_type(et)

    et = ''.join(['a']*257)
    assert not Entity.is_event_type(et)

    et = ''.join(['a']*256)
    assert Entity.is_event_type(et)

def test_join_keys():
    l = 'L'
    r = 'R'
    assert Entity.join_keys(l,r) == 'L|R'

def test_disjoin_key():
    t = 'L|R'
    l, r = Entity.disjoin_key(t)
    assert l == 'L'
    assert r == 'R'

    t = 'L|R|C'
    l, r = Entity.disjoin_key(t)
    assert l == 'L'
    assert r == 'R|C'

    t = 'L||R'
    l, r = Entity.disjoin_key(t)
    assert l == 'L'
    assert r == '|R'

