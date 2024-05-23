from flask import Flask, request, send_file
from xml.dom import minidom
from zipfile import ZipFile
import shutil
import os
from datetime import datetime
import tiktoken

from prompt_templates import PromptTemplates
from azure_services import *
from code_parser import *

app = Flask(__name__)

@app.route('/generate_plugin', methods=['POST'])
def handleRequest():
    
    data = request.get_json()
    deviceName = data.get("deviceName")
    dir = f"plugins/raw_files/{deviceName}"
    path_to_zip = f"plugins/zip_files/{deviceName}.zip"

    if os.path.exists(dir):
        dir += "_"
        now = datetime.now()
        formatted_date_time = now.strftime("%m.%d.%y.%H.%M")
        dir += formatted_date_time

    os.makedirs(dir)

    instrument_code = createInstrument(data, dir)

    for test_step in data.get("commands"):

        python_code = createStep(data, test_step, instrument_code)
        buildPy(dir, test_step, python_code)

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

def createStep(data, test_step, instrument_code, allowed_attempts=1):

    pt = PromptTemplates(data)

    deviceName = data.get("deviceName")

    context = callAISearch(f"{deviceName}: {test_step}")
    prompt = pt.generate_steps_prompt(test_step, instrument_code, context)

    response = callLLM(prompt)
    python_code = extract_python_code(response)

    verification_results = test_step_validation(python_code)
    validation_prompt = pt.generate_step_validation(python_code, test_step, instrument_code, context)
    llm_check = llm_code_check(validation_prompt)
    print(verification_results)

    count = 0
    while llm_check["Sentiment"] == "Negative" and count < allowed_attempts:

        prompt = pt.failed_test_step(python_code, test_step, context, llm_check["Response"], verification_results)
        response = callLLM(prompt) # pass the 2nd llm's response to the 1st llm
        python_code = extract_python_code(response)

        validation_prompt = pt.generate_step_validation(python_code, test_step, instrument_code, context)
        llm_check = llm_code_check(prompt) # go ask the 2nd llm's response yet
        
        count += 1
    
    return python_code


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
