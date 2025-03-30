from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QListWidget, QPushButton, QInputDialog, QScrollArea, QGridLayout, QWidget, QListWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os
import sqlite3

class CreateDeckDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Criar Novo Deck")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)  # Bloqueia o redimensionamento

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
        self.search_results.itemClicked.connect(self.on_item_selected)
        self.center_layout.addWidget(self.search_results)
        
        self.add_card_button = QPushButton("Adicionar Carta ao Deck", self)
        self.add_card_button.clicked.connect(self.add_card_to_deck)
        self.center_layout.addWidget(self.add_card_button)
        
        self.save_deck_button = QPushButton("Salvar Deck", self)
        self.save_deck_button.clicked.connect(self.save_deck)
        self.center_layout.addWidget(self.save_deck_button)
        
        self.main_layout.addLayout(self.center_layout)

        # Layout direito (detalhes da carta)
        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.card_images_label = QLabel("Card Preview:")
        self.right_layout.addWidget(self.card_images_label)

        # Criando um QLabel para exibir a imagem
        self.image_label = QLabel()
        pixmap = QPixmap("dummy.jpeg")  # Substitua pelo caminho da sua imagem
        #pixmap = pixmap.scaled(300, 350, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(pixmap)
        self.right_layout.addWidget(self.image_label)

        #texto do efeito
        self.cardeff_label = QLabel("efeito aki")
        self.cardeff_label.setFixedWidth(250) 
        self.cardeff_label.setWordWrap(True)  # Habilita a quebra de linha
        self.right_layout.addWidget(self.cardeff_label)

        self.main_layout.addLayout(self.right_layout)
        self.setLayout(self.main_layout)

        # Listas para armazenar as cartas do deck
        self.main_deck_ids = []
        self.extra_deck_ids = []
        
        # Conectar o campo de busca ao método de pesquisa de cartas
        self.search_input.textChanged.connect(self.search_cards)

    def search_cards(self):
        """Buscar cartas por nome no banco de dados"""
        conie = sqlite3.connect("cards.cdb")
        query = self.search_input.text()
        if query:
            query_sql = """
            SELECT datas.id, texts.name 
            FROM datas 
            JOIN texts ON datas.id = texts.id 
            WHERE texts.name LIKE ? OR texts.desc LIKE ? LIMIT 50
            """
            cursor = conie.cursor()
            cursor.execute(query_sql, ('%' + query + '%', '%' + query + '%'))
            results = cursor.fetchall()        
            self.search_results.clear()            
            for card in results:
                self.search_results.addItem(f"{card[0]} - {card[1]}")
        else:
            self.search_results.clear()
        conie.close()
    
    def getEffect(self, cid):
        """Buscar efeito da carta pelo ID no banco de dados"""
        conie = sqlite3.connect("cards.cdb")
        query_sql = """
        SELECT texts.desc FROM datas 
        JOIN texts ON datas.id = texts.id 
        WHERE datas.id LIKE ? LIMIT 1
        """
        cursor = conie.cursor()
        cursor.execute(query_sql, ('%' + cid + '%',))  # Adicione a vírgula para criar uma tupla
        result = cursor.fetchone()  # Pega apenas um resultado  
        conie.close()
        # Retorna o efeito se encontrado, senão retorna uma string vazia
        return result[0] if result else ""

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
            # Carregar e redimensionar a nova imagem
            pixmap = QPixmap(image_path)
            #pixmap = pixmap.scaled(300, 350, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            # Atualizar a QLabel com a nova imagem
            self.image_label.setPixmap(pixmap)
        else:
            print("Imagem não encontrada:", image_path)
            pixmap = QPixmap("404.jpg")
            self.image_label.setPixmap(pixmap)
            
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

    def on_item_selected(self, item: QListWidgetItem):
        """Executa display_card_image ao selecionar um item da lista."""
        card_text = item.text()  # Exemplo: "109401 - Dark Dimension Soldier"
        card_id = card_text.split(" - ")[0]  # Pega apenas o ID antes do " - "
        self.display_card_image(card_id)
        efeito = self.getEffect(card_id)
        self.cardeff_label.setText(efeito)
