#!/usr/bin/env python
import live_stream
from live_stream.xively import Xively
from live_stream.getstream import GetStream
import threading

def main():
    threading.Timer(60.0, main).start()
    mySearch = GetStream()
    myXively = Xively()
    status = mySearch.stream_status()
    myXively.send_request(status)

main()