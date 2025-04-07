import os
import urllib.request
import hashlib
import sqlite3

# Caminho do diretório e arquivo
temp_dir = os.path.join(os.getcwd(), "temp")
os.makedirs(temp_dir, exist_ok=True)
file_path = os.path.join(temp_dir, "cards.cdb")
temp_download_path = os.path.join(temp_dir, "cards_temp.cdb")

url = "https://raw.githubusercontent.com/ProjectIgnis/BabelCDB/master/cards.cdb"


def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def baixar_arquivo():
    print("[INFO] Baixando arquivo mais recente...")
    urllib.request.urlretrieve(url, temp_download_path)
    print("[INFO] Download concluído.")


def atualizar_arquivo():
    os.replace(temp_download_path, file_path)
    print("[INFO] Arquivo atualizado com sucesso.")


def criar_view():
    print("[INFO] Verificando/criando view 'view_dtt'...")
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    # Verifica se a view já existe
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='view' AND name='view_dtt';
    """)
    exists = cursor.fetchone()

    if exists:
        print("[INFO] A view 'view_dtt' já existe.")
    else:
        cursor.execute("""
            CREATE VIEW view_dtt AS
            SELECT
                datas.*,
                texts.name,
                texts.desc
            FROM
                datas
            JOIN
                texts ON datas.id = texts.id;
        """)
        conn.commit()
        print("[INFO] View 'view_dtt' criada com sucesso.")

    conn.close()


def main():
    if not os.path.exists(file_path):
        print("[INFO] Arquivo não encontrado. Iniciando download.")
        baixar_arquivo()
        atualizar_arquivo()
    else:
        print("[INFO] Verificando por atualizações...")
        baixar_arquivo()
        hash_atual = sha256sum(file_path)
        hash_novo = sha256sum(temp_download_path)

        if hash_atual == hash_novo:
            print("[INFO] O arquivo já está atualizado.")
            os.remove(temp_download_path)
        else:
            print("[INFO] Arquivo novo encontrado. Atualizando...")
            atualizar_arquivo()

    criar_view()


if __name__ == "__main__":
    main()
