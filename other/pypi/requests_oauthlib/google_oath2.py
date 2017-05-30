#!/usr/bin/env python3
import sys
import aiohttp
import aiohttp.web
import json
import requests_oauthlib
import ssl
import modconf

conf = modconf.import_conf('google_oauth2', sys.argv[1])

SCHEME = 'https'

async def handle(request):
    
    scope = ['https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile']
    oauth = requests_oauthlib.OAuth2Session(
            conf.client_id,
            redirect_uri=SCHEME + '://' + conf.URL + '/google_oauth2_response',
            scope=scope)
    authorization_url, state = oauth.authorization_url(
            'https://accounts.google.com/o/oauth2/auth',
            # access_type and approval_prompt are Google specific extra
            # parameters.
            access_type="offline", approval_prompt="force")

    print('state =',state)

    # Store the oauth object using state as identifier.
    # It will be needed in the response handler
    app['oauth'][state] = oauth
    
    return aiohttp.web.HTTPFound(authorization_url)

async def google_oauth2_response_handler(request):

    authorization_response = request.scheme + '://' + request.host + request.path_qs

    #state = request.match_info.get('state')

    state = request.GET['state']

    oauth = app['oauth'][state]

    token = oauth.fetch_token(
            'https://accounts.google.com/o/oauth2/token',
            authorization_response=authorization_response,
            # Google specific extra parameter used for client
            # authentication
            client_secret=conf.client_secret)

    r = oauth.get('https://www.googleapis.com/oauth2/v1/userinfo')
    
    print(dict(r.json()))

    response = aiohttp.web.Response(text='hello')
    return response



app = aiohttp.web.Application()

app['oauth'] = {}

app.router.add_get('/', handle)
app.router.add_get('/google_oauth2_response', google_oauth2_response_handler)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.load_cert_chain(conf.certfile, conf.keyfile)

aiohttp.web.run_app(app, port=443, ssl_context=ssl_context)





