              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 3.1.4


    ====================================
    wishbone.module.output.elasticsearch
    ====================================

    Version: 1.0.0

    Index data into Elasticsearch.
    ------------------------------
    Index data into Elasticsearch.

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


