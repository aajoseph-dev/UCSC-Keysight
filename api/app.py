from flask import Flask, jsonify, request, make_response, send_file
from xml.dom import minidom 
import os
from io import StringIO, BytesIO
from openai import AzureOpenAI
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

#This files serves as our backend and is responsible for making calls to azure

app = Flask(__name__)


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
    response = {"generated_plugin": completion.choices[0].message.content}
    #returns response in json format to client
    return jsonify(response)

@app.route('/generate_py', methods=['POST'])
def generate_py():
    try:
        data = request.get_json() 
    except:
        return jsonify({'error': 'Invalid JSON format'}), 400  

    if not data:
        return jsonify({'error': 'No data found in request'}), 400  

    name = data.get('name')
    data = data.get('data')
    print("name: ", name, "data: ", data)

    # Create a new BytesIO, prep for generaing python file
    file_py = BytesIO() # It creates a binary stream that operates on an in-memory byte buffer.
    file_py.write(data.encode())
    file_py.seek(0)
    response = make_response(file_py.read())
    response.headers['Content-Type'] = 'text/x-python'
    return response

@app.route('/generate_xml', methods=['POST'])
def generate_xml():
    try:
        data = request.get_json() 
    except:
        return jsonify({'error': 'Invalid JSON format'}), 400  

    if not data:
        return jsonify({'error': 'No data found in request'}), 400  
    name = data.get('name')
    py_file = data.get('py_file')

    print("name: ", name, "py_file: ", py_file)
    # needs name of python file, and py_file = path to python file
    
    # Initialize document called doc
    doc = minidom.Document() 
    
    # Create root element <Package>
    package = doc.createElement('Package')  
    doc.appendChild(package)

    # Set attributes for <Package>
    package.setAttribute('Name', name) 
    package.setAttribute('xmlns', "http://keysight.com/Schemas/tap") 
    package.setAttribute('Version', "$(GitVersion)") 
    package.setAttribute('OS', "Windows,Linux,MacOS") 

    # Create child element <Description>
    des = doc.createElement('Description')
    package.appendChild(des)
    
    # Add text to description
    des_text = doc.createTextNode('TEST')
    des.appendChild(des_text)

    # Create child element <Prerequisites>
    prereq = doc.createElement('Prerequisites')
    des.appendChild(prereq)
    prereq_text = doc.createTextNode(' Python (>3.7) ')
    prereq.appendChild(prereq_text)

    # Create child element <Files>
    files = doc.createElement('Files')
    package.appendChild(files)

    # Create child element <File>
    py = doc.createElement('File')
    py.setAttribute('Path', py_file)
    files.appendChild(py)

    # Create end tag for project file
    end_project_file = doc.createElement('ProjectFile')
    py.appendChild(end_project_file) 

    # Generate the xml string
    xml_str = doc.toprettyxml(indent ="\t", encoding="UTF-8")  

    # TODO: Write to file
  
    # XML file name created in the same direction as where the create_xml.py is ran
    save_path_file = "new_xml.xml"
    
    # Save the xml file in binary
    with open(save_path_file, "wb") as f: 
         f.write(xml_str)

if __name__ == '__main__':
    app.run(debug=True)
    generate_xml()
