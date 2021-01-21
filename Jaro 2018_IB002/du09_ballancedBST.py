# !/usr/bin/env python3

# Povolene knihovny: copy, math
# Import jakekoli jine knihovny neprojde vyhodnocovaci sluzbou.
# To, ze jsou nejake knihovny povolene, neznamena, ze je nutne je pouzit.


# IB002 Domaci uloha 9.
#
# V teto uloze se budeme zabyvat binarnimi vyhledavacimi stromy.
#
# V prvni casti bude Vasi ulohou sestavit skoro uplny binarni vyhledavaci strom
# obsahujici zadane klice. Vstupni pole klicu bude usporadano od nejmensich po
# nejvetsi. Vas algoritmus musi mit LINEARNI casovou slozitost vzhledem k poctu
# zadanych klicu. Tento pozadavek je splnitelny diky usporadanosti pole na
# vstupu.
#
# V druhe casti bude Vasi ulohou zjistit, jestli zadany binarni vyhledavaci
# strom je skoro uplny. Pozadovana casova slozitost je linearni vuci poctu uzlu
# ve strome.
#
# Ve treti casti bude Vasi ulohou zjistit, jestli zadany binarni vyhledavaci
# strom ma vsechny listy ve stejne hloubce. Pozadovana casova slozitost je opet
# linearni vuci poctu uzlu ve strome.
#
# Skoro uplny strom ma zaplnena vsechna patra, jen posledni nemusi byt uplne
# zaplneno (a rovnez nemusi byt doleva zarovnane).
#
# Pro ilustraci, pro vstup (1,2,3,4,5,6,7,8,9,10) je korektnim vystupem
# algoritmu z prvni casti napriklad jeden z nasledujicich stromu:
#
#             ( 5 )                           ( 7 )
#            /     \                         /     \
#          (2)     (8)                  ( 4 )       ( 9 )
#         /  \     /  \                /     \      /   \
#       (1)  (3) (6)  (9)            (2)     (6)  (8)   (10)
#              \   \    \            / \     /
#              (4) (7)  (10)       (1) (3) (5)


# Do nasledujicich definic trid nijak nezasahujte.
# Pro vykreslovani stromu muzete pouzit dodanou funkci make_graph nize.

class BSTree:
    """Trida BSTree pro reprezentaci binarniho vyhledavacicho stromu.

    Atributy:
        root   koren stromu typu Node, nebo None, pokud je strom prazdny
    """

    def __init__(self):
        self.root = None


class Node:
    """Trida Node pro reprezentaci uzlu binarniho vyhledavaciho stromu.

    Atributy:
        data    hodnota daneho uzlu (zadana pri inicializaci)
        left    odkaz na leveho potomka typu Node, nebo None, pokud neexistuje
        right   odkaz na praveho potomka typu Node, nebo None, pokud neexistuje
    """

    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data


# Ukol 1.
# Implementuje funkci build_bst, ktera dostane vzestupne serazeny seznam hodnot
# a vytvori z nich skoro uplny binarni vyhledavaci strom (typu BSTree).

def build_bst(array):
    """
    vstup: 'array' vzestupne serazene pole hodnot
    vystup: strom typu BSTree, ktery je skoro uplny (viz vyse) a obsahuje
            hodnoty z pole array
    casova slozitost: O(n), kde 'n' je delka array
    extrasekvencni prostorova slozitost:
         O(1), nepocitame do ni ovsem vstupni pole ani vystupni strom
    """

    def build_bst_nodes(start, end):
        if end - start < 1:
            return None
        middle = (start + end) // 2

        root = Node(array[middle])
        root.left = build_bst_nodes(start, middle)
        root.right = build_bst_nodes(middle + 1, end)

        return root

    tree = BSTree()
    tree.root = build_bst_nodes(0, len(array))
    return tree


# Ukol 2.
# Implementujte funkci check_almost_complete, ktera dostane binarni vyhledavaci
# strom a otestujte, zda je skoro uplny.
def get_leaf_path_len(node, cmp_fn):
    if node is None:
        return None
    if node.left is None and node.right is None:
        return 0
    path_l = get_leaf_path_len(node.left, cmp_fn)
    path_r = get_leaf_path_len(node.right, cmp_fn)
    if path_l is not None:
        if path_r is not None:
            return 1 + cmp_fn(path_l, path_r)
        return 1 + path_l
    return 1 + path_r


def get_path_len(node, cmp_fn):
    if node is None:
        return -1
    path_l = get_path_len(node.left, cmp_fn)
    path_r = get_path_len(node.right, cmp_fn)
    return 1 + cmp_fn(path_l, path_r)


def check_leaf_diff(node, path_f, diff):
    min_depth = path_f(node, min)
    max_depth = path_f(node, max)
    if min_depth is None and max_depth is None:
        return True
    return max_depth - min_depth <= diff


def check_almost_complete(tree):
    """
    vstup: 'tree' binarni vyhledavaci strom typu BSTree
    vystup: True, pokud je 'tree' skoro uplny
            False, jinak
    casova slozitost: O(n), kde 'n' je pocet uzlu stromu
    extrasekvencni prostorova slozitost: O(1) (nepocitame vstup)
    """
    return check_leaf_diff(tree.root, get_path_len, 1)


# Ukol 3.
# Implementujte funkci check_all_leaves_same_depth, ktera overi, zda jsou
# vsechny listy zadaneho binarniho vyhledavaciho stromu ve stejne hloubce.
def check_all_leaves_same_depth(tree):
    """
    vstup: 'tree' binarni vyhledavaci strom typu BSTree
    vystup: True, pokud jsou vsechny listy 'tree' ve stejne hloubce
            False, jinak
    casova slozitost: O(n), kde 'n' je pocet uzlu stromu
    extrasekvencni prostorova slozitost: O(1) (nepocitame vstup)
    """
    return check_leaf_diff(tree.root, get_leaf_path_len, 0)


# Pomocna funkce make_graph vygeneruje .dot soubor na zaklade stromu predaneho
# v argumentu. Cilem funkce je jen zobrazit aktualni stav daneho uzlu a jeho
# potomku, nijak nekontroluje jestli se jedna o BVS.
#
# Na vygenerovany soubor si bud najdete nastroj, nebo pouzijte odkazy:
# http://sandbox.kidstrythisathome.com/erdos/ nebo http://www.webgraphviz.com/
#
# Staci zkopirovat obsah souboru do formulare webove stranky.

def make_graph(tree, filename="bst.dot"):
    def dot_node(fd, node):
        if node is None:
            return

        fd.write('{} [label="{}"]\n'.format(id(node), node.data))

        for child, lr in (node.left, 'L'), (node.right, 'R'):
            dot_node(fd, child)
            dot_node_relations(fd, node, child, lr)

    def dot_node_relations(fd, parent, node, direction):
        if node is None:
            nil = direction + str(id(parent))
            fd.write('{} [label="",color=white]\n{} -> {}\n'
                     .format(nil, id(parent), nil))
        else:
            fd.write('{} -> {}\n'.format(id(parent), id(node)))

    with open(filename, "w") as fd:
        fd.write("digraph {\n")
        fd.write("node [color=lightblue2,style=filled]\n")
        dot_node(fd, tree.root)
        fd.write("}\n")


# -------------- TESTS -------------------- #
# bstree = build_bst([i for i in range(6)])
# bstree.root.right = None
bstree = BSTree()
bstree.root = Node(5)
bstree.root.right = Node(4)
bstree.root.right.left = Node(4.5)
# bstree.root.left = Node(6)
# bstree.root.left.right = Node(3)
# bstree.root.left.right.right = Node(7)
# bstree.root.right.left.left = Node(4.5)
make_graph(bstree)
print(check_almost_complete(bstree))
print(check_all_leaves_same_depth(bstree))
