import os
from dotenv import load_dotenv
import json
from openai import AzureOpenAI
load_dotenv()

endpoint = os.environ["AZURE_OPENAI_API_ENDPOINT"]
deployment = os.environ["AZURE_OPENAI_API_MODEL"]
key = os.environ["AZURE_OPENAI_API_KEY"]
version = os.environ["AZURE_OPENAI_API_VERSION"]

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=key,
    api_version=version,
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "Extract the weather data."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "The temperature in London has reached freezing point, and there's an easterly wind."
                }
            ]
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "weather_data",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location to get the weather for"
                    },
                    "unit": {
                        "type": [
                            "string",
                            "null"
                        ],
                        "description": "The unit to return the temperature in",
                        "enum": [
                            "F",
                            "C"
                        ]
                    },
                    "value": {
                        "type": "number",
                        "description": "The actual temperature value in the location",
                        "minimum": -130,
                        "maximum": 130
                    },
                    "wind_direction": {
                        "type": "string",
                        "description": "The wind direction using compass points",
                        "pattern": r"\b(N|S|E|W|NNE|NE|ENE|ESE|SE|SSE|SSW|SW|WSW|WNW|NW|NNW)\b"
                    }
                },
                "additionalProperties": False,
                "required": [
                    "location",
                    "unit",
                    "value",
                    "wind_direction"
                ]
            }
        }
    },
    temperature=1,
    max_completion_tokens=2048,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

completion_json = response.to_json()
completion_text = json.loads(completion_json)

content = completion_text['choices'][0]['message']['content']
print(content)