import os
import sqlite3

db_path = "cards.cdb"  # Caminho do banco de dados .cdb
decks_dir = "../deck"  # Caminho onde os decks .ydk estão armazenados
pics_dir = "../pics"  # Caminho onde as imagens das cartas estão armazenadas

def test_database():
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
    conn.close()

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
    opencon = sqlite3.connect(db_path) 
    cursor = opencon.cursor()
    # Lista para armazenar os resultados das cartas
    card_details = []  
    # Consultar detalhes de cada carta no banco de dados
    for card_id in card_ids:
        # Query SQL com JOIN entre as tabelas datas e texts para obter os detalhes da carta
        query = """SELECT datas.id, texts.name, texts.desc, datas.type  
        FROM datas JOIN texts ON datas.id = texts.id WHERE datas.id = ?"""
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
    opencon.close()
    return card_details    

def whattype(numero: int) -> str:
    color1 = "black"
    color2 = "white"
    desc = "ukw"
    match numero:
        case 17:
            desc = "mon-nor"
            color1 = "#c7c1ad"
            color2 = "black"
        case 33:
            desc = "mon-eff"
            color1 = "#bfa78f"
            color2 = "black"
        case 4129:
            desc = "mon-tun"
            color1 = "#bfa78f"
            color2 = "black"
        case 161:
            desc = "mon-rit"
            color1 = "black"
            color2 = "black"
        case 16777249:
            desc = "pendulum"
            color1 = "black"
            color2 = "black"
        case 2:
            desc = "spell"
            color1 = "#8fbfba"
            color2 = "black"
        case 65538:
            desc = "quic-spell"
            color1 = "#8fbfba"
            color2 = "black"
        case 131074:
            desc = "cont-spell"
            color1 = "#8fbfba"
            color2 = "black"
        case 524290:
            desc = "field"
            color1 = "#8fbfba"
            color2 = "black"
        case 4:
            desc = "trap"
            color1 = "#bf8fb4"
            color2 = "black"
        case 1048580:
            desc = "coun-trap"
            color1 = "#bf8fb4"
            color2 = "black"
        case 131076:
            desc = "cont-trap"
            color1 = "#bf8fb4"
            color2 = "black"
        case 97:
            desc = "fusion"    
            color1 = "#4d3478"  
            color2 = "white"
        case 8225:
            desc = "synchro"
            color1 = "white"
            color2 = "black"
        case 12321:
            desc = "synchro"
            color1 = "white"
            color2 = "black"
        case 8388641:
            desc = "xyz"
            color1 = "black"
            color2 = "white"
        case 67108897:
            desc = "link"  
            color1 = "#0341fc"   
            color2 = "white" 
        case _:
            print(numero)
    return color1, color2, desc
