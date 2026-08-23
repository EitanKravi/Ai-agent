import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("API key wasn't found")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        }
    ],
)

if response.usage.completion_tokens is None:
    raise RuntimeError()

print("User prompt: {}".format(response.choices[0].message.content))

print("Prompt tokens: {}".format(response.usage.prompt_tokens))
print("Response tokens: {}".format(response.usage.completion_tokens))

print("Response:")
print(response.choices[0].message.content)
