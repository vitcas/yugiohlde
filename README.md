# YugiohLDE

YugiohLDE é um projeto que facilita a exportação de decks para o site [**www.db.yugioh-card.com**](http://www.db.yugioh-card.com). Ele converte arquivos `.ydk` em `.txt`, permitindo a importação simplificada pelo **monkey\_script.js** em navegadores com **Tampermonkey**.

Por praticidade o ideal é usar junto com o [**Project Ignis EDOPro**](https://projectignis.github.io/index.html), um simulador com seu próprio editor de decks, para obter as imagens das cartas exibidas pelo programa.

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
│    ├── create_deck_dialog.py
│    ├── requirements.txt
│    ├── exported/
```

### 2. Instalar Dependências

Certifique-se de ter **Python 3.10+** instalado e rode o seguinte comando para instalar as dependências necessárias:

```bash
pip install -r requirements.txt
```

### 3. Instalar Tampermonkey e o Script

1. Instale a extensão **Tampermonkey** no seu navegador: [Tampermonkey](https://www.tampermonkey.net/)
2. Abra a interface do Tampermonkey e adicione o script **monkey\_script.js**

## 🚀 Como Usar

1. Abra **main.py** para acessar a interface principal:
   ```bash
   python main.py
   ```
2. Exporte o deck selecionado pelo programa gerando um arquivo txt na pasta exported.
3. Acesse [**www.db.yugioh-card.com**](http://www.db.yugioh-card.com), use o Tampermonkey para importar o deck convertido.

## 📌 Estrutura do Projeto

- **monkey\_script.js** → Script para **Tampermonkey**, permitindo importar decks para o site.
- **main.py** → Interface principal usando **PyQt6**.
- **smooth\_operator.py** → Funções principais do projeto.
- **konamify.py** → Converte `.ydk` para `.txt`, facilitando a importação no site.
- **create\_deck\_dialog.py** → Interface para criação de decks (em desenvolvimento).
- **requirements.txt** → Lista de dependências Python necessárias.

## 🛠️ Contribuição

Pull requests são bem-vindos! Para grandes mudanças, abra uma issue primeiro para discutirmos o que você gostaria de modificar.

## 📜 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usá-lo e modificá-lo.

---

Projeto criado para facilitar a importação de decks do edoPro para o banco de dados oficial de cartas do Yu-Gi-Oh!.

