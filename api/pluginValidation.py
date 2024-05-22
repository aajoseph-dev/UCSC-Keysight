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




def llm_code_check(command, code, device_name, selection): # selction 0 for test step; selection 1 for instrument
    load_dotenv()

    sid = SentimentIntensityAnalyzer()

    client = AzureOpenAI(
            azure_endpoint = "https://opentap-forum-openai.openai.azure.com/", 
            api_key=os.getenv("Forum-GPT4_KEY1"),  
            api_version="2024-02-15-preview"
    )

    prompt = ""

    if selection == 0:
        context = callAISearch(command)
        
        prompt = f"""Is the following code an acceptable file to be part of a Opentap plugin. This file is 
                    the {command} subsystem for the {device_name}:
                    
                    Here is some revelant documentation related to the device use it to verify the following code:
                    
                    documentation:
                    {context}

                    Verify this code:
                    {code}
                    """
    elif selection == 1:
        context = callAISearch(command)
        
        prompt = f"""Is the following code an acceptable file to be a test instrument declaration for an Opentap plugin. 
                    This file is for the {device_name}.
                    
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

    if scores['compound'] >= 0.25: # before it was 0.05
        print(f'''
              - 2nd LLM believes the plugin to be correct.
              - 2nd LLM's response: {content}''')
        return {"Sentiment" : "Positive", "Response" : content}
    elif scores['compound'] <= -0.25: # before it was 0.05
        print(f'''
              - 2nd LLM believes the plugin to be incorrect.
              - 2nd LLM's response: {content}''')
        return {"Sentiment" : "Negative", "Response" : content}
    else:
        print(f'''
              - 2nd LLM could not determine if the plugin was correct.
              - 2nd LLM's response: {content}''')
        return {"Sentiment" : "Neutral", "Response" : content}

    