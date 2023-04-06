# -*- coding: utf-8 -*-


from summ.kv_stores.kv_store import KVStore


class DictStore(KVStore):

    def __init__(self):
        self.buf = {}

    def get(self, key: str) -> str:
        if key not in self.buf:
            raise KeyError(f"Key {key} is not exist.")
        return self.buf[key]
    
    def set(self, key: str, val: str) -> bool:
        self.buf[key] = val

    def keys(self):
        for key in self.buf.keys():
            yield key

