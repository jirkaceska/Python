#!/usr/bin/env python3


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
# Relace je tranzitivni, pokud pro vsechny prvky plati:
# Je-li A v relaci s B a B je v relaci s C, pak taky A je v relaci s C.

def get_bit_line(line, size):
    output = 0
    for i in range(size):
        if line[i]:
            output |= 2**(size - (i + 1))

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
                    if bit_lines[line] & 2**(size - (v + 1)):
                        bit_lines[line] |= compute_line_closure(v)
            return bit_lines[line]

        for i in range(size):
            bit_lines[i] |= compute_line_closure(i)


def compare_lists(a, b, size):
    for i in range(size):
        if a[i] != b[i]:
            return False
    return True


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
# splnuje podminky dane vlastnosti. Graf je zadan identicky s predchozim
# ukolem, tj. vstupni graf je reprezentovan matici sousednosti indexovanou
# od [0,0], kde indexy odpovidaji vrcholum:
# [i,j] = 1, je-li v grafu hrana z i do j, tj. i je v relaci s j,
# [i,j] = 0, neni-li v grafu hrana z i do j, tj. i neni v relaci s j.
# Vystupem je odpoved (True/False).


def is_reflexive(graph):
    matrix = graph.matrix

    for u in range(graph.size):
        if not matrix[u][u]:
            return False

    return True


def is_symmetric(graph):
    matrix = graph.matrix

    for u in range(graph.size):
        for v in range(u + 1, graph.size):
            if matrix[u][v] != matrix[v][u]:
                return False

    return True


def is_antisymmetric(graph):
    matrix = graph.matrix

    for u in range(graph.size):
        for v in range(u + 1, graph.size):
            if matrix[u][v] and matrix[v][u]:
                return False

    return True


def is_transitive(graph):
    bit_lines_orig = get_bit_lines(graph)
    bit_lines = get_bit_lines(graph)

    compute_transitive_closure(bit_lines, graph.size)

    return compare_lists(bit_lines_orig, bit_lines, graph.size)


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
# Vystupem je matice sousednosti reprezentujici graf, ktery je tranzitivnim
# uzaverem puvodniho grafu. Puvodni graf nemente, vytvorte jeho kopii.
# Lze implementovat v kubickem case vzhledem k poctu vrcholu = O(|V|^3).

def transitive_closure(graph):
    bit_lines = get_bit_lines(graph)
    compute_transitive_closure(bit_lines, graph.size)
    return create_matrix_from(bit_lines)


# ----------------- TESTS -------------- #
from random import randint


class Graph:
    """Trida Graph drzi graf reprezentovany matici sousednosti.
    Atributy:
        size: velikost (pocet vrcholu) grafu
        matrix: matice sousednosti
                [u][v] reprezentuje hranu u -> v
    """

    def __init__(self, size):
        self.size = size
        self.matrix = [[False] * size for _ in range(size)]


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
two_graph = Graph(2)
zero = Graph(0)
graphs = [one_graph, two_graph, test_graph, failed, zero]
for graph_i in graphs:
    print("Reflexive:", is_reflexive(graph_i))
    print("Symmetric:", is_symmetric(graph_i))
    print("Antisymmetric:", is_antisymmetric(graph_i))
    print("Transitive:", is_transitive(graph_i))
    print()

print(transitive_closure(zero))
