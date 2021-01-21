#!/usr/bin/env python3

# Povolene knihovny: copy, math
# Import jakekoli jine knihovny neprojde vyhodnocovaci sluzbou.
# To, ze jsou nejake knihovny povolene, neznamena, ze je nutne je pouzit.


# IB002 Domaci uloha 7.
#
# Souctovy strom je binarni strom, kde kazdy uzel ma nasledujici vlastnost:
# Pokud ma uzel alespon jednoho syna, potom je klic uzlu roven souctu klicu
# vsech jeho synu. Listy stromu tedy mohou obsahovat libovolne hodnoty.
# Za souctovy je povazovan i strom, ktery neobsahuje zadne uzly, a strom,
# ktery obsahuje prave jeden uzel.
#
# Muzete si samozrejme pridat vlastni pomocne funkce.
#
# Priklad:
# souctove stromy      nesouctove stromy
#   53       47            53       47
#  /  \        \          /  \     /
# 21  32       47        21  21   46
#             /  \                  \
#            1    46                 1

# Do nasledujicich definic trid nijak nezasahujte.
#
# Trida pro reprezentaci souctoveho stromu.
# root je koren stromu a je typu Node, nebo None, pokud je strom prazdny.
#
# Pro vykreslovani stromu muzete pouzit funkci make_graph z cv07.

class SumTree:
    def __init__(self):
        self.root = None


# Trida pro reprezentaci uzlu v souctovem strome.
# key je hodnota uzlu, ktera ma byt rovna souctu hodnot vsech synu.

class Node:
    def __init__(self):
        self.key = 0
        self.left = None
        self.right = None


# Ukol 1.
# Vasim prvnim ukolem je napsat funkci, ktera vybuduje uplny souctovy strom ze
# zadaneho pole. Listy stromu budou prave prvky pole v poradi zleva doprava.
# Delka pole bude vzdy mocninou dvojky.
#
# Napriklad:
# Z pole [1,2,3,4] vznikne strom:
#      10
#    /    \
#   3      7
#  / \    / \
# 1   2  3   4


def connect_trees(trees):
    length = len(trees)
    if length == 1:
        return trees[0]
    sup_trees = []
    for i in range(0, length, 2):
        tree = SumTree()
        tree.root = Node()
        left, right = trees[i].root, trees[i + 1].root
        tree.root.left = left
        tree.root.right = right
        tree.root.key = left.key + right.key
        sup_trees.append(tree)
    return connect_trees(sup_trees)


def build_sum_tree(array):
    """
    vstup: pole (Pythonovsky seznam) 'array' cisel delky 'n',
           kde 'n' je nejaka mocnina dvojky
    vystup: korektni strom typu SumTree, ktery ma v listech (v poradi zleva
            doprava) hodnoty ze zadaneho pole 'array'
            strom musi byt uplny, tj. vsechna jeho patra musi byt zcela
            zaplnena
    casova slozitost: O(n)
    """
    trees = []
    for key in array:
        tree = SumTree()
        tree.root = Node()
        tree.root.key = key
        trees.append(tree)
    return connect_trees(trees)


def is_sum_root(root):
    if root is None:
        return True
    left, right = root.left, root.right
    if left is None and right is None:
        return True
    if left is not None and right is None:
        return root.key == left.key and is_sum_root(left)
    elif right is not None and left is None:
        return root.key == right.key and is_sum_root(right)
    else:
        return root.key == right.key + left.key and is_sum_root(left) and is_sum_root(right)


# Ukol 2.
# Vasim druhym ukolem je napsat funkci is_sum_tree, ktera overi, zda je strom
# souctovy. Pokud ano, vraci True, jinak False.
def is_sum_tree(tree):
    """
    vstup: 'tree' typu SumTree
           (je zaruceno, ze uzly ve strome jsou typu Node;
            neni zaruceno, ze splnuji souctovou podminku)
    vystup: True, pokud je 'tree' korektni SumTree, tj. vsechny jeho uzly
                  splnuji souctovou podminku
            False, jinak
    casova slozitost: O(n), kde 'n' je pocet prvku 'tree'
    """
    return is_sum_root(tree.root)


# -----------------TESTS----------------- #
from random import randint

arrExpLen = 15


def print_tree(root, level=0, line=''):
    if root is None:
        return
    if root.left is None and root.right is None:
        print('\t'*level, line, root.key)
    else:
        print_tree(root.right, level + 1, '/')
        print('\t'*level, line, root.key)
        print_tree(root.left, level + 1, '\\')


# inputArr = [randint(0, 30) for _ in range(2 ** arrExpLen)]
# sum_tree = build_sum_tree(inputArr)
# # print_tree(sum_tree.root)
# print(is_sum_tree(sum_tree))
# print(2**arrExpLen, counter)
sum_tree_false = SumTree()
# sum_tree_false.root = Node()
# sum_tree_false.root.key = 2

# sum_tree_false.root.right = Node()
# sum_tree_false.root.right.key = 1
#
# sum_tree_false.root.left = Node()
# sum_tree_false.root.left.key = 2
print_tree(sum_tree_false.root)
print(is_sum_tree(sum_tree_false))

