#!/usr/bin/python

from xively import Xively
from getstream import GetStream
import threading

def main():
    threading.Timer(60.0, main).start()
    mySearch = GetStream()
    myXively = Xively()
    status = mySearch.stream_status()
    myXively.send_request(status)

main()