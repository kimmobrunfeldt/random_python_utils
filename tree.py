"""
This is an example how to draw tree graphs using networkx and matplotlib.

Tree generator:
Is an itreable object which yields nodes in format:
[node, branch_nodes, leaf_nodes]

Example tree:
    mainbranch
  /           \
leaf1          branch1
             /        \
          leaf2      leaf3
Would yield:
['mainbranch', ['branch1'], ['leaf1']]
['branch1', [], ['leaf2', 'leaf3']]
Amount of yielded items == amount of branch nodes.
"""

import networkx as nx
import matplotlib.pyplot as pyplot


def walk_tree(node, branch_node_class, children_method_name):
    """Walks through a tree in DFS preorder.
    See http://en.wikipedia.org/wiki/Tree_traversal#Example
    """
    queue = [node]
    visited = set()
    while queue:
        node = queue.pop()
        if isinstance(node, branch_node_class):
            branch_nodes = []
            leaf_nodes = []
            node_children = getattr(node, children_method_name)()
            for child in node_children:
                if isinstance(child, branch_node_class):
                    branch_nodes.append(child)
                else:
                    leaf_nodes.append(child)
            yield node, branch_nodes, leaf_nodes

            new_branch_nodes = []
            for child in node_children:
                if isinstance(child, branch_node_class) and child not in visited:
                    new_branch_nodes.append(child)
            visited.add(node)
            queue.extend(new_branch_nodes)


def generate_tree_graph(tree_generator, func=lambda x: str(x)):
    """Generates tree graph.
    TODO: Ordered tree.

    Args:
        tree_generator: Iterable object which yields branch nodes,
                        see file's docstring.
        func: Function to apply to all node objects, by default their str
              representation is used.
    """
    tree_graph = nx.DiGraph()

    for node, branch_nodes, leaf_nodes in tree_generator:
        node = func(node)
        branch_nodes = map(func, branch_nodes)
        leaf_nodes = map(func, leaf_nodes)

        tree_graph.add_node(node)
        for branch_node in branch_nodes:
            tree_graph.add_node(branch_node)
            tree_graph.add_edge(node, branch_node)
        for leaf_node in leaf_nodes:
            print leaf_node
            tree_graph.add_node(leaf_node)
            tree_graph.add_edge(node, leaf_node)

    return tree_graph


class Branch(object):
    def __init__(self, children, name):
        self.children = children
        self.name = name

    def get_children(self):
        return self.children


class Leaf(object):
    def __init__(self, name):
        self.name = name


def generate_leaf():
    if not hasattr(generate_leaf, "counter"):
        generate_leaf.counter = 0
    generate_leaf.counter += 1
    return Leaf('leaf%s' % generate_leaf.counter)


# Generate tree which is same as the tree in file's docstring
subtree = Branch([Leaf('leaf2'), Leaf('leaf3')], 'branch1')
exampletree = Branch([Leaf('leaf1'), subtree], 'mainbranch')

level1tree = Branch([generate_leaf() for x in range(3)], 'level1tree')
level2tree = Branch([generate_leaf(), level1tree], 'level2tree')
level3tree = Branch([level2tree, generate_leaf(), generate_leaf(), generate_leaf()],
                    'level3tree')
level4tree = Branch([level3tree, generate_leaf()],
                    'level4tree')


if __name__ == '__main__':
    gen = walk_tree(level4tree, Branch, 'get_children')
    tree_graph = generate_tree_graph(gen, func=lambda x: x.name)

    # write dot file to use with graphviz
    # run "dot -Tpng test.dot >test.png"
    nx.write_dot(tree_graph, 'test.dot')

    # same layout using matplotlib with no labels
    pyplot.title("Tree")
    pos = nx.graphviz_layout(tree_graph, prog='dot')
    nx.draw(tree_graph, pos, with_labels=True, arrows=False)
    pyplot.savefig('nx_test.png')
    pyplot.show()
