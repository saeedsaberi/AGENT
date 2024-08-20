import os
import openai
from openai import OpenAI


openai.api_key = os.environ["OPENAI_API_KEY"]
messages = [{"role": "system", "content": "You are an intelligent assistant."}]
   

client = OpenAI(api_key=openai.api_key)


MODEL="gpt-4"

completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": "You are a helpful assistant that helps me with my math homework!"},
    {"role": "user", "content": "Hello! Could you solve 20 x 5?"}
  ]
)
print("Assistant: " + completion.choices[0].message.content)


# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")