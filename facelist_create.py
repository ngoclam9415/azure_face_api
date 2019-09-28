import config as Config

# endpoint = " https://westcentralus.api.cognitive.microsoft.com/face/v1.0"
subscription_key = "21a089f5199d436798ccbacbbf22b6f3"

########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64, json

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': Config.subscription_key,
}

params = urllib.parse.urlencode({
})

body = {
    "name": Config.faceListId,
    "userData": "Hello Lam Nguyen",
    "recognitionModel": "recognition_02"
}

try:
    conn = http.client.HTTPSConnection(Config.endpoint)
    conn.request("PUT", "/face/v1.0/facelists/{}".format(Config.faceListId), json.dumps(body), headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {}".format(e))

####################################