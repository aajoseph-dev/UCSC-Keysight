from flask import Flask, jsonify, request, send_file
from xml.dom import minidom
import os
import requests
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path
from dotenv import load_dotenv
import openai
import re
import importlib.metadata as metadata


from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

import tiktoken

from promptTemplates import PromptTemplates


app = Flask(__name__)

@app.route('/generate_plugin', methods=['POST'])
def handleRequest():
    print("hello1")

    data = request.get_json()
    deviceName = data.get("deviceName")
    path = f"plugins/raw_files/{deviceName}"
    path_to_zip = f"plugins/zip_files/{deviceName}.zip"
    requirements = set()
    
    if not os.path.exists(path):
        os.makedirs(path)  
        for command in data.get("commands"):
            context = callAiSearch(f"{deviceName}: {command}")
            prompt = createPrompt(data, command, context)
            response = callLLM(prompt, data)
            buildPy(path, command, response, requirements)
        packageFiles(path, path_to_zip, requirements)
    
    return send_file(path_to_zip, as_attachment=True)


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
    print("hello")
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
    
    with open(f"something1.txt", 'w') as file:
        file.write(generated_text)
    #remove string and send to validation
    # pattern = r"`python(.*?)`"
    # match = re.findall(pattern, generated_text, re.DOTALL)
    # print(match)
    # return match
    return generated_text

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


def buildPy(path, command, code, req):

    # pattern = r'^\s*(?:import|from)\s+(\S+)'
    # matches = re.findall(pattern, code, re.MULTILINE)
    # req.update(matches)

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
    package.setAttribute('Version', "$(GitVersion)")
    package.setAttribute('OS', "Windows,Linux,MacOS")

    # Create the description element with prerequisites
    description = doc.createElement('Description')
    package.appendChild(description)
    description_text = doc.createTextNode('TEST')
    description.appendChild(description_text)

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

    python_dependency = doc.createElement('PackageDependency')
    dependencies.appendChild(python_dependency)
    python_dependency.setAttribute('Package', 'Python')
    python_dependency.setAttribute('Version', '^$(GitVersion)')

    # Create the files section
    files = doc.createElement('Files')
    package.appendChild(files)

    file_element = doc.createElement('File')
    files.appendChild(file_element)
    file_element.setAttribute('Path', folder_path)

    project_file = doc.createElement('ProjectFile')
    file_element.appendChild(project_file)

    # Convert the document to a string format
    xml_str = doc.toprettyxml(indent="\t", encoding="UTF-8")

    # Save the XML file
    save_path_file = os.path.join(folder_path, plugin_name + ".xml")
    with open(save_path_file, "wb") as f:
        f.write(xml_str)
    
    return save_path_file

def packageFiles(source, destination, req):

    with open(f"{source}/requirements.txt", 'w') as file:
        for lib in req:
            try:
                version = metadata.version(lib)
                if version:
                    file.write(f"{lib}=={version}\n")
                else:
                    file.write(f"{lib}\n")
            except metadata.PackageNotFoundError:
                file.write(f"{lib}\n")

    with ZipFile(destination, 'w') as zip_object:
        for file_name in os.listdir(source):
            file_path = os.path.join(source, file_name)
            if os.path.isfile(file_path):
                zip_object.write(file_path, file_name)


if __name__ == '__main__':
    # path = "/Users/shaun/Desktop/115b/UCSC-Keysight/api/plugins/raw_files/EDU36311A"
    # zip = "/Users/shaun/Desktop/115b/UCSC-Keysight/api/plugins/zip_files/EDU36311A.zip"
    # packageFiles(path,zip)
    app.run(debug=True, port=5000)
