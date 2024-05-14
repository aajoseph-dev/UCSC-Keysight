import sys
from PyQt6.QtWidgets import QRadioButton, QSizePolicy, QTableWidget, QTableWidgetItem, QPushButton, QComboBox, QApplication, QFileDialog, QStackedWidget, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QVBoxLayout, QWidget, QDialog, QProgressBar
from PyQt6.QtGui import QPixmap, QIcon
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

    def setup_single_screen(self):
        layout = QVBoxLayout(self.single_screen)

        single_label = QLabel("Plugin Generation")
        single_label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(single_label)

        # Main vertical layout
        main_layout = QVBoxLayout()

        # First horizontal layout for the labels and text fields
        horizontal_layout_1 = QHBoxLayout()

        # Labels
        left_labels = ["Instrument:", "Category:", "Interface:", "Role:"]
        for label_text in left_labels:
            label = QLabel(label_text)
            label.setStyleSheet("color: white;")
            horizontal_layout_1.addWidget(label)

        # Text fields
        text_fields = []
        for _ in range(len(left_labels)):
            text_field = QLineEdit()
            text_field.setMaximumWidth(250)
            text_fields.append(text_field)
            horizontal_layout_1.addWidget(text_field)

        main_layout.addLayout(horizontal_layout_1)

        # Second horizontal layout for radio buttons
        horizontal_layout_2 = QHBoxLayout()

        # Add radio buttons
        for _ in range(len(left_labels)):
            radio_layout = QVBoxLayout()
            radio_button1 = QRadioButton("Option 1")
            radio_button2 = QRadioButton("Option 2")
            radio_layout.addWidget(radio_button1)
            radio_layout.addWidget(radio_button2)
            horizontal_layout_2.addLayout(radio_layout)

        main_layout.addLayout(horizontal_layout_2)

        layout.addLayout(main_layout)

        # Spacer
        layout.addSpacing(20)

        # Generate button
        self.generate_button = QPushButton("Generate")
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
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Instrument", "Category", "SCPI Subsystems", "Interface", "Role"])

        # Set table height
        table.setFixedHeight(400)  # Adjust the height as needed

        layout.addWidget(table)

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

        # Add input fields
        instrument_label = QLabel("Instrument:")
        instrument_input = QLineEdit()
        layout.addWidget(instrument_label)
        layout.addWidget(instrument_input)

        category_label = QLabel("Category:")
        category_input = QLineEdit()
        layout.addWidget(category_label)
        layout.addWidget(category_input)

        scpi_label = QLabel("SCPI Subsystems:")
        scpi_input = QLineEdit()
        layout.addWidget(scpi_label)
        layout.addWidget(scpi_input)

        interface_label = QLabel("Interface:")
        interface_input = QLineEdit()
        layout.addWidget(interface_label)
        layout.addWidget(interface_input)

        role_label = QLabel("Role:")
        role_input = QLineEdit()
        layout.addWidget(role_label)
        layout.addWidget(role_input)

        # Add OK button to confirm entry
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(lambda: self.add_entry_to_table(dialog, instrument_input.text(), category_input.text(), scpi_input.text(), interface_input.text(), role_input.text()))
        layout.addWidget(ok_button)

        dialog.exec()

    def add_entry_to_table(self, dialog, instrument, category, scpi, interface, role):
        # Assuming 'table' is accessible here as it is a member of the class
        table = self.findChild(QTableWidget)
        row_position = table.rowCount()
        table.insertRow(row_position)
        table.setItem(row_position, 0, QTableWidgetItem(instrument))
        table.setItem(row_position, 1, QTableWidgetItem(category))
        table.setItem(row_position, 2, QTableWidgetItem(scpi))
        table.setItem(row_position, 3, QTableWidgetItem(interface))
        table.setItem(row_position, 4, QTableWidgetItem(role))
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
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
