# Projeto para a disciplina MAC0459-MAC5865 - Ciência e Engenharia de Dados (2021)

# The Oracle of Baseball

Neste projeto será ilustrado o processo de coleta de dados via raspagem (scrapping), o armazenamento destes em um banco de dados orientado à grafos (neo4j) e finalmente alguns exemplos de consultas serão apresentados. O tema do projeto será a formação de um grafo de adjacências de jogadores e times de baseball. Usado este grafo iremos medir a "distância entre os jogadores", isso é, jogadores que jogaram num mesmo time serão vizinhos no grafo e o menor caminho entre dois jogadores é a distância entre os jogadores. Este projeto é inspirado no [The Oracle of Bacon](https://oracleofbacon.org/), que é um grafo de atores que atuaram num mesmo filme.

O site de coleta de dados usado será o [BASEBALL REFERENCE](https://www.baseball-reference.com/).

Na fase de raspagem iremos:

- Coletar os times disponíveis.
  - Os anos em que estes times existiram.
- Os jogadores de cada time.
  - Os anos em que eles jogaram em cada time.

Na fase de análise dos dados iremos remontar o [The Oracle of Bacon](https://oracleofbacon.org/), mas com jogadores de baseball.

Este projeto usa o python 3.8 e a biblioteca pyppeteer.

Este projeto contém 3 etapas e pode ser iniciado a partir de qualquer uma delas:

1. [A estrutura do site](#a-estrutura-do-site) - Para iniciar o processo de raspagem é preciso conhecer a estrutura interna das páginas do site alvo. Uma vez que o site alvo tenha sido análisado podemos desenvolver scripts de javascript para facilitar o processo de raspagem.

2. [A raspagem](#a-raspagem) - Usando o pyppeteer iremos acessar a página [BASEBALL REFERENCE](https://www.baseball-reference.com/) usando python e injetar os scrips de javascript desenvolvidos na etapa anterior. Através da comunicação entre o script de python com a página alvo, facilitada pelo script de javascript injetado, podemos começar a coletar os dados diretamente do HTML da página alvo. Os dados coletados então são armazenados em arquivos .json que serão usados na próxima etapa para formar um grafo de jogadores e times de baseball.

3. [O oráculo de baseball](#o-oráculo-de-baseball) - Usando o banco de dados orientado a grafos [neo4j](https://neo4j.com/) iremos construir um grafo a partir dos arquivos .json coletados na etapa anterior, onde cada jogador será ligado por uma aresta a cada um dos times em que ele jogou. Dois jogadores ligados a um mesmo time terão uma aresta os conectando. O menor caminho entre dois jogadores será então a distância entre os jogadores no grafo.



## A estrutura do site

Para entender a estrutura do site iremos usar as ferramentas de desenvolvedor do navegador **chrome devtools** (ou o equivalente em outro navegador). Ao acessar o site alvo o google chrome podemos abrir o **DevTools** apertando *F12* ou usando a sequencia *Ctrl+Shift+i*. Abaixo vemos o [site alvo](https://www.baseball-reference.com/teams/) com o **DevTools** aberto.

![devtools](https://user-images.githubusercontent.com/1486993/134050296-3789d554-b9e2-41d3-99df-c65c3dc77557.png)

Neste site é mais simples fazer a raspagem coletando o texto diretamente do HTML do que inspecionando as chamadas feitas ao servidor. Na figura anterior o círculo com o número **1** indica o botão de seleção de elementos, este botão permite que selecionemos algum elemento diretamente no site renderizado e inspecionemos o código HTML associado a ele. Neste exemplo vamos selecionar o primeiro time da lista o **Arizona Diamondbacks**, indicado pelo círculo **2**. Ao clicar no nome do time (após termos clicado na ferramenta de seleção) a aba de elementos do **DevTools** irá automaticamente selecionar o código HTML responsável pelo elemento selecionado, ao clicarmos com o botão direito do mouse sobre o texto HTML marcado podemos copiar o código seletor deste elemento (clicando em **3** e **4**), este código seletor pode ser usado no javascript para interagir programaticamente com a página.

Na figura abaixo vemos a aba console (**1**), onde podemos escrever comandos com javascript que servem para interagir com a página atualmente carregada no navegador. Usando o comando `documento.querySelector('SELETOR')` podemos capturar o elemento no código e interagir com ele. Por exemplo usando o seletor que foi copiado na etapa anterior `document.querySelector('#teams_active > tbody > tr:nth-child(2) > td.left > a').innerText` (**2**) podemos extrair o nome do time (**3**).

![devtools-console](https://user-images.githubusercontent.com/1486993/134052677-fab3011f-2e85-4d25-a702-19503cdc3f35.png)


## O oráculo de baseball

a

a

a

a

a

a

a

a

a

a

a

a

a

a

a

a

a

a

a

a

a

a

