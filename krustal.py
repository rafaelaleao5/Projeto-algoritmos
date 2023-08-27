import pandas as pd
import math
import networkx as nx
import matplotlib.pyplot as plt

class unirconjuntos:
    # estrutura com 'n' elementos iniciais
    def __init__(self, n):
        self.parent = list(range(n)) # guarda o pai de cada elemento
        self.altura = [0] * n # altura da árvore para cada elemento
    
    
    def achar(self, x):
        # Retorna a raiz do conjunto que contém o elemento 'x'
        if self.parent[x] != x:
            self.parent[x] = self.achar(self.parent[x])
        return self.parent[x]
    
    def uniao(self, x, y):
        # Une os dois conjuntos
        raiz_x = self.achar(x)
        raiz_y = self.achar(y)
        
        if raiz_x != raiz_y:
            if self.altura[raiz_x] > self.altura[raiz_y]:
                self.parent[raiz_y] = raiz_x
            else:
                self.parent[raiz_x] = raiz_y
                if self.altura[raiz_x] == self.altura[raiz_y]:
                    self.altura[raiz_y] += 1

def calculardistancia_haversine(lat1, lon1, lat2, lon2):
    R = 6371  # raio médio da Terra em quilômetros

    # graus para radianos
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    distancia_lat = lat2_rad - lat1_rad
    distancia_lon = lon2_rad - lon1_rad

    a = math.sin(distancia_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(distancia_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distancia = R * c
    return distancia

def kruskal(arestas, num_vertices):
    arestas.sort(key=lambda aresta: aresta[2])
    uniao_achar = unirconjuntos(num_vertices)
    arvore_geradora_minima = []
    
    for aresta in arestas:
        u, v, peso = aresta
        if uniao_achar.achar(u) != uniao_achar.achar(v):
            uniao_achar.uniao(u, v)
            arvore_geradora_minima.append(aresta)
    
    return arvore_geradora_minima

filename = "list-of-airports-in-india-hxl-tags-1.csv"  
df = pd.read_csv(filename, sep=',', dtype={'latitude_deg': float, 'longitude_deg': float})

G = nx.Graph()

for index, row in df.iterrows():
    G.add_no(row['ident'], name=row['name'], city=row['iso_region'])

arestas = []
vertices_map = {}  # mapear nomes de vértices para índices

for index, row in df.iterrows():
    vertices_map[index] = row['ident']

for index1, row1 in df.iterrows():
    for index2, row2 in df.iterrows():
        if index1 < index2 and not math.isnan(row1['latitude_deg']) and not math.isnan(row1['longitude_deg']) and not math.isnan(row2['latitude_deg']) and not math.isnan(row2['longitude_deg']):
            distancia = calculardistancia_haversine(row1['latitude_deg'], row1['longitude_deg'], row2['latitude_deg'], row2['longitude_deg'])
            arestas.append((index1, index2, distancia))

# grafo com arestas geradas com pesos (distâncias)
G.add_com_pesos(arestas)

arvore_geradora_minima = nx.arvore_geradora_minima(G)

 # exportar as informações da AGM para arquivo CSV 
mst_data = []
for u, v, data in arvore_geradora_minima.arestas(data=True):
    peso = data['peso']
    u_name, v_name = vertices_map[u], vertices_map[v]
    mst_data.append({'source': u_name, 'target': v_name, 'peso': peso})

mst_df = pd.DataFrame(mst_data)
mst_df.to_csv('arvore_geradora_minima.csv', index=False)

print("Dados da Árvore Geradora Mínima: ")
for u, v, data in arvore_geradora_minima.arestas(data=True):
    peso = data['peso']
    u_name, v_name = vertices_map[u], vertices_map[v]
    u_name = df.loc[u, 'name']  # nome aeroporto do vértice u
    v_name = df.loc[v, 'name']  # nome aeroporto do vértice v
    print(f"Origem: {u_name}, Destino: {v_name}, Peso: {peso:.2f}")

# ver grafo gerado
G_visualizar = nx.Graph()

for index, row in df.iterrows():
    if not pd.isnull(row['ident']):  # identificador do aeroporto não é nulo
        G_visualizar.add_no(row['ident'], name=row['name'], city=row['iso_region'])

for u, v, data in arvore_geradora_minima.arestas(data=True): # arestas da AGM
    peso = data['peso']
    u_name, v_name = vertices_map[u], vertices_map[v]
    G_visualizar.add_aresta(u_name, v_name, peso=peso)

# desenhar grafo
pos = nx.circular_layout(G_visualizar)
nx.draw(G_visualizar, pos, with_labels=True, font_peso='bold', node_size=200)

# desenhar rótulos das arestas
aresta_labels = {}
for u, v, data in arvore_geradora_minima.arestas(data=True):
    peso = data['peso']
    u_name, v_name = vertices_map[u], vertices_map[v]
    aresta_labels[(u_name, v_name)] = f"{peso:.2f}\n{u_name}-{v_name}"

# desenhar rótulos das arestas
nx.draw_networkx_aresta_labels(G_visualizar, pos, aresta_labels=aresta_labels, font_size=8, label_pos=0.5)
# mostrar grafo
plt.show()