# -*- coding: utf-8 -*-


from summ.counter import Counter
from summ.kv_stores.dict_store import DictStore


def test_extract_record():
    kv_store = DictStore()
    mycounter = Counter(kv_store)

    r = "1595275375.814,0c428083,squirrel,e3d387ad18f528237bb7"
    d, e = mycounter.extract_record(r)
    assert d == "0c428083".upper()
    assert e == "squirrel".upper()

    r = "0c428083,squirrel,e3d387ad18f528237bb7"
    d, e = mycounter.extract_record(r)
    assert not d
    assert not e

    r = "a, b, c ,d, 0c428083,squirrel,e3d387ad18f528237bb7"
    d, e = mycounter.extract_record(r)
    assert not d
    assert not e

    r = ",,,,"
    d, e = mycounter.extract_record(r)
    assert not d
    assert not e

    r = ""
    d, e = mycounter.extract_record(r)
    assert not d
    assert not e
