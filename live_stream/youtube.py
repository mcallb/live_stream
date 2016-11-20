#!/usr/bin/python

import httplib2
import os
from retrying import retry
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


class GoogleConnection(object):
    def __init__(self,filename):
        # The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
        # the OAuth 2.0 information for this application, including its client_id and
        # client_secret. You can acquire an OAuth 2.0 client ID and client secret from
        # the {{ Google Cloud Console }} at
        # {{ https://cloud.google.com/console }}.
        # Please ensure that you have enabled the YouTube Data API for your project.
        # For more information about using OAuth2 to access the YouTube Data API, see:
        #   https://developers.google.com/youtube/v3/guides/authentication
        # For more information about the client_secrets.json file format, see:
        #   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        self.CLIENT_SECRETS_FILE = filename
        # This OAuth 2.0 access scope allows for read-only access to the authenticated
        # user's account, but not other types of account access.
        self.YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"
        # Path to the client.json file
        self.channel_id = "UCe3yFIa92jfAHEu4Ql4u69A"
        # This variable defines a message to display if the CLIENT_SECRETS_FILE is
        # missing.
        self.MISSING_CLIENT_SECRETS_MESSAGE = """
        WARNING: Please configure OAuth 2.0

        To make this sample run you will need to populate the client_secrets.json file
        found at:

           %s

        with information from the {{ Cloud Console }}
        {{ https://cloud.google.com/console }}

        For more information about the client_secrets.json file format, please visit:
        https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           self.CLIENT_SECRETS_FILE))
        #self.youtube=self._get_authenticated_service()


    def _get_authenticated_service(self):
        flow = flow_from_clientsecrets(self.CLIENT_SECRETS_FILE,
                                       scope=self.YOUTUBE_READONLY_SCOPE,
                                       message=self.MISSING_CLIENT_SECRETS_MESSAGE)

        flow.params['access_type'] = 'offline'
        storage = Storage("mysecret-oauth2.json")
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)

        return build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
                     http=credentials.authorize(httplib2.Http()))

    # Returns the status of a live stream to determine if it's online or offline
    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_delay=30000)
    def stream_status(self):
        youtube = self._get_authenticated_service()
        list_streams_request = youtube.search().list(
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
    #args = argparser.parse_args()
    myyoutube = GoogleConnection('/home/brian/.credentials/client_secrets.json')
    myyoutube.stream_status()
