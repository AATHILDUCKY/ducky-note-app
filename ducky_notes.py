import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QTextEdit, QScrollArea, QFrame,
    QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sqlite3


class NoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note-Taking App")
        self.setGeometry(100, 100, 1050, 700)

        # SQLite database setup
        self.conn = sqlite3.connect("notes.db")
        self.create_table()

        # Central Widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Navigation Bar
        self.nav_bar = QHBoxLayout()
        self.main_layout.addLayout(self.nav_bar)

        self.insert_btn = QPushButton("Insert Notes")
        self.insert_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.insert_btn.setStyleSheet("""
            QPushButton {
                background-color: #ed750c;
                border-radius: 7px;
                color: #FFFFFF;
                border: 1px solid #006400;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #f5cc84;
                color: black;
            }
        """)
        self.insert_btn.clicked.connect(self.show_insert_section)
        self.nav_bar.addWidget(self.insert_btn)

        self.search_btn = QPushButton("Search Notes")
        self.search_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #ed750c;
                border-radius: 7px;
                color: #FFFFFF;
                border: 1px solid #006400;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #f5cc84;
                color: black;
            }
        """)
        self.search_btn.clicked.connect(self.show_search_section)
        self.nav_bar.addWidget(self.search_btn)

        # Content Section
        self.content_frame = QVBoxLayout()
        self.main_layout.addLayout(self.content_frame)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
            }
            QLabel {
                color: #FFFFFF;
                padding:3px;
            }
            QLineEdit, QTextEdit {
                background-color: #2E2E2E;
                color: white;
                border: 1px solid gray;
                padding: 5px;
            }
            QPushButton {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: 1px solid #555555;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #1E1E1E;
            }
            QScrollArea {
                background-color: #1E1E1E;
            }
            QFrame {
                background-color: #2E2E2E;
                border: 1px solid #555555;
            }
        """)

        self.show_search_section()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                keywords TEXT,
                content TEXT
            )
        """)
        self.conn.commit()

    def show_insert_section(self):
        self.clear_content_frame()

        title_label = QLabel("Title:")
        title_label.setFont(QFont("Arial", 13))
        self.content_frame.addWidget(title_label)

        self.title_entry = QLineEdit()
        self.title_entry.setFont(QFont("Consolas", 12))
        self.title_entry.setPlaceholderText("Enter the title...")
        self.content_frame.addWidget(self.title_entry)

        keywords_label = QLabel("Keywords (comma-separated):")
        keywords_label.setFont(QFont("Arial", 13))
        self.content_frame.addWidget(keywords_label)

        self.keywords_entry = QLineEdit()
        self.keywords_entry.setFont(QFont("Consolas", 12))
        self.keywords_entry.setPlaceholderText("Enter keywords...")
        self.content_frame.addWidget(self.keywords_entry)

        content_label = QLabel("Content:")
        content_label.setFont(QFont("Arial", 13))
        self.content_frame.addWidget(content_label)

        self.content_text = QTextEdit()
        self.content_text.setFont(QFont("Consolas", 12))
        self.content_frame.addWidget(self.content_text)

        insert_button = QPushButton("Insert Note")
        insert_button.setFont(QFont("Arial", 14, QFont.Bold))
        insert_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius:8px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        insert_button.clicked.connect(self.insert_note)
        self.content_frame.addWidget(insert_button)

    def insert_note(self):
        title = self.title_entry.text().strip()
        keywords = self.keywords_entry.text().strip()
        content = self.content_text.toPlainText().strip()

        if not title or not keywords or not content:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO notes (title, keywords, content) VALUES (?, ?, ?)", (title, keywords, content))
        self.conn.commit()
        QMessageBox.information(self, "Success", "Note inserted successfully!")
        self.title_entry.clear()
        self.keywords_entry.clear()
        self.content_text.clear()

    def show_search_section(self):
        self.clear_content_frame()

        search_label = QLabel("Search Keywords (comma-separated):")
        search_label.setFont(QFont("Arial", 14))
        self.content_frame.addWidget(search_label)

        self.search_entry = QLineEdit()
        self.search_entry.setFont(QFont("Consolas", 12))
        self.search_entry.setPlaceholderText("Type keywords to search...")
        self.search_entry.textChanged.connect(self.search_notes)
        self.content_frame.addWidget(self.search_entry)

        # Scrollable results section
        self.results_scroll = QScrollArea()
        self.results_scroll.setWidgetResizable(True)
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_scroll.setWidget(self.results_container)
        self.content_frame.addWidget(self.results_scroll)

    def search_notes(self):
        keywords = self.search_entry.text().strip()
        self.clear_results_layout()

        if not keywords:
            return

        keywords_list = [kw.strip().lower() for kw in keywords.split(",")]
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, title, content, keywords FROM notes")
        results = cursor.fetchall()

        for note_id, title, content, note_keywords in results:
            note_keywords_list = [kw.strip().lower() for kw in note_keywords.split(",")]
            if all(any(kw in db_kw for db_kw in note_keywords_list) for kw in keywords_list):
                self.display_result(note_id, title, content)

    def display_result(self, note_id, title, content):
        result_frame = QFrame()
        result_frame.setStyleSheet("background-color: #2E2E2E; border: 1px solid #555555; padding: 10px;")
        result_layout = QVBoxLayout(result_frame)

        # Display the title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #FFA500;")
        result_layout.addWidget(title_label)

        # Display the content directly as-is, ensuring it's in plain text format
        content_text = QTextEdit()
        content_text.setFont(QFont("Consolas", 12))
        content_text.setPlainText(content)
        content_text.setReadOnly(True)
        result_layout.addWidget(content_text)

        # Add edit and delete buttons
        button_layout = QHBoxLayout()

        edit_button = QPushButton("Edit")
        edit_button.setFont(QFont("Arial", 8))
        edit_button.setFixedSize(100, 40)
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #64B5F6;
            }
            QPushButton:pressed {
                background-color: #1976D2;
            }
        """)
        edit_button.clicked.connect(lambda: self.toggle_edit_mode(edit_button, content_text, note_id))

        delete_button = QPushButton("Delete")
        delete_button.setFont(QFont("Arial", 8))
        delete_button.setFixedSize(100, 40)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4500;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FF6347;
            }
            QPushButton:pressed {
                background-color: #FF0000;
            }
        """)
        delete_button.clicked.connect(lambda: self.delete_note(note_id))
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        result_layout.addLayout(button_layout)

        self.results_layout.addWidget(result_frame)

    def toggle_edit_mode(self, edit_button, content_text, note_id):
        if edit_button.text() == "Edit":
            content_text.setReadOnly(False)
            content_text.setStyleSheet("background-color: white; color: black; border: 2px solid #1976D2;")
            edit_button.setText("Update")
        else:
            new_content = content_text.toPlainText().strip()
            if new_content:
                cursor = self.conn.cursor()
                cursor.execute("UPDATE notes SET content = ? WHERE id = ?", (new_content, note_id))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Note updated successfully!")
                content_text.setReadOnly(True)
                content_text.setStyleSheet("background-color: #2E2E2E; color: white; border: 1px solid gray;")
                edit_button.setText("Edit")

    def delete_note(self, note_id):
        confirm = QMessageBox.question(self, "Confirm", "Are you sure you want to delete this note?")
        if confirm == QMessageBox.Yes:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            self.conn.commit()
            QMessageBox.information(self, "Success", "Note deleted successfully!")
            self.search_notes()

    def clear_content_frame(self):
        for i in reversed(range(self.content_frame.count())):
            widget = self.content_frame.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def clear_results_layout(self):
        for i in reversed(range(self.results_layout.count())):
            widget = self.results_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    note_app = NoteApp()
    note_app.show()
    sys.exit(app.exec_())
