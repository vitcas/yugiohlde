from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QListWidget, QPushButton, QInputDialog, QScrollArea, QGridLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os

class CreateDeckDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Criar Novo Deck")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal (horizontal)
        self.main_layout = QHBoxLayout()

        # Layout esquerdo (Lista de cartas do deck)
        self.left_layout = QVBoxLayout()
        self.deck_list_label = QLabel("Cartas no Deck:")
        self.left_layout.addWidget(self.deck_list_label)
        self.deck_card_list = QListWidget()
        self.left_layout.addWidget(self.deck_card_list)
        
        # Botão para remover carta do deck
        self.remove_card_button = QPushButton("Remover Carta do Deck", self)
        self.remove_card_button.clicked.connect(self.remove_card_from_deck)
        self.left_layout.addWidget(self.remove_card_button)

        self.main_layout.addLayout(self.left_layout)

        # Layout central (formulário de criação de deck)
        self.center_layout = QVBoxLayout()
        
        self.deck_choice_label = QLabel("Escolha o Deck:")
        self.center_layout.addWidget(self.deck_choice_label)
        
        self.deck_choice = QComboBox()
        self.deck_choice.addItem("Main Deck")
        self.deck_choice.addItem("Extra Deck")
        self.center_layout.addWidget(self.deck_choice)
        
        self.search_label = QLabel("Pesquisar carta por nome:")
        self.center_layout.addWidget(self.search_label)
        
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Digite o nome da carta...")
        self.center_layout.addWidget(self.search_input)
        
        self.search_results = QListWidget(self)
        self.center_layout.addWidget(self.search_results)
        
        self.add_card_button = QPushButton("Adicionar Carta ao Deck", self)
        self.add_card_button.clicked.connect(self.add_card_to_deck)
        self.center_layout.addWidget(self.add_card_button)
        
        self.save_deck_button = QPushButton("Salvar Deck", self)
        self.save_deck_button.clicked.connect(self.save_deck)
        self.center_layout.addWidget(self.save_deck_button)
        
        self.main_layout.addLayout(self.center_layout)

        # Layout direito (Imagens das cartas)
        self.right_layout = QVBoxLayout()
        self.card_images_label = QLabel("Preview das Cartas:")
        self.right_layout.addWidget(self.card_images_label)
        
        self.card_images_area = QScrollArea(self)
        self.card_images_area.setWidgetResizable(True)
        
        self.card_images_grid = QGridLayout()
        self.card_images_widget = QWidget()
        self.card_images_widget.setLayout(self.card_images_grid)
        self.card_images_area.setWidget(self.card_images_widget)
        
        self.right_layout.addWidget(self.card_images_area)
        self.main_layout.addLayout(self.right_layout)

        self.setLayout(self.main_layout)

        # Listas para armazenar as cartas do deck
        self.main_deck_ids = []
        self.extra_deck_ids = []
        
        # Conectar o campo de busca ao método de pesquisa de cartas
        self.search_input.textChanged.connect(self.search_cards)

    def search_cards(self):
        """Buscar cartas por nome no banco de dados"""
        global conn
        query = self.search_input.text()
        if query:
            query_sql = """
            SELECT datas.id, texts.name 
            FROM datas 
            JOIN texts ON datas.id = texts.id 
            WHERE texts.name LIKE ? LIMIT 50
            """
            cursor = conn.cursor()
            cursor.execute(query_sql, ('%' + query + '%',))
            results = cursor.fetchall()
            
            self.search_results.clear()
            
            for card in results:
                self.search_results.addItem(f"{card[0]} - {card[1]}")
        else:
            self.search_results.clear()

    def add_card_to_deck(self):
        """Adicionar carta selecionada ao deck"""
        selected_item = self.search_results.currentItem()
        if selected_item:
            card_id = int(selected_item.text().split(" - ")[0])

            if self.deck_choice.currentText() == "Main Deck":
                self.main_deck_ids.append(card_id)
            else:
                self.extra_deck_ids.append(card_id)
            
            self.deck_card_list.addItem(selected_item.text())
            self.display_card_image(card_id)
            
    def remove_card_from_deck(self):
        """Remover carta selecionada do deck"""
        selected_item = self.deck_card_list.currentItem()
        if selected_item:
            card_text = selected_item.text()
            card_id = int(card_text.split(" - ")[0])
            
            if card_id in self.main_deck_ids:
                self.main_deck_ids.remove(card_id)
            elif card_id in self.extra_deck_ids:
                self.extra_deck_ids.remove(card_id)
            
            self.deck_card_list.takeItem(self.deck_card_list.row(selected_item))

    def display_card_image(self, card_id):
        """Exibir a imagem da carta com base no seu ID na grade"""
        image_path = os.path.join("../pics", f"{card_id}.jpg")
        
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(60, 80, Qt.AspectRatioMode.KeepAspectRatio)
            
            label = QLabel()
            label.setPixmap(pixmap)
            
            max_columns = 5
            row = self.card_images_grid.count() // max_columns
            col = self.card_images_grid.count() % max_columns
            
            self.card_images_grid.addWidget(label, row, col)
            
    def save_deck(self):
        """Salvar o novo deck em um arquivo .ydk"""
        if not self.main_deck_ids and not self.extra_deck_ids:
            print("Por favor, adicione cartas ao deck antes de salvar.")
            return

        deck_name, ok = QInputDialog.getText(self, "Nome do Deck", "Digite o nome do novo deck:")
        
        if ok and deck_name:
            deck_path = os.path.join("../deck", f"{deck_name}.ydk")
            
            with open(deck_path, 'w') as deck_file:
                deck_file.write("#main\n")
                deck_file.write("\n".join(str(card_id) for card_id in self.main_deck_ids))
                deck_file.write("\n#extra\n")
                deck_file.write("\n".join(str(card_id) for card_id in self.extra_deck_ids))
            
            print(f"Deck '{deck_name}' salvo com sucesso!")
            self.accept()
