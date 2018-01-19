import sys
import json
from pprint import pprint

with open(sys.argv[1]) as f:
    p = json.load(f)

for entity in p['blueprint']['entities']:
    if entity['name'] == 'fast-inserter':
        print(entity)

