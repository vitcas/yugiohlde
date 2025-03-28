import os
import sqlite3

db_path = "cards.cdb"  # Caminho do banco de dados .cdb
decks_dir = "../deck"  # Caminho onde os decks .ydk estão armazenados
pics_dir = "../pics"  # Caminho onde as imagens das cartas estão armazenadas
conn = None

def load_database():
    """Conectar ao banco de dados SQLite (.cdb)"""
    global conn
    if not os.path.exists(db_path):
        print(f"Banco de dados {db_path} não encontrado!")
        return
        
    conn = sqlite3.connect(db_path)  # Conectando ao banco de dados
    print("Banco de dados carregado com sucesso!")
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM datas"  # Ajuste o nome da tabela, se necessário
    cursor.execute(query)
    card_count = cursor.fetchone()[0]
    print(f"{card_count} cartas disponíveis.")

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

def get_card_details(card_ids):
    # Conectar ao banco de dados SQLite
    global conn
    cursor = conn.cursor()
    
    # Lista para armazenar os resultados das cartas
    card_details = []
    
    # Consultar detalhes de cada carta no banco de dados
    for card_id in card_ids:
        # Query SQL com JOIN entre as tabelas datas e texts para obter os detalhes da carta
        query = """
        SELECT datas.id, texts.name, texts.desc, datas.type  
        FROM datas JOIN texts ON datas.id = texts.id WHERE datas.id = ?
        """
        cursor.execute(query, (card_id,))
        result = cursor.fetchone()
        
        # Se a carta for encontrada, adicione os detalhes à lista
        if result:
            card_details.append({
                'id': result[0],
                'name': result[1],
                'description': result[2],
                'type': result[3]
            })  
    return card_details

def showcards(deck, sauce):
    card_details = get_card_details_from_db(sauce)
    print(deck)
    for card in card_details:
        print(f"{card['id']} - {card['name']}")

def whattype(numero: int) -> str:
    match numero:
        case 17:
            return "mon-nor"
        case 33:
            return "mon-eff"
        case 4129:
            return "mon-tun"
        case 161:
            return "mon-rit"
        case 16777249:
            return "pendulum"
        case 2:
            return "spell"
        case 65538:
            return "quic-spell"
        case 131074:
            return "cont-spell"
        case 4:
            return "trap"
        case 1048580:
            return "coun-trap"
        case 131076:
            return "cont-trap"
        case 97:
            return "fusion"      
        case 8225:
            return "synchro"
        case 8388641:
            return "xyz"
        case 67108897:
            return "link"      
        case _:
            return numero
