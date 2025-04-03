import sys
import os
import time
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QGridLayout, QScrollArea, QListWidgetItem, QMenuBar, QMainWindow, QMessageBox, QSizePolicy

# meus scripts
from new_deck import CreateDeckDialog
from settings import SettingsDialog
from smooth_operator import load_decks, install_check, read_deck_file, get_card_details, test_database, save_to_file, get_konamiIDs, gerar_hash, buscar_imagem, baixar_imagem

main_deck = []
extra_deck = []
side_deck = []  

class DeckEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        # Inicializa a interface
        self.setWindowTitle("Deck Editor")
        self.setGeometry(100, 100, 840, 600)

        # Criando barra de menus
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Menu")

        # Criando ação para abrir as configurações
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        settings_menu.addAction(about_action)
        settings_menu.addSeparator()
        settings_menu.addAction(QAction("Quit", self, triggered=self.close))

        # Criando widget central para conter o layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        self.main_layout = QHBoxLayout(central_widget)

        # Layout da parte esquerda
        self.left_layout = QVBoxLayout()
        self.deck_list = QListWidget()
        self.left_layout.addWidget(QLabel("Pick Deck:"))
        self.deck_list.currentItemChanged.connect(self.on_item_selected)
        self.left_layout.addWidget(self.deck_list)

        # Botões
        self.load_deck_button = QPushButton("Edit Deck")
        self.load_deck_button.clicked.connect(self.open_edit_deck_dialog)
        self.left_layout.addWidget(self.load_deck_button)

        self.export_deck_button = QPushButton("Export Deck")
        self.export_deck_button.clicked.connect(self.export_deck)
        self.left_layout.addWidget(self.export_deck_button)

        self.create_deck_button = QPushButton("New Deck")
        self.create_deck_button.clicked.connect(self.open_create_deck_dialog)
        self.left_layout.addWidget(self.create_deck_button)

        # Área de detalhes da carta
        self.card_details_label = QLabel("Content:")
        self.left_layout.addWidget(self.card_details_label)

        # Lista de informações das cartas
        self.card_info_list = QListWidget()
        self.left_layout.addWidget(self.card_info_list)

        # Adicionar a parte esquerda ao layout principal
        self.main_layout.addLayout(self.left_layout)

        # Layout da parte direita
        self.right_layout = QVBoxLayout()
        self.card_images_label = QLabel("Preview:")
        self.right_layout.addWidget(self.card_images_label)

        # Scroll area para exibir imagens
        self.card_images_area = QScrollArea(self)
        self.card_images_area.setWidgetResizable(True)
        # Criar a grade inicial
        self.create_grid()  
        

        # Adicionar área de imagens ao layout da direita
        self.right_layout.addWidget(self.card_images_area)

        # Adicionar a parte direita ao layout principal
        self.main_layout.addLayout(self.right_layout)

        # Carregar o banco de dados e os decks
        self.decks_dir = "../deck"  # Caminho onde os decks .ydk estão armazenados
        self.pics_dir = "../pics"  # Caminho onde as imagens das cartas estão armazenadas
        test_database()
        install_check()
        self.load_decks()   

    def load_decks(self):
        """Carregar e exibir os decks"""
        decks = load_decks()
        self.deck_list.addItems(decks)

    def on_item_selected(self):
        global main_deck, extra_deck, side_deck
        selected_deck = self.deck_list.currentItem().text()
        file_pathx = os.path.join(self.decks_dir, selected_deck)
        main_deck, extra_deck, side_deck = read_deck_file(file_pathx)
        self.card_info_list.clear()  # Limpar a lista de cartas
        self.create_grid() # Limpar as imagens das cartas
        self.show_decklist("Main Deck", main_deck)
        self.show_decklist("Extra Deck", extra_deck)
        self.card_images_widget.adjustSize()

    def show_decklist(self, deck_name, card_ids):
        card_details = get_card_details(card_ids)
        self.card_info_list.addItem(f"{deck_name} - {len(card_details)} cartas:")
        for card in card_details:
            texto = f"[{card['type'][0]}] {card['name']}"
            item = QListWidgetItem(texto)
            self.card_info_list.addItem(item)         
            self.display_card_image(card['ydk_id'])          
    
    def create_grid(self):
        """Cria uma nova grade do zero."""
        # Remover grade anterior, se existir
        if hasattr(self, 'card_images_widget'):
            self.card_images_widget.deleteLater()

        # Criar nova grade
        self.card_images_widget = QWidget()
        self.card_images_grid = QGridLayout()
        self.card_images_grid.setSpacing(3)
        self.card_images_grid.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.card_images_widget.setLayout(self.card_images_grid)
        self.card_images_area.setWidget(self.card_images_widget)
        self.card_images_area.setFixedWidth(600) 
        # Resetar contador de imagens
        self.image_count = 0

    def display_card_image(self, card_id):
        """Exibir a imagem da carta com base no seu ID na grade"""
        image_path = os.path.join(self.pics_dir, f"{card_id}.jpg")
        encontrado, image_path = buscar_imagem(card_id)
        if encontrado:
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(54, 80, Qt.AspectRatioMode.IgnoreAspectRatio)
            #pixmap.fill(Qt.GlobalColor.red)   Placeholder vermelho para teste
            label = QLabel()
            label.setPixmap(pixmap)
            max_columns = 10
            row = self.image_count // max_columns
            col = self.image_count % max_columns
            self.card_images_grid.addWidget(label, row, col)
            self.image_count += 1  # Atualizar contador            
        else:
            print(image_path)
            baixar_imagem(card_id)
            time.sleep(0.2)        
        
    def open_create_deck_dialog(self, vector1=None, vector2=None):
        self.create_deck_dialog = CreateDeckDialog(self, vector1, vector2)
        self.create_deck_dialog.exec()
    
    def open_edit_deck_dialog(self, vector1=None, vector2=None):
        global main_deck
        global extra_deck
        vector1 = main_deck
        vector2 = extra_deck
        self.create_deck_dialog = CreateDeckDialog(self, vector1, vector2)
        self.create_deck_dialog.exec()

    def export_deck(self):
        global main_deck, extra_deck
        #asyncio.run(ydk2konami(main_deck, extra_deck, side_deck))
        kids = get_konamiIDs(main_deck, extra_deck)
        finame = f"deck_output_{gerar_hash()}.txt"
        save_to_file(finame, "\n".join(kids))
        print(f"Deck exportado em {finame}")
    
    def open_settings(self):
        settings_dialog = SettingsDialog()
        settings_dialog.exec()  # Exibe como janela modal

    def show_about(self):
        QMessageBox.information(self, "Sobre", "Deck Editor v1.0.1")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #app.setStyle("Fusion") deactivate
    window = DeckEditor()
    window.show()
    sys.exit(app.exec())
