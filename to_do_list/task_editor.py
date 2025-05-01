"""
Description: This file contains the TaskEditor class, which allows users to update the status of a task in the To-Do list.
Author: Abhishek gill
"""

from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QDialog, QComboBox, QPushButton, QVBoxLayout

class TaskEditor(QDialog):
    """
    TaskEditor Class (QDialog). Allows users to update the status of a task.
    """

    # Define the task_updated signal, which sends an int (row) and a str (new status)
    task_updated = Signal(int, str)

    def __init__(self, row: int, status: str):
        """
        Initializes a Task Editor dialog with the current status of a task.
        
        Parameters:
            row (int): The row index of the task being edited.
            status (str): The current status of the task.
        """
        super().__init__()
        self.row = row  # Store the row number for the task being edited
        self.initialize_widgets(status)

    def initialize_widgets(self, status: str):
        """
        Initializes and arranges all widgets in the Task Editor window.
        Sets up the main layout and widget properties.
        
        Parameters:
            status (str): The current status of the task to be set as the default value in the combo box.
        """
        self.setWindowTitle("Edit Task Status")

        # ComboBox to select status
        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Backlog", "In Progress", "Done"])
        self.status_combo.setCurrentText(status)  # Set the initial status in the combo box

        # Save button to confirm the status update
        self.save_button = QPushButton("Save", self)

        # Layout for arranging widgets vertically
        layout = QVBoxLayout()
        layout.addWidget(self.status_combo)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
        self.setFixedWidth(150)

        # Connect the Save button to the on_save_status slot
        self.save_button.clicked.connect(self.on_save_status)

    @Slot()
    def on_save_status(self):
        """
        Slot to handle saving the updated status when the Save button is clicked.
        Retrieves the selected status, emits a signal with the row and new status, and closes the dialog.
        """
        # Extract the current status selected in the combo box
        new_status = self.status_combo.currentText()

        # Emit the task_updated signal with the row and new status
        self.task_updated.emit(self.row, new_status)

        # Accept the dialog to indicate a successful save
        self.accept()

    def get_updated_status(self):
        """
        Retrieves the updated status selected by the user.
        
        Returns:
            str: The updated status.
        """
        return self.status_combo.currentText()
