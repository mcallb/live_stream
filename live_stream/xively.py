import requests
import json
from retrying import retry
from credstash import getSecret

class Xively():
    def __init__(self):
        #self.file_name = filename
        self.header = self._load_api_key()
        self.xively_endpoint = 'https://api.xively.com/v2/feeds/727218522'

    # Load xively api key from encrypted table in dynamodb and create the header
    # getSecret is a method on the credstash class that returns the credential
    # for the xively api key
    def _load_api_key(self):
        header = {"X-ApiKey": getSecret('xively-key')}
        return header

    # Create the data for the request
    def create_json(self,status):
        data={
          "version":"1.0.0",
           "datastreams" : [ {
                "id" : "status",
                "current_value" : status
            }
          ]
        }
        json_data = json.dumps(data)
        return json_data

    # Put the request
    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_delay=30000)
    def send_request(self,status):
        json_data = self.create_json(status)
        try:
            r = requests.put(url=self.xively_endpoint,headers=self.header,data=json_data)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print e

# Entry point for an aws lambda function. Pass in the value "up" or "down" as a dictionary
def lambda_handler(event, context):
    x = Xively()
    print "Sending the request: %s" % event['status']
    x.send_request(event['status'])


if __name__ == "__main__":
    x = Xively()
    x.send_request("down")