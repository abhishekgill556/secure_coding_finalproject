"""
Description: This file contains the ContactList class, which allows users to add and remove contacts.
Author: Abhishek Gill
"""

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QTableWidget, QLabel, QVBoxLayout, QWidget, QTableWidgetItem, QMessageBox

class ContactList(QMainWindow):
    """
    Contact List Class (QMainWindow). Provides users a 
    way to manage their contacts.
    """
    
    def __init__(self):
        """
        Initializes a Contact List window in which 
        users can add and remove contact data.
        Sets up the user interface and connects signals to slots.
        """
        super().__init__()
        self.__initialize_widgets()

        # Connect the Add Contact button to the on_add_contact slot
        self.add_button.clicked.connect(self.__on_add_contact)
        # Connect the Remove Contact button to the on_remove_contact slot
        self.remove_button.clicked.connect(self.__on_remove_contact)

    def __initialize_widgets(self):
        """
        Initializes and arranges all widgets in the Contact List window.
        Sets up the main layout and widget properties.
        """
        # Set the window title
        self.setWindowTitle("Contact List")

        # Create and set up input fields for contact name and phone number
        self.contact_name_input = QLineEdit(self)
        self.contact_name_input.setPlaceholderText("Contact Name")

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Phone Number")

        # Create buttons for adding and removing contacts
        self.add_button = QPushButton("Add Contact", self)
        self.remove_button = QPushButton("Remove Contact", self)
        
        # Set up the table for displaying contacts with two columns: Name and Phone
        self.contact_table = QTableWidget(self)
        self.contact_table.setColumnCount(2)
        self.contact_table.setHorizontalHeaderLabels(["Name", "Phone"])

        # Status label to show messages to the user
        self.status_label = QLabel(self)

        # Arrange widgets vertically in the layout
        layout = QVBoxLayout()
        layout.addWidget(self.contact_name_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.contact_table)
        layout.addWidget(self.status_label)

        # Set the layout in a central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    @Slot()
    def __on_add_contact(self):
        """
        Slot to handle adding a new contact when the Add Contact button is clicked.
        Extracts the contact name and phone number from input fields, validates them,
        and adds them to the contact table if both fields are populated.
        
        If either field is empty, displays a message prompting the user to fill in both fields.
        """
        # Extract data from input fields, trimming extra whitespace
        name = self.contact_name_input.text().strip()
        phone = self.phone_input.text().strip()
        
        # Check if both name and phone are provided
        if name and phone:
            # Get the current row count to add a new row at the bottom
            row_position = self.contact_table.rowCount()
            self.contact_table.insertRow(row_position)
            
            # Create table items for name and phone
            name_item = QTableWidgetItem(name)
            phone_item = QTableWidgetItem(phone)
            
            # Add items to the table
            self.contact_table.setItem(row_position, 0, name_item)
            self.contact_table.setItem(row_position, 1, phone_item)
            
            # Update status label with a success message
            self.status_label.setText(f"Added contact: {name}")
        else:
            # If either field is empty, prompt the user
            self.status_label.setText("Please enter a contact name and phone number.")

    @Slot()
    def __on_remove_contact(self):
        """
        Slot to handle removing a selected contact when the Remove Contact button is clicked.
        Checks if a row is selected, confirms with the user, and removes the selected contact if confirmed.
        
        If no row is selected, displays a message prompting the user to select a row first.
        """
        # Check if a row is explicitly selected
        if self.contact_table.selectionModel().hasSelection():
            # Get the currently selected row
            selected_row = self.contact_table.currentRow()

            # Confirm removal with the user
            reply = QMessageBox.question(
                self, 
                "Remove Contact", 
                "Are you sure you want to remove the selected contact?", 
                QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.No
            )
            
            # Remove the row if the user confirmed with 'Yes'
            if reply == QMessageBox.Yes:
                self.contact_table.removeRow(selected_row)
                self.status_label.setText("Contact removed.")
            else:
                # If the user clicked 'No', update the status label with a cancellation message
                self.status_label.setText("Removal canceled.")
        else:
            # Inform the user that no row was selected
            self.status_label.setText("Please select a row to be removed.")
