from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton, QFormLayout, QWidget, QLineEdit
import sys
import sqlite3

mocatypes = ["Normal","Effect","Ritual","Fusion","Synchro","Xyz","Toon","Spirit","Union","Gemini","Tuner","Flip","Pendulum","Link"]
motypes = ["Spellcaster","Dragon","Zombie","Warrior","Beast-Warrior","Beast","Winged Beast","Fiend","Fairy","Insect","Dinosaur","Reptile","Fish","Sea Serpent","Aqua","Pyro","Thunder","Rock","Plant","Machine","Psychic","Divine-Beast","Wyrm","Cyberse","Illusion"]

class AdvancedSearch(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Search")
        self.setGeometry(100, 100, 400, 350)
        
        # Layout principal
        self.main_layout = QVBoxLayout()
        
        # Campo de busca por nome e efeito
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Name or Effect Text...")
        self.main_layout.addWidget(QLabel("Search:"))
        self.main_layout.addWidget(self.search_input)
        
        # Opções principais
        self.card_types = ["any", "monster", "spell", "trap"]
        self.combo_card_type = QComboBox()
        self.combo_card_type.addItems(self.card_types)
        self.combo_card_type.currentIndexChanged.connect(self.update_filters)
        self.main_layout.addWidget(QLabel("Card Type:"))
        self.main_layout.addWidget(self.combo_card_type)
        
        # Layout dos filtros
        self.filter_widget = QWidget()
        self.filter_layout = QFormLayout()
        self.filter_widget.setLayout(self.filter_layout)
        self.main_layout.addWidget(self.filter_widget)
        
        # Botão de pesquisa
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.execute_search)
        self.main_layout.addWidget(self.search_button)
        
        self.setLayout(self.main_layout)
        self.update_filters()
    
    def update_filters(self):
        # Limpar os filtros
        while self.filter_layout.rowCount() > 0:
            self.filter_layout.removeRow(0)      
        self.filters = {}
        selected_type = self.combo_card_type.currentText()     
        if selected_type == "monster":
            self.monster_subs = mocatypes
            self.monster_types = motypes
            self.monster_attr = ["any", "light", "water", "fire", "wind", "earth", "dark", "divine"]
            
            combo_monster_subs = QComboBox()
            combo_monster_subs.addItems(self.monster_subs)
            #self.filters['monster_subs'] = combo_monster_subs
            #self.filter_layout.addRow("Monster Subtype:", combo_monster_subs)
            
            combo_monster_attr = QComboBox()
            combo_monster_attr.addItems(self.monster_attr)
            self.filters['englishAttribute'] = combo_monster_attr
            self.filter_layout.addRow("Monster Attribute:", combo_monster_attr)
            
            combo_monster_types = QComboBox()
            combo_monster_types.addItems(self.monster_types)
            #self.filters['monster_types'] = combo_monster_types
            #self.filter_layout.addRow("Monster Type:", combo_monster_types)
            
            spin_stars = QSpinBox()
            spin_stars.setRange(0, 12)
            self.filters['level'] = spin_stars
            self.filter_layout.addRow("Monster Stars:", spin_stars)
            
            spin_atk = QSpinBox()
            spin_atk.setRange(0, 5000)
            spin_stars.setValue(0)
            self.filters['atk'] = spin_atk
            self.filter_layout.addRow("Monster ATK:", spin_atk)
            
            spin_def = QSpinBox()
            spin_def.setRange(0, 5000)
            spin_stars.setValue(0)
            self.filters['def'] = spin_def
            self.filter_layout.addRow("Monster DEF:", spin_def)
        
        elif selected_type == "spell":
            self.spell_subs = ["any","quick","equip","field","continuous","ritual"]
            combo_spell_subs = QComboBox()
            combo_spell_subs.addItems(self.spell_subs)
            #self.filters['spell_subs'] = combo_spell_subs
            self.filter_layout.addRow("Spell Subtype:", combo_spell_subs)
        
        elif selected_type == "trap":
            self.trap_subs = ["any", "counter", "continuous"]
            combo_trap_subs = QComboBox()
            combo_trap_subs.addItems(self.trap_subs)
            #self.filters['trap_subs'] = combo_trap_subs
            self.filter_layout.addRow("Trap Subtype:", combo_trap_subs)
    
    def execute_search(self):
        conn = sqlite3.connect("gehenna.db")
        cursor = conn.cursor()       
        query = "SELECT * FROM cartas WHERE 1=1"
        params = [] 
        # Filtro de nome e efeito
        search_text = self.search_input.text().strip()
        if search_text:
            query += " AND (name LIKE ? OR effectText LIKE ?)"
            params.extend([f"%{search_text}%", f"%{search_text}%"])   
        # Tipo da carta
        card_type = self.combo_card_type.currentText()
        if card_type != "any":
            query += " AND type = ?"
            params.append(card_type) 
        # Filtros adicionais
        for key, widget in self.filters.items():
            if isinstance(widget, QComboBox):
                value = widget.currentText()
                if value != "any":
                    query += f" AND {key} = ?"
                    params.append(value)
            elif isinstance(widget, QSpinBox):
                value = widget.value()
                if value != 0:
                    query += f" AND {key} = ?"
                    params.append(value)
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()      
        print("Results:", len(results))
        return results
