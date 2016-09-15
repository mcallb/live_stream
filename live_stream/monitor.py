#!/usr/bin/env python

from live_stream.xively import Xively
from live_stream.getstream import GetStream
import threading
import argparse


class Monitor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #self.daemon = True

    def run(self):
        threading.Timer(60, self.run).start()
        mySearch = GetStream(args.client_secret)
        myXively = Xively(args.xively_secret)
        status = mySearch.stream_status()
        myXively.send_request(status)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--client_secret', help='The fully qualified path to your google api client_secret.json',
                    required=True)
    parser.add_argument('-x', '--xively_secret', help='The fully qualified path to your xively api client_secret.json',
                    required=True)
    args=parser.parse_args(['--client_secret', '/home/pi/.credentials/client_secrets.json', '--xively_secret', '/home/pi/.credentials/xively.json'])

    mon=Monitor()
    mon.run()
