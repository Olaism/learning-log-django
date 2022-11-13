import requests
from requests.auth import HTTPBasicAuth

url = 'http://127.0.0.1:8000/api/logs/ecn313/topic/5/entry/6/'

data = {'text': 'lorem ipsum dolor sit amet wewe.'}

auth0 = HTTPBasicAuth('admin', 'admin')
auth1 = HTTPBasicAuth('testuser01', 'testpassword01')

r = requests.get(url, auth=auth0)

print(r.json())