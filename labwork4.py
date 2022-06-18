"""

This program loads the graph from the file and draws it,
processes and outputs information about its connected components,
determines a diameter and displays it on the graphic file,
and draws the spanning forest of the Graph.

Variant: 52.
Coded by Nazarenko Andriy

"""

import networkx as nx
import matplotlib.pyplot as plt


class Graph(nx.Graph):
    """
    Inherited from networkx.Graph() class, which has additional methods.
    """

    def draw_a_tree(self, pos: dict = None):
        """
        Makes a graphic file, where is drawn a graph whit its spanning forest.
        :param pos: determines the positions of nodes.
        :return:
        """
        tree = nx.minimum_spanning_tree(self)
        edge_tree_colors = ['g' if t_e in tree.edges() else 'k' for t_e in self.edges()]
        node_tree_colors = ['g' if t_n in tree.nodes() else 'k' for t_n in self.nodes()]
        nx.draw(self, pos=pos, with_labels=True, node_color=node_tree_colors, font_color='white',
                edge_color=edge_tree_colors)
        plt.show()

    def info_about_components(self):
        """
        Prints the number of nodes and edges, degrees,eccentricities,
        radius and diameter of each connected component
        :return: Nothing
        """
        number = 0
        for component in nx.connected_components(self):
            subgraph = self.subgraph(component)
            number += 1
            print(f"Connected Component №{number}.")
            print(f"The number of vertex = {nx.number_of_nodes(subgraph)}.")
            print(f"The number of edges = {nx.number_of_edges(subgraph)}.")
            print(f"Nodes degrees: {subgraph.degree}.")
            print(f"Nodes eccentricities: {nx.eccentricity(subgraph)}.")
            print(f"Radius of the component = {nx.radius(subgraph)}.")
            print(f"Diameter of the component = {nx.diameter(subgraph)}.")

    def draw_diameters(self, pos=None):
        """
        Makes a graphic file, where is drawn a graph whit its diameters.
        :param pos: argument that determines positions of the nodes.
        :return:
        """
        diameter_paths = []
        diameter = None

        for component in nx.connected_components(self):
            subgraph = self.subgraph(component)
            d = nx.diameter(subgraph)
            short_paths = dict(nx.all_pairs_shortest_path(subgraph))
            for node in short_paths.values():
                for path in node.values():
                    if 0 < len(path) - 1 == d:
                        diameter = path
                        break
            diameter_paths += [tuple(diameter)]
        d_graph = nx.Graph(diameter_paths)
        d_edge_colors = ['r' if (d_e in d_graph.edges) else 'k' for d_e in self.edges()]
        d_node_colors = ['r' if (d_n in d_graph.nodes) else 'k' for d_n in self.nodes()]

        nx.draw(self, with_labels=True, pos=pos, font_color='white', edge_color=d_edge_colors,
                node_color=d_node_colors)
        plt.show()


try:
    # 2
    g = Graph(nx.read_adjlist('C:/Temp/adj_list.txt'))
    nx.draw_shell(g, with_labels=True, font_color='w', edge_color='k', node_color='k')
    plt.show()

    # 3
    positions = {'1': [3, 3], '2': [0, 0], '3': [3, 6], '4': [6, 0], '5': [8, 0], '6': [11, 6], '7': [14, 0],
                 '8': [16, 0],
                 '9': [19, 6], '10': [22, 0], '11': [24, 0], '12': [24, 6], '13': [25, 3]}
    nx.draw(g, pos=positions, with_labels=True, font_color='w', edge_color='k', node_color='k')
    plt.show()

    # 4
    g.info_about_components()

    # 5
    g.draw_diameters(pos=positions)

    # 6
    g.draw_a_tree(pos=positions)
except Exception as e:
    print(e)
