import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, QPushButton, QInputDialog, QListWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from slave import get_card_details, get_card_by_name, buscar_imagem, baixar_imagem, get_card_view_by_id
from adv_search import AdvancedSearch

main_count = 0
extra_count = 0

class CreateDeckDialog(QDialog):
    def __init__(self, parent=None, vector1=None, vector2=None):
        super().__init__(parent)
        self.vector1 = vector1
        self.vector2 = vector2
        self.setWindowTitle("New Deck")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)  # Bloqueia o redimensionamento

        # Layout principal (horizontal)
        self.main_layout = QHBoxLayout()
        # Layout esquerdo (Lista de cartas do deck)
        self.left_layout = QVBoxLayout()
        # main deck
        self.deck_list_label = QLabel("Main Deck - 0 cards")
        self.left_layout.addWidget(self.deck_list_label)
        self.deck_card_list = QListWidget()
        self.deck_card_list.currentItemChanged.connect(self.on_item_selected)
        self.left_layout.addWidget(self.deck_card_list)
        # extra deck
        self.deck_list_label2 = QLabel("Extra Deck - 0 cards")
        self.left_layout.addWidget(self.deck_list_label2)
        self.deck_card_list_extra = QListWidget()
        self.deck_card_list_extra.currentItemChanged.connect(self.on_item_selected)
        self.deck_card_list_extra.setFixedHeight(150) 
        self.left_layout.addWidget(self.deck_card_list_extra)      
        # Botão para remover carta do deck
        self.remove_card_button = QPushButton("Remove card", self)
        self.remove_card_button.clicked.connect(self.remove_card_from_deck)
        self.left_layout.addWidget(self.remove_card_button)

        self.main_layout.addLayout(self.left_layout)

        # Layout central (formulário de criação de deck)
        self.center_layout = QVBoxLayout()
        # campo de busca
        self.search_label = QLabel("Search card by text:")
        self.center_layout.addWidget(self.search_label)        
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Some card text...")
        self.center_layout.addWidget(self.search_input)
        # botao busca avançada
        self.advanced_search_button = QPushButton("Advanced Search")
        self.advanced_search_button.clicked.connect(self.open_advanced_search)
        self.center_layout.addWidget(self.advanced_search_button)
        
        self.search_results = QListWidget(self)
        self.search_results.currentItemChanged.connect(self.on_item_selected)
        self.center_layout.addWidget(self.search_results)
        
        self.add_card_button = QPushButton("Add to deck", self)
        self.add_card_button.clicked.connect(self.add_card_to_deck)
        self.center_layout.addWidget(self.add_card_button)
        
        self.save_deck_button = QPushButton("Save deck", self)
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
        pixmap = QPixmap("assets/dummy.jpeg")  # Substitua pelo caminho da sua imagem
        #pixmap = pixmap.scaled(300, 350, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(pixmap)
        self.right_layout.addWidget(self.image_label)

        #texto do efeito
        self.cardeff_label = QLabel("Card text")
        self.cardeff_label.setFixedWidth(250) 
        self.cardeff_label.setWordWrap(True)  # Habilita a quebra de linha
        self.right_layout.addWidget(self.cardeff_label)

        self.main_layout.addLayout(self.right_layout)
        self.setLayout(self.main_layout)

        # Listas para armazenar as cartas do deck
        self.main_deck_ids = []
        self.extra_deck_ids = []
        self.witchlist = 1
        
        if self.has_both_vectors():
            self.main_deck_ids = self.vector1
            self.extra_deck_ids = self.vector2
            self.show_decklist(self.deck_card_list, self.main_deck_ids)
            self.show_decklist(self.deck_card_list_extra, self.extra_deck_ids)
            self.fix_counters(self.main_deck_ids, self.extra_deck_ids)
            self.update__deck_label()
        # Conectar o campo de busca ao método de pesquisa de cartas
        self.search_input.textChanged.connect(self.search_cards)

        self.center_on_parent()
    
    def center_on_parent(self):
        if self.parent():
            parent_geom = self.parent().frameGeometry()
            dialog_geom = self.frameGeometry()
            center_point = parent_geom.center()
            dialog_geom.moveCenter(center_point)
            self.move(dialog_geom.topLeft())

    def has_both_vectors(self):
        return self.vector1 is not None and self.vector2 is not None
    
    def update__deck_label(self):
        self.deck_list_label.setText(f"Main Deck - {len(self.main_deck_ids)} cards")
        self.deck_list_label2.setText(f"Extra Deck - {len(self.extra_deck_ids)} cards")
    
    def show_decklist(self, qlist, card_ids):
        card_details = get_card_details(card_ids)
        for card in card_details:
            texto = f"{card['ydk_id']} - {card['name']}"
            item = QListWidgetItem(texto)
            qlist.addItem(item)    

    def fix_counters(self, mids, eids):
        global main_count
        global extra_count   
        main_count = len(mids)
        extra_count = len(eids)

    def search_cards(self):     
        query = self.search_input.text()
        if query:
            results = get_card_by_name(query)       
            self.search_results.clear()            
            for card in results:
                self.search_results.addItem(f"{card[0]} - {card[1]}")
        else:
            self.search_results.clear()

    def open_advanced_search(self):
        dialog = AdvancedSearch()
        if dialog.exec():
            results = dialog.results
            self.search_results.clear()
            for card in results:
                self.search_results.addItem(f"{card[1]} - {card[2]}")
        else:
            print("Search cancelled")
          
    def getEffect(self, cid):
        card =  get_card_details(cid)
        if card:
            return card[0]['description']  
        else:
            return "erro"

    def on_item_selected(self, item: QListWidgetItem):
        """Executa display_card_image ao selecionar um item da lista."""
        if item:
            card_text = item.text()  # Exemplo: "109401 - Dark Dimension Soldier"
            card_id = card_text.split(" - ")[0]  # Pega apenas o ID antes do " - "
            self.display_card_image(card_id)
            efeito = self.getEffect(card_id)
            self.cardeff_label.setText(efeito)
            if int(card_id) in self.main_deck_ids:
                self.witchlist = 1
            else:
                self.witchlist = 2

    def display_card_image(self, card_id):
        """Exibir a imagem da carta com base no seu ID na grade"""
        encontrado, image_path = buscar_imagem(card_id)
        if encontrado:
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(177, 254, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            # Atualizar a QLabel com a nova imagem
            self.image_label.setPixmap(pixmap)
        else:
            print(image_path)
            pixmap = QPixmap("assets/404.jpg")
            self.image_label.setPixmap(pixmap)  
            baixar_imagem(card_id)         

    def add_card_to_deck(self):
        """Adicionar carta selecionada ao deck"""
        selected_item = self.search_results.currentItem()
        if selected_item:
            card_id = int(selected_item.text().split(" - ")[0])
            card = get_card_view_by_id(card_id)
            if card["is_extra"] < 1:
                if self.main_deck_ids.count(card_id) >= 3:  # Limite de 3 cópias
                    print("3 copies limit!")
                    return
                if len(self.main_deck_ids) < 60:  # Verifica limite do deck
                    self.main_deck_ids.append(card_id)
                else:
                    print("Main Deck limit is 60!")
                    return
                self.deck_card_list.addItem(selected_item.text())
            else:  # Extra Deck
                if self.extra_deck_ids.count(card_id) >= 3:  # Limite de 3 cópias
                    print("3 copies limit!")
                    return
                if len(self.extra_deck_ids) < 15:  # Verifica limite do Extra Deck
                    self.extra_deck_ids.append(card_id)
                else:
                    print("Extra Deck limit is 15!")
                    return
                self.deck_card_list_extra.addItem(selected_item.text())
            # Adicionar carta à lista gráfica          
            self.display_card_image(card_id)
            self.update__deck_label()
            
    def remove_card_from_deck(self):
        """Remover carta selecionada do deck"""
        if self.witchlist < 2:         
            selected_item = self.deck_card_list.currentItem()
            if selected_item:
                card_text = selected_item.text()
                card_id = int(card_text.split(" - ")[0])
                if card_id in self.main_deck_ids:
                    self.main_deck_ids.remove(card_id)        
                self.deck_card_list.takeItem(self.deck_card_list.row(selected_item))
        else:
            selected_item = self.deck_card_list_extra.currentItem()
            if selected_item:
                card_text = selected_item.text()
                card_id = int(card_text.split(" - ")[0])
                if card_id in self.extra_deck_ids:
                    self.extra_deck_ids.remove(card_id)        
                self.deck_card_list_extra.takeItem(self.deck_card_list_extra.row(selected_item))
        self.update__deck_label()
            
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

