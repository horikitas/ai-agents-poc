import os
import json
from annotated_types import LowerCase
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from IPython.display import display, Markdown

load_dotenv(override=True)

open_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

if open_api_key:
    print(f"OpenAI API key found: {open_api_key[:8]}...")
else:
    print("OpenAI API key not found")

if anthropic_api_key:
    print(f"Anthropic API key found: {anthropic_api_key[:8]}...")
else:
    print("Anthropic API key not found")

if google_api_key:
    print(f"Google API key found: {google_api_key[:8]}...")
else:
    print("Google API key not found")

if deepseek_api_key:
    print(f"DeepSeek API key found: {deepseek_api_key[:8]}...")
else:
    print("DeepSeek API key not found")

if groq_api_key:
    print(f"Groq API key found: {groq_api_key[:8]}...")
else:
    print("Groq API key not found")


def queryOpenAI(messages, model_name):
    openai_client = OpenAI(api_key=open_api_key)
    response = openai_client.chat.completions.create(
        model=model_name,
        messages=messages)
    return response.choices[0].message.content

def queryClaude(messages, model_name):
    claude_client = Anthropic(api_key=anthropic_api_key)
    response = claude_client.messages.create(model=model_name, messages=messages, max_tokens=1000)
    return response.content[0].text

def queryModel(company_name, model_name, messages):
    response=""
    company=company_name.lower()
    if(company == "openai"):
        response=queryOpenAI(messages, model_name)
    elif(company == "anthropic"):
        #response=queryClaude(messages, model_name)
        response="Enable Claude for this"
    else:
        response="No valid company"
    return response

request = "Please come up with a challenging, nuanced question that I can ask a number of LLMs to evaulate their intelligence. Please provide the question, the answer, and the model used to answer the question."
request += "Answer only with questions, no explanation, no answers."
messages = [{'role': 'user', 'content': request}]
question = queryOpenAI(messages, "gpt-4o-mini")
print(f"{question}")

competitor_models = {"anthropic": "claude-3-7-sonnet-latest", "openai": "gpt-4o-mini"}#, "google": ""}
question_messages = [{'role': 'user', 'content': question}]
answers = {}

for company, model_name in competitor_models.items():
    answers[company]=queryModel(company_name=company, model_name=model_name, messages=question_messages)
    print(f"\n------------------------------------------------")
    print(f"Answer from {company}: \n")
    print(answers[company])
    print(f"-------------------------------------------------\n")




