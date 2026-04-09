import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from IPython.display import display, Markdown

load_dotenv(override=True)

open_api_key = os.getenv("OPENAI_API_KEY")


if open_api_key:
    print(f"OpenAI API key found: {open_api_key[:8]}...")
else:
    print("OpenAI API key not found")

print(f"-------------------------------------------\n")


request = "Please come up with a challenging, nuanced question that I can ask a number of LLMs to evaulate their intelligence. Please provide the question, the answer, and the model used to answer the question."
request += "Answer only with questions, no explanation, no answers."

messages = [{'role': 'user', 'content': request}]

openai_client = OpenAI(api_key=open_api_key)
response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages)

question = response.choices[0].message.content
print(f"{question}")

competitors = ["gpt-4o-mini", "gpt-4o", "gpt-4o-2024-08-06", "gpt-4o-2024-08-06"]
question_messages = [{'role': 'user', 'content': question}]
answers = {}

for competitor in competitors:
    client = OpenAI(api_key=open_api_key)
    response = client.chat.completions.create(
        model=competitor,
        messages=question_messages)
    answers[competitor] = response.choices[0].message.content
    print(f"\n------------------------------------")
    print(f"Answer by {competitor}: {answers[competitor]}")
    print(f"\n-------------------------------------\n")



