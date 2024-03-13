from PyQt5 import QtWidgets, QtCore, QtGui
import requests


class PluginGeneratorApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Initialize layout
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # Create labels
        self.plugin_name_label = QtWidgets.QLabel("Plugin Name:")
        self.device_name_label = QtWidgets.QLabel("Device Name:")
        self.device_category_label = QtWidgets.QLabel("Device Category:")
        self.description_label = QtWidgets.QLabel("Description:")
        self.language_label = QtWidgets.QLabel("Choose Language:")

        # Create entry fields
        self.plugin_name_input = QtWidgets.QLineEdit()
        self.device_name_input = QtWidgets.QLineEdit()
        self.description_input = QtWidgets.QTextEdit()

        # Create dropdown menu for device category
        self.device_category_combo = QtWidgets.QComboBox()
        self.device_category_combo.addItems([
            "Generators", "Sources", "Power Products", "Oscilloscopes",
            "Analyzer", "Meters", "Modular Instruments", "Software",
            "Common Commands", "Power Supplies", "Other"
        ])

        # Create radio buttons
        self.csharp_button = QtWidgets.QRadioButton("C#")
        self.python_button = QtWidgets.QRadioButton("Python")
        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.addButton(self.csharp_button)
        self.button_group.addButton(self.python_button)
        self.python_button.setChecked(True)  # Set default selection to Python

        # Create submit button
        self.submit_button = QtWidgets.QPushButton("Generate")
        self.submit_button.clicked.connect(self.submit_info)

        # Add widgets to layout
        self.main_layout.addWidget(self.plugin_name_label)
        self.main_layout.addWidget(self.plugin_name_input)
        self.main_layout.addWidget(self.device_name_label)
        self.main_layout.addWidget(self.device_name_input)
        self.main_layout.addWidget(self.device_category_label)
        self.main_layout.addWidget(self.device_category_combo)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addWidget(self.description_input)
        self.main_layout.addWidget(self.language_label)
        self.main_layout.addWidget(self.csharp_button)
        self.main_layout.addWidget(self.python_button)
        self.main_layout.addWidget(self.submit_button)

        # Set window title
        self.setWindowTitle("Plugin Generator")

        # Show the window
        self.show()

    # Retrieves user input from the form and displays a popup window
    def submit_info(self):
        message = f"""
            Plugin Name: {self.plugin_name_input.text()}
            Device Name: {self.device_name_input.text()}
            Device Category: {self.device_category_combo.currentText()}
            Description: {self.description_input.toPlainText()}
            Language: {self.button_group.checkedButton().text()}
        """

        question = f"""
                    Write {self.button_group.checkedButton().text()} code for an opentap plugin for the {self.device_name_input.text()} {self.device_category_combo.currentText()}.\n 
                    Keep in mind, the .xml file, and init py has already been created. 
                    Also, adhere to these constraints: 
                    - {self.description_input.toPlainText()}.
                    - Please only return the code (put any English text in comments using #)."""
        question = f"""Using the scpi commands avaible to you can you create plugin for {self.device_name_input.text()}. Implement the startup, charge, and discharge functions in python"""

        # payload is what gets passed to the LLM/chat bot
        payload = {"plugin_name" : self.device_name_input.text(), "question": question}

        api_url = "http://127.0.0.1:5000/generate_plugin" 
        response = requests.post(api_url, json=payload)

        # Error handling 
        if response.status_code == 200:
            if response.headers.get('Content-Type') == 'application/json':
                result = response.json()
            else:
                try:
                    with open(f"{self.device_name_input.text()}.zip", 'wb') as f:
                        f.write(response.content)
                    print("Downloaded successfully")
                    self.close() # close the popup window
                except Exception as e:
                    print("error", e)
        else:
            print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = PluginGeneratorApp()
    app.exec_()
