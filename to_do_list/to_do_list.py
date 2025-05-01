"""
Description: This file contains the ToDoList class, which allows users to add, edit, and manage to-do tasks.
Author: Abhishek Gill
"""

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QTableWidget, QLabel, QMessageBox, QVBoxLayout, QWidget, QTableWidgetItem, QComboBox, QDialog
from to_do_list.task_editor import TaskEditor
import csv


class ToDoList(QMainWindow):
    """
    ToDoList Class (QMainWindow). Provides users a 
    way to manage their to-do list tasks.
    """

    def __init__(self):
        """
        Initializes a ToDo List window in which 
        users can add, edit, and remove to-do tasks.
        Sets up the user interface and connects signals to slots.
        Loads initial data from a CSV file.
        """
        super().__init__()
        self.__initialize_widgets()

        # Connect signals to slots
        self.add_button.clicked.connect(self.__on_add_task)
        self.task_table.cellClicked.connect(self.__on_edit_task)
        self.save_button.clicked.connect(self.__save_to_csv)

        # Load data from the CSV file
        try:
            self.__load_data('output/todo.csv')
        except FileNotFoundError:
            self.__load_data('data/todo.csv')

    def __initialize_widgets(self):
        """
        Initializes and arranges all widgets in the ToDo List window.
        Sets up the main layout and widget properties.
        """
        self.setWindowTitle("To-Do List")

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("New Task")

        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Backlog", "In Progress", "Done"])

        self.add_button = QPushButton("Add Task", self)
        self.save_button = QPushButton("Save to CSV", self)

        self.task_table = QTableWidget(self)
        self.task_table.setColumnCount(2)
        self.task_table.setHorizontalHeaderLabels(["Task", "Status"])

        self.status_label = QLabel(self)

        layout = QVBoxLayout()
        layout.addWidget(self.task_input)
        layout.addWidget(self.status_combo)
        layout.addWidget(self.add_button)
        layout.addWidget(self.task_table)
        layout.addWidget(self.save_button)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    @Slot()
    def __on_add_task(self):
        """
        Slot to handle adding a new task when the Add Task button is clicked.
        Extracts the task description and status, validates them,
        and adds them to the task table if the task description is provided.

        If the task description is empty, displays a message prompting the user to fill it in.
        """
        # Extract data from input fields, trimming extra whitespace
        task = self.task_input.text().strip()
        status = self.status_combo.currentText()

        # Check if the task is provided
        if task:
            # Add a new row to the table with the task and status
            self.__add_table_row([task, status])
            # Update status label with a success message
            self.status_label.setText(f"Added task: {task}")
            # Clear the task input field after adding
            self.task_input.clear()
        else:
            # If task description is empty, prompt the user
            self.status_label.setText("Please enter a task and select its status.")

    @Slot(int, str)
    def update_task_status(self, row: int, new_status: str):
        """
        Slot to handle updating the task status when the task_updated signal is emitted.
        
        Parameters:
            row (int): The row of the task to update.
            new_status (str): The new status to set for the task.
        """
        # Update the status cell in the task table
        self.task_table.setItem(row, 1, QTableWidgetItem(new_status))

        # Update status label to confirm the change
        self.status_label.setText(f"Task status updated to: {new_status}")

    @Slot(int, int)
    def __on_edit_task(self, row: int, column: int):
        """
        Slot to handle editing a selected task when the user clicks on a row in the task table.
        Opens a TaskEditor dialog to allow the user to edit the status of the selected task.
        
        Parameters:
            row (int): The row of the clicked task in the task table.
            column (int): The column of the clicked cell (not used here).
        """
        # Get the current status of the selected task
        current_status = self.task_table.item(row, 1).text()
        
        # Open TaskEditor dialog
        task_editor = TaskEditor(row, current_status)

        # Connect TaskEditor’s task_updated signal to update_task_status
        task_editor.task_updated.connect(self.update_task_status)

        # Execute the dialog
        task_editor.exec()

    def __add_table_row(self, row_data):
        """
        Adds a new row to the task_table with the specified data.

        Args:
            row_data (list): A list containing task and status information.
        """
        # Determine the next available row position
        row_position = self.task_table.rowCount()

        # Insert a new row at the determined position
        self.task_table.insertRow(row_position)

        # Create QTableWidgetItem objects for each column in row_data
        task_item = QTableWidgetItem(row_data[0])
        status_item = QTableWidgetItem(row_data[1])

        # Place the items in the task_table at the specified row and columns
        self.task_table.setItem(row_position, 0, task_item)  # Task column
        self.task_table.setItem(row_position, 1, status_item)  # Status column


    def __load_data(self, file_path: str):
        """
        Reads data from a CSV file and populates the task table.

        Args:
            file_path (str): The file path to the CSV file containing task data.
        """
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            # Skip the header row
            next(reader)
            # Add each row from the file to the table
            for row in reader:
                self.__add_table_row(row)
    
    def __save_to_csv(self):
        """
        Saves the data from task_table to a CSV file.
        
        Iterates through each row in the task table, extracts the task and status values,
        and writes them to a CSV file located in the output directory. Displays a confirmation
        message in the status label upon successful save.
        """
        file_path = 'output/todo.csv'
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(["Task", "Status"])
            
            # Iterate through each row in the task table and write to the CSV
            for row in range(self.task_table.rowCount()):
                # Extract task and status text from the table cells
                task = self.task_table.item(row, 0).text() if self.task_table.item(row, 0) else ""
                status = self.task_table.item(row, 1).text() if self.task_table.item(row, 1) else ""
                # Write the row of data to the CSV file
                writer.writerow([task, status])
    
        # Confirm the save action to the user
        self.status_label.setText("Tasks saved to todo.csv.")
    