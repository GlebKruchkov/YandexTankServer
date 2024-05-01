import networkx as nx
with open("graph.dot") as f:
    graph = nx.drawing.nx_pydot.read_dot(f)
    degrees = nx.degree_centrality(graph)
    print(max(degrees, key=degrees.get))
