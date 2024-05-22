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

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

import tiktoken

from promptTemplates import PromptTemplates
from pluginValidation import *

load_dotenv()
app = Flask(__name__)

@app.route('/generate_plugin', methods=['POST'])
def handleRequest():
    
    data = request.get_json()
    deviceName = data.get("deviceName")
    path = f"plugins/raw_files/{deviceName}"
    path_to_zip = f"plugins/zip_files/{deviceName}.zip"

    #update this
    if os.path.exists(path):
        shutil.rmtree(path)

    if not os.path.exists(path):
        os.makedirs(path)  
        response = createInstrument(data, path)
        for command in data.get("commands"):
            context = callAISearch(f"{deviceName}: {command}")
            prompt = createStepsPrompt(data, command, context, response)
            # pattern = r'```python(.*?)```'
            response = callLLM(prompt)
            # match = re.findall(pattern, response, re.DOTALL)
            # response = match[0]
            response = extract_python_code(response)
            buildPy(path, command, response)

            response_dict = llm_code_check(command, response, deviceName, 0) # go ask the 2nd llm's response yet
            # {"Sentiment" : "Positive", "Response" : content}
            if response_dict["Sentiment"] == "Negative":

                prompt += f'''
                    \nThe plugin that was generated was incorrect, please try again by using the following feedback:
                    {response_dict["Response"]}
                    '''
                response = callLLM(prompt) # pass the 2nd llm's response to the 1st llm
                response = extract_python_code(response)

                buildPy(path, command, response)
                result, verified_code = verify_code(response)
                response_dict = llm_code_check(command, response, deviceName, 0) # go ask the 2nd llm's response yet
                buildXML(deviceName, path)
                packageFiles(path, path_to_zip)
  
            else: # response_dict["Sentiment"] == "Neutral" or "Positive":
                buildXML(deviceName, path)
                packageFiles(path, path_to_zip)
    return send_file(path_to_zip, as_attachment=True)
    #     buildXML(deviceName, path)
    #     packageFiles(path, path_to_zip, requirements)

    # return send_file(path_to_zip, as_attachment=True)

# Remove comments before and after the Python code
def extract_python_code(text):
    start_index = text.find("```python")
    end_index = text.find("```", start_index + 1)
    if start_index != -1 and end_index != -1:
        return text[start_index + 9:end_index].strip()
    else:
        return text

def verify_code(code):
    # checking for certain keywords
    if 'def' in code and 'class' in code:
        verification_result = 'Found class and function definitions.'
    else:
        verification_result = 'Unable to find class and function definitions.'

    # checking for OpenTAP import
    if 'import OpenTAP' not in code:
        # Adding OpenTAP import if not present
        code = '\nimport OpenTAP\n' + code

    if 'import opentap' not in code:
        code = '\n import opentap\n' + code

    # checking for @attribute
    if '@attribute' in code:
        verification_result += ' Found @attribute.'
    else:
        verification_result += ' @attribute not found.'

    return verification_result, code


def createStepsPrompt(data, command, context, instrument):
    prompt_templates = PromptTemplates(data, context)
    
    prompt = prompt_templates.generate_steps_prompt(command, instrument)

    return prompt

def createInstrument(data, path):
    deviceName = data.get("deviceName")
    context = callAISearch(f"{deviceName}")
    
    prompt_templates = PromptTemplates(data, context)
    prompt = prompt_templates.generate_instrument_prompt()
    response = callLLM(prompt)
    response = extract_python_code(response)

    response_dict = llm_code_check("", response, deviceName, 1)

    buildPy(path, deviceName, response)

    if response_dict["Sentiment"] == "Negative":
        # already tried, this is the second time
        prompt += f'''
            \nThe plugin that was generated was incorrect, please try again by using the following feedback:
            {response_dict["Response"]}'''
        response = callLLM(prompt) # pass the 2nd llm's response to the 1st llm
        response = extract_python_code(response)
        buildPy(path, deviceName, response)
        response_dict = llm_code_check("", response, deviceName, 0) # go ask the 2nd llm's response yet


    return response


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
    name = "".join( x for x in command if (x.isalnum() or x in "._- "))

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
    # package.setAttribute('Version', "$(GitVersion)")
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
