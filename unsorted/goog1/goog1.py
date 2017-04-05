import urllib, os
import json as m_json
import string

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


query = raw_input ( 'Query: ' )
query = urllib.urlencode ( { '' : query } )
query = string.lstrip(query,'=')
query = 'q=site:' + query

response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
json = m_json.loads ( response )
results = json [ 'responseData' ] [ 'results' ]
#for result in results:
    # title = result['title']
    #url = result['url']   # was URL in the original and that threw a name error exception
    # print ( title + '; ' + url )
    #print ( url )

#first_result = results[0]
url = results[0]['url']
print url

#create desination directory
urlclean = string.replace(url,':','')
urlclean = string.replace(urlclean,'/','')
filename = 'vids/' + urlclean + '/'

ensure_dir(filename)

urllib.urlretrieve (url + 'videos/1.wmv', filename + '1.wmv')


