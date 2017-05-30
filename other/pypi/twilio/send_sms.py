#!/usr/bin/env python3

import sys
from twilio.rest import Client
import modconf

if len(sys.argv) == 1:
    print('Usage: ' + sys.argv[0] + ' <mod_conf folder> <phone number> <message>')
    sys.exit(0)

conf = modconf.import_conf('twilio_conf', sys.argv[1])

print(sys.argv[2])
print(sys.argv[3])

client = Client(conf.account_sid, conf.auth_token)

client.messages.create(
        to=sys.argv[2],
        from_=conf.number,
        body=sys.argv[3])


