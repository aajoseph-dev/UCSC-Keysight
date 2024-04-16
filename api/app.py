from flask import Flask, jsonify, request, send_from_directory
from xml.dom import minidom
import os
import requests
from io import BytesIO
import zipfile
from pathlib import Path
from dotenv import load_dotenv
import openai
import re

# This file serves as our backend and is responsible for making calls to Azure

app = Flask(__name__)

# This function configures chat bot and gets response
@app.route('/generate_plugin', methods=['POST'])
def generate_plugin():

    # Loading api keys from .env folder
    load_dotenv()
    openai.api_type = "azure"
    openai.api_version = "2023-08-01-preview"
    openai.api_base = os.getenv('OPENAI_ENDPOINT')
    openai.api_key = os.getenv("OPENAI_KEY1")
    deployment_id = "OpenTap-Plugin-LLM"
   
    # get data sent from client.py
    data = request.get_json()
    user_prompt = data.get('question')
    name = data.get('plugin_name')

    # functions = data.get('functions')
    selected_commands = data.get('selected_commands')
    print("selected commands", selected_commands)

#     send_zip_path = data.get('file_path')


    # Sets up the OpenAI Python SDK to use your own data for the chat endpoint.
    # :param deployment_id: The deployment ID for the model to use with your own data.
    # To remove this configuration, simply set openai.requestssession to None.
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

    setup_byod(deployment_id)
    
    search_endpoint = "https://azure-plugin-ai-search.search.windows.net"; 
    search_key = os.getenv("AZURE_AI_SEARCH_API_KEY"); 

    # search_index_name = "pdf_data"; 

    # zip_file_paths = []

    py_filepaths = []

    folder_path = name

    # Ensure the folder exists
    Path(folder_path).mkdir(parents=True, exist_ok=True)

    search_index_name = "plugin-pdf-vector"; 
#     message_text = [
#         {"role" : "system", "content": "Generate Python code based on SCPI commands and do not include anything beside the python code"},
#         {"role": "user", "content": user_prompt}]


    # TODO: Check if the search is using vectors
    # Ask the chat bot

    print("FINAL selected_commands: ", selected_commands)
    for index, function in enumerate(selected_commands):
        full_prompt = user_prompt + "- Using SCPI commands, implement this specific function: " + function
        print("full prompt: ", full_prompt)
#         message_text = [{"role": "user", "content": full_prompt}]
        message_text = [
        {"role" : "system", "content": "Generate Python code based on SCPI commands and do not include anything beside the python code"},
        {"role": "user", "content": user_prompt}]
        completion = openai.ChatCompletion.create(
            messages=message_text,
            deployment_id=deployment_id,
            dataSources=[  # camelCase is intentional, as this is the format the API expects
                {
                    "type": "AzureCognitiveSearch",
                    "parameters": {
                        "endpoint": search_endpoint,
                        "indexName": search_index_name,
                        "semanticConfiguration": "default",
                        "queryType": "simple",
                        "fieldsMapping": {},
                        "inScope": True,
                        "roleInformation": "You are an AI assistant that takes in a user-specified device and writes only Python code yourself for OpenTAP plugins. Does not write any text. You take the specified command you are given and write plugin code for it.",
                        "filter": None,
                        "strictness": 3,
                        "topNDocuments": 5,
                        "key": search_key
                    }
                }
            ],
            temperature=0,
            top_p=1,
            max_tokens=800,
        )

        # Grabbing just the response and leaving our unnecessary data (i.e. token used, filters, etc.) 
        response = completion.choices[0].message.content
        print(response)
        #returns response in json format to client
        # file_path = generate_zipfolder(name, response)
        new_name = name + "-" + function
        py_filepath = generate_py(new_name, response, folder_path) # for each call to chatbot, generate its own .py file
        py_filepaths.append(py_filepath)

        # zip_file_path = generate_zipfolder(f"{name}_{function}", response)
        # zip_file_paths.append(zip_file_path)

        print("for loop iteration")



    final_zip_file_path = pack_zip_file(py_filepaths, name)
    
    return send_zip_file(final_zip_file_path, name)

    # return send_zip_file(file_path,name)

def verify_code():
    pass



# def pack_zip_file(py_filepaths, final_zip_name):
#     final_zip_file_path = f"{final_zip_name}.zip"
#     file_path = final_zip_name
#     os.makedirs(file_path, exist_ok=True)
#     os.chmod(file_path, 0o700)
#     with zipfile.ZipFile(final_zip_file_path, 'w') as final_zip:
#         for py_filepath in py_filepaths:
#             final_zip.write(py_filepath)
#     # also write an .xml file
#     generate_xml(final_zip_name, final_zip_name)
#     return final_zip_file_path

def pack_zip_file(py_filepaths, final_zip_name):
    final_zip_file_path = f"{final_zip_name}.zip"
    
    # Create the directory for the zip file
    file_path = final_zip_name
    os.makedirs(file_path, exist_ok=True)
    os.chmod(file_path, 0o700)
    
    # Write the Python files into the directory
    for py_filepath in py_filepaths:
        filename = os.path.basename(py_filepath)
        destination_path = os.path.join(file_path, filename)
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        os.rename(py_filepath, destination_path)

    # Generate XML file and get its path
    xml_file_path = generate_xml(final_zip_name, final_zip_name)

    # Create the zip file
    with zipfile.ZipFile(final_zip_file_path, 'w') as final_zip:
        for root, _, files in os.walk(file_path):
            for file in files:
                final_zip.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), file_path))


        # Add the XML file to the zip folder
        final_zip.write(xml_file_path, os.path.basename(xml_file_path))
    
    return final_zip_file_path

#     completion = openai.ChatCompletion.create(
#         messages=message_text,
#         deployment_id=deployment_id,
        
#         dataSources=[  # camelCase is intentional, as this is the format the API expects
#             {
#                 "type": "AzureCognitiveSearch",
#                 "parameters": {
#                     "endpoint": search_endpoint,
#                     "indexName": search_index_name,
#                     "semanticConfiguration": "default",
#                     "queryType": "simple",
#                     "fieldsMapping": {},
#                     "inScope": True,
#                     "roleInformation": "You are an AI assistant that takes in a user-specified device and writes only Python code yourself for OpenTAP plugins. Does not write any text.",
#                     "filter": None,
#                     "strictness": 3,
#                     "topNDocuments": 5,
#                     "key": search_key
#                 }
#             }
#         ],
#         temperature=0,
#         top_p=1,
#         max_tokens=800,
#     )

#     # Grabbing just the response and leaving our unnecessary data (i.e. token used, filters, etc.) 
#     response = completion.choices[0].message.content

#     #returns response in json format to client
#     generate_zipfolder(name, response)
#     # zip = send_from_directory('.', f"{name}.zip", as_attachment=True)
#     # print("send_zip_path:", send_zip_path)
#     # zip = send_from_directory(send_zip_path, f"{name}.zip", as_attachment=True)
#     zip = send_from_directory('.', f"{name}.zip", as_attachment=True)
#     return zip


# Generating zip file
def generate_zipfolder(plugin_name, data):
    file_path = plugin_name
    print(f"generate_zipfolder(): {file_path}")
    os.makedirs(file_path, exist_ok=True)
    os.chmod(file_path, 0o700)

    py_file = generate_py(plugin_name, data, file_path)
    # xml_file = generate_xml(plugin_name, file_path)

    with zipfile.ZipFile(f"{plugin_name}.zip", 'w', zipfile.ZIP_DEFLATED) as zip:
        zip.write(xml_file)
        zip.write(py_file)

    return file_path

def clean_code(code, file_path):
    pattern = r"`python(.*?)`"
    match = re.findall(pattern, code, re.DOTALL)
    print(match)
    with open(file_path, 'w') as file:
        for m in match:
            file.write(m)
            file.write('\n')

# Generating python file that eventually gets populated with the LLM's generated plugin
def generate_py(name, code, folder_path):
    # Path(file_path).mkdir(parents=True, exist_ok=True)
    
    # # Create a file inside the directory
    # name += '.py'
    # file_path = Path(file_path) / name
    # file_path.write_text(code)
    # print(f"name: {name}, file_path: {file_path}")
    # return file_path

    # Ensure the folder exists
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    
    # Create a file inside the directory
    file_path = Path(folder_path) / (name + '.py')
    file_path.write_text(code)
    print(f"name: {name}, file_path: {file_path}")
    return file_path

# Generating .xml file that contains info about which .py file the plugin was made for
def generate_xml(name, folder_path):
    doc = minidom.Document()
    package = doc.createElement('Package')
    doc.appendChild(package)

    package.setAttribute('Name', name)
    package.setAttribute('xmlns', "http://keysight.com/Schemas/tap")
    package.setAttribute('Version', "$(GitVersion)")
    package.setAttribute('OS', "Windows,Linux,MacOS")

    des = doc.createElement('Description')
    package.appendChild(des)
    des_text = doc.createTextNode('TEST')
    des.appendChild(des_text)

    prereq = doc.createElement('Prerequisites')
    des.appendChild(prereq)
    prereq_text = doc.createTextNode(' Python (>3.7) ')
    prereq.appendChild(prereq_text)

    # Add dependency for OpenTAP
    dep = doc.createElement('Dependencies')
    package.appendChild(dep)
    dep_text = doc.createElement('PackageDependency')
    dep_text.setAttribute("Package", "OpenTAP")
    dep_text.setAttribute("Version", "^9.18.2")
    dep.appendChild(dep_text)

    # Add dependency for Python
    dep_text = doc.createElement('PackageDependency')
    dep_text.setAttribute("Package", "Python")
    dep_text.setAttribute("Version", "^$(GitVersion)")
    dep.appendChild(dep_text)
    
    files = doc.createElement('Files')
    package.appendChild(files)

    py = doc.createElement('File')
    py.setAttribute('Path', folder_path)  
    files.appendChild(py)

    end_project_file = doc.createElement('ProjectFile')
    py.appendChild(end_project_file)

    xml_str = doc.toprettyxml(indent="\t", encoding="UTF-8")

    save_path_file = folder_path + '/' + "package" + ".xml"
    with open(save_path_file, "wb") as f:
        f.write(xml_str)
    
    return save_path_file
    
# Send back the zip file to the user's directory
def send_zip_file(file_path, plugin_name):
    return send_from_directory('.', f"{plugin_name}.zip", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)