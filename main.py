import os
import shutil
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextBrowser, QMessageBox
from PyQt5 import QtCore

class ModSelectorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mod Selector")
        self.setGeometry(100, 100, 800, 500)
        
        layout = QVBoxLayout()

        title_label = QLabel("Mod Selector")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        # Paths for input and output folders
        self.input_folder_path = "modpacks"
        self.output_folder_path = "mods"
        
        # Create input folder if it doesn't exist
        if not os.path.exists(self.input_folder_path) or not os.path.isdir(self.input_folder_path):
            os.makedirs(self.input_folder_path)
        
        # Check if output folder exists and create modpack01 subfolder with files
        if os.path.exists(self.output_folder_path) and os.path.isdir(self.output_folder_path):
            self.modpack01_folder_path = os.path.join(self.input_folder_path, "modpack01")
            if not os.path.exists(self.modpack01_folder_path):
                os.makedirs(self.modpack01_folder_path)
                with open(os.path.join(self.modpack01_folder_path, "mod1.jar"), "w") as mod1_file:
                    pass
                with open(os.path.join(self.modpack01_folder_path, "mod2.jar"), "w") as mod2_file:
                    pass
                with open(os.path.join(self.modpack01_folder_path, "op.txt"), "w") as op_file:
                    op_file.write("This is a test modpack")
        
        # List of folders in the input folder
        self.folders = self.list_folders(self.input_folder_path)
        
        self.buttons_layout = QVBoxLayout()

        # Create buttons for each folder
        for folder in self.folders:
            button = QPushButton(folder)
            button.clicked.connect(lambda checked, folder=folder: self.folder_selected(folder))
            self.buttons_layout.addWidget(button)

        self.info_layout = QVBoxLayout()

        self.info_label = QLabel("Description")
        self.info_layout.addWidget(self.info_label)

        self.text_browser = QTextBrowser()
        self.info_layout.addWidget(self.text_browser)

        # Button for final selection
        self.final_button = QPushButton("Final Selection")
        self.final_button.clicked.connect(self.final_selection)

        self.final_button.setFixedWidth(180)  # Set fixed width for square button
        self.final_button.setFixedHeight(80)  # Set fixed height for square button

        layout.addLayout(self.buttons_layout)
        layout.addLayout(self.info_layout)
        layout.addWidget(self.final_button)

        self.output_folder_button = QPushButton("Browse for Output Folder")  # New button
        self.output_folder_button.clicked.connect(self.choose_output_folder)  # Connect to the function
        layout.addWidget(self.output_folder_button)

        self.selected_folder = None
        self.selected_output_folder = None  # Store the selected output folder

        self.setLayout(layout)

    def list_folders(self, path):
        folders = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
        return folders

    def folder_selected(self, selected_folder):
        self.text_browser.clear()
        self.selected_folder = selected_folder
        selected_folder_path = os.path.join(self.input_folder_path, selected_folder)
        
        op_file_path = os.path.join(selected_folder_path, "op.txt")
        if os.path.exists(op_file_path):
            with open(op_file_path, "r", encoding="utf-8") as op_file:
                op_content = op_file.read()
                self.text_browser.setPlainText(op_content)
        else:
            self.text_browser.setPlainText("No description available. You can add one through the op.txt file in your custom build folder")

    def choose_output_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        selected_folder = QFileDialog.getExistingDirectory(self, "Choose Output Folder", self.selected_output_folder or self.output_folder_path, options=options)
        
        if selected_folder:
            self.selected_output_folder = selected_folder

    def final_selection(self):
        if self.selected_folder and self.selected_output_folder:
            selected_folder_path = os.path.join(self.input_folder_path, self.selected_folder)

            for root, _, files in os.walk(self.selected_output_folder):
                for file in files:
                    os.remove(os.path.join(root, file))
            
            for root, _, files in os.walk(selected_folder_path):
                for file in files:
                    src_path = os.path.join(selected_folder_path, file)
                    dest_path = os.path.join(self.selected_output_folder, file)
                    shutil.copy(src_path, dest_path)
            
            self.show_info("Files successfully copied.")
        else:
            self.show_info("Select both an input folder and an output folder before performing the final selection.")

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
        sys.exit()

    def show_info(self, message):
        QMessageBox.information(self, "Information", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModSelectorApp()
    window.show()
    sys.exit(app.exec_())
