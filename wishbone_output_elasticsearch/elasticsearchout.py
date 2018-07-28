#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  elasticsearchout.py
#
#  Copyright 2018 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from wishbone.module import OutputModule
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from wishbone.event import extractBulkItems


class ElasticSearchOut(OutputModule):
    """Index data into Elasticsearch.

    Index JSON data into the Elasticsearch document store. Events can be
    indexed one by one or in bulk if the submitted event is of such type.

    Parameters:
        - ca_certs(str)(None)
           |  The path to cacerts to include

        - doc_type(str)("wishbone")
           |  The document type

        - hosts(list)(["localhost:9200"])
           |  A list of "hostname:port" strings.

        - index(str)("wishbone")
           |  The name of the index

        - native_events(bool)(False)
           |  Outgoing events should be native Wishbone events

        - parallel_streams(int)(1)
           |  The number of outgoing parallel data streams.

        - payload(str)(None)
           |  The string to submit.
           |  If defined takes precedence over `selection`.

        - selection(str)("data")
           |  The part of the event to submit externally.
           |  Use an empty string to refer to the complete event.

        - use_ssl(bool)(False)
           |  When enable expects SSL connectivity

        - verify_certs(bool)(False)
           |  When using SSL do certificate verification


    Queues:

        - inbox
           |  Incoming events submitted to the outside.

    """

    def __init__(
        self,
        actor_config,
        ca_certs=None,
        doc_type="wishbone",
        hosts=["localhost:9200"],
        index="wishbone",
        native_events=False,
        payload=None,
        selection="data",
        parallel_streams=1,
        use_ssl=False,
        verify_certs=False,
    ):
        OutputModule.__init__(self, actor_config)
        self.pool.createQueue("inbox")
        self.registerConsumer(self.consume, "inbox")

    def preHook(self):
        self.elasticsearch = Elasticsearch(
            self.kwargs.hosts,
            use_ssl=self.kwargs.use_ssl,
            verify_certs=self.kwargs.verify_certs,
            ca_certs=self.kwargs.ca_certs,
        )

    def consume(self, event):
        if event.isBulk():
            bulk_items = []
            for e in extractBulkItems(event):
                kwargs = {"_index": self.kwargs.index, "_type": self.kwargs.doc_type}
                source = e.get(self.kwargs.selection)
                if "_id" in source:
                    kwargs["id"] = source.pop("_id")
                kwargs["_source"] = source
                bulk_items.append(kwargs)
            resp = bulk(self.elasticsearch, bulk_items)
            self.logging.debug("Indexed bulk: {}".format(resp))
        else:
            body = event.get(self.kwargs.selection)
            kwargs = {"index": self.kwargs.index, "doc_type": self.kwargs.doc_type}
            if "_id" in body:
                kwargs["id"] = body.pop("_id")
            kwargs["body"] = body
            resp = self.elasticsearch.index(**kwargs)
            self.logging.debug("Idexed: {}".format(resp))
