from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import os

project_connection_string = os.environ.get("PROJECT_CONNECTION_STRING")

project = AIProjectClient.from_connection_string(
    conn_str=project_connection_string, credential=DefaultAzureCredential()
)

chat = project.inference.get_chat_completions_client()
response = chat.complete(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "Describe this image" },
                {
                    "type": "image_url",
                    "image_url": { "url": "https://azure.microsoft.com/en-us/blog/wp-content/uploads/2024/07/bCLO20b_Sylvie_office_night_001-1024x683.jpg" }
                }
            ]
        }
    ],
)

print(response.choices[0].message.content)