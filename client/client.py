import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QIcon, QCursor
from PyQt6.QtCore import Qt, QThread, QObject, pyqtSlot
from PyQt6 import QtCore

import requests

from test_steps import test_steps
from multiDropDown import MultiSelectDropdown

class LoadingThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def run(self):
        # Simulate some time-consuming task
        for i in range(101):
            self.msleep(50)
            self.progress_update.emit(i)

    progress_update = QtCore.pyqtSignal(int)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OpenTap Plugin Generation")
        self.setFixedSize(800, 600)  # Fixed screen size

        logo_pixmap = QPixmap("../assets/tap_icon.png")


        self.setWindowIcon(QIcon(logo_pixmap))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)

        # Sidebar
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)

        # Company logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("../assets/tap_icon.png").scaledToWidth(100)
        logo_label.setPixmap(logo_pixmap)
        self.sidebar_layout.addWidget(logo_label)

        single_button = QPushButton("Single")
        single_button.setFixedSize(100, 50)
        single_button.clicked.connect(self.show_single_screen)
        self.sidebar_layout.addWidget(single_button)

        batch_button = QPushButton("Batch")
        batch_button.setFixedSize(100, 50)
        batch_button.clicked.connect(self.show_batch_screen)
        self.sidebar_layout.addWidget(batch_button)

        self.layout.addLayout(self.sidebar_layout)

        # Container for the screens
        self.screen_container = QStackedWidget()
        self.layout.addWidget(self.screen_container)

        # Initialize screens
        self.single_screen = QWidget()
        self.batch_screen = QWidget()

        self.screen_container.addWidget(self.single_screen)
        self.screen_container.addWidget(self.batch_screen)

        # Setup screens
        self.setup_single_screen()
        self.setup_batch_screen()

        # Show the Single screen by default
        self.show_single_screen()

        # Inside the MainWindow class, modify the setup_single_screen method
        
    def setup_single_screen(self):
        layout = QVBoxLayout(self.single_screen)

        single_label = QLabel("Plugin Generation")
        single_label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(single_label)

        form_layout = QGridLayout()

        # Row 1
        form_layout.addWidget(QLabel("Plugin Name:"), 0, 0)
        self.instrument_input = QLineEdit()  # Make it a class attribute
        form_layout.addWidget(self.instrument_input, 0, 1)

        form_layout.addWidget(QLabel("Interface:"), 0, 2)
        self.interface_input = QComboBox()  # Make it a class attribute
        self.interface_input.addItems([
            "USB (Universal Serial Bus)",
            "LAN (Local Area Network)",
            "GPIB (General Purpose Interface Bus)",
            "GPIB-USB or GPIB-to-USB Converters",
            "RS-232 (Recommended Standard 232)",
            "IEEE 802.11 (Wi-Fi)",
            "PCI (Peripheral Component Interconnect)",
            "PCIe (Peripheral Component Interconnect Express)",
            "PXI (PCI eXtensions for Instrumentation)",
            "VXI (VME eXtensions for Instrumentation)",
            "Thunderbolt",
            "Fiber Optic"
        ])
        form_layout.addWidget(self.interface_input, 0, 3)

        # Row 2
        form_layout.addWidget(QLabel("Device Name:"), 1, 0)
        self.device_name_input = QLineEdit()  # Make it a class attribute
        form_layout.addWidget(self.device_name_input, 1, 1)

        form_layout.addWidget(QLabel("Language:"), 1, 2)
        self.language_input = QComboBox()  # Make it a class attribute
        self.language_input.addItems(["Python", "C#"])
        form_layout.addWidget(self.language_input, 1, 3)

        # Row 3
        form_layout.addWidget(QLabel("Category:"), 2, 0)
        self.category_input = QComboBox()  # Make it a class attribute
        self.category_input.addItems([
            "Generator", "Power Source", "Power Products", "Oscilloscope",
            "Analyzer", "Meter", "Modular Instrument", "Software",
            "Common Command", "Power Supply", "Other"
        ])
        form_layout.addWidget(self.category_input, 2, 1)

        self.role_input = QComboBox()  # Make it a class attribute
        form_layout.addWidget(QLabel("Role:"), 2, 2)
        self.role_input.addItems([
            "Administrator",
            "Developer",
            "Tester/QA",
            "End User",
            "Contributor/Community Member"
        ])
        form_layout.addWidget(self.role_input, 2, 3)

        layout.addLayout(form_layout)

        # Add Test Steps section with checkboxes
        test_steps_label = QLabel("Test Steps:")
        layout.addWidget(test_steps_label)

        self.radio_layout = QGridLayout()
        layout.addLayout(self.radio_layout)

        # Create the controller instance and pass the category input and radio layout
        self.single_screen_controller = SingleScreenController(self.category_input, self.radio_layout)

        # Generate button
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_button_clicked)
        layout.addWidget(self.generate_button, alignment=Qt.AlignmentFlag.AlignCenter)


    def generate_button_clicked(self):
        if self.screen_container.currentWidget() == self.single_screen:
            data = self.get_single_data()
        else:
            data = self.get_batch_data()

        if not data:
            return

        directory = QFileDialog.getExistingDirectory(self, "Select Directory to Save Plugin")

        if directory:
            # Create and show the progress dialog
            progress_dialog = QProgressDialog("Generating Plugin...", None, 0, 0, self)
            progress_dialog.setWindowTitle("Generating Plugin")
            progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            progress_dialog.setAutoClose(True)
            progress_dialog.setMinimumDuration(0)
            progress_dialog.show()

            # Start the thread
            self.thread = GenerationThread(data, directory)
            self.thread.progress_update.connect(progress_dialog.setValue)  # Connect to update progress
            self.thread.finished.connect(progress_dialog.close)  # Close the dialog when thread finishes
            self.thread.start()

    def get_single_data(self):
        plugin_name = self.instrument_input.text()
        interface = self.interface_input.currentText()
        device_name = self.device_name_input.text()
        language = self.language_input.currentText()
        category = self.category_input.currentText()
        role = self.role_input.currentText()

        selected_test_steps = []
        for i in range(self.single_screen_controller.radio_layout.count()):
            checkbox = self.single_screen_controller.radio_layout.itemAt(i).widget()
            if checkbox and checkbox.isChecked():
                selected_test_steps.append(checkbox.text())

        if not all([plugin_name, interface, device_name, language, category, role, selected_test_steps]):
            return None

        return [(plugin_name, interface, device_name, language, category, role, selected_test_steps)]

    def get_batch_data(self):
        # Get batch data
        batch_data = []

        # Assuming 'table' is accessible here as it is a member of the class
        table = self.batch_screen.findChild(QTableWidget)

        if table:
            for row in range(table.rowCount()):
                plugin_name = table.item(row, 0).text()
                interface = table.item(row, 1).text()
                device_name = table.item(row, 2).text()
                language = table.item(row, 3).text()
                category = table.item(row, 4).text()
                role = table.item(row, 5).text()

                selected_test_steps = []
                for col in range(6, table.columnCount()):
                    checkbox = table.cellWidget(row, col)
                    if checkbox and isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                        selected_test_steps.append(checkbox.text())

                if all([plugin_name, interface, device_name, language, category, role]):
                    batch_data.append((plugin_name, interface, device_name, language, category, role, selected_test_steps))
        print(batch_data)
        return batch_data



    def thread_finished(self):
        # Handle thread cleanup and deletion
        self.thread.deleteLater()

    def show_message_dialog(self, title, message):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)

        layout = QVBoxLayout(dialog)

        label = QLabel(message)
        layout.addWidget(label)

        dialog.exec()

    def setup_batch_screen(self):
        layout = QVBoxLayout(self.batch_screen)

        batch_label = QLabel("Batch Generation")
        batch_label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(batch_label)

        # Table setup
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Plugin Name", "Device Name", "Category", "Interface", "Subsystems", "Language", "Role"])

        # Set table height
        self.table.setFixedHeight(400)

        layout.addWidget(self.table)

        # Plus and minus buttons layout
        buttons_layout = QHBoxLayout()

        plus_button = QPushButton("+")
        plus_button.clicked.connect(self.show_add_entry_dialog)
        buttons_layout.addWidget(plus_button)

        minus_button = QPushButton("-")
        minus_button.clicked.connect(self.delete_selected_entry)
        buttons_layout.addWidget(minus_button)

        # Add stretch to push buttons to the right
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        # Generate button
        generate_button = QPushButton("Generate")
        generate_button.clicked.connect(self.generate_button_clicked)

        # Add generate button to the right
        generate_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)  # Set size policy
        buttons_layout.addWidget(generate_button, alignment=Qt.AlignmentFlag.AlignRight)

    def show_add_entry_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Entry")

        layout = QVBoxLayout(dialog)

        # Labels and inputs vertically arranged
        labels_inputs_layout = QVBoxLayout()

        # Row 1
        row_layout = QHBoxLayout()

        label1 = QLabel("Plugin Name:")
        plugin_name_input = QLineEdit()
        label1.setFixedWidth(100)  # Adjust the width of the label
        row_layout.addWidget(label1)
        row_layout.addWidget(plugin_name_input)

        labels_inputs_layout.addLayout(row_layout)

        # Row 2
        row_layout = QHBoxLayout()

        label2 = QLabel("Device Name:")
        device_name_input = QLineEdit()
        label2.setFixedWidth(100)  # Adjust the width of the label
        row_layout.addWidget(label2)
        row_layout.addWidget(device_name_input)

        labels_inputs_layout.addLayout(row_layout)

        # Row 3
        row_layout = QHBoxLayout()

        label3 = QLabel("Category:")
        category_input = QComboBox()
        category_input.addItems([
            "Generator", "Power Source", "Power Products", "Oscilloscope",
            "Analyzer", "Meter", "Modular Instrument", "Software",
            "Common Command", "Power Supply", "Other"])
        label3.setFixedWidth(100)  # Adjust the width of the label
        row_layout.addWidget(label3)
        row_layout.addWidget(category_input)

        labels_inputs_layout.addLayout(row_layout)

        # Row 4
        row_layout = QHBoxLayout()

        label4 = QLabel("Interface:")
        interface_input = QComboBox()
        interface_input.addItems([
            "USB (Universal Serial Bus)",
            "LAN (Local Area Network)",
            "GPIB (General Purpose Interface Bus)",
            "GPIB-USB or GPIB-to-USB Converters",
            "RS-232 (Recommended Standard 232)",
            "IEEE 802.11 (Wi-Fi)",
            "PCI (Peripheral Component Interconnect)",
            "PCIe (Peripheral Component Interconnect Express)",
            "PXI (PCI eXtensions for Instrumentation)",
            "VXI (VME eXtensions for Instrumentation)",
            "Thunderbolt",
            "Fiber Optic"])
        label4.setFixedWidth(100)  # Adjust the width of the label
        row_layout.addWidget(label4)
        row_layout.addWidget(interface_input)

        labels_inputs_layout.addLayout(row_layout)

        # Row 5
        row_layout = QHBoxLayout()

        label5 = QLabel("Language:")
        language_input = QComboBox()
        language_input.addItems(["Python", "C#"])
        label5.setFixedWidth(100)  # Adjust the width of the label
        row_layout.addWidget(label5)
        row_layout.addWidget(language_input)

        labels_inputs_layout.addLayout(row_layout)

        # Row 6
        row_layout = QHBoxLayout()

        label6 = QLabel("Role:")
        role_input = QComboBox()
        role_input.addItems([
            "Administrator",
            "Developer",
            "Tester/QA",
            "End User",
            "Contributor/Community Member"
        ])
        label6.setFixedWidth(100)  # Adjust the width of the label
        row_layout.addWidget(label6)
        row_layout.addWidget(role_input)

        labels_inputs_layout.addLayout(row_layout)

        # Row 7
        row_layout = QHBoxLayout()

        label7 = QLabel("Test Steps:")
        subsystem_input = QComboBox()  # ComboBox for subsystems
        label7.setFixedWidth(100)  # Adjust the width of the label
        row_layout.addWidget(label7)
        row_layout.addWidget(subsystem_input)

        labels_inputs_layout.addLayout(row_layout)
                # Update subsystems based on category selection
        category_input.currentIndexChanged.connect(lambda index: self.update_subsystems(subsystem_input, category_input.currentText()))

        # Add button
        add_button = QPushButton("ADD")
        add_button.clicked.connect(lambda: self.add_entry_to_table(dialog, plugin_name_input.text(), subsystem_input.currentText(), device_name_input.text(), language_input.currentText(), role_input.currentText(), category_input.currentText(), subsystem_input.currentText()))

        layout.addLayout(labels_inputs_layout)
        layout.addWidget(add_button)

        dialog.exec()


    def update_subsystems(self, subsystem_input, category):
        # Clear existing items
            subsystem_input.clear()

            # Get subsystems based on category
            subsystems = self.get_subsystems(category)

            # Add new subsystems
            subsystem_input.addItems(subsystems)

    def get_subsystems(self, category):
            # Define subsystems for each category
            return test_steps.get(category, [])


    def add_entry_to_table(self, dialog, plugin_name, scpi, device_name, language, interface, role, device_category):
        # Assuming 'table' is accessible here as it is a member of the class
        table = self.findChild(QTableWidget)
        row_position = table.rowCount()
        table.insertRow(row_position)
        table.setItem(row_position, 0, QTableWidgetItem(plugin_name))
        table.setItem(row_position, 1, QTableWidgetItem(device_name))
        table.setItem(row_position, 2, QTableWidgetItem(device_category))
        table.setItem(row_position, 3, QTableWidgetItem(interface))
        table.setItem(row_position, 4, QTableWidgetItem(scpi))
        table.setItem(row_position, 5, QTableWidgetItem(language))
        table.setItem(row_position, 6, QTableWidgetItem(role))
        dialog.close()

    def delete_selected_entry(self):
        # Assuming 'table' is accessible here as it is a member of the class
        table = self.findChild(QTableWidget)
        selected_row = table.currentRow()
        if selected_row >= 0:
            table.removeRow(selected_row)

    def show_single_screen(self):
        self.screen_container.setCurrentWidget(self.single_screen)

    def show_batch_screen(self):
        self.screen_container.setCurrentWidget(self.batch_screen)

    def show_loading_dialog(self):
        self.loading_dialog = QDialog(self)
        self.loading_dialog.setWindowTitle("Loading...")
        self.loading_dialog.setFixedSize(200, 100)

        layout = QVBoxLayout(self.loading_dialog)
        label = QLabel("Processing...")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        progress = QProgressBar()
        progress.setMinimum(0)
        progress.setMaximum(100)

        layout.addWidget(label)
        layout.addWidget(progress)

        # Start a thread to simulate loading
        self.loading_thread = LoadingThread()
        self.loading_thread.progress_update.connect(progress.setValue)
        self.loading_thread.start()

        self.loading_dialog.exec()

class SingleScreenController(QObject):
    def __init__(self, category_input, radio_layout):
        super().__init__()
        self.category_input = category_input
        self.radio_layout = radio_layout

        # Connect the category input's currentIndexChanged signal to the update_checkboxes slot
        self.category_input.currentIndexChanged.connect(self.update_checkboxes)

        # Set default checkboxes
        self.update_checkboxes(0)  # Pass 0 to simulate the default index

    @pyqtSlot(int)
    def update_checkboxes(self, index):
        # Get the selected category
        selected_category = self.category_input.currentText()

        # Clear existing checkboxes
        for i in reversed(range(self.radio_layout.count())):
            widget = self.radio_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Add new checkboxes based on the selected category
        test_steps = self.get_test_steps(selected_category)
        row = 0
        col = 0
        for i, option in enumerate(test_steps):
            checkbox = QCheckBox(option)
            checkbox.setStyleSheet("QCheckBox { padding: 5px; }")
            self.radio_layout.addWidget(checkbox, row, col)
            col += 1
            if col == 3:  # Three items per row
                col = 0
                row += 1

    def get_test_steps(self, category):
        # Define the test steps for each category
        return test_steps.get(category, ["Default Test Step 1", "Default Test Step 2"])

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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())