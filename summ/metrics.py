# -*- coding: utf-8 -*-


from typing import List
from logging import Logger
from collections import defaultdict

from summ.kv_stores.kv_store import KVStore
from summ.entity import Entity


class Metric:
    def __init__(self, logger: Logger, kvstore: KVStore):
        self._logger = logger
        self._kvstore = kvstore
        self._supported_metrics = {
                'device_id': {'min', 'max', 'mean',},
                'event_type': {'hist10',}
                }
    
    def calc_stats(
            self, 
            eval_key: str = '*',
            eval_type: str = '',
            metrics: List[str] = ['*']
        ) -> dict:
        """ Calculate the metrics for given key and its evaluation type. 
            
        Args:
            metrics: list of metric names, for example ['min', 'max']
            
        Returns:
            A dict object stores the calculated metrics.
        """
        res = {}

        if eval_type not in self._supported_metrics:
            self._logger.warning('The eval_type is missing. available options: {}.' % self._supported_metrics.keys())
            return res

        if eval_type == 'device_id' and eval_key != '*' and  !Entity.is_device_id(eval_key):
            self._logger.warning('The input eval_key is a malformed device_id.')
            return res
        
        if eval_type == 'event_type' and eval_key != '*' and !Entity.is_event_type(eval_key):
            self._logger.warning('The input eval_key is a malformed event_type.')
            return res

        # Check the name of given metrics
        filtered_metrics = set()
        if len(metrics) == 1 and metrics[0] == '*':
            filtered_metrics = self._supported_metrics[eval_type]
        else:
            for m in metrics:
                if m in self._supported_metrics[eval_type]:
                    filtered_metrics.add(m)

        if not filtered_metrics:
            return res
        
        # Do calculation Iteratively
        for k in self._kvstore.keys():
            dev_id, ev_type = Entity.disjoin_key(k)
            if not dev_id or not ev_type:
                continue
            
            # Not a match.
            if (eval_type == 'device_id' and eval_key != '*' and eval_key != dev_id) or 
               (eval_type == 'event_type' and eval_key != '*' and eval_key != ev_type):
                continue
            
            self._update_stats_once(eval_key, int(self._kvstore.get(k)), filtered_metrics, res)

        return res
            
    def _update_stats_once(self, key: str, val: int,  metrics: List[str], metric_buf: dict) -> None:
        """ Update the statistics of a key with value val.
         
        Args:
            key: the evaluation key.
            val: the new value of key.
            metrics: list of metrics about to calculating.
            metric_buf: the buffer which stores the calculated statistical results.
        """
        if key in metric_buf:
            stat = metric_buf[key]
        else:
            stat = {'cnt': 0}
            metric_buf[key] = stat

        # Count in current key. Please aware while calculating complex statistics.
        stat['cnt'] += 1

        for metric in metrics:
            if metric == 'min':
                if 'min' not in stat:
                    stat['min'] = val
                elif val < stat['min']:
                    stat['min'] = val

            if metric == 'max':
                if 'max' not in stat:
                    stat['max'] = val
                elif val > stat['max']:
                    stat['max'] = val

            if metric == 'mean':
                if 'mean' not in stat:
                    stat['mean'] = val
                else:
                    stat['mean'] += (val - stat['mean'])/stat['cnt']

            if metric == 'hist10':
                if 'hist10' not in stat:
                    stat['hist10'] = defaultdict(int)
                else:
                    idx = val // 10  # histogram with bin size 10
                    stat['hist10'][idx] += 1

        metric[key] = stat
        
