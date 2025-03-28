import sys
import os
import asyncio
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QComboBox, QLineEdit, QDialog, QFormLayout, QInputDialog, QGridLayout, QScrollArea, QFileDialog

# meus scripts
from create_deck_dialog import CreateDeckDialog
from smooth_operator import load_decks, read_deck_file, get_card_details, load_database, whattype
from konamify import ydk2konami

main_deck = []
extra_deck = []
side_deck = []

class DeckEditor(QWidget):
    def __init__(self):
        super().__init__()
        # Inicializa a interface
        self.setWindowTitle("Deck Editor")
        self.setGeometry(100, 100, 800, 600)
        # Layout principal
        self.main_layout = QHBoxLayout()
        # Layout da parte esquerda
        self.left_layout = QVBoxLayout()
        # Lista de decks disponíveis
        self.deck_list = QListWidget()
        self.left_layout.addWidget(QLabel("Pick Deck:"))
        self.left_layout.addWidget(self.deck_list)
        # Botão para carregar o deck escolhido
        self.load_deck_button = QPushButton("Load Deck")
        self.load_deck_button.clicked.connect(self.load_selected_deck)
        self.left_layout.addWidget(self.load_deck_button)
        # Botão para exportar deck
        self.export_deck_button = QPushButton("Export Deck")
        self.export_deck_button.clicked.connect(self.export_deck)
        self.left_layout.addWidget(self.export_deck_button)
        # Botão para criar um novo deck
        self.create_deck_button = QPushButton("New Deck")
        self.create_deck_button.clicked.connect(self.open_create_deck_dialog)
        self.left_layout.addWidget(self.create_deck_button)
        # Área de detalhes da carta
        self.card_details_label = QLabel("Content:")
        self.left_layout.addWidget(self.card_details_label)
        # Mostrar informações das cartas
        self.card_info_list = QListWidget()
        self.left_layout.addWidget(self.card_info_list)
        # Adicionar a parte esquerda ao layout principal
        self.main_layout.addLayout(self.left_layout)
        # Layout da parte direita para as imagens das cartas
        self.right_layout = QVBoxLayout()
        # Rótulo para a área de imagens
        self.card_images_label = QLabel("Preview:")
        self.right_layout.addWidget(self.card_images_label)
        # Scroll area para exibir as imagens em uma grade
        self.card_images_area = QScrollArea(self)
        self.card_images_area.setWidgetResizable(True)
        # Layout para as imagens das cartas
        self.card_images_grid = QGridLayout()
        self.card_images_widget = QWidget()
        self.card_images_widget.setLayout(self.card_images_grid)
        self.card_images_area.setWidget(self.card_images_widget)
        # Adicionar a área de imagens ao layout da parte direita
        self.right_layout.addWidget(self.card_images_area)
        # Adicionar a parte direita ao layout principal
        self.main_layout.addLayout(self.right_layout, stretch=3)  # pdireita para 60% da tela
        # Definir layout principal
        self.setLayout(self.main_layout)
        # Carregar o banco de dados e os decks
        self.decks_dir = "../deck"  # Caminho onde os decks .ydk estão armazenados
        self.pics_dir = "../pics"  # Caminho onde as imagens das cartas estão armazenadas
        self.load_database()
        self.load_decks()

    def load_database(self):
        """Carregar o banco de dados"""
        load_database()

    def load_decks(self):
        """Carregar e exibir os decks"""
        decks = load_decks()
        self.deck_list.addItems(decks)

    def load_selected_deck(self):
        global main_deck, extra_deck, side_deck
        selected_deck = self.deck_list.currentItem().text()
        file_pathx = os.path.join(self.decks_dir, selected_deck)
        main_deck, extra_deck, side_deck = read_deck_file(file_pathx)
        # Limpar a lista de cartas antes de adicionar novas
        self.card_info_list.clear()
        # Limpar as imagens das cartas antes de adicionar novas
        for i in range(self.card_images_grid.count()):
            widget = self.card_images_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()     
        self.show_decklist("Main Deck", main_deck)
        self.show_decklist("Extra Deck", extra_deck)

    def show_decklist(self, deck_name, card_ids):
        card_details = get_card_details(card_ids)
        self.card_info_list.addItem(f"{deck_name} - {len(card_details)} cartas:")
        for card in card_details:
            self.card_info_list.addItem(f"[{whattype(card['type'])}] {card['name']}")           
            # Carregar e exibir a imagem da carta
            self.display_card_image(card['id'])

    def display_card_image(self, card_id):
        """Exibir a imagem da carta com base no seu ID na grade"""
        image_path = os.path.join(self.pics_dir, f"{card_id}.jpg")
        
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            
            # Ajuste do tamanho da imagem para ficar pequena e adequada
            pixmap = pixmap.scaled(60, 80, Qt.AspectRatioMode.KeepAspectRatio)  # Ajuste o tamanho conforme necessário
    
            # Criar o QLabel para exibir a imagem
            label = QLabel()
            label.setPixmap(pixmap)
    
            # Calcular o número de colunas para manter as imagens em uma grade (4 colunas, por exemplo)
            max_columns = 8
    
            # Calcular a posição correta da linha e coluna para manter as imagens organizadas
            row = self.card_images_grid.count() // max_columns  # Número da linha
            col = self.card_images_grid.count() % max_columns  # Número da coluna
    
            # Adicionar a imagem no layout
            self.card_images_grid.addWidget(label, row, col)
    
            # Redefinir o layout para ajustar melhor as imagens
            self.card_images_grid.setSpacing(3)  # Definindo o espaçamento entre as imagens
            self.card_images_grid.setColumnStretch(col, 1)  # Ajusta o espaço das colunas
            self.card_images_grid.setRowStretch(row, 1)  # Ajusta o espaço das linhas
        
    def open_create_deck_dialog(self):
        self.create_deck_dialog = CreateDeckDialog(self)
        self.create_deck_dialog.exec()

    def export_deck(self):
        global main_deck, extra_deck, side_deck
        asyncio.run(ydk2konami(main_deck, extra_deck, side_deck))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DeckEditor()
    window.show()
    sys.exit(app.exec())
