
class TreeNode:
    def __init__(self):
        self.children = []      # Lista de nós
        self.keys = []          # Lista de chaves
        self.is_leaf = False    # Folha

    def insert(self, key): pass

class BTree:
    def __init__(self):
        self.root = TreeNode()

    def insert(self, value):
        overflow = self.root.insert(value)
        