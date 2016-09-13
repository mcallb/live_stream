#!/usr/bin/python
from retrying import retry
from connection import GoogleConnection

class GetStream():
    def __init__(self):
        # Create a connection to the google api
        self.youtube = GoogleConnection().youtube
        self.channel_id = "UCe3yFIa92jfAHEu4Ql4u69A"

    # Issue a search for a live video event on the users channel
    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_delay=30000)
    def stream_status(self):

        list_streams_request = self.youtube.search().list(
            part="id,snippet",
            channelId=self.channel_id,
            maxResults= "1",
            eventType="live",
            type="video"
        )

        while list_streams_request:
            list_streams_response = list_streams_request.execute()

            # No results are returned the live stream is down
            if list_streams_response.get("pageInfo")["totalResults"]==0:
                print "Live stream is down"
                return "down"
            else:
                # There is at least one element returned so the feed is up
                for stream in list_streams_response.get("items", []):
                    if stream["snippet"]["liveBroadcastContent"]=="live":
                        print "Live stream %s is up" % stream["snippet"]["title"]
                        return "up"

if __name__ == "__main__":
    myStream=GetStream()
    myStream.stream_status()


