# Using the OpenAI API to interact with the Llama 3.1 hosted on Azure AI Model-as-a-Service
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

endpoint = os.environ["LLAMA_API_ENDPOINT"]
deployment = os.environ["LLAMA_API_MODEL"]
key = os.environ["LLAMA_API_KEY"]

client = OpenAI(
api_key = key,
base_url = endpoint
)

response = client.chat.completions.create(
model=deployment,
messages=[
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "Why is the sky blue?"}
]

)

#print(response.model_dump_json(indent=2))
print(response.choices[0].message.content)

