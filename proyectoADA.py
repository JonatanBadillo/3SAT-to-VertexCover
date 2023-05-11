import networkx as nx

x1=True
x2=False
x3=False
x4=True

import networkx as nx

# Valores de las variables
values = {1: True, 2: False, 3: False, 4: True}

# La fórmula en 3CNF
formula = [
    [(1, True), (2, True), (3, True)],
    [(1, False), (2, False), (4, False)],
    [(1, False), (3, False), (4, True)]
]

# Verificar si los valores satisfacen la fórmula
satisfiable = all(any(values[var] == sign for var, sign in clause) for clause in formula)

if not satisfiable:
    print("Los valores proporcionados no satisfacen la fórmula.")
else:

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

    # Usar el algoritmo de aproximación para Vertex Cover
    vertex_cover = nx.algorithms.approximation.vertex_cover.min_weighted_vertex_cover(G)

    # Visualizar el grafo y resaltar el Vertex Cover
    import matplotlib.pyplot as plt

    # Crear dos listas de nodos, una para variables y otra para sus negaciones
    var_nodes = [f'x{i}' for i in range(1, 5)]
    neg_nodes = [f'¬x{i}' for i in range(1, 5)]

    # Visualizar el grafo y resaltar el Vertex Cover
    pos = nx.circular_layout(G)

    # Dibujar los nodos con el color y tamaño especificados
    nx.draw(G, pos, with_labels=False, node_color='lightblue', node_size=500)

    # Dibujar los nodos del Vertex Cover con el color y tamaño especificados
    nx.draw_networkx_nodes(G, pos, nodelist=vertex_cover, node_color='red', node_size=500)

    # Dibujar las etiquetas de los nodos con un tamaño de fuente más pequeño
    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')

    plt.show()


    # Mostrar el número de vértices en el Vertex Cover
    print(f"El número de vértices en el Vertex Cover es: {len(vertex_cover)}")