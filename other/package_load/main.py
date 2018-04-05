import subprocess
import requests

url = 'https://github.com/chuck1/jessica/archive/master.zip'

r = requests.get(url)

with open('temp.zip', 'wb') as f:
    f.write(r.content)



