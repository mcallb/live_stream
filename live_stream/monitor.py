#!/usr/bin/env python

from live_stream.xively import Xively
import threading
import argparse
from live_stream.youtube import GoogleConnection

def run():
    threading.Timer(60, run).start()
    mySearch = GoogleConnection(args.client_secret)
    myXively = Xively(args.xively_secret)
    status = mySearch.stream_status()
    myXively.send_request(status)

if __name__ == '__main__':
    my = GoogleConnection('/home/brian/.credentials/client_secrets.json')
    print dir(my)
    print my._get_authenticated_service()
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-c', '--client_secret', help='The fully qualified path to your google api client_secret.json',
    #                 required=True)
    # parser.add_argument('-x', '--xively_secret', help='The fully qualified path to your xively api client_secret.json',
    #                 required=True)
    #
    # args=parser.parse_args()
    # run()