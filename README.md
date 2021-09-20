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


## A raspagem

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

