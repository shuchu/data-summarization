# -*- coding: utf-8 -*-


from typing import List


class Entity:

    @classmethod
    def is_device_id(cls, device_id: str) -> bool :
        if len(device_id) != 8:
            return False
        try:
            id_int = int(device_id, 16)
        except Exception:
            return False
        return True

    @classmethod
    def is_event_type(cls, event_type: str) -> bool:
        if len(event_type) > 0 and len(event_type) <= 256:
            return True
        else:
            return False

    @classmethod
    def join_keys(cls, device_id: str, event_type: str) -> str:
        return '{}|{}' % (device_id, event_type)

    @classmethod
    def disjoin_key(cls, key: str) -> List[str]:
        res = key.strip().split('|')
        if len(res) != 2:
            # Malformed one
            return ['', '']
        else:
            return res


