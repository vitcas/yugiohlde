from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QComboBox, QSpinBox,
    QPushButton, QFormLayout, QWidget, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
import sqlite3

class AdvancedSearch(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Search")
        self.setGeometry(100, 100, 400, 350)
        
        self.main_layout = QVBoxLayout()
        self.results = []

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Name or Effect Text...")
        self.main_layout.addWidget(QLabel("Search:"))
        self.main_layout.addWidget(self.search_input)

        self.combo_card_type = QComboBox()
        self.combo_card_type.addItem("any")
        self.card_types = self.load_types()
        self.combo_card_type.addItems(self.card_types)

        self.combo_card_type.currentIndexChanged.connect(self.update_filters)
        self.main_layout.addWidget(QLabel("Card Type:"))
        self.main_layout.addWidget(self.combo_card_type)

        self.filter_widget = QWidget()
        self.filter_layout = QFormLayout()
        self.filter_widget.setLayout(self.filter_layout)
        self.main_layout.addWidget(self.filter_widget)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.execute_search)
        self.main_layout.addWidget(self.search_button)

        self.setLayout(self.main_layout)
        self.update_filters()
        self.center_on_screen()

    def center_on_screen(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        dialog_geometry = self.frameGeometry()
        dialog_geometry.moveCenter(screen_geometry.center())
        self.move(dialog_geometry.topLeft())

    def load_types(self):
        conn = sqlite3.connect("gehenna.db")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT major FROM types ORDER BY major")
        results = cursor.fetchall()
        conn.close()
        return [row[0] for row in results if row[0]]

    def load_races(self):
        conn = sqlite3.connect("gehenna.db")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT race_name FROM cards_view ORDER BY race_name")
        results = cursor.fetchall()
        conn.close()
        return [row[0] for row in results if row[0]]

    def update_filters(self):
        while self.filter_layout.rowCount() > 0:
            self.filter_layout.removeRow(0)
        self.filters = {}

        selected_type = self.combo_card_type.currentText()
        # subtypes (desc from types where major = selected_type)
        conn = sqlite3.connect("gehenna.db")
        cursor = conn.cursor()
        cursor.execute("SELECT desc FROM types WHERE major = ? ORDER BY desc", (selected_type,))
        subtypes = [row[0] for row in cursor.fetchall()]
        conn.close()

        if subtypes:
            subtype_combo = QComboBox()
            subtype_combo.addItem("any")
            subtype_combo.addItems(subtypes)
            self.filters["type_name"] = subtype_combo
            self.filter_layout.addRow("Subtype:", subtype_combo)
        if selected_type.lower() in ["monster"]:
            # attribute
            attr_combo = QComboBox()
            attr_combo.addItems(["any", "light", "water", "fire", "wind", "earth", "dark", "divine"])
            self.filters["eng_attr"] = attr_combo
            self.filter_layout.addRow("Attribute:", attr_combo)

            # race
            race_combo = QComboBox()
            race_combo.addItem("any")
            race_combo.addItems(self.load_races())
            self.filters["race_name"] = race_combo
            self.filter_layout.addRow("Race:", race_combo)

            # level
            level_spin = QSpinBox()
            level_spin.setRange(0, 12)
            self.filters["level"] = level_spin
            self.filter_layout.addRow("Level:", level_spin)

            # atk
            atk_spin = QSpinBox()
            atk_spin.setRange(0, 5000)
            self.filters["atk"] = atk_spin
            self.filter_layout.addRow("ATK:", atk_spin)

            # def
            def_spin = QSpinBox()
            def_spin.setRange(0, 5000)
            self.filters["def"] = def_spin
            self.filter_layout.addRow("DEF:", def_spin)

    def execute_search(self):
        conn = sqlite3.connect("gehenna.db")
        cursor = conn.cursor()
        query = "SELECT * FROM cards_view WHERE 1=1"
        params = []

        text = self.search_input.text().strip()
        if text:
            query += " AND (name LIKE ? OR effect LIKE ?)"
            params.extend([f"%{text}%", f"%{text}%"])

        type_selected = self.combo_card_type.currentText()
        if type_selected != "any":
            query += " AND type = ?"
            params.append(type_selected)

        for key, widget in self.filters.items():
            if isinstance(widget, QComboBox):
                val = widget.currentText()
                if val != "any":
                    query += f" AND {key} = ?"
                    params.append(val)
            elif isinstance(widget, QSpinBox):
                val = widget.value()
                if val > 0:
                    query += f" AND {key} = ?"
                    params.append(val)

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        print("Results:", len(results))
        self.results = results
        self.accept()  # fecha o QDialog com código de aceitação    
        #return results
