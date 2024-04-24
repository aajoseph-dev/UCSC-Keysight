from flask import Flask, jsonify, request, send_from_directory
from xml.dom import minidom
import os
import requests
from io import BytesIO
import zipfile
from pathlib import Path
from dotenv import load_dotenv
import openai

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient


def setup_byod(deployment_id: str) -> None:

    class BringYourOwnDataAdapter(requests.adapters.HTTPAdapter):

        def send(self, request, **kwargs):
            request.url = f"{openai.api_base}/openai/deployments/{deployment_id}/extensions/chat/completions?api-version={openai.api_version}"
            return super().send(request, **kwargs)

    session = requests.Session()

    # Mount a custom adapter which will use the extensions endpoint for any call using the given `deployment_id`
    session.mount(
        prefix=f"{openai.api_base}/openai/deployments/{deployment_id}",
        adapter=BringYourOwnDataAdapter()
    )

    openai.requestssession = session

def retrieve_context(code):
    # Define Azure search index properties
    endpoint = "https://azure-plugin-ai-search.search.windows.net"; 
    key = os.getenv("AZURE_AI_SEARCH_API_KEY"); 
    index_name = "plugin-pdf-vector"

    # Init the search index client
    credential = AzureKeyCredential(key)
    client = SearchClient(endpoint=endpoint,
                        index_name=index_name,
                        credential=credential)
    # fetch the related chunks for Azure AI Search
    context = """"""
    results = client.search(search_text=code, top = 2)
    for doc in results:
        print(f"content! {doc['content']}")
        context += "\n" + doc['content']
        
    print(f"context!: {context}")
    return context

def llm2_call(code):

    print(f"\ninitial code: {code}\n\n")

    # Loading api keys from .env folder
    load_dotenv()

    # for 2nd llm:
    openai.api_type = "azure"
    openai.api_version = "2024-02-15-preview" # maybe?2023-05-15   api_version="2024-02-15-preview"

    openai.api_base = os.getenv('Forum-GPT4_ENDPOINT') 
    openai.api_key = os.getenv("Forum-GPT4_KEY1")
    deployment_id2 = "gpt-4-1106-Preview" 

    # Sets up the OpenAI Python SDK to use your own data for the chat endpoint.
    setup_byod(deployment_id2)

    context = retrieve_context(code)

    content = '''Your answer should contain CORRECT if you believe the Python code is part of a correctly 
                 implemented OpenTAP plugin based on the context that is provided to you below.
                 Otherwise, your answer should contain INCORRECT if you believe it to be wrong, and if so
                 return any errors that you believe there to be. Make your response as concise as possible.
                 Use this context to base your answer off of:\n'''
    content += context
    message_text = [
        {"role" : "system", "content": content},
        {"role": "user", "content": code}]
    print(f"\n\nmessage_text: {message_text}\n\n")

    completion = openai.ChatCompletion.create(
            messages=message_text,
            deployment_id=deployment_id2,
            temperature=0,
            top_p=1,
            max_tokens=200,
        )

    print("\ndone talking with 2nd llm\n")

    # Grabbing just the response and leaving our unnecessary data (i.e. token used, filters, etc.) 
    response = completion.choices[0].message.content
    print(f"\n\nLLM 2's response: {response}\n\n")

    return response
