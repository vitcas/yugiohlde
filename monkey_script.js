// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      2025-03-28
// @description  try to take over the world!
// @author       bakura
// @match        https://www.db.yugioh-card.com/yugiohdb/member_deck.action?ope=2*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=yugioh-card.com
// @grant        none
// ==/UserScript==

async function carregarCartasArquivo(file) {
    console.log("Carregando arquivo...");
    const text = await file.text();
    const linhas = text.split('\n');
    let tabelaAtual = null;
    let sufixoTabela = "mo";
    let tipo_carta = "MONSTER";
    let mini_tipo = tipo_carta.toLowerCase()
    for (let linha of linhas) {
        linha = linha.trim();
        console.log("Lendo linha:", linha)
        if (linha === "#main") {
            tabelaAtual = document.querySelector("#monster_list tbody");
            console.log("Tabela principal selecionada", tabelaAtual);
        } else if (linha === "#extra") {
            tabelaAtual = document.querySelector("#extra_list tbody");
            sufixoTabela = "ex";
            tipo_carta = "EXTRA";
            mini_tipo = tipo_carta.toLowerCase();
            console.log("Tabela extra selecionada", tabelaAtual);
        } else if (linha.startsWith("!side")) {
            console.log("Fim do arquivo detectado");
            break;
        } else if (tabelaAtual && linha) {
            const [id, nome, tipo] = linha.split(",");
            console.log("Inserindo carta:", { id, nome, tipo });
            inserirCarta(tabelaAtual, id, nome, tipo, sufixoTabela, mini_tipo);
        }
    }
}

function inserirCarta(tabela, id_carta, nome, tipo_carta, sufixoTabela, mini_tipo) {
  console.log("Inserindo na tabela:", tabela?.id, "ID:", id_carta, "Nome:", nome);
  let copias_carta = 1;
  if (!tabela) {
    console.error("Tabela não encontrada!");
    return;
  }
  // Verifica se a carta já está na tabela e aumenta a quantidade de cópias se necessário
  for (let i = 0; i < tabela.rows.length; i++) {
    const linha = tabela.rows[i]
    const inputIdCarta = linha.querySelector("input[name='"+mini_tipo+"CardId']")
    const inputNome = linha.querySelector("input[name='"+sufixoTabela+"nm']");
    const inputCopia = linha.querySelector("input[name='"+sufixoTabela+"num']");
    // Se a linha estiver vazia (sem nome ou cópias), preenche
    if (inputNome.value == "") {
        linha.querySelector("th.row_num span").textContent = i + 1; // Atualiza o número da linha
        inputNome.value = nome;
        linha.querySelector("input[name='"+mini_tipo+"CardId']").value = id_carta;
        inputCopia.value = copias_carta;
        console.log(`Linha ${i + 1} preenchida com a carta ${nome}`);
        return; // Sai da função após preencher uma linha vazia
    }
    // Se o ID da carta já estiver na tabela, aumenta a quantidade de cópias
    if (inputIdCarta && inputIdCarta.value == id_carta) {
        const inputCopia = linha.querySelector("input[name='"+sufixoTabela+"num']");
        inputCopia.value = parseInt(inputCopia.value) + 1; // Incrementa a quantidade de cópias
        console.log(`Carta ${nome} já existe. Atualizando cópias para ${inputCopia.value}`);
        return; // Sai da função após atualizar a cópia
      }
    // Se não encontrar a carta, cria uma nova linha
    const novaLinha = document.createElement("tr");
    novaLinha.classList.add("row");
    let numeroLinha = tabela.rows.length + 1
    novaLinha.innerHTML = `
      <th class="row_num"><span>${numeroLinha}</span></th>
      <td>
          <div class="card_name">
              <p class="inpErroricon" title="">!</p>
              <input type="text" id="${sufixoTabela}nm_${numeroLinha}" name="${sufixoTabela}nm" autocomplete="off" class="keyword" alt="${tipo_carta}" value="${nome}">
              <div class="card_image_modal_open btn" title="Change Artwork">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 55.56 51.17">
                      <g id="a"><g id="b">
                          <path d="M22.24,9.15h10.83c1.26,0,2.29,1.02,2.29,2.29v4.1h-11.7l15.95,22.69,15.95-22.69h-11.16v-6.71c0-4.88-3.95-8.83-8.83-8.83h-15.83c-2.02,0-3.87,.68-5.36,1.82l5.88,8.48c.4-.68,1.13-1.15,1.97-1.15Zm10.83,32.21h-10.83c-1.26,0-2.29-1.02-2.29-2.29v-4.34h11.96L15.95,12.07,0,34.73H10.91v7.6c0,4.88,3.95,8.83,8.83,8.83h15.83c2.24,0,4.28-.84,5.84-2.22l-6.23-8.98c-.35,.82-1.16,1.39-2.1,1.39Z"></path>
                      </g></g>
                  </svg>
              </div>
          </div>
      </td>
      <td class="num">
          <input type="text" id="${sufixoTabela}num_${numeroLinha}" name="${sufixoTabela}num" autocomplete="off" maxlength="1" class="cnum t_center" alt="${tipo_carta}" value="${copias_carta}">
          <input type="hidden" id="card_id_${numeroLinha}" name="monsterCardId" value="${id_carta}">
      </td>
      <td class="rowupdown">
          <div class="rowup">▲</div>
          <div class="rowdown">▼</div>
      </td>
      <input type="hidden" class="imgs" id="imgs_${sufixoTabela}_${numeroLinha}" name="imgs" value="${id_carta}_1_1_1">
    `;
    tabela.appendChild(novaLinha);
    console.log("Carta inserida com sucesso");
  }
}

// Criar botão para carregar arquivo
const botao = document.createElement("button");
botao.textContent = "Import deck";
botao.style.position = "fixed";
botao.style.top = "10px";
botao.style.right = "10px";
botao.onclick = () => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".txt";
    input.onchange = (e) => {
        carregarCartasArquivo(e.target.files[0]);
    };
    input.click();
};
document.body.appendChild(botao);
