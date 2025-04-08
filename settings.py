from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QCheckBox, QComboBox, QFileDialog
)
from PyQt6.QtCore import QSettings
import sqlite3
import os
from config import update_config

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configurações")

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Campo do caminho EDOPro
        self.edopro_path_input = QLineEdit()
        self.edopro_browse_btn = QPushButton("Procurar")
        self.edopro_browse_btn.clicked.connect(self.browse_edopro_path)

        form_layout.addRow("Caminho EDOPro:", self.edopro_path_input)
        form_layout.addRow("", self.edopro_browse_btn)

        # Checkbox usar EDOPro
        self.use_edopro_checkbox = QCheckBox("Usar EDOPro")

        # ComboBox da banlist
        self.banlist_combo = QComboBox()
        self.banlist_combo.addItem("nenhuma")
        self.banlist_combo.addItems(self.load_banlists())

        form_layout.addRow("Banlist favorita:", self.banlist_combo)

        layout.addLayout(form_layout)
        layout.addWidget(self.use_edopro_checkbox)

        self.setLayout(layout)
        self.load_settings()

    def load_banlists(self):
        db_path = os.path.join(os.path.dirname(__file__), "..", "gehenna.db")
        if not os.path.exists(db_path):
            return []
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT format FROM banlists ORDER BY format")
        results = cursor.fetchall()
        conn.close()
        return [row[0] for row in results if row[0]]

    def browse_edopro_path(self):
        path = QFileDialog.getExistingDirectory(self, "Selecionar pasta do EDOPro")
        if path:
            self.edopro_path_input.setText(path)

    def load_settings(self):
        settings = QSettings("MeuApp", "Config")
        self.edopro_path_input.setText(settings.value("edopro_path", "C:/ProjectIgnis"))
        self.use_edopro_checkbox.setChecked(settings.value("use_edopro", False, type=bool))
        self.banlist_combo.setCurrentText(settings.value("banlist", "nenhuma"))

    def closeEvent(self, event):
        # Salvar automaticamente ao fechar
        update_config("edopro_path", self.edopro_path_input.text())
        update_config("use_edopro", self.use_edopro_checkbox.isChecked())
        update_config("banlist", self.banlist_combo.currentText())
        event.accept()
