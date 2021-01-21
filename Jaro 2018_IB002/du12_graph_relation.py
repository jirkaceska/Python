#!/usr/bin/env python3

# Povolene knihovny: copy, math, collections

# IB002 Domaci uloha 12.
#
# S relacemi se vetsina z vas setkala na predmetu Matematicke zaklady
# informatiky. Relace na mnozine intuitivne popisuje vztah mezi prvky
# teto mnoziny. Mejme treba relaci "byt kamaradem", kdy prvky A a B
# (z mnoziny lidi) jsou v relaci, pokud A je kamaradem B.
# Orientovany graf lze chapat jako (binarni) relaci mezi prvky, kde uzly
# reprezentuji prvky mnoziny a z uzlu A do B vede hrana, prave kdyz je
# A v relaci s B.

# Mezi zakladni vlastnosti binarnich relaci patri:
#
# *reflexivita*
# Relace je reflexivni, pokud je kazdy prvek v relaci sam se sebou.
#
# *symetrie*
# Relace je symetricka, pokud pro libovolne dva prvky A a B plati:
# Pokud A je v relaci s B, pak je taky B v relaci s A.
#
# *antisymetrie*
# Relace je antisymetricka, pokud pro libovolne dva ruzne prvky A a B plati:
# Pokud A je v relaci s B, pak B neni v relaci s A.
#
# *tranzitivita*
# Relace je tranzitivni, pokud pro libovolne prvky A, B, C plati:
# Je-li A v relaci s B a B je v relaci s C, pak taky A je v relaci s C.


# Nasledujici definici tridy Graph nijak nemodifikujte.
# Reprezentace grafu je stejna jako v minulem du.

class Graph:
    """Trida Graph drzi graf reprezentovany matici sousednosti.
    Atributy:
        size: velikost (pocet vrcholu) grafu
        matrix: matice sousednosti
                [u][v] reprezentuje hranu u -> v
                (True: hrana existuje, False: hrana neexistuje)
    """

    def __init__(self, size):
        self.size = size
        self.matrix = [[False] * size for _ in range(size)]


def get_bit_line(line, size):
    output = 0
    for i in range(size):
        if line[i]:
            output |= 2 ** (size - (i + 1))

    return output


def get_bit_lines(graph):
    size = graph.size
    output = [0 for _ in range(size)]
    for i in range(size):
        output[i] = get_bit_line(graph.matrix[i], size)

    return output


def compute_transitive_closure(bit_lines, size):
    for _ in range(size):
        visited = [False for _ in range(size)]

        def compute_line_closure(line):
            if not visited[line]:
                visited[line] = True

                for v in range(size):
                    if bit_lines[line] & 2 ** (size - (v + 1)):
                        bit_lines[line] |= compute_line_closure(v)
            return bit_lines[line]

        for i in range(size):
            bit_lines[i] |= compute_line_closure(i)


def create_matrix_from(bit_lines):
    size = len(bit_lines)
    matrix = [[False] * size for _ in range(size)]

    for i in range(size):
        for j in range(size):
            if bit_lines[i] & 2 ** (size - (j + 1)):
                matrix[i][j] = True

    return matrix


# Ukol 1.
# Implementujte funkce is_reflexive, is_symmetric, is_antisymmetric
# a is_transitive, ktere pro vstupni graf overi, zda jim reprezentovana relace
# splnuje podminky dane vlastnosti.

def is_reflexive(graph):
    """Zjisti, zda je relace zadana grafem reflexivni.
    Vstup: graph - orientovany graf typu Graph
    Vystup: True/False
    casova slozitost: O(n), kde n je pocet vrcholu grafu
    extrasekvencni prostorova slozitost: O(1)
    """
    matrix = graph.matrix

    for u in range(graph.size):
        if not matrix[u][u]:
            return False

    return True


def is_symmetric(graph):
    """Zjisti, zda je relace zadana grafem symetricka.
    Vstup: graph - orientovany graf typu Graph
    Vystup: True/False
    casova slozitost: O(n^2), kde n je pocet vrcholu grafu
    extrasekvencni prostorova slozitost: O(1)
    """
    matrix = graph.matrix

    for u in range(graph.size):
        for v in range(u + 1, graph.size):
            if matrix[u][v] != matrix[v][u]:
                return False

    return True


def is_antisymmetric(graph):
    """Zjisti, zda je relace zadana grafem antisymetricka.
    Vstup: graph - orientovany graf typu Graph
    Vystup: True/False
    casova slozitost: O(n^2), kde n je pocet vrcholu grafu
    extrasekvencni prostorova slozitost: O(1)
    """
    matrix = graph.matrix

    for u in range(graph.size):
        for v in range(u + 1, graph.size):
            if matrix[u][v] and matrix[v][u]:
                return False

    return True


def is_transitive(graph):
    """Zjisti, zda je relace zadana grafem tranzitivni.
    Vstup: graph - orientovany graf typu Graph
    Vystup: True/False
    casova slozitost: O(n^3), kde n je pocet vrcholu grafu
    extrasekvencni prostorova slozitost: O(1)
    """
    matrix = graph.matrix
    size = graph.size

    for u in range(size):
        for v in range(size):
            if matrix[u][v]:
                for w in range(size):
                    if matrix[v][w] and not matrix [u][w]:
                        return False
    return True


# Ukol 2.
# Implementujte funkci transitive_closure, ktera spocita tranzitivni
# uzaver daneho grafu. Tranzitivni uzaver je nejmensi nadmnozina relace,
# ktera splnuje podminky pro tranzitivitu (relace je chapana jako mnozina
# vsech dvojic, ktere jsou v dane relaci).
#
# Tranzitivni uzaver grafu lze taky definovat jako graf, ve kterem vede
# hrana z vrcholu A do vrcholu B, pokud v puvodnim grafu existovala
# nejaka orientovana cesta vedouci z vrcholu A do vrcholu B.
#
# Puvodni graf nemente, vytvorte si kopii.

def transitive_closure(graph):
    """Vypocita tranzitivni uzaver zadaneho grafu.
    Vstup: graph - orientovany graf typu Graph
    Vystup: tranzitivni uzaver grafu (objekt typu Graph)
    casova slozitost: O(n^3), kde n je pocet vrcholu grafu
    """
    bit_lines = get_bit_lines(graph)
    compute_transitive_closure(bit_lines, graph.size)
    output = Graph(graph.size)
    output.matrix = create_matrix_from(bit_lines)
    return output


# ----------------- TESTS -------------- #
from random import randint


g_size = 8
test_graph = Graph(g_size)

# matrix_v = "1 1 0 0 0 1 0 0;1 0 0 0 0 0 1 0;0 0 1 0 1 0 0 0;0 0 0 0 0 0 0 0;0 0 1 0 0 1 0 0;1 0 0 0 1 0 0 0;0 1 0 0 0 0 0 1;0 0 0 0 0 0 1 1"
matrix_v = "0 0 0 0 0 0 0 0;0 0 0 0 0 0 0 1;0 0 0 0 0 0 0 0;0 1 0 0 0 0 0 0;0 0 1 0 0 1 0 0;0 0 0 0 0 0 0 0;1 0 0 0 0 0 0 0;0 0 1 0 0 0 0 1"
failed = Graph(3)


def gen_mat(mat):
    mat_out = []
    for row in mat.split(";"):
        row_out = []
        for col in row.split(" "):
            row_out.append(int(col))
        mat_out.append(row_out)
    return mat_out


def gen_rand_mat(matrix):
    for i in range(g_size):
        for j in range(i + 1):
            connected = randint(0, 10) > 7
            matrix[i][j] = connected
            matrix[j][i] = connected


def gen_rand_un_mat(matrix):
    for i in range(g_size):
        for j in range(g_size):
            connected = 1 if randint(0, 5) > 4 else 0
            matrix[i][j] = connected


def print_matrix(matrix):
    for row in matrix:
        print(row)
    for row in matrix:
        print(*row, end=";")


# test_graph.matrix = gen_mat(matrix_v)
# gen_rand_mat(test_graph.matrix)
gen_rand_un_mat(test_graph.matrix)
failed.matrix = gen_mat("1 0 0;1 0 1;1 0 0")
print_matrix(test_graph.matrix)
print()
one_graph = Graph(1)
one_graph.matrix = [[1]]
two_graph = Graph(2)
zero = Graph(0)
graphs = [one_graph, two_graph, test_graph, failed, zero]
for graph_i in graphs:
    print("Reflexive:", is_reflexive(graph_i))
    print("Symmetric:", is_symmetric(graph_i))
    print("Antisymmetric:", is_antisymmetric(graph_i))
    print("Transitive:", is_transitive(graph_i))
    print()

print("TEST:", is_transitive(transitive_closure(test_graph)))
