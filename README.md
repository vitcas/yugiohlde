
# YugiohLDE

YugiohLDE é um projeto que oferece um editor de decks e facilita a exportação para o site [**oficial**](http://www.db.yugioh-card.com). Ele converte arquivos `.ydk` em `.txt`, permitindo a importação simplificada em navegadores injetando um script com **Tampermonkey**.

A ideia era usar junto com o [**Project Ignis EDOPro**](https://projectignis.github.io/index.html), aproveitando a estrutura de pastas e os arquivos usados pelo programa.

<img src="https://imgur.com/UbkUVyg.png" alt="screen1" width="350"><img src="https://imgur.com/Fi4EJUA.png" alt="screen2" width="350">

## 📥 Instalação

### 1. Baixar e Extrair o Projeto

Após baixar o repositório como **.zip**, extraia a pasta **YugiohLDE** dentro do diretório raiz **ProjectIgnis**, que contém o programa **EDOPro**.

```
ProjectIgnis/
│── EDOPro.exe
│── pics/
│── deck/
│── ...
│── YugiohLDE/  <-- Extraia o projeto aqui
│    ├── main.py
│    ├── smooth_operator.py
│    ├── konamify.py
│    ├── new_deck.py
│    ├── requirements.txt
│    ├── exported/
```

### 2. Instalar Dependências

Certifique-se de ter **Python 3.10+** instalado e rode o seguinte comando para instalar as dependências necessárias:

```bash
pip install -r requirements.txt
```

### 3. Instalar Tampermonkey e o Script

1. Instale a extensão [Tampermonkey](https://www.tampermonkey.net/) no seu navegador
2. Abra o Tampermonkey e adicione o script **monkey\_script.js**

### 4. Pré-requisitos para exportação
- A registered Konami ID linked to your master duel game
- Must login to Yu-Gi-Oh! Cards DB using the same Konami ID
- If the Yu-Gi-Oh! DB website asks to login with Game Card ID just click "I don't have a game card ID" and fill some basic information to proceed

## 🚀 Como Usar

1. Abra **main.py** para acessar a interface principal:
   ```bash
   python main.py
   ```
2. Exporte o deck selecionado pelo programa gerando um arquivo txt na pasta exported.
3. Acesse [**www.db.yugioh-card.com**](http://www.db.yugioh-card.com), crie um novo deck e clique em editar, deve aparecer o botão gerado pelo Tampermonkey para importar o deck salvo no txt.
4. Depois de salvar o deck, vá no Master Duel => Main menu => Deck option => The Card database option no topo direito => seu deck exportado deve aparecer

## 📌 Estrutura do Projeto

- **monkey\_script.js** → Script para **Tampermonkey**, permitindo importar decks para o site.
- **main.py** → Interface principal usando **PyQt6**.
- **smooth\_operator.py** → Funções principais do projeto.
- **konamify.py** → Converte `.ydk` para `.txt`, facilitando a importação no site. Não é mais utilizado.
- **new\_deck.py** → Interface para criação e edição de decks (em desenvolvimento).
- **requirements.txt** → Lista de dependências Python necessárias.

## 🛠️ Contribuição

Pull requests são bem-vindos! Para grandes mudanças, abra uma issue primeiro para discutirmos o que você gostaria de modificar.

## 📜 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usá-lo e modificá-lo.
