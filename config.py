import os
import logging
from datetime import datetime
from PyQt6.QtCore import QSettings

settings = QSettings("MeuApp", "Config")

# Valores padrão
edopro_path = settings.value("edopro_path", "C:/ProjectIgnis")
use_edopro = settings.value("use_edopro", False, type=bool)
banlist = settings.value("banlist", "nenhuma")
decks_path = os.path.join(edopro_path, "deck")
pics_path = os.path.join(edopro_path, "pics")

ABOUT_TEXT = "Deck Editor v1.0.5"
DB_PATH = "gehenna.db"
PICS_HD = "../pics_hd" 
LOG_DIR = "logs"

os.makedirs(pics_path, exist_ok=True)
os.makedirs(decks_path, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_and_print(message):
    """Exibe no console e salva no log"""
    print(message)
    logging.info(message)

def get_setting(key, default=None):
    return settings.value(key, default)

def update_config(key, value):
    settings.setValue(key, value)
    refresh_paths()

# Atualiza os caminhos base conforme `use_edopro`
def refresh_paths():
    global edopro_path, decks_path, pics_path
    use_edopro = get_setting("use_edopro", False) in [True, "true", "1"]
    base_path = get_setting("edopro_path", "C:/ProjectIgnis") if use_edopro else os.getcwd()

    edopro_path = base_path
    decks_path = os.path.join(base_path, "deck")
    pics_path = os.path.join(base_path, "pics")

refresh_paths()