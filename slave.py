import os
import sqlite3
import hashlib
import requests
from config import DB_PATH, edopro_path, decks_path, pics_path, PICS_HD, log_and_print

def verifica_arquivo(caminho):
    """
    Verifica se o arquivo especificado existe.
    :param caminho: Caminho do arquivo a ser verificado.
    :return: True se o arquivo existir, False caso contrário.
    """
    return os.path.isfile(caminho)

def contar_arquivos(diretorio):
    """
    Conta quantos arquivos existem dentro de um diretório.
    :param diretorio: Caminho do diretório a ser verificado.
    :return: Número de arquivos dentro do diretório.
    """
    if os.path.isdir(diretorio):
        return len([f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))])
    return 0

def install_check():
    if verifica_arquivo(os.path.join(edopro_path, "EDOPro.exe")):
        print("EDOPro.exe found!")
        #num_arquivos = contar_arquivos(PICS_PATH)
        #print(f"O diretório '{pics_dir}' contém {num_arquivos} arquivos.")
    else:
        print("EDOPro.exe not found!")

def buscar_imagem(id_carta):
    nome_arquivo = f"{id_carta}.jpg"   
    caminho1 = os.path.join(pics_path, nome_arquivo)
    if os.path.isfile(caminho1):
        return True, caminho1
    caminho2 = os.path.join(PICS_HD, nome_arquivo)
    if os.path.isfile(caminho2):
        return True, caminho2
    return False, "Image not found."

def baixar_imagem(nome_arquivo):
    url = f"https://images.ygoprodeck.com/images/cards_small/{nome_arquivo}.jpg"
    caminho_arquivo = os.path.join(pics_path, f"{nome_arquivo}.jpg")    
    os.makedirs(pics_path, exist_ok=True)
    try:
        resposta = requests.get(url, stream=True)
        if resposta.status_code == 200:
            with open(caminho_arquivo, "wb") as f:
                for chunk in resposta.iter_content(1024):
                    f.write(chunk)
            print(f"Imagem baixada: {caminho_arquivo}")
        else:
            print("Erro ao baixar a imagem.")
    except Exception as e:
        print(f"Erro: {e}")

def gerar_hash():
    dado_aleatorio = os.urandom(32)  # Gera 32 bytes aleatórios
    hash_gerado = hashlib.sha256(dado_aleatorio).hexdigest()
    return hash_gerado[:7]

def save_to_file(file_path, content):
    if not os.path.exists('exported'):
        os.makedirs('exported')
    output_file_path = os.path.join('exported', file_path)
    with open(output_file_path, 'w') as file:
        file.write(content)
        
def load_decks():
    """Carregar os decks da pasta onde estão armazenados (no formato .ydk)"""
    if not os.path.exists(decks_path):
        print(f"Pasta de decks {decks_path} não encontrada!")
        return []        
    decks = [f for f in os.listdir(decks_path) if f.endswith(".ydk")]
    return decks

def read_deck_file(file_path):
    main, extra, side = [], [], []
    section = None
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line == "#main":
            section = "main"
        elif line == "#extra":
            section = "extra"
        elif line == "!side":
            section = "side"
        elif line.startswith("#") or not line:  # Ignora comentários e linhas em branco
            continue
        else:
            if section == "main":
                main.append(int(line))
            elif section == "extra":
                extra.append(int(line))
            elif section == "side":
                side.append(int(line))
    return main, extra, side

def test_database():
    if not os.path.exists(DB_PATH):
        log_and_print(f"Database {DB_PATH} not found!")
        return        
    conn = sqlite3.connect(DB_PATH)  # Conectando ao banco de dados
    log_and_print("Database loaded successfully!")
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM cards"  # Ajuste o nome da tabela, se necessário
    cursor.execute(query)
    card_count = cursor.fetchone()[0]
    log_and_print(f"{card_count} cards available.")
    conn.close()

def get_card_by_name(name):
    """Buscar cartas por nome no banco de dados"""
    conie = sqlite3.connect(DB_PATH)
    query_sql = """SELECT ydk_id, name FROM cards WHERE name LIKE ? OR effect LIKE ? LIMIT 50"""
    cursor = conie.cursor()
    cursor.execute(query_sql, ('%' + name + '%', '%' + name + '%'))
    results = cursor.fetchall() 
    conie.close()
    return results

def get_konamiIDs(main, extra):
    deckids = []
    deckids.append("#main")
    main_cards = get_card_details(main)
    for card in main_cards:
        deckids.append(f"{card['konami_id']},{card['name']},{card['type']}")    
    deckids.append("#extra")
    extra_cards = get_card_details(extra)
    for card in extra_cards:
        deckids.append(f"{card['konami_id']},{card['name']}") 
    deckids.append("!side")
    return deckids

def get_card_details(card_ids):
    if not isinstance(card_ids, list):  # Se for um único ID, transforma em lista
        card_ids = [card_ids]
    opencon = sqlite3.connect(DB_PATH) 
    cursor = opencon.cursor()
    card_details = []  
    query = """SELECT * FROM cards WHERE ydk_id = ?"""
    for card_id in card_ids:        
        cursor.execute(query, (card_id,))
        result = cursor.fetchone()      
        if result:
            card_details.append({
                'konami_id': result[0],
                'ydk_id': result[1],
                'name': result[2],
                'type': result[3],
                'description': result[4],
                'attribute': result[5],
                'race': result[6],
                'level': result[7],
                'atk': result[8],
                'def': result[9],
                'rarity': result[10]
            })  
    opencon.close()
    if len(card_details) == 1 and not isinstance(card_ids, list):  
        return card_details[0]  # Retorna um dicionário se só houver um item
    return card_details    
