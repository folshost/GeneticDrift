from colour import Color
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class Map:
    def __init__(self):
        self.graph = nx.empty_graph()

    def __getitem__(self, key):
        return self.graph[key]['coloring']


class StarMap:
    # I need population policies for starting out
    def __init__(self, n, colors, policy=None):
        self.graph = nx.star_graph(n)
        self.num_colors = colors
        if policy is None:
            state = {}
            counter = 0
            for node in self.graph:
                state[node] = counter
                counter += 1
                counter %= colors
            nx.set_node_attributes(self.graph, state, 'coloring')

    def __getitem__(self, key):
        return nx.get_node_attributes(self.graph, 'coloring')[key]

    def get_colors(self):
        return nx.get_node_attributes(self.graph, 'coloring')

    def draw(self):
        # Try doing so with the colors being properly reflected?
        num_colors = np.zeros(self.num_colors, dtype=int)
        red = Color("red")
        colors = list(red.range_to(Color("green"), self.num_colors))
        for k, v in self.get_colors().items():
            num_colors[v] += 1
        num_colors_max = num_colors.max()
        node_lists = np.zeros((self.num_colors, num_colors_max), dtype=int)
        node_lists_indices = np.zeros(self.num_colors, dtype=int)
        for k, v in self.get_colors().items():
            node_lists[v, node_lists_indices[v]] = k
            node_lists_indices[v] += 1
        for k in range(self.num_colors):
            tmp_node_list = list(node_lists[k][:node_lists_indices[k]])
            nx.draw_networkx_nodes(self.graph, node_list=tmp_node_list, color)
        plt.show()


def test_func():
    print("Hello!")
