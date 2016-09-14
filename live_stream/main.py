#!/usr/bin/env python
import live_stream
from live_stream.xively import Xively
from live_stream.getstream import GetStream
import threading
import argparse


def main():
    threading.Timer(60.0, main).start()
    mySearch = GetStream('/home/brian/.credentials/client_secrets.json')
    myXively = Xively('/home/brian/.credentials/xively.json')
    status = mySearch.stream_status()
    myXively.send_request(status)

main()