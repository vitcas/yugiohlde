import random, sqlite3, hashlib, os
from config import decks_path, DB_PATH
from collections import Counter

EXCLUDED_TYPES = (129, 161, 673, 4257, 2097313, 16777233, 16777249, 16777313, 16777377, 16777761, 16781329, 16781345)

def gerar_hash():
    return hashlib.sha1(str(random.random()).encode()).hexdigest()[:8]

def get_default_card_pools():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    p = ",".join("?" for _ in EXCLUDED_TYPES)
    q1 = f"SELECT ydk_id, type, is_extra FROM cards_view WHERE type LIKE '%monster%' AND arc_id IS NULL AND type_ext NOT IN ({p})"
    q2 = f"SELECT ydk_id, type, is_extra FROM cards_view WHERE type LIKE '%spell%' AND race < 1 AND arc_id IS NULL AND type_ext NOT IN ({p})"
    q3 = f"SELECT ydk_id, type, is_extra FROM cards_view WHERE type LIKE '%trap%' AND race < 1 AND arc_id IS NULL AND type_ext NOT IN ({p})"
    cursor.execute(q1, EXCLUDED_TYPES); m = cursor.fetchall()
    cursor.execute(q2, EXCLUDED_TYPES); s = cursor.fetchall()
    cursor.execute(q3, EXCLUDED_TYPES); t = cursor.fetchall()
    conn.close()
    return m, s, t

def get_custom_card_pool(custom_query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT ydk_id, name, is_extra, type_name FROM cards_view {custom_query}")
    cards = cursor.fetchall()
    conn.close()
    return cards

def split_card_types(cards):
    main, extra, spells, traps = [], [], [], []
    for ydk_id, name, is_extra, type_name in cards:
        if "Monster" in type_name:
            (extra if int(is_extra) > 0 else main).append((ydk_id, name))
        elif "Spell" in type_name:
            spells.append((ydk_id, name))
        elif "Trap" in type_name:
            traps.append((ydk_id, name))
    return main, extra, spells, traps

def fill_deck(target, needed, pool):
    if len(target) >= needed:
        return
    used = set(card[0] for card in target)
    for card in pool:
        if card[0] not in used:
            target.append(card)
            used.add(card[0])
            if len(target) >= needed:
                break

def generate_deck(cards, label):
    main, extra, spells, traps = split_card_types(cards)    
    dm, ds, dt = get_default_card_pools()     
    random.shuffle(dm)
    random.shuffle(ds)
    random.shuffle(dt)
    random.shuffle(main)
    random.shuffle(spells)
    random.shuffle(traps)
    random.shuffle(extra)
    extra_pool = [(c[0], c[1]) for c in dm if c[2] == 1] 
    main_pool = [(c[0], c[1]) for c in dm if c[2] == 0]
    main = main[:20]; spells = spells[:10]; traps = traps[:10]; extra = extra[:15]
    fill_deck(main, 20, main_pool)
    fill_deck(spells, 10, ds)
    fill_deck(traps, 10, dt)   
    fill_deck(extra, 15, extra_pool)
    return main + spells + traps, extra, label

def default_mode():
    m, s, t = get_default_card_pools()
    extra = [(c[0], c[1]) for c in m if c[2] == 1]
    main = [(c[0], c[1]) for c in m if c[2] == 0]
    return random.sample(main, 20) + random.sample(s, 10) + random.sample(t, 10), random.sample(extra, 15), "rnd_bullshit"

def smart_fill(cards):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    ids = [str(c[0]) for c in cards]
    if not ids:
        print("[smart_fill] Empty card list.")
        return
    placeholders = ",".join("?" for _ in ids)
    query = f"""
        SELECT eng_attr, race_name FROM cards_view
        WHERE ydk_id IN ({placeholders})
    """
    cursor.execute(query, ids)
    results = cursor.fetchall()
    conn.close()
    attrs = [r[0] for r in results if r[0]]
    races = [r[1] for r in results if r[1]]
    attr_mode = Counter(attrs).most_common(1)
    race_mode = Counter(races).most_common(1)
    print(f"[smart_fill] Predominant Attribute: {attr_mode[0][0] if attr_mode else 'N/A'}")
    print(f"[smart_fill] Predominant Race: {race_mode[0][0] if race_mode else 'N/A'}")

def archetype_mode(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM archetypes ORDER BY RANDOM() LIMIT 1")
    arc_id, name = cursor.fetchone()
    query = f"WHERE arc_id = {arc_id}"
    cards = get_custom_card_pool(query)
    smart_fill(cards)
    return generate_deck(cards, name)

def element_mode():
    attr = random.choice(["fire", "water", "wind", "earth", "light", "dark", "divine"])
    return generate_deck(get_custom_card_pool(f"WHERE lower(eng_attr) = '{attr}' AND arc_id IS NULL"), f"element_{attr}")

def race_mode(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT edo_code, desc FROM races ORDER BY RANDOM() LIMIT 1")
    race_id, race_name = cursor.fetchone()
    return generate_deck(get_custom_card_pool(f"WHERE race = {race_id} AND arc_id IS NULL"), f"race_{race_name.lower()}")

def mode_select(mode):
    conn = sqlite3.connect(DB_PATH)
    match mode:
        case 1: print("default_mode"); m, e, n = default_mode()
        case 2: print("archetype_mode"); m, e, n = archetype_mode(conn)
        case 3: print("element_mode"); m, e, n = element_mode()
        case 4: print("race_mode"); m, e, n = race_mode(conn)
    conn.close()
    return m, e, n

def save_deck(main, extra, name):
    fn = f"{name}_{gerar_hash()}.ydk"
    path = os.path.join(decks_path, fn)
    with open(path, "w", encoding="utf-8") as f:
        f.write("#created by kaiba_ai\n")
        f.write(f"#deck_name: {name}\n")
        f.write("#main\n")
        for c in main:
            f.write(f"{c[0]}\n")
        f.write("#extra\n")
        for c in extra:
            f.write(f"{c[0]}\n")
    print(f"[✓] Deck saved as {path}")

if __name__ == "__main__":
    mode = random.choice([1, 2, 3, 4])
    main, extra, name = mode_select(mode)
    os.makedirs(decks_path, exist_ok=True)
    save_deck(main, extra, name)
