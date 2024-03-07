from flask import Flask, jsonify, request
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

#This files serves as our backend and is responsible for making calls to azure

app = Flask(__name__)

#Example call
#The route specifics the call to reach this function
#if you wanted to use this call you would call http://127.0.0.1:5000/helloworld" 
@app.route('/helloworld')
def hello():
    return 'Hello, World!'


#This function configures chat bot and gets response
@app.route('/generate_plugin', methods=['POST'])
def generate_plugin():
    #loading api keys from .env folder
    load_dotenv()
    #configures Azure chatbot with our specified keys
    llm = AzureOpenAI(
        azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
        api_key=os.getenv("OPENAI_KEY1"),  
        api_version=os.getenv("OPENAI_API_VERSION_ENV")
    )

    #get data sent from client.py
    data = request.get_json()
    user_input = data.get('user_input', '')
    #formatting message based on azure requirments
    message_text = [{"role": "user", "content": user_input}]

    #message is sent to chatbot and response is returned
    completion = llm.chat.completions.create(
        model="OpenTap-Plugin-LLM", 
        messages = message_text,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    #grabbing just the response and leaving our unnecessary data(i.e. token used, filters, etc.)
    response = {
            "generated_plugin": completion.choices[0].message.content
        }
    #returns response in json format to client
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
