import sys
from PyQt6.QtWidgets import QSizePolicy, QTableWidget, QTableWidgetItem, QPushButton, QComboBox, QApplication, QFileDialog, QStackedWidget, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QVBoxLayout, QWidget, QDialog, QProgressBar, QGridLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QThread
from PyQt6 import QtCore

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

    def setup_single_screen(self):
        layout = QVBoxLayout(self.single_screen)

        single_label = QLabel("Plugin Generation")
        single_label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(single_label)

        # First horizontal layout for the first half of input elements
        horizontal_layout_1 = QHBoxLayout()
        horizontal_layout_1.setSpacing(20)  # Adjust spacing between elements

        title_label = QLabel("Instrument:")
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)  # Align label to the right
        horizontal_layout_1.addWidget(title_label)

        text_field_1 = QLineEdit()
        text_field_1.setMaximumWidth(100)  # Set maximum width for the text field
        horizontal_layout_1.addWidget(text_field_1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_label = QLabel("Category:")
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignRight)  # Align label to the right
        horizontal_layout_1.addWidget(title_label)

        dropdown_menu_1 = QComboBox()
        dropdown_menu_1.addItems([
            "Generator", "Power Source", "Power Products", "Oscilloscope",
            "Analyzer", "Meter", "Modular Instrument", "Software",
            "Common Command", "Power Supply", "Other"
        ])  
        horizontal_layout_1.addWidget(dropdown_menu_1)

        layout.addLayout(horizontal_layout_1)

        # Second horizontal layout for the remaining input elements
        horizontal_layout_2 = QHBoxLayout()
        horizontal_layout_2.setSpacing(20)  # Adjust spacing between elements

        title_label = QLabel("Interface:")
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignRight)  # Align label to the right
        horizontal_layout_2.addWidget(title_label)

        dropdown_menu_2 = QComboBox()
        dropdown_menu_2.addItems([
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
        horizontal_layout_2.addWidget(dropdown_menu_2)

        title_label = QLabel("Role:")
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignRight)  # Align label to the right
        horizontal_layout_2.addWidget(title_label)

        dropdown_menu_3 = QComboBox()
        dropdown_menu_3.addItems([
            "Administrator",
            "Developer",
            "Tester/QA",
            "End User",
            "Contributor/Community Member"
        ])  
        horizontal_layout_2.addWidget(dropdown_menu_3)

        layout.addLayout(horizontal_layout_2)

        # Add a Save to input field
        title_label = QLabel("Save to:")
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignRight)  # Align label to the right
        layout.addWidget(title_label)

        # Use a QLineEdit widget to show the selected folder path
        folder_path_edit = QLineEdit()
        folder_path_edit.setMaximumWidth(200)  # Set maximum width for the text field
        layout.addWidget(folder_path_edit)

        # Add a spacer item to create space between the save path and the Scpi Subsystems section
        layout.addSpacing(20)

        # Scpi Subsystems label and input field
        title_label = QLabel("Scpi Subsystems:")
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignRight)  # Align label to the right
        layout.addWidget(title_label)

        text_field_2 = QLineEdit()
        text_field_2.setMaximumWidth(100)  # Set maximum width for the text field
        layout.addWidget(text_field_2)

        # Generate button
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.show_loading_dialog)  # Connect button click to show_loading_dialog method
        layout.addWidget(self.generate_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def generate_data(self):
            # Here you can implement the logic to process the user input
            # This method will be triggered when the "Generate" button is clicked
        pass

    def setup_batch_screen(self):
        layout = QVBoxLayout(self.batch_screen)

        batch_label = QLabel("Batch Generation")
        batch_label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(batch_label)

        # Table setup
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Plugin Name", "SCPI Subsystems", "Device Name", "Language", "Path to Save File", "Interface", "Role", "Device Category"])

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
        generate_button.clicked.connect(self.generate_data)

        # Add generate button to the right
        generate_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)  # Set size policy
        buttons_layout.addWidget(generate_button, alignment=Qt.AlignmentFlag.AlignRight)

    def show_add_entry_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Entry")

        layout = QVBoxLayout(dialog)

        form_layout = QGridLayout()

        # Row 1
        form_layout.addWidget(QLabel("Plugin Name:"), 0, 0)
        plugin_name_input = QLineEdit()
        form_layout.addWidget(plugin_name_input, 0, 1)

        form_layout.addWidget(QLabel("SCPI Subsystems:"), 0, 2)
        scpi_input = QComboBox()
        scpi_input.addItems(["Subsystem1", "Subsystem2", "Subsystem3"]) 
        form_layout.addWidget(scpi_input, 0, 3)

        # Row 2
        form_layout.addWidget(QLabel("Device Name:"), 1, 0)
        device_name_input = QLineEdit()
        form_layout.addWidget(device_name_input, 1, 1)

        form_layout.addWidget(QLabel("Language:"), 1, 2)
        language_input = QComboBox()
        language_input.addItems(["Python", "C#"])
        form_layout.addWidget(language_input, 1, 3)

        # Row 3
        form_layout.addWidget(QLabel("Path to Save File:"), 2, 0)
        save_path_input = QLineEdit()
        form_layout.addWidget(save_path_input, 2, 1)

        form_layout.addWidget(QLabel("Interface:"), 2, 2)
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
        form_layout.addWidget(interface_input, 2, 3)

       # Row 4
        form_layout.addWidget(QLabel("Role:"), 3, 0)
        role_input = QComboBox()
        role_input.addItems([
            "Administrator",
            "Developer",
            "Tester/QA",
            "End User",
            "Contributor/Community Member"
        ])
        form_layout.addWidget(role_input, 3, 1)

        form_layout.addWidget(QLabel("Device Category:"), 3, 2)
        device_category_input = QComboBox()
        device_category_input.addItems([
            "Generator", "Power Source", "Power Products", "Oscilloscope",
            "Analyzer", "Meter", "Modular Instrument", "Software",
            "Common Command", "Power Supply", "Other"])
        form_layout.addWidget(device_category_input, 3, 3)

        layout.addLayout(form_layout)

        # Add button
        add_button = QPushButton("ADD")
        add_button.clicked.connect(lambda: self.add_entry_to_table(dialog, plugin_name_input.text(), scpi_input.currentText(), device_name_input.text(), language_input.currentText(), save_path_input.text(), interface_input.currentText(), role_input.currentText(), device_category_input.currentText()))
        layout.addWidget(add_button)

        dialog.exec()

    def add_entry_to_table(self, dialog, plugin_name, scpi, device_name, language, save_path, interface, device_category, role):
        # Assuming 'table' is accessible here as it is a member of the class
        table = self.findChild(QTableWidget)
        row_position = table.rowCount()
        table.insertRow(row_position)
        table.setItem(row_position, 0, QTableWidgetItem(plugin_name))
        table.setItem(row_position, 1, QTableWidgetItem(scpi))
        table.setItem(row_position, 2, QTableWidgetItem(device_name))
        table.setItem(row_position, 3, QTableWidgetItem(language))
        table.setItem(row_position, 4, QTableWidgetItem(save_path))
        table.setItem(row_position, 5, QTableWidgetItem(interface))
        table.setItem(row_position, 6, QTableWidgetItem(role))
        table.setItem(row_position, 7, QTableWidgetItem(device_category))
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
