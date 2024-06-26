from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6 import QtCore
import time
import requests

class GenerationThread(QThread):
    finished_signal = pyqtSignal()

    def __init__(self, plugin_data, directory):
        super().__init__()
        self.plugin_data = plugin_data
        self.directory = directory

    def run(self):
        for plugin_info in self.plugin_data:
            start_time = time.time()
            payload = {
                "deviceName": plugin_info["deviceName"],
                "category": plugin_info["category"],
                "commands": plugin_info["commands"],
                "interface": plugin_info["interface"],
                "progLang": plugin_info["progLang"],
                "role": plugin_info["role"],
            }
            api_url = "http://127.0.0.1:5003/generate_plugin"
            device = plugin_info["deviceName"]
            try:
                response = requests.post(api_url, json=payload, stream=True)
                with open(f"{self.directory}/{device}.zip", 'wb') as f:
                    for data in response:
                        f.write(data)
                print(f"Plugin {device} downloaded successfully")
            except Exception as e:
                print(f"Error downloading plugin {device}:", e)
            commands = plugin_info["commands"]
            end = time.time() - start_time
            with open("output.txt", "a+") as f:
                f.write(f"{device} with these {commands} complete: {end}\n")
        self.finished_signal.emit()

