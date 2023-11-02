# -*- coding: utf-8 -*-
from datetime import datetime
import time


class SnowFlake:
    twepoch = int(datetime(2023, 1, 1, 0, 0, 0, 0).timestamp() * 1000)
    worker_id_bits = 5
    datacenter_id_bits = 5
    max_worker_id = -1 ^ (-1 << worker_id_bits)
    max_datacenter_id = -1 ^ (-1 << datacenter_id_bits)
    sequence_bits = 12
    worker_id_shift = sequence_bits
    datacenter_id_shift = sequence_bits + worker_id_bits
    timestamp_left_shift = sequence_bits + worker_id_bits + datacenter_id_bits
    sequence_mask = -1 ^ (-1 << sequence_bits)

    sequence = 0
    last_timestamp = -1
    current_id = -1

    def __init__(self, worker_id: int, datacenter_id: int):
        self.worker_id = worker_id
        self.datacenter_id = datacenter_id

        self.sequence = 0
        self.last_timestamp = -1
        self._current_id = None

        assert worker_id >= 0 and worker_id <= self.max_worker_id
        assert datacenter_id >= 0 and datacenter_id <= self.max_datacenter_id

    @staticmethod
    def time_gen():
        return int(time.time() * 1000)

    def til_next_millis(self):
        timestamp = self.time_gen()
        while timestamp <= self.last_timestamp:
            timestamp = self.time_gen()
        return timestamp

    def next_id(self):
        timestamp = self.time_gen()
        if timestamp < self.last_timestamp:
            raise RuntimeError(
                f"Clock moved backwards. Refusing to generate id for {self.last_timestamp - timestamp} milliseconds"
            )
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.sequence_mask
            if self.sequence == 0:
                timestamp = self.til_next_millis()
        else:
            self.sequence = 0
        self.last_timestamp = timestamp
        next_id = str(
            timestamp - self.twepoch << self.timestamp_left_shift
            | self.datacenter_id << self.datacenter_id_shift
            | self.worker_id << self.worker_id_shift
            | self.sequence
        )
        self._current_id = next_id
        return next_id

    def current_id(self):
        if self._current_id == None:
            return self.next_id()
        return self._current_id


id_gen = SnowFlake(0, 0)
