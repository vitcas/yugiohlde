import aiohttp
import os
import hashlib

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

async def ydk2konami(main, extra, side):
    fulldeck = set(main + extra + side)
    parameter = ",".join(map(str, fulldeck))

    async with aiohttp.ClientSession() as session:
        # Requisição para buscar as cartas
        async with session.get(f'https://db.ygoprodeck.com/api/v7/cardinfo.php?utm_source=storm-access&misc=yes&id={parameter}') as response:
            payload = await response.json()

        cards = {card['id']: card for card in payload['data']}     
        deck_konami_ids = {
            'monster': {},
            'spell': {},
            'trap': {},
            'extra': {},
            'side': {}
        }
        deckids = []

        # Função para buscar o konami_id
        async def get_konami_id(name):
            async with session.post("https://www.db.yugioh-card.com/yugiohdb/member_deck_card_search.action", data={'srclang': 'en', 'keyword': name}, headers={"X-Requested-With": "XMLHttpRequest"}) as response:
                data = await response.json()
                if data.get('result') and data['list']:
                    return data['list'][0]['card_id']   
                return None

        deckids.append("#main")    
        for password in main:
            card = cards.get(password)
            name = card['name']
            type_ = card['type']
            konami_id = card['misc_info'][0].get('konami_id') if card['misc_info'] else None
            if not konami_id:
                konami_id = await get_konami_id(name)
            if type_ == "Spell Card":
                deck_konami_ids['spell'][name] = konami_id
            elif type_ == "Trap Card":
                deck_konami_ids['trap'][name] = konami_id
            else:
                deck_konami_ids['monster'][name] = konami_id
            deckids.append(f"{konami_id},{name},{type_}")

        deckids.append("#extra")
        for password in extra:
            card = cards.get(password)
            name = card['name']
            konami_id = card['misc_info'][0].get('konami_id') if card['misc_info'] else None
            deck_konami_ids['extra'][name] = konami_id
            deckids.append(f"{konami_id},{name}")

        deckids.append("!side")
        for password in side:
            card = cards.get(password)
            name = card['name']
            konami_id = card['misc_info'][0].get('konami_id') if card['misc_info'] else None
            deck_konami_ids['side'][name] = konami_id
            deckids.append(f"{konami_id},{name}")

        finame = f"deck_output_{gerar_hash()}.txt"
        save_to_file(finame, "\n".join(deckids))
        print(f"Deck exportado em {finame}")
