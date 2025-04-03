from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton
from PyQt6.QtCore import QSettings

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        form_layout.addRow("Usuário:", self.username_input)

        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.save_settings)

        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

        self.load_settings()

    def save_settings(self):
        settings = QSettings("MeuApp", "Config")
        settings.setValue("username", self.username_input.text())

    def load_settings(self):
        settings = QSettings("MeuApp", "Config")
        self.username_input.setText(settings.value("username", ""))