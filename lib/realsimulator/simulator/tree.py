#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from graphviz import Digraph

class Tree(object):
    """docstring for Tree"""
    def __init__(self, vector):
        super(Tree, self).__init__()
        self.vector = vector

    def __validate_vactor(self):
        ans = (self.vector[0] == 0)
        for i in range(len(self.vector)):
            ans = ans and (self.vector[i] < i)
        return ans

    def output_tree(self, output_file_name):
        self.output_vector(output_file_name + '.txt')
        self.output_graph(output_file_name)

    def output_vector(self, output_txt):
        with open(output_txt, 'w') as output_txt_file:
            output_string = '\t'.join(map(str, self.vector))
            output_string = output_string.replace('\n', '')
            output_string = output_string + '\n'
            output_txt_file.writelines(output_string)

    def output_graph(self, output_png):
        G = Digraph(format='png')
        G.attr('node', shape='circle')

        self.__def_nodes(G)
        self.__add_edge_in_graph(G)
        G.render(output_png)

    def __def_nodes(self, G):
        for i in range(len(self.vector)):
            G.node(str(i), str(i))

    def __add_edge_in_graph(self, G):
        for i in range(len(self.vector)):
            parent = self.vector[i]
            child  = i
            G.edge(str(parent), str(child))

    def size(self):
        return len(self.vector)

    def childs(self, at):
        ans = [ i for i in range(at, len(self.vector)) if (self.vector[i] == at and i > 0) ]
        return ans

    def sub_tree_nodes(self, at = 0):
        ans = [at]
        for child in self.childs(at):
            ans.extend(self.sub_tree_nodes(child))
        return ans

    def leaves(self, at = 0):
        sub_tree_nodes = self.sub_tree_nodes(at)
        pointed = set( [ self.vector[i] for i in sub_tree_nodes] )
        ans = []
        for i in sub_tree_nodes:
            if i not in pointed:
                ans.append(i)
        return ans

    def height(self, at = 0):
        pass
        # minHeight = len(self.parseIDList())
        # maxHeight = 0

        # if len(self.childNodes) > 0:
        #     for child in self.childNodes:
        #         minChild, maxChild = child.getHeight()
        #         minHeight = min(minHeight, minChild+1)
        #         maxHeight = max(maxHeight, maxChild+1)
        # elif len(self.childNodes) == 0:
        #     minHeight = 0
        #     maxHeight = 0
        # else:
        #     raise Exception('childNodes size in valid! @ Class Tree.getHeight(self)')

        # return minHeight, maxHeight

def test_sub_tree_nodes(K, at, seed = 0):
    assert (at < K)
    import numpy as np
    import sys

    np.random.seed(seed=seed)
    tree_vector = [0 for i in range(K)]
    sub_tree_set = set([at])
    for i in range(1, K):
        tree_vector[i] = np.random.randint(0, i)
        if tree_vector[i] in sub_tree_set:
            sub_tree_set.add(i)

    tree = Tree(tree_vector)
    sys.stderr.writelines("tree_vector: " + str(tree_vector) + "\n")
    if set(tree.sub_tree_nodes(at)) != sub_tree_set:
        sys.stderr.writelines("sub_tree_set: " + str(sub_tree_set) + "\n")
        sys.stderr.writelines("set(tree.sub_tree_nodes(at)): " + str(set(tree.sub_tree_nodes(at))) + "\n")
        raise Exception("test_sub_tree_nodes failed, (K, at, seed): " + str( (K, at, seed)))
    else:
        sys.stderr.writelines("passed. sub_tree_set: " + str(sub_tree_set) + "\n")

def test_leaves(K, at, seed = 0):
    assert (at < K)
    import numpy as np
    import sys

    np.random.seed(seed=seed)
    tree_vector = [0 for i in range(K)]

    sub_tree_set = set([at])
    for i in range(1, K):
        tree_vector[i] = np.random.randint(0, i)
        if tree_vector[i] in sub_tree_set:
            sub_tree_set.add(i)

    passed      = set([at])
    true_leaves = set([])
    for node in sub_tree_set:
        now = tree_vector[node]
        while now not in passed:
            passed.add(now)
            now = tree_vector[now]

    for node in sub_tree_set:
        if node not in passed:
            true_leaves.add(node)

    if len(true_leaves) == 0:
        true_leaves.add(at)

    tree = Tree(tree_vector)

    sys.stderr.writelines("tree_vector: " + str(tree_vector) + "\n")
    if set(tree.leaves(at)) != true_leaves:
        sys.stderr.writelines("true_leaves: " + str(true_leaves) + "\n")
        sys.stderr.writelines("set(tree.leaves(at)): " + str(set(tree.leaves(at))) + "\n")
        raise Exception("test_leaves failed, (K, at, seed): " + str( (K, at, seed)) )
    else:
        sys.stderr.writelines("passed. true_leaves: " + str(true_leaves) + "\n")










