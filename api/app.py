from flask import Flask, jsonify, request, send_from_directory
from xml.dom import minidom
import os
import requests
from io import BytesIO
import zipfile
from pathlib import Path
from dotenv import load_dotenv
import openai
import re

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

import tiktoken

from promptTemplates import PromptTemplates


app = Flask(__name__)

@app.route('/generate_plugin', methods=['POST'])
def handleRequest():
    # Get data from client
    data = request.get_json()
    # prompt = createPrompt(data)

    deviceName = data.get("deviceName")
    for command in data.get("commands"):
        context = callAiSearch(f"{deviceName}: {command}")
        prompt = createPrompt(data, command, context)
        callLLM(prompt, data)
        # clean the data and format to python File
        # we send it function
        
    
    return jsonify({"status": "success"})



def createPrompt(data, command, context):
    prompt_templates = PromptTemplates(data, context)
    
    scpi_commands = context.split('|')

    if data.get("useCase") == "generate_plugin":
        prompt = prompt_templates.generate_plugin_prompt(scpi_commands)
    # elif data.get("useCase") == "Power_supply_plugin":
    #     prompt = prompt_templates.test_plugin_prompt(scpi_commands)
    # elif data.get("useCase") == "Oscilloscopes_plugin":
    #     prompt = prompt_templates.test_plugin_prompt(scpi_commands)
    # etc..
    else:
        raise ValueError("Unknown use case")

    return prompt

def callLLM(prompt, data):

    openai.api_type = "azure"
    openai.api_base = "https://opentappluginai.openai.azure.com/"
    openai.api_version = "2023-09-15-preview"
    openai.api_key = os.getenv("OPENAI_KEY1")

    response = openai.Completion.create(
        engine="OpenTap-Plugin-LLM",
        prompt=prompt,
        temperature=0.7,  # Increase temperature for more diverse and creative responses
        max_tokens=1000,  # Increase max tokens to allow for longer responses
        top_p=1,
        frequency_penalty=0.2,  # Add frequency penalty to reduce repetition
        presence_penalty=0.2,  # Add presence penalty to encourage new ideas
        stop=None  # Remove stop sequence to allow complete responses
    )

    
    for choice in response['choices']:
        generated_text = choice['text']
        print(generated_text)

    return

def callAiSearch(query, TOKEN_LIMIT=500):

    load_dotenv()
    service_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
    index_name = "plugin-pdf-vector"
    key = os.getenv("AZURE_AI_SEARCH_API_KEY")

    try:
        search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))

        results = search_client.search(search_text=query)

        context = ""
        token_count = 0

        tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")

        for result in results:
            content = result['content']
            tokens = tokenizer.encode(content)
            if token_count + len(tokens) <= TOKEN_LIMIT:
                context += content
                token_count += len(tokens)
            else:
                remaining_tokens = TOKEN_LIMIT - token_count
                truncated_content = tokenizer.decode(tokens[:remaining_tokens])
                context += truncated_content
                break

        return context
    
    except Exception as e:
        print(f"Error during AI search: {e}")


def buildPy():
    pass

def buildXML():
    pass

def packageFiles():
    pass

if __name__ == '__main__':
    app.run(debug=True, port=5002)
