#!/usr/bin/env python3

# Povolene knihovny: copy, math, collections
# Z knihovny collections se vam muze hodit datova struktura deque:

from collections import deque

# IB002 Domaci uloha 11.
#
# Tento tyden bude vasim ukolem implementovat dva grafove algoritmy.
# Ukoly jsou zamereny na aplikace pruchodu grafem.
#
# Reprezentace grafu je stejna jako v ukolu cv11, tedy matici sousednosti.
# Matice je indexovana od [0][0], vrcholum odpovidaji cisla 0 .. graph.size-1.
# V matici je na indexu [u][v] hodnota True, pokud graf obsahuje hranu u -> v,
# jinak je tam hodnota False.
#
# Grafy (i neorientovane!) mohou obsahovat smycky (tj. situace, kdy v matici
# na indexu [u][u] je True) a mohou byt i nesouvisle.
#
# Pripomenuti prace s frontou typu deque:
# inicializace fronty: queue = deque() nebo queue = deque([seznam prvku])
# vlozeni prvku do fronty: queue.append(prvek)
# vybrani prvku z fronty: queue.popleft(prvek)
#
# Definici tridy Graph nijak nemodifikujte, ani nepridavejte zadne atributy.
# Zamerne se v teto uloze budete muset obejit bez pomocnych poli ve tride
# Graph; budete muset pouzit lokalni promenne a pripadne parametry v rekurzi.
#
# Nepouzivejte globalni promenne. I kdyz je mozne, ze vyhodnocovaci sluzba
# neodhali vsechna pouziti globalnich promennych, u implementacnich testu
# vas pouzivani globalnich promennych zbytecne pripravi o body. Ma tedy smysl
# se naucit programovat spravne uz ted.


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


# Ukol 1.
# Implementujte funkci colourable, ktera zjisti, zda je dany neorientovany graf
# obarvitelny dvema barvami tak, aby kazde dva sousedni vrcholy mely ruznou
# barvu.
#
# Neorientovany graf v nasi reprezentaci znamena, ze
#    graph.matrix[u][v] == graph.matrix[v][u] pro vsechny vrcholy u, v.

def colourable(graph):
    """Zjisti, zda je zadany neorientovany graf obarvitelny dvema barvami.
    Vstup:
        graph - neorientovany graf typu Graph
    Vystup:
        True, pokud je graf obarvitelny dvema barvami
        False, jinak
    casova slozitost: O(n^2), kde n je pocet vrcholu grafu
    extrasekvencni prostorova slozitost: O(n), kde n je pocet vrcholu grafu
    """
    # None - without color, True - first color, False - second color
    colors = [None for _ in range(graph.size)]
    queue = deque()

    def matrix_colourable():
        if len(queue) == 0:
            return True
        vertex = queue.pop()

        for succ in range(graph.size):
            if graph.matrix[vertex][succ]:
                if colors[succ] is None:
                    queue.append(succ)
                    colors[succ] = not colors[vertex]
                elif colors[vertex] == colors[succ]:
                    return False

        return matrix_colourable()

    for i in range(graph.size):
        if colors[i] is None:
            queue.append(i)
            colors[i] = True
            if not matrix_colourable():
                return False

    return True


# Ukol 2.
# Implementujte funkci compute_dependencies, ktera pro zadany orientovany graf
# spocita topologicke usporadani vrcholu, tj. ocislovani vrcholu takove, ze
# kazda hrana vede z vrcholu s nizsim cislem do vrcholu s vyssim cislem.
#
# Vystupem je pole zadavajici topologicke usporadani (ocislovani vrcholu),
# kde na prvni pozici (tedy s indexem 0) je vrchol nejmensi
# v tomto usporadani, tj. nevede do nej zadna hrana,
# a na posledni pozici vrchol nejvetsi, tj. nevede z nej zadna hrana.
# Pokud topologicke usporadani neexistuje, algoritmus vraci None.
#
# Priklad:
#    mejme graf s vrcholy 0, 1, 2 a hranami 0 -> 1, 2 -> 1, 2 -> 0;
#    vystupem bude pole (Pythonovsky seznam] [2, 0, 1]

def compute_dependencies(graph):
    """Spocita topologicke usporadani vrcholu v grafu.
    Vstup:
        graph - orientovany graf typu Graph
    Vystup:
        pole cisel reprezentujici topologicke usporadani vrcholu
        None, pokud zadne topologicke usporadani neexistuje
    casova slozitost: O(n^2), kde n je pocet vrcholu grafu
    extrasekvencni prostorova slozitost: O(n), kde n je pocet vrcholu grafu
    """
    # -1 - not visited, 0 - started, 1 - completed
    completed = [-1 for _ in range(graph.size)]
    reverted_depenedncies = []

    def dfs(vertex):
        if completed[vertex] == 0:
            return False
        elif completed[vertex] == -1:
            completed[vertex] = 0
            for succ in range(graph.size):
                if graph.matrix[vertex][succ] and not dfs(succ):
                    return False

            completed[vertex] = 1
            reverted_depenedncies.append(vertex)

        return True

    for i in range(graph.size):
        if not dfs(i):
            return None

    return list(reversed(reverted_depenedncies))


# ----------------- TESTS -------------- #
from random import randint

g_size = 8
test_graph = Graph(g_size)

matrix_v = "0 0 0 1 0 0 0 1;0 0 0 0 0 0 0 0;1 1 0 0 0 0 0 0;0 0 0 0 1 0 0 0;0 0 0 0 0 0 0 0;0 0 0 0 0 0 0 0;0 0 0 1 0 1 0 0;0 0 0 0 1 0 0 0"
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
            connected = 1 if randint(0, 10) > 9 else 0
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
gen_rand_mat(test_graph.matrix)
gen_rand_un_mat(test_graph.matrix)
failed.matrix = gen_mat("0 1 1;1 0 0;1 0 0")
print_matrix(test_graph.matrix)
print()
print(colourable(failed))
