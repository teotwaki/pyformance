#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import time
from twisted.internet.task import LoopingCall

from pyformance.registry import global_registry


class TxReporter(object):
    def __init__(self, registry=None, reporting_interval=30, clock=None):
        self.registry = registry or global_registry()
        self.reporting_interval = reporting_interval
        self.clock = clock or time
        self._looping_call = LoopingCall(self.report_now, self.registry)

    def start(self):
        if not self._looping_call.running:
            self._looping_call.start(self.reporting_interval)

    def stop(self):
        if self._looping_call.running:
            self._looping_call.stop()

    def report_now(self, registry=None, timestamp=None):
        raise NotImplementedError(self.report_now)
