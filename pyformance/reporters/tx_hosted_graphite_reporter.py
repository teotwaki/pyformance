#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import base64

from StringIO import StringIO
from twisted.internet import reactor
from twisted.web.client import (Agent, FileBodyProducer)
from twisted.web.http_headers import Headers

from pyformance.reporters.txreporter import TxReporter


class TxHostedGraphiteReporter(TxReporter):

    def __init__(self, api_key, reactor=reactor, registry=None,
                 reporting_interval=10,
                 url="https://hostedgraphite.com/api/v1/sink", clock=None):
        super(TxHostedGraphiteReporter, self).__init__(registry,
                                                       reporting_interval,
                                                       clock)
        self._agent = Agent(reactor)
        self.url = url.encode('utf-8')
        self.api_key = api_key

        encoded = base64.encodestring(self.api_key).strip().encode('utf-8')
        self._headers = Headers({b'Authorization': [b'Basic %s' % (encoded,)]})

    def report_now(self, registry=None, timestamp=None):
        metrics = self._collect_metrics(registry or self._registry, timestamp)

        if metrics:
            body = FileBodyProducer(StringIO(metrics.encode('utf-8')))
            self._agent.request(b'POST', self.url, self._headers, body)

    def _collect_metrics(self, registry, timestamp=None):
        timestamp = timestamp or int(round(self.clock.time()))
        metrics = registry.dump_metrics()
        metrics_data = []

        for key in metrics.keys():
            for value_key in metrics[key].keys():
                metric_line = "%s.%s %s %s\n" % (key, value_key,
                                                 metrics[key][value_key],
                                                 timestamp)
                metrics_data.append(metric_line)

        return ''.join(metrics_data)
