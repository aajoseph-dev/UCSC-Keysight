from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QCheckBox

from menu_data import test_steps

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