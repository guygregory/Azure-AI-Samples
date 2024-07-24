# Interacting with the Llama 3.1 model hosted on Azure AI Model-as-a-Service directly via the API
import urllib.request
import json
import os
import ssl
from dotenv import load_dotenv

load_dotenv()

endpoint = os.environ["LLAMA_API_ENDPOINT"]
deployment = os.environ["LLAMA_API_MODEL"]
key = os.environ["LLAMA_API_KEY"]

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

data =  {
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful AI assistant."
    },
    {
      "role": "user",
      "content": "Why is the sky blue?"
    }
  ],
  "model":deployment,
  "max_tokens": 128,
  "temperature": 0.8,
  "top_p": 0.1,
  "best_of": 1,
  "presence_penalty": 0,
  "use_beam_search": "false",
  "ignore_eos": "false",
  "skip_special_tokens": "false"
}

body = str.encode(json.dumps(data))

url = endpoint+"/chat/completions"
# Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
api_key = key
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")


headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    #print(result)
    response = json.loads(result.decode("utf-8"))
    print(response['choices'][0]['message']['content'])

except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))
