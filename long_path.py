import networkx as nx
with open("dependencies.dot") as f:
    graph = nx.drawing.nx_pydot.read_dot(f)
    paths = nx.all_simple_paths(graph, source=list(graph.nodes)[0], target=list(graph.nodes)[-1])
    print(max(paths, key=len))
