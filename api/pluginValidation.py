from flask import Flask, jsonify, request, send_file
from xml.dom import minidom
import requests
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path
from dotenv import load_dotenv
import re
import importlib.metadata as metadata
import shutil
import os
from datetime import datetime

from openai import AzureOpenAI
from nltk.sentiment.vader import SentimentIntensityAnalyzer


from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from promptTemplates import *
from app import *

def llm_code_check(command, code, device_name):
    load_dotenv()

    sid = SentimentIntensityAnalyzer()

    client = AzureOpenAI(
            azure_endpoint = "https://opentap-forum-openai.openai.azure.com/", 
            api_key=os.getenv("Forum-GPT4_KEY1"),  
            api_version="2024-02-15-preview"
    )

    context = callAiSearch(command)

    prompt = f"""Is the following code an acceptable file to be part of a Opentap plugin. This file is 
                the {command} subsystem for the {device_name}:
                
                Here is some revelant documentation related to the device use it to verify the following code:
                
                documentation:
                {context}

                Verify this code:
                {code}
                """
    message_text = [{"role":"system", "content":"You are an AI assistant that helps people verify Opentap plugins."}, 
                    {"role": "user", "content": prompt}]

    completion = client.chat.completions.create(
        model="gpt-4-1106-Preview",
        messages = message_text,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    content = completion.choices[0].message.content
    print(content)
    scores = sid.polarity_scores(content)

    if scores['compound'] >= 0.05:
        print("Positive")
    elif scores['compound'] <= -0.05:
        print("Negative")
    else:
        print("Neutral")
    
    return content

# def soemhing()
#     print(f"\ninitial code: {code}\n\n")

#     # Loading api keys from .env folder
#     load_dotenv()

#     # for 2nd llm:
#     openai.api_type = "azure"
#     openai.api_version = "2024-02-15-preview" # maybe?2023-05-15   api_version="2024-02-15-preview"

#     openai.api_base = os.getenv('Forum-GPT4_ENDPOINT') 
#     openai.api_key = os.getenv("Forum-GPT4_KEY1")
#     deployment_id2 = "gpt-4-1106-Preview" 

#     # Sets up the OpenAI Python SDK to use your own data for the chat endpoint.
#     setup_byod(deployment_id2)

#     context = retrieve_context(code)

#     content = '''Your answer should contain CORRECT if you believe the Python code is part of a correctly 
#                  implemented OpenTAP plugin based on the context that is provided to you below.
#                  Otherwise, your answer should contain INCORRECT if you believe it to be wrong, and if so
#                  return any errors that you believe there to be. Make your response as concise as possible.
#                  Use this context to base your answer off of:\n'''
#     content += context
#     message_text = [
#         {"role" : "system", "content": content},
#         {"role": "user", "content": code}]
#     print(f"\n\nmessage_text: {message_text}\n\n")

#     completion = openai.ChatCompletion.create(
#             messages=message_text,
#             deployment_id=deployment_id2,
#             temperature=0,
#             top_p=1,
#             max_tokens=200,
#         )

#     print("\ndone talking with 2nd llm\n")

#     # Grabbing just the response and leaving our unnecessary data (i.e. token used, filters, etc.) 
#     response = completion.choices[0].message.content
#     print(f"\n\nLLM 2's response: {response}\n\n")

#     return response
