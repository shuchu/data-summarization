# -*- coding: utf-8 -*-


from typing import Generator

from summ.kv_stores.kv_store import KVStore


class DictStore(KVStore):
    def __init__(self):
        self.buf = {}

    def get(self, key: str) -> str:
        if key not in self.buf:
            raise KeyError(f"Key {key} is not exist.")
        return self.buf[key]

    def set(self, key: str, val: str) -> None:
        self.buf[key] = val

    def keys(self) -> Generator[None, str, None]:
        for key in self.buf.keys():
            yield key
