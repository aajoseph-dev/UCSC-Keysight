import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QThread
from menu_data import *
from singe_page_controller import SingleScreenController
from generation_thread import GenerationThread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OpenTap Plugin Generation")
        self.setFixedSize(800, 600)  # Fixed screen size

        logo_pixmap = QPixmap("../assets/tap_icon.png")
        self.setWindowIcon(QIcon(logo_pixmap))

        self.spinner = None  

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

        self.thread = None

        self.faded_background = QLabel(self.central_widget)
        self.faded_background.setStyleSheet("background-color: rgba(0, 0, 0, 0.7);")  # Adjusted alpha value for a darker background
        self.faded_background.setGeometry(0, 0, self.width(), self.height())
        self.faded_background.hide()

        # Progress box
        self.progress_box = QProgressBar(self.central_widget)
        self.progress_box.setRange(0, 0)
        self.progress_box.setGeometry(300, 200, 200, 25)
        self.progress_box.hide()

    def setup_single_screen(self):
        layout = QVBoxLayout(self.single_screen)

        single_label = QLabel("Plugin Generation")
        single_label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(single_label)

        form_layout = QGridLayout()

        # Row 1
        form_layout.addWidget(QLabel("Manufacturer:"), 0, 0)
        self.instrument_input = QComboBox()  # Make it a class attribute
        self.instrument_input.addItems(manufacturer)
        form_layout.addWidget(self.instrument_input, 0, 1)

        form_layout.addWidget(QLabel("Interface:"), 0, 2)
        self.interface_input = QComboBox()  # Make it a class attribute
        self.interface_input.addItems(interface)
        form_layout.addWidget(self.interface_input, 0, 3)

        # Row 2
        form_layout.addWidget(QLabel("Device Name:"), 1, 0)
        self.device_name_input = QLineEdit()  # Make it a class attribute
        form_layout.addWidget(self.device_name_input, 1, 1)

        form_layout.addWidget(QLabel("Language:"), 1, 2)
        self.language_input = QComboBox()  # Make it a class attribute
        self.language_input.addItems(language)
        form_layout.addWidget(self.language_input, 1, 3)

        # Row 3
        form_layout.addWidget(QLabel("Category:"), 2, 0)
        self.category_input = QComboBox()  # Make it a class attribute
        self.category_input.addItems(category)
        form_layout.addWidget(self.category_input, 2, 1)

        self.role_input = QComboBox()  # Make it a class attribute
        form_layout.addWidget(QLabel("Role:"), 2, 2)
        self.role_input.addItems(role)
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
            self.show_spinner()  # Show spinner before starting the thread
            self.thread = GenerationThread(data, directory)
            self.thread.finished_signal.connect(self.hide_spinner)  # Connect signal to hide spinner
            self.thread.start()

    def show_spinner(self):
        self.faded_background.show()
        self.progress_box.show()

    def hide_spinner(self):
        self.faded_background.hide()
        self.progress_box.hide()
        self.thread = None

    def get_single_data(self):
        plugin_name = self.instrument_input.currentText()
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

        return [{
            "deviceName": device_name,
            "category": category,
            "commands": selected_test_steps,
            "interface": interface,
            "progLang": language.lower(),
            "role": role.lower(),
            "useCase": ""
        }]

    def get_batch_data(self):
        batch_data = []
        table = self.batch_screen.findChild(QTableWidget)

        if table:
            for row in range(table.rowCount()):
                plugin_name = table.item(row, 0).text()
                device_name = table.item(row, 1).text()
                category = table.item(row, 2).text()
                interface = table.item(row, 3).text()
                scpi = table.item(row, 4).text()  # Corrected to get SCPI data
                language = table.item(row, 5).text()
                role = table.item(row, 6).text()

                if all([plugin_name, device_name, category, interface, scpi, language, role]):
                    batch_data.append({
                        "deviceName": device_name,
                        "category": category,
                        "commands": scpi,  # Added subsystem (SCPI) correctly
                        "interface": interface,
                        "progLang": language.lower(),
                        "role": role.lower(),
                        "useCase": ""  # Assuming useCase is blank, as not specified
                    })

        return batch_data

    def on_thread_finished(self):
        self.thread.deleteLater()
        self.thread = None

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
        generate_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)  # Set size policy
        buttons_layout.addWidget(generate_button, alignment=Qt.AlignmentFlag.AlignRight)

    def show_add_entry_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Entry")

        layout = QVBoxLayout(dialog)

        # Labels and inputs vertically arranged
        labels_inputs_layout = QVBoxLayout()

        def create_row(label_text, input_widget):
            row_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(100)
            row_layout.addWidget(label)
            row_layout.addWidget(input_widget)
            labels_inputs_layout.addLayout(row_layout)
            return input_widget

        plugin_name_input = create_row("Plugin Name:", QLineEdit())
        device_name_input = create_row("Device Name:", QLineEdit())
        category_input = create_row("Category:", QComboBox())
        interface_input = create_row("Interface:", QComboBox())
        scpi_input = create_row("SCPI:", QLineEdit())  # Assuming SCPI is a line edit
        language_input = create_row("Language:", QComboBox())
        role_input = create_row("Role:", QComboBox())

        category_input.addItems(category)
        interface_input.addItems(interface)
        language_input.addItems(language)
        role_input.addItems(role)

        # Update subsystems based on category selection
        category_input.currentIndexChanged.connect(lambda index: self.update_subsystems(scpi_input, category_input.currentText()))

        add_button = QPushButton("ADD")
        add_button.clicked.connect(lambda: self.add_entry_to_table(dialog, plugin_name_input.text(), device_name_input.text(), category_input.currentText(), interface_input.currentText(), scpi_input.text(), language_input.currentText(), role_input.currentText()))

        layout.addLayout(labels_inputs_layout)
        layout.addWidget(add_button)

        dialog.exec()

    def add_entry_to_table(self, dialog, plugin_name, device_name, category, interface, scpi, language, role):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(plugin_name))
        self.table.setItem(row_position, 1, QTableWidgetItem(device_name))
        self.table.setItem(row_position, 2, QTableWidgetItem(category))
        self.table.setItem(row_position, 3, QTableWidgetItem(interface))
        self.table.setItem(row_position, 4, QTableWidgetItem(scpi))
        self.table.setItem(row_position, 5, QTableWidgetItem(language))
        self.table.setItem(row_position, 6, QTableWidgetItem(role))
        dialog.accept()

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

    def delete_selected_entry(self):
        # Assuming 'table' is accessible here as it is a member of the class
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)

    def show_single_screen(self):
        self.screen_container.setCurrentWidget(self.single_screen)

    def show_batch_screen(self):
        self.screen_container.setCurrentWidget(self.batch_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
