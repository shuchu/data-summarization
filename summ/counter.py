# -*- coding: utf-8 -*-

from typing import List, Tuple
import logging 
from collections import defaultdict

from summ.kv_stores.kv_store import KVStore
from summ.entity import Entity


_logger = logging.getLogger(__name__)


class Counter:
    def __init__(self, kv_store: KVStore):
        self._store = kv_store

        # Record the counts of (device_id, event_type) pairs for a single file.
        self._count_buf = defaultdict(int)  

    def update_by_file(self, fpath: str, header: bool = True) -> None:
        _logger.info('Processing file: {}' % fpath)

        with open(fpath, 'r') as f:
            if header:
                next(f)   
            for line in f:
                dev_id, ev_type = self.extract_record(line)
                if dev_id and ev_type:
                    self._count_buf[Entity.join_keys(dev_id, ev_type)] += 1
        
        # updated the buffered result to global kvstor
        self.update_to_global_store()

        _logger.info('Processed file: {}' % fpath)

    def extract_record(self, record: str) -> Tuple[str, str]:
        """ Extract the content of one line in the .csv data file. The extraced values will be
        checked. If any of them are malformed, this line will be ignored.
        
        Assume the content has following format with an example:
            ------
            #timestamp,device_id,event_type,event_payload
            1595275375.814,0c428083,squirrel,e3d387ad18f528237bb7
            ...
            ------
        timestamp: floating-point timestamp as seconds from UTC epoch with milliseconds as the decimal
        device_id: an 8 character hexadecimal string
        event_type: an ascii string under 256 characters
        event_payload: a binary payload for the event type

        The value of device_id and event_type are case-insensitive

        Args:
            record: an input string end with a newline-delimited.

        Returns:
            The tuple (device_id, event_type). Both strings will be transferred to uppercase. 
            An tuple ('','') will be returned if the line is malformed.
        """
        res = ('', '')

        r = record.strip().split(',')

        # Check the size of content
        if len(r) != 4:
            return res

        # Check the device_id as a hex string
        if not Entity.is_device_id(res[1]):
            return res

        # Check the length of event_type
        if not Entity.is_event_type(res[2]):
            return res

        # Transfer to uppercase
        res = (r[1].upper(), r[2].upper())

        return res

    def update_to_global_store(self,) -> None:
        """ Update one file's statisitcs to the global storage. """

        if not self._store:
            _logger.error("The instance of global storage is empty.")
            return

        for key in self._count_buf:
            try:
                global_val = self._store.get(key)
            except KeyError:
                # Key is not exist
                self._store.set(key, str(self._count_buf[key]))
            except Exception as e:
                # Unexcepted exception, stop and check
                _logger.error("Unexcepted errors while reading from global store: {}" % e)
                return
            else:
                tmp = self._count_buf[key] + int(global_val)
                self._store.set(key, str(tmp))

        # clean the buff
        self._count_buf.clear()


