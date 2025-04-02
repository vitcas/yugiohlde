
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

#### 3.1. Pré-requisitos para exportação
- Caso você ainda não tenha uma Konami ID, basta registrar uma nova
- Será necessária uma Konami ID conectada ao Master Duel
- Faça login em Yu-Gi-Oh! Cards DB usando essa Konami ID

## 🚀 Como Usar

1. Abra **main.py** para acessar a interface principal:
   ```bash
   python main.py
   ```
2. Exporte o deck selecionado pelo programa gerando um arquivo txt na pasta exported.
3. Acesse [**www.db.yugioh-card.com**](http://www.db.yugioh-card.com), crie um novo deck e clique em editar, deve aparecer o botão gerado pelo Tampermonkey para importar o deck salvo no txt.
4. Depois de salvar o deck, vá no Master Duel => Main menu => Deck option => The Card database option no topo direito => seu deck exportado deve aparecer

## 🛠️ Contribuição

Pull requests são bem-vindos! Para grandes mudanças, abra uma issue primeiro para discutirmos o que você gostaria de modificar.

## 📜 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usá-lo e modificá-lo.
