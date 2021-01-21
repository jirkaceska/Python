#!/usr/bin/env python3


# IB002 Domaci uloha 2.
#
# Jednosmerne spojovany seznam znate z prednasky - jde o zretezeny seznam
# uzlu (Node), kde kazdy uzel ukazuje na sveho naslednika. V tomto prikladu
# nemame first a last, seznam je zadany "prvnim" ze svych uzlu.
#
# Tato uloha pracuje se dvema typy jednosmerne spojovanych seznamu:
# Linearni seznam - kde posledni prvek seznamu ukazuje na None.
# Kruhovy seznam - kde posledni prvek seznamu ukazuje zpet na prvni prvek.
#
# Pro vsechny funkce muzete predpokladat, ze seznam na vstupu je linearni,
# nebo kruhovy, tj. nemusite napriklad osetrovat situaci, kdy naslednikem
# "posledniho" v seznamu je "druhy".
#
# Do definice tridy Node nijak nezasahujte.

class Node:
    """Trida Node reprezentujici prvek ve spojovanem seznamu

    Atributy:
        key        klic daneho uzlu (cele cislo)
        next       odkaz na dalsi prvek seznamu
        opposite   odkaz na protejsi prvek seznamu, viz ukol 3.
    """

    def __init__(self):
        self.key = 0
        self.next = None
        self.opposite = None


# Ukol 1.
# Implementujte funkci is_circular, ktera dostane prvni uzel seznamu
# a otestuje, zda je zadany zretezeny seznam kruhovy.
# Prazdny seznam neni kruhovy.

def is_circular(node):
    """
    vstup: 'node' prvni uzel seznamu, ktery je linearni, nebo kruhovy
    vystup: True, pokud je seznam z uzlu 'node' kruhovy
            False, jinak
    casova slozitost: O(n), kde 'n' je pocet prvku seznamu
    """
    if node is not None:
        tested_node = node.next

        while tested_node is not None:
            if tested_node is node:
                return True

            tested_node = tested_node.next

    return False


# Ukol 2.
# Implementujte funkci get_length, ktera vrati delku (tj. pocet ruznych uzlu)
# (linearniho nebo kruhoveho) zretezeneho seznamu zacinajiciho v zadanem uzlu.
# Pokud je seznam prazdny (None), vrati 0.

def get_length(node):
    """
    vstup: 'node' prvni uzel seznamu, ktery je linearni, nebo kruhovy
    vystup: pocet prvku v zadanem seznamu
    casova slozitost: O(n), kde 'n' je pocet prvku seznamu
    """
    length = 0

    if node is not None:
        length = 1
        tested_node = node.next

        while tested_node is not None and tested_node is not node:
            length += 1
            tested_node = tested_node.next

    return length


# Ukol 3.
# Implementujte funkci calculate_opposites, ktera korektne naplni atributy
# "opposite" v uzlech kruhoveho seznamu sude delky. Tj. pro kruhove seznamy
# delky 2n naplni u kazdeho uzlu atribut opposite uzlem, ktery je o n kroku
# dale (tedy v kruhu je to uzel "naproti").
#
# Napriklad v kruhovem seznamu 1 -> 2 -> 3 -> 4 (-> 1) je opposite
# uzlu 1 uzel 3, uzlu 2 uzel 4, uzlu 3 uzel 1 a uzlu 4 uzel 2.
#
# Pokud vstupni seznam neni kruhovy nebo ma lichou delku, tak funkce
# calculate_opposites seznam neupravuje.
#
# Pozor na casovou a prostorovou slozitost vaseho algoritmu!

def calculate_opposites(node):
    """
    vstup: 'node' prvni uzel seznamu, ktery je linearni, nebo kruhovy
    vystup: nic, kokretne doplni atribut opposite pro seznam sude delky
    casova slozitost: O(n), kde 'n' je pocet prvku seznamu
    """
    if node is not None:
        length = 1
        tested_node = node.next

        while tested_node is not None and tested_node is not node:
            length += 1
            tested_node = tested_node.next

        if tested_node is node and length % 2 == 0:
            first_node = node
            opposite_node = node
            for _ in range(int(length / 2)):
                opposite_node = opposite_node.next
            for _ in range(int(length / 2)):
                first_node.opposite = opposite_node
                opposite_node.opposite = first_node

                first_node = first_node.next
                opposite_node = opposite_node.next


# ------------- TESTS --------------- #
# Linear list
# lin_length = 1
# linear = [Node() for _ in range(lin_length)]
# first_lin = linear[0]
#
# for i in range(lin_length - 1):
#     linear[i].next = linear[i + 1]
#
# print(not is_circular(first_lin))
# print(not is_circular(None))
# print(get_length(first_lin) == lin_length)
# print(get_length(None) == 0)
#
# # Circular list
# circ_length = 10
# circular = [Node() for _ in range(circ_length)]
# first_circ = circular[0]
#
# for j in range(circ_length):
#     circular[j].next = circular[(j + 1) % circ_length]
#
# print(is_circular(first_circ))
# print(get_length(first_circ) == circ_length)
#
# calculate_opposites(first_circ)
#
# for k in range(circ_length):
#     if circular[k].opposite is not circular[int(k + circ_length / 2) % circ_length]:
#         print(False)
# print("Ended")