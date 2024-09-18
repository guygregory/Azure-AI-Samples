import os
from openai import AzureOpenAI
import base64
from dotenv import load_dotenv
import json

load_dotenv()

endpoint = os.environ["AZURE_OPENAI_API_ENDPOINT"]
deployment = os.environ["AZURE_OPENAI_API_MODEL"] # Ensure you are using gpt-4o, version 2024-08-06, or later to use Structured Outputs
key = os.environ["AZURE_OPENAI_API_KEY"]
version = os.environ["AZURE_OPENAI_API_VERSION"] #  #Ensure you are using "2024-08-01-preview" version of the API, or later to use Structured Outputs

IMAGE_PATH = "./book.jpeg"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image(IMAGE_PATH)
   
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=key,
    api_version=version,
)
      
completion = client.chat.completions.create(
    model=deployment,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract the key information from this book."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                            "detail": "high"
                            },]
        }],          
            
    response_format={
        "type": "json_schema",
        "json_schema": {   
        "name": "structured_output",
            "schema": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string"
                    },
                    "author": {
                        "type": "string"
                    },
                    "publisher": {
                        "type": "string"
                    }
                },
                "required": ["title", "author", "publisher"]
            }
        }
    }

)

completion_json = completion.to_json()
completion_text = json.loads(completion_json)

content = completion_text['choices'][0]['message']['content']
print(content)