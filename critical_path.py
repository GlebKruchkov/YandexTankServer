import networkx as nx
with open("dependencies.dot") as f:
  g = nx.drawing.nx_pydot.read_dot(f)
  paths = nx.all_simple_paths(g, source=list(g.nodes)[0], target=list(g.nodes)[-1])
  print(max(paths, key=len))
