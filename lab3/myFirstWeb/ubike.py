import urllib.request as request
import json


def get_data():
    src="https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    print("hi")
    with request.urlopen(src) as response:
        
        return json.load(response)