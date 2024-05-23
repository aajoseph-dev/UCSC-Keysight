from flask import Flask, jsonify, request, send_file
from xml.dom import minidom
from zipfile import ZipFile
from dotenv import load_dotenv
import shutil
import os
from datetime import datetime

from openai import AzureOpenAI

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

import tiktoken

from promptTemplates import PromptTemplates
from pluginValidation import *
from code_parser import *

load_dotenv()
app = Flask(__name__)

@app.route('/generate_plugin', methods=['POST'])
def handleRequest():
    
    data = request.get_json()
    print(data)
    deviceName = data.get("deviceName")
    dir = f"plugins/raw_files/{deviceName}"
    path_to_zip = f"plugins/zip_files/{deviceName}.zip"

    allowed_attempts = 1

    pt = PromptTemplates(data)

    if os.path.exists(dir):
        dir += "_"
        now = datetime.now()
        formatted_date_time = now.strftime("%m.%d.%y.%H.%M")
        dir += formatted_date_time

    os.makedirs(dir)

    instrument_code = createInstrument(data, dir)

    for command in data.get("commands"):

        context = callAISearch(f"{deviceName}: {command}")
        prompt = pt.generate_steps_prompt(command, instrument_code, context)
        response = callLLM(prompt)
        python_code = extract_python_code(response)

        verification_results = test_step_validation(python_code)
        validation_prompt = pt.generate_step_validation(python_code, command, instrument_code, context)
        llm_check = llm_code_check(validation_prompt)
        print(verification_results)

        count = 0
        while llm_check["Sentiment"] == "Negative" and count < allowed_attempts:

            prompt = pt.failed_test_step(python_code, command, context, llm_check["Response"], verification_results)
            response = callLLM(prompt) # pass the 2nd llm's response to the 1st llm
            python_code = extract_python_code(response)

            validation_prompt = pt.generate_step_validation(python_code, command, instrument_code, context)
            llm_check = llm_code_check(prompt) # go ask the 2nd llm's response yet
            
            count += 1

        buildPy(dir, command, response)

    buildXML(deviceName, dir)
    packageFiles(dir, path_to_zip)
    return send_file(path_to_zip, as_attachment=True)

def createInstrument(data, path):
    pt = PromptTemplates(data)
    
    deviceName = data.get("deviceName")

    context = callAISearch(f"{deviceName}")

    prompt = pt.generate_instrument_prompt(context)
    LLM_response = callLLM(prompt)

    python_code = extract_python_code(LLM_response)

    validation_results = instrument_validation(python_code)
    print(validation_results)

    if (len(validation_results) != 0):

        callAISearch(f"{deviceName}")
        validation_prompt = pt.generate_instrument_validation(python_code, context)
        llm_check = llm_code_check(validation_prompt)

        prompt = pt.failed_insturment(python_code, context, llm_check["Response"], validation_results)
        LLM_response = callLLM(prompt) # pass the 2nd llm's response to the 1st llm
        python_code = extract_python_code(LLM_response)

    buildPy(path, deviceName, python_code)
    return python_code


def callLLM(prompt):

    client = AzureOpenAI(
            azure_endpoint = "https://opentap-forum-openai.openai.azure.com/", 
            api_key=os.getenv("Forum-GPT4_KEY1"),  
            api_version="2024-02-15-preview"
    )

    message_text = [{"role":"system", "content":"You are an AI assistant that helps people Opentap plugins using SCPI commands in Python."}, 
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

    return content

def callAISearch(query, TOKEN_LIMIT=1500):

    service_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
    index_name = "plugin-pdf-vector"
    key = os.getenv("AZURE_AI_SEARCH_API_KEY")

    try:
        search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))

        results = search_client.search(search_text=query)

        context = ""
        token_count = 0

        tokenizer = tiktoken.encoding_for_model("gpt-4")

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


def buildPy(path, command, code):
    name = command.replace(" ", "_")

    pyFile = f"{path}/{name}.py"
    with open(pyFile, 'w') as file:
        file.write(code)
    return pyFile

def buildXML(plugin_name, folder_path):
    # Create an XML document
    doc = minidom.Document()
    
    # Create the main package element
    package = doc.createElement('Package')
    doc.appendChild(package)
    package.setAttribute('Name', plugin_name)
    package.setAttribute('xmlns', "http://keysight.com/Schemas/tap")
    package.setAttribute('Version', "1.0.0")
    package.setAttribute('OS', "Windows,Linux,MacOS")

    # Create the description element with prerequisites
    description = doc.createElement('Description')
    package.appendChild(description)

    prerequisites = doc.createElement('Prerequisites')
    description.appendChild(prerequisites)
    prerequisites_text = doc.createTextNode(' Python (>3.7) ')
    prerequisites.appendChild(prerequisites_text)

    # Create dependencies with specific package requirements
    dependencies = doc.createElement('Dependencies')
    package.appendChild(dependencies)

    opentap_dependency = doc.createElement('PackageDependency')
    dependencies.appendChild(opentap_dependency)
    opentap_dependency.setAttribute('Package', 'OpenTAP')
    opentap_dependency.setAttribute('Version', '^9.18.2')

    files = doc.createElement('Files')
    package.appendChild(files)

    file_element = doc.createElement('File')
    files.appendChild(file_element)
    file_element.setAttribute('Path', "*.py")

    file_element = doc.createElement('File')
    files.appendChild(file_element)
    file_element.setAttribute('Path', "requirements.txt")

    project_file = doc.createElement('ProjectFile')
    file_element.appendChild(project_file)

    # Convert the document to a string format
    xml_str = doc.toprettyxml(indent="\t", encoding="UTF-8")

    # Save the XML file
    save_path_file = os.path.join(folder_path, plugin_name + ".xml")
    with open(save_path_file, "wb") as f:
        f.write(xml_str)
    
    return save_path_file

def packageFiles(source, destination):
     
    with open(f"{source}/__init__.py", 'w') as file:
        pass

    shutil.copyfile("plugins/plugin_components/requirements.txt", f"{source}/requirements.txt")
 
    with ZipFile(destination, 'w') as zip_object:
        for file_name in os.listdir(source):
            file_path = os.path.join(source, file_name)
            if os.path.isfile(file_path):
                zip_object.write(file_path, file_name)


if __name__ == '__main__':
    app.run(debug=True, port=5003)
