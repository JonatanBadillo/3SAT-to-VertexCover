import networkx as nx
import pulp
import matplotlib.pyplot as plt

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
        G.add_node(f'x{var}')
        G.add_node(f'¬x{var}')

# Añadir aristas entre las variables y sus negaciones
for i in range(1, 5):
    G.add_edge(f'x{i}', f'¬x{i}')

# Añadir aristas entre literales de diferentes cláusulas
for i in range(len(formula)):
    for j in range(i + 1, len(formula)):
        for literal1 in formula[i]:
            for literal2 in formula[j]:
                if literal1[0] != literal2[0]:
                    G.add_edge(str(literal1), str(literal2))

# Añadir aristas correspondientes a la cláusula solo si el literal no está satisfecho
for clause in formula:
    unsatisfied_literals = [str(literal) for literal in clause if values[literal[0]] != literal[1]]
    for i, u in enumerate(unsatisfied_literals):
        for v in unsatisfied_literals[i + 1:]:
            G.add_edge(u, v)

# Crear el problema de programación lineal entera
vertex_cover_problem = pulp.LpProblem("VertexCover", pulp.LpMinimize)

# Crear variables binarias para cada nodo
node_vars = {node: pulp.LpVariable(f"{node}", 0, 1, pulp.LpInteger) for node in G.nodes()}

# Agregar la función objetivo: minimizar la suma de las variables binarias
vertex_cover_problem += pulp.lpSum(node_vars)

# Agregar restricciones: para cada arista, al menos uno de sus nodos debe estar en el Vertex Cover
for u, v in G.edges():
    vertex_cover_problem += node_vars[u] + node_vars[v] >= 1

# Resolver el problema de programación lineal entera
vertex_cover_problem.solve()

# Obtener el Vertex Cover mínimo
min_vertex_cover = [node for node, node_var in node_vars.items() if node_var.value() == 1]

print(f"El número de vértices en el Vertex Cover mínimo es: {len(min_vertex_cover)}")
print(f"Los vértices en el Vertex Cover mínimo son: {min_vertex_cover}")

# Visualizar el grafo y resaltar el Vertex Cover mínimo
pos = nx.circular_layout(G)
nx.draw(G, pos, with_labels=False, node_color='lightblue', node_size=500)
nx.draw_networkx_nodes(G, pos, nodelist=min_vertex_cover, node_color='red', node_size=500)
labels = {node: node for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
plt.show()
