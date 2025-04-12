import random
import sqlite3
import os

from config import DB_PATH, decks_path
from slave import gerar_hash

def get_cards_by_category():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    excluded_types = (
        129,161,673,4257,2097313,
        16777233,16777249,16777313,16777377,
        16777761,16781329,16781345
    )
    placeholders = ",".join("?" for _ in excluded_types)

    query_monsters_main = f"""
        SELECT ydk_id, name, level FROM cards_view
        WHERE type_name LIKE '%Monster%' AND arc_name IS NULL
        AND is_extra = 0
        AND type_ext NOT IN ({placeholders})
    """
    cursor.execute(query_monsters_main, excluded_types)
    main_monsters = cursor.fetchall()

    query_monsters_extra = f"""
        SELECT ydk_id, name, level FROM cards_view
        WHERE type_name LIKE '%Monster%' AND arc_name IS NULL
        AND is_extra = 1
    """
    cursor.execute(query_monsters_extra)
    extra_monsters = cursor.fetchall()

    query_spells = f"""
        SELECT ydk_id, name FROM cards_view
        WHERE type_name LIKE '%Spell%' AND arc_name IS NULL
        AND type_ext NOT IN ({placeholders})
    """
    cursor.execute(query_spells, excluded_types)
    spells = cursor.fetchall()

    query_traps = f"""
        SELECT ydk_id, name FROM cards_view
        WHERE type_name LIKE '%Trap%' AND arc_name IS NULL
    """
    cursor.execute(query_traps)
    traps = cursor.fetchall()

    conn.close()
    return main_monsters, extra_monsters, spells, traps

def generate_random_deck():
    main_monsters, extra_monsters, spells, traps = get_cards_by_category()
    if len(main_monsters) < 20 or len(extra_monsters) < 15 or len(spells) < 10 or len(traps) < 10:
        raise Exception("Cartas insuficientes para gerar o deck.")
    
    main_deck_monsters = random.sample(main_monsters, 20)
    main_deck_spells = random.sample(spells, 10)
    main_deck_traps = random.sample(traps, 10)
    extra_deck = random.sample(extra_monsters, 15)

    # Ordenar monstros por level (maior → menor)
    main_deck_monsters.sort(key=lambda x: x[2] if x[2] is not None else 0, reverse=True)
    extra_deck.sort(key=lambda x: x[2] if x[2] is not None else 0, reverse=True)

    return main_deck_monsters + main_deck_spells + main_deck_traps, extra_deck

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
