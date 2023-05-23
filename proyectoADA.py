import networkx as nx
import matplotlib.pyplot as plt
import itertools

# Valores de las variables
values = {1: True, 2: False, 3: False, 4: True}

# La fórmula en 3CNF
formula = [
    [(1, True), (2, True), (3, True)],
    [(1, False), (2, False), (4, False)],
    [(1, False), (3, False), (4, True)]
]

# Crear un grafo vacío
G = nx.Graph()

# Añadir vértices al grafo
for clause in formula:
    for literal in clause:
        var = literal[0]
        G.add_node(f'x{var}')  # Representa la variable
        G.add_node(f'¬x{var}')  # Representa la negación de la variable

# Añadir aristas entre las variables y sus negaciones
for i in range(1, 5):
    G.add_edge(f'x{i}', f'¬x{i}')  # Conexión entre variable y negación

# Añadir aristas entre literales de diferentes cláusulas
for i in range(len(formula)):
    for j in range(i + 1, len(formula)):
        for literal1 in formula[i]:
            for literal2 in formula[j]:
                if literal1[0] != literal2[0]:  # Comprueba que las variables sean diferentes
                    G.add_edge(str(literal1), str(literal2))  # Conexión entre literales de diferentes cláusulas

# Añadir aristas correspondientes a la cláusula solo si el literal no está satisfecho
for clause in formula:
    unsatisfied_literals = [str(literal) for literal in clause if values[literal[0]] != literal[1]]
    for i, u in enumerate(unsatisfied_literals):
        for v in unsatisfied_literals[i + 1:]:
            G.add_edge(u, v)  # Conexión entre literales insatisfechos de la misma cláusula

def is_vertex_cover(graph, cover):
    for u, v in graph.edges():
        if u not in cover and v not in cover:
            return False
    return True

def find_min_vertex_cover(graph):
    nodes = list(graph.nodes())
    min_cover = nodes
    for cover_size in range(1, len(nodes) + 1):
        for cover in itertools.combinations(nodes, cover_size):
            if is_vertex_cover(graph, cover) and len(cover) < len(min_cover):
                min_cover = cover
    return min_cover

'''
n: El número de variables en la expresión 3CNF. 
En el código de ejemplo, se establece n en 4 (ya que hay 4 variables: 1, 2, 3 y 4). 
Este valor se utiliza para determinar el número de literales y vértices relacionados con las variables en el grafo.

m: El número de cláusulas en la expresión 3CNF. 
En el código de ejemplo, se establece m en 3 (ya que hay 3 cláusulas en la lista formula). Este valor se utiliza para asegurar que al menos un vértice se agregue por cada cláusula en el grafo.
'''    

# Calcula el número k de vértices para el Vertex Cover mínimo
n = len(values)
m = len(formula)
k = 2 * n + m

# Encuentra el Vertex Cover mínimo
min_vertex_cover = find_min_vertex_cover(G)

print(f"El número de vértices en el Vertex Cover mínimo es: {len(min_vertex_cover)}")
print(f"Los vértices en el Vertex Cover mínimo son: {min_vertex_cover}")

# Visualizar el grafo y resaltar el Vertex Cover mínimo
pos = nx.circular_layout(G)
nx.draw(G, pos, with_labels=False, node_color='lightblue', node_size=500)
nx.draw_networkx_nodes(G, pos, nodelist=min_vertex_cover, node_color='red', node_size=500)
labels = {node: node for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
plt.show()
