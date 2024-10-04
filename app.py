import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QTabWidget, QLabel, QScrollArea, QTextEdit, QTableWidget, QTableWidgetItem, QSizePolicy,
                             QPushButton, QFileDialog)
from PyQt5.QtCore import Qt, QUrl
from get_file_info import get_file_info, get_file_hash, get_strings, get_header, get_shared_libraries, get_entropy

# GUI App for ElfStudio

class ELFStudioGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ELF Studio")
        self.setGeometry(300, 300, 800, 600)

        # Tab widget to hold different analysis categories
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Initial file path
        self.file_path = ""

        # File selection tab
        self.add_tab("File", self.get_file_selection_tab())
        # Add analysis tabs
        self.add_tab("Overview", self.get_empty_tab())
        self.add_tab("Strings", self.get_empty_tab())
        self.add_tab("Header", self.get_empty_tab())
        self.add_tab("Libraries", self.get_empty_tab())

    def add_tab(self, title, content_widget):
        self.tabs.addTab(content_widget, title)

    def create_scrollable_text(self, content: str):
        scroll_area = QScrollArea()
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(content)
        scroll_area.setWidget(text_edit)
        scroll_area.setWidgetResizable(True)
        return scroll_area

    # Tab: File Selection
    def get_file_selection_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.select_button = QPushButton("Select File")
        self.select_button.clicked.connect(self.select_file)

        layout.addWidget(self.select_button)
        layout.setAlignment(Qt.AlignTop)

        widget.setLayout(layout)
        return widget

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if file_path:
            self.file_path = file_path
            self.update_tabs(file_path)

    def update_tabs(self, file_path):
        self.file_path = file_path 

        for index in range(1, self.tabs.count()):
            tab_widget = self.tabs.widget(index)
            if tab_widget is not None:  
                tab_widget.setParent(None)  

        self.tabs.clear()

        self.add_tab("File", self.get_file_selection_tab())

        self.add_tab("Overview", self.get_file_info_tab(file_path))
        self.add_tab("Strings", self.get_strings_tab(file_path))
        self.add_tab("Header", self.get_header_tab(file_path))
        self.add_tab("Libraries", self.get_shared_libraries_tab(file_path))

        self.tabs.setCurrentIndex(1) 

    def get_empty_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Please select a file to analyze."))
        widget.setLayout(layout)
        return widget

    # Tab: File Info
    def get_file_info_tab(self, file_path):
        file_info = get_file_info(file_path)  
        file_hash = get_file_hash(file_path)  
        entropy = get_entropy(file_path)
        
        table_widget = QTableWidget()
        
        table_widget.setRowCount(len(file_info) + 1)  
        table_widget.setColumnCount(2)
        
        table_widget.setHorizontalHeaderLabels(['Field', 'Data'])
        
        hash_item_key = QTableWidgetItem("sha256 hash")
        hash_item_key.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  
        table_widget.setItem(0, 0, hash_item_key)  
        
        hash_item_value = QTableWidgetItem(file_hash)
        hash_item_value.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  
        table_widget.setItem(0, 1, hash_item_value)  
        
        for row, (key, value) in enumerate(file_info.items(), start=1): 
            key_item = QTableWidgetItem(str(key))
            key_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  
            table_widget.setItem(row, 0, key_item)  
            
            value_item = QTableWidgetItem(str(value))
            value_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            table_widget.setItem(row, 1, value_item) 
        
        current_row_count = table_widget.rowCount()  
        table_widget.setRowCount(current_row_count + 1)  

        entropy_item_key = QTableWidgetItem("entropy")
        entropy_item_key.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        table_widget.setItem(current_row_count, 0, entropy_item_key)  

        entropy_item_value = QTableWidgetItem(f"{entropy:.6f}")
        entropy_item_value.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        table_widget.setItem(current_row_count, 1, entropy_item_value) 
        
        table_widget.resizeColumnsToContents()
        table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(table_widget)
        
        layout.setContentsMargins(0, 0, 0, 0)  
        layout.setSpacing(0)  
        
        widget.setLayout(layout)
        
        return widget

    # Tab: Strings
    def get_strings_tab(self, file_path):
        strings = get_strings(file_path)
        table_widget = QTableWidget()

        table_widget.setRowCount(len(strings) + 1)
        table_widget.setColumnCount(1)

        for row, item in enumerate(strings):
            string_item = QTableWidgetItem(str(item))
            string_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            table_widget.setItem(row, 0, string_item)

        table_widget.resizeColumnsToContents()
        
        table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        widget = QWidget()
        layout = QVBoxLayout()
    
        layout.addWidget(table_widget)
        
        layout.setContentsMargins(0, 0, 0, 0)  
        layout.setSpacing(0)  
        
        widget.setLayout(layout)
        
        return widget

    # Tab: Header
    def get_header_tab(self, file_path):
        header = get_header(file_path)
        header_lines = header['header']
        
        table_widget = QTableWidget()
    
        table_widget.setRowCount(len(header_lines))
        table_widget.setColumnCount(2) 
        
        table_widget.setHorizontalHeaderLabels(['Field', 'Data'])
        
        for row, line in enumerate(header_lines):
            if ':' in line:  
                field, value = line.split(':', 1)  
                field_item = QTableWidgetItem(field.strip())
                field_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  
                table_widget.setItem(row, 0, field_item)  

                value_item = QTableWidgetItem(value.strip())
                value_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  
                table_widget.setItem(row, 1, value_item)  
            else:
                field_item = QTableWidgetItem(line.strip())
                field_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                table_widget.setItem(row, 0, field_item)  
                table_widget.setItem(row, 1, QTableWidgetItem("")) 
        
        table_widget.resizeColumnsToContents()
        
        table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(table_widget)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        widget.setLayout(layout)
        
        return widget

    # Tab: Shared Libraries
    def get_shared_libraries_tab(self, file_path):
        libraries = get_shared_libraries(file_path)

        table_widget = QTableWidget()
        
        table_widget.setRowCount(len(libraries))
        table_widget.setColumnCount(1)  
        
        table_widget.setHorizontalHeaderLabels(['Shared Libraries'])
        
        for row, library in enumerate(libraries):
            stripped_library = library.strip()
            library_item = QTableWidgetItem(stripped_library)
            library_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled) 
            table_widget.setItem(row, 0, library_item) 
        
        table_widget.resizeColumnsToContents()
        
        table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(table_widget)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        widget.setLayout(layout)
        
        return widget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ELFStudioGUI()
    window.show()
    sys.exit(app.exec_())
