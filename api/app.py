from flask import Flask, jsonify, request
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/generate_plugin', methods=['POST'])
def generate_plugin():
    load_dotenv()
    llm = AzureOpenAI(
        azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
        api_key=os.getenv("OPENAI_KEY1"),  
        api_version=os.getenv("OPENAI_API_VERSION_ENV")
    )
    data = request.get_json()
    user_input = data.get('user_input', '')
    message_text = [{"role": "user", "content": user_input}]
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
    response = {
            "generated_plugin": completion.choices[0].message.content
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
