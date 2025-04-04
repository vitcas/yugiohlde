import os
import logging
from datetime import datetime

DB_PATH = "gehenna.db"
EDOPRO_PATH = "../EDOPro.exe"
DECKS_PATH = "../deck"  
PICS_PATH = "../pics" 
PICS_HD = "../pics_hd" 
LOG_DIR = "logs"

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
