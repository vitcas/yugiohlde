import sys
import os
import time
from collections import Counter
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QAction, QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QGridLayout, QScrollArea, QListWidgetItem, QMainWindow, QMessageBox, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem

# meus scripts
from config import log_and_print, DECKS_PATH, PICS_PATH
from new_deck import CreateDeckDialog
from settings import SettingsDialog
from slave import load_decks, install_check, read_deck_file, get_card_details, test_database, save_to_file, get_konamiIDs, gerar_hash, buscar_imagem, baixar_imagem

main_deck = []
extra_deck = []
side_deck = []  

class DeckEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        # Inicializa a interface
        self.setWindowTitle("Deck Editor")
        self.setGeometry(100, 100, 1000, 600)
        # Criando barra de menus
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Menu")
        # Criando ação para abrir as configurações
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)
        update_action = QAction("Check for updates...", self)
        settings_menu.addAction(update_action)
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
        self.deck_list.setFixedWidth(160)
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

        # Adicionar a parte esquerda ao layout principal
        self.main_layout.addLayout(self.left_layout)

        # Layout centro
        self.center_layout = QVBoxLayout()
        self.card_images_label = QLabel("Preview:")
        self.center_layout.addWidget(self.card_images_label)
        # Scroll area para exibir imagens
        self.card_images_area = QScrollArea(self)
        self.card_images_area.setWidgetResizable(True)
        # Criar a grade inicial
        self.create_grid()         
        # Adicionar área de imagens ao layout da direita
        self.center_layout.addWidget(self.card_images_area)
        
        self.extra_area = QScrollArea(self)
        self.extra_area.setFixedHeight(100)
        self.extra_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.extra_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.center_layout.addWidget(self.extra_area)

        self.main_layout.addLayout(self.center_layout)

        #layout direita
        self.right_layout = QVBoxLayout()
        # Área de detalhes da carta
        self.card_details_label = QLabel("Content:")
        self.right_layout.addWidget(self.card_details_label)

        # Lista de informações das cartas
        self.card_info_list = QListWidget()
        self.right_layout.addWidget(self.card_info_list)
        self.main_layout.addLayout(self.right_layout)

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
        file_pathx = os.path.join(DECKS_PATH, selected_deck)
        main_deck, extra_deck, side_deck = read_deck_file(file_pathx)
        self.card_info_list.clear()  # Limpar a lista de cartas
        self.create_grid() # Limpar as imagens das cartas
        self.show_decklist("Main Deck", main_deck)
        self.show_decklist("Extra Deck", extra_deck)     
        self.extra_stack(extra_deck)
        self.card_images_widget.adjustSize()

    def get_rarity_icon(self, rarity):
        path_map = {
            "UR": "assets/rarity_ur.webp",
            "SR": "assets/rarity_sr.webp",
            "R":  "assets/rarity_r.webp",
            "N":  "assets/rarity_n.webp"
        }
        path = path_map.get(rarity.upper())
        return QIcon(path) if path else QIcon()

    def show_decklist(self, deck_name, card_ids):
        card_count = Counter(card_ids)
        card_details = get_card_details(card_ids)
        self.card_info_list.addItem(f"---------- {deck_name} ({len(card_details)}) -----------")
        for card in card_details:
            ydk_id = int(card['ydk_id'])
            if ydk_id in card_count:
                qtd = card_count[ydk_id]
                icon = self.get_rarity_icon(card['rarity'])
                texto = f"{card['name']} x{qtd}"
                item = QListWidgetItem(icon, texto)
                self.card_info_list.addItem(item)
                # Mostrar imagem repetida conforme a quantidade
                if deck_name == "Main Deck":
                    for _ in range(qtd):
                        self.display_card_image(card['ydk_id'])
                del card_count[ydk_id]  # impede duplicação do texto                   
    
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

    def extra_stack(self, extra_deck):             
        view = QGraphicsView()
        scene = QGraphicsScene()
        view.setScene(scene)
        num_cartas = len(extra_deck)
        largura_max = 600
        offset = 38
        for i in range(num_cartas):
            sauce = os.path.join(PICS_PATH, f"{extra_deck[i]}.jpg")
            pixmap = QPixmap(sauce).scaledToHeight(80, Qt.TransformationMode.SmoothTransformation)
            item = QGraphicsPixmapItem(pixmap)
            item.setZValue(i)
            item.setPos(i * offset, 0)
            scene.addItem(item)
        scene.setSceneRect(0, 0, largura_max, 80)
        view.setFixedSize(largura_max, 80)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.extra_area.setWidget(view)

    def display_card_image(self, card_id):
        """Exibir a imagem da carta com base no seu ID na grade"""
        image_path = os.path.join(PICS_PATH, f"{card_id}.jpg")
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
            log_and_print(image_path)
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
        log_and_print(f"Deck exportado em {finame}")
    
    def open_settings(self):
        settings_dialog = SettingsDialog()
        settings_dialog.exec()  # Exibe como janela modal

    def show_about(self):
        QMessageBox.information(self, "Sobre", "Deck Editor v1.0.1")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion") #deactivate
    window = DeckEditor()
    window.show()
    sys.exit(app.exec())
