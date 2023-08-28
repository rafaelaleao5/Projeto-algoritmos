# Projeto-algoritmos

Instruções para rodar o projeto:

- Ter certeza que o arquivo da base de dados (list-of-airports-in-india-hxl-tags-1) esteja na mesma pasta que o código
- Ter todas as bibliotecas utilizadas instaladas no Pythom (math, pandas, networkz e matplotlib)
- Quando rodar o código deve aparecer a visualização grafica do grafo e no terminal as informações sobre a AGM.
- Arquivo CSV vai ser criado com os dados exportados das informações das arestas


# COPIA DO RELATÒRIO

OBS: Não consegui inserir fotos no README

- Contexto do problema
      A base de dados escolhida foi sobre os aeroportos da Índia, nela contém, várias informações, inclusive a latitude e longitude de cada aeroporto, o que tornou possível calcular a distância entre eles. Cada aeroporto é o vértice e cada aresta é a conexão entres eles, e o peso é a distância, assim, o intuito é criar uma Árvore Geradora Minima que conecte o grafo com os menores pesos.

    Colunas da base de dados:
      id: Um identificador único para o aeroporto.
      ident: Um código de identificação para o aeroporto.
      type: O tipo de aeroporto (por exemplo, "large_airport").
      name: O nome do aeroporto.
      latitude_deg: A latitude em graus da localização do aeroporto.
      longitude_deg: A longitude em graus da localização do aeroporto.
      elevation_ft: A elevação do aeroporto em pés.
      continent: O código do continente onde o aeroporto está localizado.
      iso_country: O código ISO do país onde o aeroporto está localizado.
      iso_region: O código ISO da região onde o aeroporto está localizado.
      municipality: O nome do município onde o aeroporto está situado.
      scheduled_service: Indica se o aeroporto possui serviço programado (1 para sim, 0 para não).
      gps_code: O código GPS do aeroporto.
      iata_code: O código IATA do aeroporto.
      local_code: O código local do aeroporto.
      home_link: Um link para o site oficial do aeroporto.
      wikipedia_link: Um link para a página do aeroporto na Wikipedia.
      keywords: Palavras-chave associadas ao aeroporto.
      score: Uma pontuação associada ao aeroporto.
      last_updated: A data em que as informações foram atualizadas pela última vez

  Porém, utilizei no projeto apenas o id, ident, latitude_deg, longitude_deg, name e iso_region. 

  Link da base de dados: https://www.kaggle.com/datasets/bhanupratapbiswas/list-of-airports-in-india

- Implementação

    Algoritmo utilizado. Krustal

    Desenvolvimento. 

        A ideia foi usar o algoritmo Krustal que passa por todos os vértices do grafo pelo menor caminho possível, ou seja, busca uma Árvore Geradora Mínima (AGM). Cada vértice do grafo seria um aeroporto e as arestas seriam justamente essa conexão           entre eles, e o peso seria a distância que liga cada um. 

        Criei a classe `unirconjuntos` onde eu implemento a estrutura de dados e encontro os conjuntos com a otimização da altura.
  
        Criei também uma função ‘calcular_distancia’ onde usa a fórmula haversine para calcular a distância entre dois aeroportos usando suas coordenadas (latitude e longitude). 

	      Crie uma função ‘Krustal’ para executar esse algoritmo no intuito de encontrar a Árvore Geradora Mínima do grafo.

        Ler e processa os dados do arquivo CSV da base de dados usando a biblioteca Pandas, depois cria o grafo vazio usando NetWorkX, e integra os dados sobre os aeroportos e vai adicionando nós ao grafo com as informações de ‘ident’, ‘name’ (nome) e         ‘iso_region’ (região).

      Cria uma lista vazia para armazenar as arestas do grafo, e um dicionário vazio para mapear os índices das linhas do DataFrame aos identificadores dos vértices. Depois disso, fiz um loop que percorre as linhas do df com ‘index’ e ‘row’, criando um     mapeamento entre o ‘index’ e o ‘ident’ (identificador do aeroporto), o que facilita identificar o vértice pelo índice. 
      O segundo  e o terceiro loop percorrem de novo todas as linhas do df para comparar cada par de aeroportos para criar uma aresta entre eles. Eles usam a condição index1 < index2 and not math.isnan(row1['latitude_deg']) and not
    math.isnan(row1['longitude_deg']) and not math.isnan(row2['latitude_deg']) and not math.isnan(row2['longitude_deg']): para garantir que os pares não são repetidos e só calculam valores válidos de latitude e longitude.
      Depois ele calcula a distância com Haversine entre as coordenadas dos aeroportos row1 e row2. Ai cria uma tupla com o índice da linha e a distância entre os 2 aeroportos, o que representa uma aresta no grafo, ai adiciona essa tupla a lista arestas.
  
    	Crio uma função que vai adicionando arestas com pesos (distância) ao grafo chamado de G, depois eu calculo a AGM do grafo usando Krustal, o que traz a menor soma total de pesos possível. Depois disso, ele vai iterando sobre as arestas da AGM e         recebendo o peso e os vértices de origem e destino, ai uso o vertices_map para converter o índice dos vértices para os valores correspondentes a coluna ‘ident’ da base de dados, e assim cada informação é adicionado a uma lista chamado ‘mst_data’.         Essa lista vai ter as arestas da AGM com seus pesos, e depois importo eles para um arquivo CSV (isso foi feito antes quando eu ia usar o Gephi para fazer a visualização do grafo, mas não baixei, mas de qualquer jeito deixei para identificar melhor      os dados que estavam saindo do código).

	    Imprimo a mensagem com os dados das arestas da AGM e depois as informações específicas com os nomes dos aeroportos destino e origem, e também os pesos, essas informações são coletadas pelo for que converte o índice dos vértices para os ‘idents’         originais, ai obtém todas as informações.
  
	    Criei um objeto do grafo vazio pra usar na visualização, ai fiz um loop para percorrer as linhas do df e adicionar os vértices do grafo, verificando se o id não é nulo, para não adicionar algo invalido, o que estava acontecendo muito, ai adiciona       um nó com o id, nome e cidade. No segundo loop, é percorrido todas as  arestas da AGM e obtém os vértices de origem e destino com o mapeamento, e assim vai adicionando uma aresta do grafo que também contém o peso.
  
	    Agora, é para mostrar a visualização gráfica do grafo usando Networkx e Matplotlib, calcula as posições dos nós e armazena em uma variável, depois desenha esses nós e as arestas nas posições definidas, define a fonte dos pesos e o tamanho dos nós.     Depois cria um dicionário que armazena os rótulos das arestas, com os pesos e os ‘idents’ dos vértices de origem e destino. Depois, desenha os rótulos que são obtidos do dicionário, e exibe o grafo com a biblioteca Matplotlib.

      O código em resumo lê os dados dos aeroportos, constrói um grafo ponderado com as distâncias entre aeroportos, encontra a Árvore Geradora Mínima desse grafo usando o algoritmo de Kruskal, exibe as informações da AGM e visualiza o grafo e a Árvore       Geradora Mínima.

      LINK DO PROJETO NO GITHUB (Instruções para rodar no README): https://github.com/rafaelaleao5/Projeto-algoritmos.git

- Bibliotecas utilizadas. 
      Pandas: usado para manipular e analisar os dados da base de dados que estavam em um arquivo CSV
      Math: todos os cálculos matemáticos 
      Networkx: cria o grafo, manipula, e usa a função ‘minimum_spanning_tree’ para encontrar a AGM.
      Matplotlib: cria a visualização gráfica, usando o grafo e a AGM, usando as funções ‘draw’ e ‘draw_networkx_edge_labels’ para desenhar o grafo e rótulos nas arestas.

- Conclusão

      O código apresenta uma implementação do algoritmo de Kruskal para encontrar a Árvore Geradora Mínima (AGM) de um grafo de aeroportos, sendo a distância entre eles o peso das arestas. Ele utiliza a biblioteca Pandas para processar dados de               aeroportos, calcula distâncias usando a fórmula de Haversine, e cria um grafo ponderado. A AGM é gerada e exportada para um arquivo CSV, e a visualização do grafo é desenhada utilizando NetworkX e Matplotlib

Referências (TRANSFORMAR PRA ABNT)

Techie Delight. "Kruskal's Algorithm for Finding Minimum Spanning Tree". Techie Delight. Disponível em: https://www.techiedelight.com/pt/kruskals-algorithm-for-finding-minimum-spanning-tree/.

"Título da Resposta" em Título da Pergunta. Stack Overflow. Disponível em: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points

Algoritmos em Python. "Representação de Grafos". Algoritmos em Python. Disponível em: https://algoritmosempython.com.br/cursos/algoritmos-python/algoritmos-grafos/representacao-grafos/.


