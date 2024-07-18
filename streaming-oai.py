# Streaming example for OpenAI's GPT-4o mini model (platform.openai.com) - NB this approach will not work with the AzureOpenAI service, please use the streaming-aoai.py example instead.
# NB - in the .env file, you will need to set the OPENAI_API_KEY environment variable to your OpenAI API key.

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Give me a recipe for chocolate cake"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
