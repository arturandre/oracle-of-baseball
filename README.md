# Projeto para a disciplina MAC0459-MAC5865 - Ciência e Engenharia de Dados (2021)

# The Oracle of Baseball

Neste projeto será ilustrado o processo de coleta de dados via raspagem (scrapping), o armazenamento destes em um banco de dados orientado à grafos (neo4j) e finalmente alguns exemplos de consultas serão apresentados. O tema do projeto será a formação de um grafo de adjacências de jogadores e times de baseball. Usado este grafo iremos medir a "distância entre os jogadores", isso é, jogadores que jogaram num mesmo time serão vizinhos no grafo e o menor caminho entre dois jogadores é a distância entre os jogadores. Este projeto é inspirado no [The Oracle of Bacon](https://oracleofbacon.org/), que é um grafo de atores que atuaram num mesmo filme.

Todos os arquivos gerados ao longo do tutorial estão disponíveis [aqui](http://vision.ime.usp.br/~arturao/baseball/).

O site de coleta de dados usado será o [BASEBALL REFERENCE](https://www.baseball-reference.com/).

Na fase de raspagem iremos:

- Coletar os times disponíveis.
  ~~- Os anos em que estes times existiram.~~
- Os jogadores de cada time.
  ~~- Os anos em que eles jogaram em cada time.~~

Na fase de análise dos dados iremos remontar o [The Oracle of Bacon](https://oracleofbacon.org/), mas com jogadores de baseball.

Este projeto usa o python 3.8 e a biblioteca pyppeteer.

Este projeto contém 3 etapas e pode ser iniciado a partir de qualquer uma delas:

1. [A estrutura do site](#a-estrutura-do-site) - Para iniciar o processo de raspagem é preciso conhecer a estrutura interna das páginas do site alvo. Uma vez que o site alvo tenha sido análisado podemos desenvolver scripts de javascript para facilitar o processo de raspagem.

2. [A raspagem e o web crawler](#a-raspagem-e-o-web-crawler) - Usando o pyppeteer iremos acessar a página [BASEBALL REFERENCE](https://www.baseball-reference.com/) usando python e injetar os scrips de javascript desenvolvidos na etapa anterior. Através da comunicação entre o script de python com a página alvo, facilitada pelo script de javascript injetado, podemos começar a coletar os dados diretamente do HTML da página alvo. Os dados coletados então são armazenados em arquivos .json que serão usados na próxima etapa para formar um grafo de jogadores e times de baseball.

3. [O oráculo de baseball](#o-oráculo-de-baseball) - Usando o banco de dados orientado a grafos [neo4j](https://neo4j.com/) iremos construir um grafo a partir dos arquivos .json coletados na etapa anterior, onde cada jogador será ligado por uma aresta a cada um dos times em que ele jogou. Dois jogadores ligados a um mesmo time terão uma aresta os conectando. O menor caminho entre dois jogadores será então a distância entre os jogadores no grafo.



## A estrutura do site

Para entender a estrutura do site iremos usar as ferramentas de desenvolvedor do navegador **chrome devtools** (ou o equivalente em outro navegador). Ao acessar o site alvo o google chrome podemos abrir o **DevTools** apertando *F12* ou usando a sequencia *Ctrl+Shift+i*. Abaixo vemos o [site alvo](https://www.baseball-reference.com/teams/) com o **DevTools** aberto.

![devtools](https://user-images.githubusercontent.com/1486993/134050296-3789d554-b9e2-41d3-99df-c65c3dc77557.png)

Neste site é mais simples fazer a raspagem coletando o texto diretamente do HTML do que inspecionando as chamadas feitas ao servidor. Na figura anterior o círculo com o número **1** indica o botão de seleção de elementos, este botão permite que selecionemos algum elemento diretamente no site renderizado e inspecionemos o código HTML associado a ele. Neste exemplo vamos selecionar o primeiro time da lista o **Arizona Diamondbacks**, indicado pelo círculo **2**. Ao clicar no nome do time (após termos clicado na ferramenta de seleção) a aba de elementos do **DevTools** irá automaticamente selecionar o código HTML responsável pelo elemento selecionado, ao clicarmos com o botão direito do mouse sobre o texto HTML marcado podemos copiar o código seletor deste elemento (clicando em **3** e **4**), este código seletor pode ser usado no javascript para interagir programaticamente com a página.

Na figura abaixo vemos a aba console (**1**), onde podemos escrever comandos com javascript que servem para interagir com a página atualmente carregada no navegador. Usando o comando `documento.querySelector('SELETOR')` podemos capturar o elemento no código e interagir com ele. Por exemplo usando o seletor que foi copiado na etapa anterior `document.querySelector('#teams_active > tbody > tr:nth-child(2) > td.left > a').innerText` (**2**) podemos extrair o nome do time (**3**).

![devtools-console](https://user-images.githubusercontent.com/1486993/134052677-fab3011f-2e85-4d25-a702-19503cdc3f35.png)

Para facilitar o trabalho os scripts para extração dos nomes dos times (**get_teams.js**) e para extração dos jogadores (**get_players.js**) já foram criados. Ao navegarmos para a página dos [times](https://www.baseball-reference.com/teams/) podemos injetar o arquivo **get_teams.js**, isso é copiar o conteúdo do arquivo e colar diretamente na aba **Console** no **DevTools**. Ao fazer isso o download de três arquivos **.json** será iniciado, estes arquivos correspondem aos times ativos, inativos e nacionais de baseball.

Se escolhermos um dos times da lista poderemos escolher entre a página dos jogadores rebatedores (i.e. *batting*) ou lançadores (i.e. *pitching*) como no exemplo do time [*Washington Nationals*](https://www.baseball-reference.com/teams/WSN/) na figura abaixo. Na página de jogadores (e.g. [rebatedores do time *Washington Nationals*](https://www.baseball-reference.com/teams/WSN/bat.shtml) podemos injetar o arquivo **get_players.js**, desta vez o script irá criar as funções `scrapplayer(playertype)` e `downloadteamlist(teamslist)`, e através destas funções podemos fazer o donwload de arquivos **.json** com a lista de jogadores, note que a chamada destas funções está comentada no final do script **get_players.js**.

![wsn_team_example](https://user-images.githubusercontent.com/1486993/134074833-993163d2-c018-4d14-9b7d-d4227dc133d0.png)

Vimos até aqui que podemos semi-automatizar o processo de coleta dos times e dos jogadores injetando manualmente os scripts **get_teams.js** e **get_players.js** nas páginas adequadas. Contudo para podemos automatizar completamente o processo de raspagem e também automatizar a navegação (i.e. *web crawler*) precisamos ter um controle maior sobre o navegador, isso é, não basta controlarmos a página, precisamos ter controle sobre o navegador em si. Para tanto usaremos o pacote **pyppeteer** que por sua vez irá instalar o navegador **Cromium**, o qual será controlado via python. A biblioteca **pyppeteer** é baseada na biblioteca **puppeteer** para a plataforma Node.js, mas para python.

## A raspagem e o web crawler
**With great powers...***

*Um web-crawler pode rapidamente sobrecarregar um website fazendo um número excessivo de consultas, use com parcimônia.*

**Para evitar transtornor ao site alvo os arquivos gerados nesta etapa estão disponíveis para download [aqui](https://vision.ime.usp.br/~arturao/baseball/). A explicação abaixo e o código referênciado tem finalidade didática.**

Tendo em posse scripts que fazem a extração dos conteúdos relevantes diretamente do website alvo, a única tarefa restante é automatizar a navegação pelo website. Note que apesar de termos uma página contendo todos os times, muitas vezes não temos acesso a uma página com todos os jogadores (ou talvez não tão detalhada quanto a página específica de um dado time). Portanto será preciso navegar até a página específica de cada um dos times, acessar a página de jogadores rebatedores/lançadores e raspar a lista de tais jogadores.

Existem diversas ferramentas para automatizar tarefas baseadas em navegadores, alguns dos mais conhecidos (e ainda ativos) incluem o **Selenium**, o **puppeteer* e o **pyppeteer** que usaremos. A finalidade principal destas ferramentas é a criação de testes automatizados durante a produção de websites, contudo elas permitem a realização de outras tarefas como navegação automática, envio de requisições HTTP, execução de scripts de javascript, controle de cookies e provavelmente tudo mais que um navegador permite. 

Através do **pyppeteer** será executado o navegador **Cromium** no modo *headless*, oque implica que não será criada uma janela para ele, ou seja, ele irá rodar em background e não será possível a interação direta com ele. O modo *headless* é o modo padrão usado pelo **pyppeteer**, mas pode ser modificado, neste projeto usaremos apenas o modo *headless*.

Neste projeto usaremos os scripts de python chamados **get_teams.py** e **get_players.py**. Ambos criam instâncias do navegador **Cromium** e uma aba de internet neste navegador. O primeiro script irá navegar até a página de [times](https://www.baseball-reference.com/teams/), irá injetar o script **get_teams.js**, mas ao invés de executar um download de arquivos **.json** pelo navegador, um dicionário (i.e. um objeto **JSON**) será criado em memória no navegador *headless* e este objeto em memória poderá ser lido diretamente em python. A partir dele iremos obter a lista de times e iremos criar os três arquivos **.json** via python. O segundo script python depende da execução do primeiro, isso é, uma vez gerados os arquivos com as listas de times (e seus respectivos endereços), o segundo script irá navegar até a página de cada time onde será injetado o script **get_players.js**, e assim como no caso dos times, um objeto **JSON** será criado na memória do navegador, este objeto será então lido diretamente via python e dará origem a um arquivo **.json** com a lista de jogadores de um dado time.

Como dito antes, ambos os scripts de python são executados por um terceiro script chamado **main.py** que irá orquestrar a ordem das chamadas, o armazenamento e carregamento  dos arquivos **.json**. Note que no arquivo **main.py** mantemos um temporizador (via a variável local `sleep_time`) de 15 segundos. Este temporizador regula o intervalo entre a navegação entre uma página e a outra no navegador *headless*. Em algumas situações seria possível reduzir este tempo e até removê-lo completamente, contudo existem dois motivos para ele existir e ser de pelo menos 10 segundos, o primeiro motivo é para [evitar transtornos ao demais usuários do site](https://www.sports-reference.com/data_use.html). O segundo motivo é porque um intervalo menor é rapidamente bloqueado pelo servidor, obrigando o web crawler a ser reiniciado.

## O oráculo de baseball

Agora que já fizemos a raspagem dos times, e dos jogadores de cada time, podemos inserir cada time como um vértice do grafo, assim como cada jogador. Como sabemos qual jogador jogou em quais times, podemos associciar o par de vértices correspondendo a cada um com uma aresta. A figura abaixo mostra alguns times (em laranja) e alguns jogadores (em azul) e suas conexões com os times em que jogaram.

![neo4j_teams_players](https://user-images.githubusercontent.com/1486993/134088072-5747b829-140e-473d-90e7-be6d7c9cae7f.png)

Este grafo foi gerado a partir do script python `insert_data_in_neo4j.py`. Este script faz uma conexão com uma instância local do banco de dados Neo4j através da biblioteca oficial do Neo4j para python. Uma vez feita esta conexão, os arquivos **.json** gerados até aqui são carregados e usando-se a linguagem **Cypher** (encapsulada em strings no script python) podemos criar os vértices e arestas. Note que no script python configuramos o endereço do servidor do Neo4j. O servidor do Neo4j disponibiliza dois endereços, um para conexões via o protocolo **bolt** (por padrão `bolt://localhost:7687`) e outro para acesso com o navegador via o protocolo **http** (por padrão `http://localhost:7474`) no python usamos o endereço (e porta) do protocolo **bolt**.

O último passo para formar o oráculo de baseball é a criação de arestas conectando jogadores do mesmo time. Podemos realizar esta última etapa diretamente no script python (usando a função `connect_teammates()`) ou através da aplicação web disponibilizada pelo servidor do neo4j (tipicamente no endereço `http://localhost:7474`). Abaixo é apresentado um exemplo do código **Cypher** para encontrar o menor caminho entre dois jogadores. Na figura abaixo temos o resultado desta consulta e podemos observar que a distância entre os dois jogandores é 1, ou seja, para se chegar de um jogador a outro passando pelo menor número de jogadores de outro(s) time(s) é preciso se passar por apenas 1 jogador. Neste dataset é díficil encontrar um par de jogadores com uma distância maior que 1, dado que muitos dos jogadores jogaram em muitos times.

```
MATCH (p1:Player),(p2:Player),
p = shortestPath((p1)-[*..15]-(p2)) 
WHERE
p1.name = 'George Yeager'
and
p2.name = 'Alex Avila'
RETURN p
```

![image](https://user-images.githubusercontent.com/1486993/134222092-3070990f-5d82-4dc2-b210-d713651a0b64.png)


## Links e truques

Todos os arquivos gerados ao longo do tutorial estão disponíveis [aqui](https://vision.ime.usp.br/~arturao/baseball/).

- Após instalar o docker (no linux) os comandos `docker` devem ser executado com permissões de administrador (e.g. `sudo docker ...`. Para poder executar os comandos do `docker` sem o uso do `sudo` podemos criar um grupo docker e inserir nosso usuário a este grupo [referência](https://docs.docker.com/engine/install/linux-postinstall/) com os comandos abaixo:

`sudo groupadd docker`
`sudo usermod -aG docker $USER`

Após executar estes comandos será preciso reiniciar a sessão do linux, isso pode significar fechar e abrir o terminal novamente, reiniciar a máquina ou as vezes simplesmente executar o seguinte comando:

`newgrp docker`

Após ter feito isso os comandos a seguir para criar um container com o neo4j devem ser possíveis sem o uso de `sudo`.


- Para se iniciar um container docker com uma imagem oficial do neo4j e mapear uma pasta local para ser visível dentro do container podemos usar o comando abaixo, (trocando os volumes, se necessário as portas, o usuário (**neo4j**) e a senha (**1234**) de acesso ao sistema web:

`docker run --publish=7474:7474 --publish=7687:7687 --volume="/c/Users/Andre/Documents/projetosdev/Baseball/neo4jdata":"/data" --env NEO4J_AUTH=neo4j/1234 neo4j`

- Para salvar os dados do Neo4j inicializado pelo docker usamos o comando abaixo (trocando os volumes, o **<nome-do-arquivo>** e se necessário as portas):

`docker run --interactive --tty --rm  --publish=7474:7474 --publish=7687:7687 --volume="/c/Users/Andre/Documents/projetosdev/Baseball/neo4jdata":"/data" --volume="/c/Users/Andre/Documents/projetosdev/Baseball/neo4jbackup":"/backups" --user="neo4j:neo4j" neo4j neo4j-admin dump --database=neo4j --to=/backups/<nome-do-arquivo>.dump`

- Para carregar os dados salvos do neo4j usamos o comando (trocando os volumes, o **<nome-do-arquivo>** e se necessário as portas):
  
`docker run --interactive --tty --rm  --publish=7474:7474 --publish=7687:7687 --volume="/c/Users/Andre/Documents/projetosdev/Baseball/neo4jdata":"/data" --volume="/c/Users/Andre/Documents/projetosdev/Baseball/neo4jbackup":"/backups" --user="neo4j:neo4j" neo4j neo4j-admin load --from=/backups/<dump-name>.dump --database=neo4j --force`
  
