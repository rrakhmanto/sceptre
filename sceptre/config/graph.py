# -*- coding: utf-8 -*-

"""
sceptre.config.graph
This module implements a StackConfig graph, which stores a directed graph
of a stack's dependencies.
"""

import logging
import networkx as nx


class StackDependencyGraph(object):
    """
    A Directed Graph representing the relationship between Stack config
    dependencies. Responsible for initalizing the graph object based on
    a given inital stack config path.

    :param inital_config_path: The inital stack config you want to generate
    the graph from
    :type inital_config_path: str
    """

    def __init__(self, dependency_map):
        self.logger = logging.getLogger(__name__)
        self.graph = nx.DiGraph()
        self.dependency_map = dependency_map
        self._generate_graph()
        nx.drawing.nx_pydot.write_dot(self.graph, "out.dot")

    def _generate_graph(self):
        """
        Generates the graph for the initalized StackDependencyGraph object
        """
        for stack, dependencies in self.dependency_map.items():
            self._generate_edges(stack, dependencies)

    def _generate_edges(self, stack_path, dependency_paths):
        """
        Adds edges to the graph based on a list of dependencies that are
        generated from the inital stack config. Each of the paths
        in the inital_dependency_paths list are a depency that the inital
        Stack config depends on.

        :param dependency_paths: a collection of dependency paths
        :type inital_dependency_paths: string
        """
        self.logger.debug(
            "Generate edges for graph {0}".format(
                self.graph
            )
        )
        for dependency_path in dependency_paths:
            edge = self.graph.add_edge(stack_path, dependency_path)
            if not nx.is_directed_acyclic_graph(self.graph):
                raise Exception("Dependency cycle detected: {} {}".format(stack_path, dependency_path))
            self.logger.debug("Added edge: {}".format(edge))

    def reverse_graph(self):
        rev = StackDependencyGraph({})
        rev.graph = nx.reverse(self.graph)
        return rev

    def __getitem__(self, param, default=None):
        """
        Enables retrival of dependencies using dependencies[stack.name]
        """
        return self.graph[param].keys()
