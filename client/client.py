from PyQt5 import QtWidgets, QtGui, QtCore
import requests


class PluginGeneratorApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Initialize layout
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.setGeometry(100, 100, 900, 200) # (x, y, width, height)

        # Add keysight logo
        self.photo_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("keysight_logo.png")
        pixmap = pixmap.scaledToWidth(600)
        self.photo_label.setPixmap(pixmap)
        self.photo_label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.photo_label)

        # Add title "AI-based..."
        title_font = QtGui.QFont("Times New Roman", 25, QtGui.QFont.Bold)  
        self.title_label = QtWidgets.QLabel("<h2 style='font-family: Times New Roman; font-size: 25px; font-weight: bold;'>AI-Based Plugin Generation</h2>")
        self.title_label.setFont(title_font)  # Set the font for the title label
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        font = QtGui.QFont("Times New Roman")
        font.setPointSize(23)  # Set font size to 14

        # Create labels
        self.plugin_name_label = QtWidgets.QLabel("Plugin Name:")
        self.plugin_name_label.setFont(font)
        self.device_name_label = QtWidgets.QLabel("Device Name(s):")
        self.device_name_label.setFont(font)
        self.device_category_label = QtWidgets.QLabel("Device Category:")
        self.device_category_label.setFont(font)
        self.commands_label = QtWidgets.QLabel("Prefilled Commands:")
        self.commands_label.setFont(font)
        self.description_label = QtWidgets.QLabel("Description:")
        self.description_label.setFont(font)
        self.language_label = QtWidgets.QLabel("Choose Language:")
        self.language_label.setFont(font)
        self.zip_path_label = QtWidgets.QLabel("Input path for zip file to save under:")
        self.zip_path_label.setFont(font)

        # Create entry fields
        self.plugin_name_input = QtWidgets.QLineEdit()
        self.plugin_name_input.setFont(font)
        self.device_name_input = QtWidgets.QLineEdit()
        self.device_name_input.setFont(font)
        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setFont(font)
        self.zip_path_input = QtWidgets.QLineEdit()
        self.zip_path_input.setFont(font)

        # Checkboxes for prefilled commands
        self.commands = [
            ("Startup", False), # All commands are off by default
            ("Charge", False),  
            ("Discharge", False),
        ]
        
        # Create dropdown menu for device category
        self.device_category_combo = QtWidgets.QComboBox()
        self.device_category_combo.setFont(font)
        self.device_category_combo.addItems([
            "Generators", "Sources", "Power Products", "Oscilloscopes",
            "Analyzer", "Meters", "Modular Instruments", "Software",
            "Common Commands", "Power Supplies", "Other"
        ])

        # Set font size for the combo box items
        combo_font = QtGui.QFont("Times New Roman", 23)  # Set the font size to 16
        self.device_category_combo.setFont(combo_font)

        # Create radio buttons
        self.csharp_button = QtWidgets.QRadioButton("C#")
        self.csharp_button.setFont(font)
        self.python_button = QtWidgets.QRadioButton("Python")
        self.python_button.setFont(font)
        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.addButton(self.csharp_button)
        self.button_group.addButton(self.python_button)
        self.python_button.setChecked(True)  # Set default selection to Python

        # Create submit button
        font_generate = QtGui.QFont("Times New Roman")
        font_generate.setPointSize(28)  # Set font size to 14
        self.submit_button = QtWidgets.QPushButton("Generate")
        self.submit_button.setFont(font_generate)
        self.submit_button.clicked.connect(self.submit_info)
        self.submit_button.setFixedSize(200, 80)

        # Add widgets to layout
        self.main_layout.addWidget(self.plugin_name_label)
        self.main_layout.addWidget(self.plugin_name_input)
        self.main_layout.addWidget(self.device_name_label)
        self.main_layout.addWidget(self.device_name_input)
        self.main_layout.addWidget(self.zip_path_label)
        self.main_layout.addWidget(self.zip_path_input)

        # Dictionary to hold the command name and its checkbox widget
        self.command_checkboxes = {}

        self.main_layout.addWidget(self.commands_label)
        # Create a checkbox for each command
        for command_name, is_checked in self.commands:
            checkbox = QtWidgets.QCheckBox(command_name)
            checkbox.setFont(font)
            checkbox.setChecked(is_checked)
            self.main_layout.addWidget(checkbox)
            self.command_checkboxes[command_name] = checkbox

        self.main_layout.addWidget(self.device_category_label)
        self.main_layout.addWidget(self.device_category_combo)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addWidget(self.description_input)
        self.main_layout.addWidget(self.language_label)
        self.main_layout.addWidget(self.csharp_button)
        self.main_layout.addWidget(self.python_button)
        # self.main_layout.addWidget(self.python_button)
        self.main_layout.addWidget(self.submit_button, alignment=QtCore.Qt.AlignHCenter)

        # Set window title
        self.setWindowTitle("Plugin Generator")

        # Show the window
        self.show()

    # Retrieves user input from the form and displays a popup window
    def submit_info(self):
        selected_commands = [command for command, checkbox in self.command_checkboxes.items() if checkbox.isChecked()]

        # to add: interface option on ui box, role option
        payload = {"deviceName" : self.device_name_input.text(),
                "category" : self.device_name_input.text(),  
                "commands" : selected_commands,
                "interface" : "none specified", 
                "progLang" : "Python",
                "role" : "As a test engineer, I want to create a plugin in Python to interface with this instrument",
                "useCase" : "generate_plugin"}


        api_url = "http://127.0.0.1:5000/generate_plugin" 

        # Specify the timeout value in seconds
        timeout_seconds = 180  # Adjust this value as needed

        response = requests.post(api_url, json=payload, timeout=timeout_seconds)

        # Error handling 
        if response.status_code == 200:
            if response.headers.get('Content-Type') == 'application/json':
                result = response.json()
            else:
                try:
                    with open(f"{self.zip_path_input.text()}/{self.device_name_input.text()}.zip", 'wb') as f:
                        f.write(response.content)
                    print("Downloaded successfully.")
                    self.close() # close the popup window
                except Exception as e:
                    print("error", e)
        else:
            print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = PluginGeneratorApp()
    app.exec_()
