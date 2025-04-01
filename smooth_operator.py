import os
import sqlite3
import hashlib
import requests

edopro = "../EDOPro.exe"
db_path = "neodados.db"  # Caminho do banco de dados .cdb
decks_dir = "../deck"  # Caminho onde os decks .ydk estão armazenados
pics_dir = "../pics"  # Caminho onde as imagens das cartas estão armazenadas
pics_hd = "../pics_hd" 

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
    if verifica_arquivo(edopro):
        print("Arquivo EDOPro.exe encontrado!")
        num_arquivos = contar_arquivos(pics_dir)
        print(f"O diretório '{pics_dir}' contém {num_arquivos} arquivos.")
    else:
        print("Arquivo EDOPro.exe não encontrado!")

def buscar_imagem(id_carta):
    nome_arquivo = f"{id_carta}.jpg"   
    caminho1 = os.path.join(pics_dir, nome_arquivo)
    if os.path.isfile(caminho1):
        return True, caminho1
    caminho2 = os.path.join(pics_hd, nome_arquivo)
    if os.path.isfile(caminho2):
        return True, caminho2
    return False, "Imagem não encontrada."

def baixar_imagem(nome_arquivo):
    url = f"https://images.ygoprodeck.com/images/cards_small/{nome_arquivo}.jpg"
    caminho_arquivo = os.path.join(pics_dir, f"{nome_arquivo}.jpg")    
    os.makedirs(pics_dir, exist_ok=True)
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
    if not os.path.exists(decks_dir):
        print(f"Pasta de decks {decks_dir} não encontrada!")
        return []        
    decks = [f for f in os.listdir(decks_dir) if f.endswith(".ydk")]
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
    if not os.path.exists(db_path):
        print(f"Banco de dados {db_path} não encontrado!")
        return        
    conn = sqlite3.connect(db_path)  # Conectando ao banco de dados
    print("Banco de dados carregado com sucesso!")
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM cartas_completas"  # Ajuste o nome da tabela, se necessário
    cursor.execute(query)
    card_count = cursor.fetchone()[0]
    print(f"{card_count} cartas disponíveis.")
    conn.close()

def get_card_by_name(name):
    """Buscar cartas por nome no banco de dados"""
    conie = sqlite3.connect(db_path)
    query_sql = """SELECT cac.ydk_id, cac.name FROM cartas_completas AS cac 
    WHERE cac.name LIKE ? OR cac.effectText LIKE ? LIMIT 50"""
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
    opencon = sqlite3.connect(db_path) 
    cursor = opencon.cursor()
    card_details = []  
    query = """SELECT cartas.ydk_id, cartas.name, cartas.effectText, cartas.type, cartas.knami_id 
        FROM cartas_completas as cartas WHERE cartas.ydk_id = ?"""
    for card_id in card_ids:        
        cursor.execute(query, (card_id,))
        result = cursor.fetchone()      
        if result:
            card_details.append({
                'ydk_id': result[0],
                'name': result[1],
                'description': result[2],
                'type': result[3],
                'konami_id': result[4]
            })  
    opencon.close()
    if len(card_details) == 1 and not isinstance(card_ids, list):  
        return card_details[0]  # Retorna um dicionário se só houver um item
    return card_details    
