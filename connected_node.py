import os
import re
import argparse
import codecs
from collections import defaultdict
from graphviz import Digraph

include_regex = re.compile('#include\s+["<"](.*)[">]')
valid_headers = [['.h', '.hpp'], 'red']
valid_sources = [['.c', '.cc', '.cpp'], 'blue']
valid_extensions = valid_headers[0] + valid_sources[0]


def normalize(path):
    filename = os.path.basename(path)
    end = filename.rfind('.')
    end = end if end != -1 else len(filename)
    return filename[:end]


def get_extension(path):
    return path[path.rfind('.'):]


def find_all_files(path, recursive=True):
    files = []
    for entry in os.scandir(path):
        if entry.is_dir() and recursive:
            files += find_all_files(entry.path)
        elif get_extension(entry.path) in valid_extensions:
            files.append(entry.path)
    return files


def find_neighbors(path):
    f = codecs.open(path, 'r', "utf-8", "ignore")
    code = f.read()
    f.close()
    return [normalize(include) for include in include_regex.findall(code)]


def create_graph(folder):
    files = find_all_files(folder)
    folder_to_files = defaultdict(list)
    for path in files:
        folder_to_files[os.path.dirname(path)].append(path)
    nodes = {normalize(path) for path in files}
    node_dict_graph = {}
    for folder in folder_to_files:
        for path in folder_to_files[folder]:
            ns = find_neighbors(path)
            node = normalize(path)
            if node not in node_dict_graph:
                new_set = set()
                node_dict_graph[node] = new_set
            for n in ns:
                if n != node:
                    if n in nodes:
                        if n not in node_dict_graph:
                            new_set = set()
                            node_dict_graph[n] = new_set
                        node_dict_graph[n].add(node)
                        node_dict_graph[node].add(n)
    return node_dict_graph


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', help='Path to the folder to scan')
    parser.add_argument('output', help='Path of the output file without the extension')
    parser.add_argument('-f', '--format', help='Format of the output', default='pdf', \
                        choices=['bmp', 'gif', 'jpg', 'png', 'pdf', 'svg'])
    parser.add_argument('-v', '--view', action='store_true', help='View the graph')
    parser.add_argument('-c', '--cluster', action='store_true', help='Create a cluster for each subfolder')
    parser.add_argument('--cluster-labels', dest='cluster_labels', action='store_true', help='Label subfolder clusters')
    parser.add_argument('-s', '--strict', action='store_true', help='Rendering should merge multi-edges', default=False)
    args = parser.parse_args()
    answer_graph = dict(sorted(create_graph(args.folder).items(), key=lambda len_val: -len(len_val[1])))
    with open("long_ways.txt", "w") as f:
        for key, value in answer_graph.items():
            f.write(f"файл {key} -> {len(answer_graph[key])} строк\n")
