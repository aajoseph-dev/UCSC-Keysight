from flask import Flask, jsonify, request, send_from_directory
from xml.dom import minidom
import os
from io import BytesIO
import zipfile
from pathlib import Path

app = Flask(__name__)

@app.route('/generate_plugin', methods=['GET', 'POST'])
def generate_plugin():
    data = request.get_json()
    user_input = data.get('question')
    name = data.get('plugin_name')

    message_text = [{"role": "user", "content": user_input}]
    response = "print('hello world')\nprint('hello world2')"

    file_path = generate_zipfolder(name, response)
    return send_zip_file(file_path)

def generate_zipfolder(plugin_name, data):
    file_path = plugin_name
    os.makedirs(file_path, exist_ok=True)
    os.chmod(file_path, 0o700)

    py_file = generate_py(plugin_name, data, file_path)
    xml_file = generate_xml(plugin_name, file_path)

    with zipfile.ZipFile('files.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
        zip.write(xml_file)
        zip.write(py_file)

    return file_path

def generate_py(name, code, file_path):
    Path(file_path).mkdir(parents=True, exist_ok=True)

    # Create a file inside the directory
    name += '.py'
    file_path = Path(file_path) / name
    file_path.write_text(code)
    return file_path

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

    files = doc.createElement('Files')
    package.appendChild(files)

    py = doc.createElement('File')
    #py.setAttribute('Path', 'my_file.txt')  # assuming the Python file is named my_file.txt
    py.setAttribute('Path', folder_path)  
    files.appendChild(py)

    end_project_file = doc.createElement('ProjectFile')
    py.appendChild(end_project_file)

    xml_str = doc.toprettyxml(indent="\t", encoding="UTF-8")

    save_path_file = folder_path + '/' + name + ".xml"
    with open(save_path_file, "wb") as f:
        f.write(xml_str)
    
    return save_path_file

def send_zip_file(file_path):
    return send_from_directory('.', 'files.zip', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
