import random
import sqlite3
import os

from config import DB_PATH, decks_path
from slave import gerar_hash

def get_cards_by_category():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ydk_id, name FROM cards_view WHERE type_name LIKE '%Monster%' AND is_extra = 0")
    main_monsters = cursor.fetchall()
    cursor.execute("SELECT ydk_id, name FROM cards_view WHERE type_name LIKE '%Monster%' AND is_extra = 1")
    extra_monsters = cursor.fetchall()   
    cursor.execute("SELECT ydk_id, name FROM cards_view WHERE type_name LIKE '%Spell%'")
    spells = cursor.fetchall()
    cursor.execute("SELECT ydk_id, name FROM cards_view WHERE type_name LIKE '%Trap%'")
    traps = cursor.fetchall()
    conn.close()
    return main_monsters, extra_monsters, spells, traps

def generate_random_deck():
    main_monsters, extra_monsters, spells, traps = get_cards_by_category()
    if len(main_monsters) < 20 or len(extra_monsters) < 15 or len(spells) < 10 or len(traps) < 10:
        raise Exception("Cartas insuficientes para gerar o deck.")
    main_deck = []
    extra_deck = []
    main_deck.extend(random.sample(main_monsters, 20))
    main_deck.extend(random.sample(spells, 10))
    main_deck.extend(random.sample(traps, 10))
    extra_deck.extend(random.sample(extra_monsters, 15))
    random.shuffle(main_deck)
    random.shuffle(extra_deck)
    return main_deck, extra_deck

def save_deck(main_deck, extra_deck):
    finame = f"random_deck_{gerar_hash()}.ydk"
    output_file = os.path.join(decks_path, finame)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("#created by kaiba_ai\n")
        f.write("#main\n")
        for card in main_deck:
            f.write(f"{card[0]}\n")
        f.write("#extra\n")
        for card in extra_deck:
            f.write(f"{card[0]}\n")
    print(f"Deck saved ass {output_file}")

   
