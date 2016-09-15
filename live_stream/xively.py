import requests
import json
from retrying import retry

class Xively():
    def __init__(self,filename):
        self.file_name = filename
        self.header = self._load_api_key()
        self.xively_endpoint = 'https://api.xively.com/v2/feeds/727218522'

    # Load xively api key from file
    def _load_api_key(self):
        with open(self.file_name) as api_key:
            header = json.load(api_key)
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

if __name__ == "__main__":
    x = Xively()
    x.send_request("down")
