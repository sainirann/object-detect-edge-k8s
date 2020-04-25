import os
import sys
import requests

url = 'http://localhost:31507'

files = {
    'file': (
        sys.argv[1], 
        open(sys.argv[1], 'rb'), 
        'application/octet-stream'
    )
}

res = requests.post(url, files=files)
print(res.status_code)
