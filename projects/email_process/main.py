import re
import json
from pprint import pprint


with open('content2.txt') as f:
    d = json.load(f)

c = d['content']


c = c.replace('\r\n','')

r = re.findall('<tr.*?>(.*?)</tr>', c)


s = r[2]
m = re.match('.*?(\d+\.\d+) USD.*', s)
amount = float(m.group(1))

s = r[3]
td = re.findall('<td.*?>(.*?)</td>', s)
a = td[1].strip()
a = re.sub('<a.*?>(.*?)</a>','\\1',a)
desc = a

s = r[4]
td = re.findall('<td.*?>(.*?)</td>', s)
a = td[1].strip()
a = re.match('.*(\d\d/\d\d/\d\d\d\d).*', a)
date = a.group(1)

r = {'amount': amount, 'description': desc, 'date': date}

print(r)



