import json
import os
import urllib.parse
import urllib.request
import urllib.error

CLIENT_ID = os.environ['GH_CLIENT_ID']
CLIENT_SECRET = os.environ['GH_CLIENT_SECRET']


def request(url, values, headers):
    data = json.dumps(values)
    data = data.encode()

    headers = {
            "Authorization": "token " + os.environ["GH_TOKEN"],
            "Content-Type": "application/json"}

    req = urllib.request.Request(url, data, headers)

    print(data)
    
    try:
        res = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print(dir(e))
        print(e.msg)
        print(e.info())
        print()
        page = e.file.read()
        print(page)
        print(json.loads(page))
    else:
        print(res.read())
    

    #print(requests.post(url, data, headers))


def pull_request():
    url = "https://api.github.com/repos/chuck1/ws_web_aiohttp/pulls"
    values = {
            "title": "test",
            "head": "iss387",
            "base": "dev",
            #"body": "this is a test of the github api",
            }

    headers = {}

    request(url, values, headers)

pull_request()

