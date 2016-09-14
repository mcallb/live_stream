#!/usr/bin/env python
import live_stream
from live_stream.xively import Xively
from live_stream.getstream import GetStream
import threading
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c','--client_secret', help='The fully qualified path to your google api client_secret.json', required=True)
parser.add_argument('-x','--xively_secret', help='The fully qualified path to your xively api client_secret.json', required=True)
args = vars(parser.parse_args())

def main():
    threading.Timer(60.0, main).start()
    mySearch = GetStream('/home/brian/.credentials/client_secrets.json')
    myXively = Xively('/home/brian/.credentials/xively.json')
    status = mySearch.stream_status()
    myXively.send_request(status)

main()

if __name__ == "__main__":
    main()