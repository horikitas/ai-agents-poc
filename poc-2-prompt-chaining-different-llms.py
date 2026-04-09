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
    print("---- Querying OpenAI-----")
    openai_client = OpenAI(api_key=open_api_key)
    response = openai_client.chat.completions.create(
        model=model_name,
        messages=messages)
    return response.choices[0].message.content

def queryClaude(messages, model_name):
    print("--------Querying Anthropic----------")
    claude_client = Anthropic(api_key=anthropic_api_key)
    response = claude_client.messages.create(model=model_name, messages=messages, max_tokens=1000)
    return response.content[0].text

def queryOllama(messages, model_name):
    print("---------Querying Ollama-----------")
    ollama_client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
    response = ollama_client.chat.completions.create(model=model_name, messages=messages)
    return response.choices[0].message.content

def queryModel(company_name, model_name, messages):
    response=""
    company=company_name.lower()
    if(company == "openai"):
        response=queryOpenAI(messages, model_name)
    elif(company == "anthropic"):
        response=queryClaude(messages, model_name)
    elif(company == "ollama"):
        response=queryOllama(messages, model_name)
    else:
        response="No valid company"
    return response


def queryModels(competitor_models, question_messages):
    answers={}
    for company, model_name in competitor_models.items():
        answers[company]=queryModel(company_name=company, model_name=model_name, messages=question_messages)
        print(f"\n------------------------------------------------")
        print(f"Answer from {company}: \n")
        print(answers[company])
        print(f"End of answer form {company} \n")
        print(f"-------------------------------------------------\n")
    return answers


request = "Please come up with a challenging, nuanced question that I can ask a number of LLMs to evaulate their intelligence. Please provide the question, the answer, and the model used to answer the question."
request += "Answer only with questions, no explanation, no answers. Do not include markdown or numbered lists in the response."
messages = [{'role': 'user', 'content': request}]
question = queryOpenAI(messages, "gpt-4o-mini")
print(f"{question}")

competitor_models = {"anthropic": "claude-sonnet-4-6", 
                    "openai": "gpt-4o-mini",
                    "ollama": "llama3.2"}#, "google": ""}
question_messages = [{'role': 'user', 'content': question}]
answers = queryModels(competitor_models=competitor_models, question_messages=question_messages)

judge_request = f"""You are judging a competition between {len(competitor_models)} competitors.
Each model has been given this question - 

{question}

Your job is to evaluate each response for clarity and strength of argument, and rank them in order of test to worst.

Respond with JSON, and only JSON, with following format:
{{"results": ["best competitor name", "second best competitor name", "third best competitor name",...]}}

Here are the responses from competitors:

{answers}

Now respond with the JSON with the ranked order of the competitors, nothing else. Do not include markdown formatting or code blocks."""

print(judge_request)

judge_request_messages = [{'role': 'user', 'content': judge_request}]

judge_response=queryOpenAI(messages=judge_request_messages, model_name="o3-mini")

print(judge_response)






