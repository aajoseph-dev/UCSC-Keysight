from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6 import QtCore
import requests

class GenerationThread(QThread):
    progress_update = QtCore.pyqtSignal(int)

    def __init__(self, plugin_data, directory):
        super().__init__()
        self.plugin_data = plugin_data
        self.directory = directory

    def run(self):
        total_plugins = len(self.plugin_data)
        for idx, plugin_info in enumerate(self.plugin_data):
            plugin_name, device_name, category, interface, scpi, language, role = plugin_info
            payload = {
                "deviceName": device_name,
                "category": category,
                "commands": scpi,
                "interface": interface,
                "progLang": language,
                "role": role,
                "useCase": ""  # Assuming useCase is not used in this example
            }
            api_url = "http://127.0.0.1:5003/generate_plugin"
            try:
                response = requests.post(api_url, json=payload, stream=True)
                total_length = response.headers.get('content-length')

                if total_length is None:
                    print("Error: Unable to determine total length for plugin:", plugin_name)
                    continue
                
                # Progress tracking variables
                downloaded = 0
                chunk_size = 1024  # Adjust chunk size as needed

                with open(f"{self.directory}/{device_name}.zip", 'wb') as f:
                    for data in response.iter_content(chunk_size=chunk_size):
                        f.write(data)
                        downloaded += len(data)
                        progress = int((downloaded / int(total_length)) * 100)
                        self.progress_update.emit(progress)

                print(f"Plugin {plugin_name} downloaded successfully")
            except Exception as e:
                print(f"Error downloading plugin {plugin_name}:", e)
