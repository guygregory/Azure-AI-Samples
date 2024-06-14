# Streaming completions with Azure OpenAI service, using the 1.x version of the openai Python package.
# Define Azure OpenAI API endpoint, deployment, key, and version in a .env file.

import os
import asyncio
from openai import AzureOpenAI, AsyncAzureOpenAI
from dotenv import load_dotenv

load_dotenv()

endpoint = os.environ["AZURE_OPENAI_API_ENDPOINT"]
deployment = os.environ["AZURE_OPENAI_API_MODEL"]
key = os.environ["AZURE_OPENAI_API_KEY"]
version = os.environ["AZURE_OPENAI_API_VERSION"]

client = AsyncAzureOpenAI(
    azure_endpoint = endpoint,
    api_key = key,
    api_version = version
    )

async def main() -> None:
    stream = await client.chat.completions.create(
        model=deployment,
        messages = [ {"role": "user", "content": "What is chatgpt?"} ],
        stream=True,
    )

    async for chunk in stream:
        if chunk.choices:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)

asyncio.run(main())