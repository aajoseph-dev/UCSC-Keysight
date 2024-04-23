from flask import Flask, jsonify, request, send_from_directory
from xml.dom import minidom
import os
import requests
from io import BytesIO
import zipfile
from pathlib import Path
from dotenv import load_dotenv
import openai



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

def llm2_call(code):

    print(f"\ninitial code: {code}\n\n")

    # Loading api keys from .env folder
    load_dotenv()

    # for 2nd llm:
    openai.api_type = "azure"
    openai.api_version = "2024-02-15-preview" # maybe?2023-05-15   api_version="2024-02-15-preview"

    openai.api_base = os.getenv('Forum-GPT4_ENDPOINT') 
    openai.api_key = os.getenv("Forum-GPT4_KEY1")
    # deployment_id2 = "OpenTAP-Forum-OpenAI"
    deployment_id2 = "gpt-4-1106-Preview" # using resource: "OpenTAP-Forum-OpenAI"

    # deployment_id = "OpenTap-Plugin-LLM"

    # Sets up the OpenAI Python SDK to use your own data for the chat endpoint.
    setup_byod(deployment_id2)

    search_endpoint = "https://azure-plugin-ai-search.search.windows.net"; 
    search_key = os.getenv("AZURE_AI_SEARCH_API_KEY"); 

    search_index_name = "plugin-pdf-vector"

    # Ask the chat bot
    # full_prompt = user_prompt + "- Using SCPI commands, implement this specific function: " + function
    message_text = [
        {"role" : "system", "content": "Verify that this Python code is correctly implemented based on SCPI commands and provide comments on whether or not you believe it to be correct. Return any errors that you believe there to be."},
        {"role": "user", "content": code}]
    print(f"\n\nmessage_text: {message_text}\n\n")

    # completion = openai.ChatCompletion.create( # openai.ChatCompletion.create
    #     model=deployment,
    #     messages=message_text,
    #     deployment_id=deployment_id2
    #     dataSources=[  # camelCase is intentional, as this is the format the API expects
    #             {
    #                 "type": "AzureCognitiveSearch",
    #                 "parameters": {
    #                     "endpoint": search_endpoint,
    #                     "indexName": search_index_name,
    #                     "semanticConfiguration": "default",
    #                     "queryType": "simple",
    #                     "fieldsMapping": {},
    #                     "inScope": True,
    #                     "roleInformation": "You are an AI assistant that takes in a user-specified device and writes only Python code yourself for OpenTAP plugins. Does not write any text. You take the specified command you are given and write plugin code for it.",
    #                     "filter": None,
    #                     "strictness": 3,
    #                     "topNDocuments": 5,
    #                     "key": search_key
    #                 }
    #             }
    #     ],
    # )
    completion = openai.ChatCompletion.create(
            messages=message_text,
            deployment_id=deployment_id2,
            # dataSources=[  # camelCase is intentional, as this is the format the API expects
            #     {
            #         "type": "AzureCognitiveSearch",
            #         "parameters": {
            #             "endpoint": search_endpoint,
            #             "indexName": search_index_name,
            #             "semanticConfiguration": "default",
            #             "queryType": "simple",
            #             "fieldsMapping": {},
            #             "inScope": True,
            #             "roleInformation": "You are an AI assistant that takes in a user-specified device and writes only Python code yourself for OpenTAP plugins. Does not write any text. You take the specified command you are given and write plugin code for it.",
            #             "filter": None,
            #             "strictness": 3,
            #             "topNDocuments": 5,
            #             "key": search_key
            #         }
            #     }
            # ],
            temperature=0,
            top_p=1,
            max_tokens=800,
        )

    print("\ndone talking with 2nd llm\n")

    # Grabbing just the response and leaving our unnecessary data (i.e. token used, filters, etc.) 
    response = completion.choices[0].message.content
    print(f"\n\nLLM 2's response: {response}\n\n")

    return response
