###
#Copyright (c) Microsoft Corporation
#All rights reserved. 
#MIT License
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the ""Software""), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###
import http.client, urllib.parse, json

#Note: Sign up at http://www.projectoxford.ai to get a subscription key.  
#Search for Speech APIs from Azure Marketplace.
#Use the subscription key as Client secret below.
clientId = "1496f70a8d8748ef971bcd1477077016"
clientSecret = "ecbb319bcecf433e93fa366c3d8cf812"
ttsHost = "https://speech.platform.bing.com"

params = urllib.parse.urlencode({'grant_type': 'client_credentials', 'client_id': clientId, 'client_secret': clientSecret, 'scope': ttsHost})

print ("The body data: %s" %(params))

headers = {"Content-type": "application/x-www-form-urlencoded"}
			
AccessTokenHost = "oxford-speech.cloudapp.net"
path = "/token/issueToken"

# Connect to server to get the Oxford Access Token
conn = http.client.HTTPSConnection(AccessTokenHost)
conn.request("POST", path, params, headers)
response = conn.getresponse()
print(response.status, response.reason)

data = response.read()
conn.close()

accesstoken = data.decode("UTF-8")
print ("Oxford Access Token: " + accesstoken)

#decode the object from json
ddata=json.loads(accesstoken)
access_token = ddata['access_token']

body = """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="zh-HK">
<voice name="Microsoft Server Speech Text to Speech Voice (zh-HK, Danny, Apollo)">
<prosody rate="slow">
    <phoneme alphabet="x-microsoft-ups" ph="D OU T2 T1 T3"> tomato </phoneme>
    <phoneme alphabet="x-microsoft-ups" ph="D OU T2 T4 T2"> tomato </phoneme>
    <phoneme alphabet="x-microsoft-ups" ph="D OU T5 T3"> tomato </phoneme>
    <phoneme alphabet="x-microsoft-ups" ph="D OU T2 T4"> tomato </phoneme>
    <phoneme alphabet="x-microsoft-ups" ph="D OU T5 T5"> tomato </phoneme>
    <phoneme alphabet="x-microsoft-ups" ph="D OU T3 T3"> tomato </phoneme>
    </prosody>
    </voice>
</speak>"""

headers = {"Content-type": "application/ssml+xml", 
			"X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm", 
			"Authorization": "Bearer " + access_token, 
			"X-Search-AppId": "07D3234E49CE426DAA29772419F436CA", 
			"X-Search-ClientID": "1ECFAE91408841A480F00935DC390960", 
			"User-Agent": "TTSForPython"}
			
#Connect to server to synthesize the wave
conn = http.client.HTTPSConnection("speech.platform.bing.com")
conn.request("POST", "/synthesize", body.encode('utf-8'), headers)
response = conn.getresponse()
print(response.status, response.reason)

data = response.read()
output = open('data.wav', 'wb')
output.write(data)
output.close()
conn.close()
print("The synthesized wave length: %d" %(len(data)))