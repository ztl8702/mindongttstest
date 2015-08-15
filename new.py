import httplib

client = None


headers = {'Content-type': 'application/ssml+xml', 'X-Microsoft-OutputFormat': 'riff-8khz-8bit-mono-mulaw', 'User-Agent': 'TESTAPI', 'X-Search-AppId':'1496f70a8d8748ef971bcd1477077016'}

ssml = """ <speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)'>Microsoft Bing Voice Output API</voice></speak> """
client = httplib.HTTPConnection('speech.platform.bing.com', 80, timeout=10)
client.request('POST', '/synthesize', ssml, headers)
response = client.getresponse()
print response.status
print response.reason
print response.read()
print response.getheaders()
client.close()