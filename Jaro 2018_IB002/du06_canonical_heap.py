#!/usr/bin/env python3


# IB002 Domaci uloha 6.
#
# V nasledujicim textu pouzivame pojem "halda" ve vyznamu "binarni halda".
#
# Minimova halda je v kanonickem tvaru, pokud pro kazdy jeji prvek se dvema
# potomky plati, ze jeho levy potomek je mensi nez ten pravy nebo se oba
# rovnaji.
#
# Je v kanonickem tvaru | Neni v kanonickem tvaru
#                       |
#       (1)             |           (1)
#      /   \            |          /   \
#    (2)   (3)          |        (3)   (2)


# Trida representujici minimovou haldu. Pro praci s ni muzete s vyhodou pouzit
# funkce, ktere jste implementovali v zakladnim domacim ukolu.

class MinHeap:
    def __init__(self):
        self.size = 0
        self.array = []


# Ukol 1.
# Vasim prvnim ukolem je implementovat funkci is_canonical_min_heap(heap),
# ktera overi, zda je zadana halda 'heap' korektni minimovou haldou
# v kanonickem tvaru. Pokud ano, vrati True, v opacnem pripade vrati False.
#
# Prazdna nebo jednoprvkova halda je v kanonickem tvaru implicitne. Mejte na
# pameti, ze halda v kanonickem tvaru musi splnovat take pozadavky kladene na
# minimovou haldu.
def get_children(i):
    return 2*i + 1, 2*i + 2


def get_parent(i):
    return (i - 1) // 2


def min_heapify(root_i, heap):
    left, right = get_children(root_i)
    if left < heap.size:
        min_child = left
        if right < heap.size and heap.array[left] > heap.array[right]:
            min_child = right
        if heap.array[min_child] < heap.array[root_i]:
            heap.array[min_child], heap.array[root_i] = heap.array[root_i], heap.array[min_child]
            min_heapify(min_child, heap)


def is_canonical_min_heap(heap):
    """
    vstup: 'heap' typu MinHeap
           (je zaruceno, ze heap.size je velikost pole heap.array;
            neni zaruceno, ze prvky heap.array splnuji haldovou podminku
            nebo podminku kanonickeho tvaru)
    vystup: True, pokud je 'heap' minimova halda v kanonickem tvaru
            False, jinak
    casova slozitost: O(n), kde 'n' je pocet prvku 'heap'
    """
    for i in range(heap.size // 2):
        left, right = get_children(i)
        if right < heap.size and (heap.array[left] > heap.array[right] or heap.array[right] < heap.array[i])\
                or left < heap.size and heap.array[left] < heap.array[i]:
            return False
    return True


# Ukol 2.
# Druhym ukolem je implementovat funkci canonise_min_heap(heap), ktera zadanou
# minimovou haldu 'heap' prevede na kanonicky tvar. Funkce bude menit primo
# haldu zadanou v argumentu, proto nebude vracet zadnou navratovou hodnotu.
#
# Napoveda:
# Pro algoritmus s linearni casovou slozitosti je potreba postupovat takto:
# - Rekurzivne resime od korene k listum haldy;
# - pro kazdy uzel haldy:
#   + zkontrolujeme, jestli potomci splnuji vlastnost kanonickeho tvaru;
#     pokud ne:
#     * prohodime hodnoty leveho a praveho potomka;
#     * tim se muze pokazit vlastnost haldy v pravem podstrome, proto
#       probublame problematickou hodnotu z korene praveho podstromu
#       tak hluboko, aby uz neporusovala vlastnost haldy (pri tomto bublani
#       opravujeme pouze vlastnost haldy, kanonicky tvar neresime)
#   + mame tedy korektni minimovou haldu, ktera navic splnuje kanonicky
#     tvar od tohoto uzlu smerem nahoru;
#   + pokracujeme v rekurzi vlevo a vpravo.

def canonise_min_heap(heap):
    """
    vstup: 'heap' korektni minimova halda typu MinHeap
    vystup: funkce nic nevraci, vstupni halda 'heap' je prevedena
            do kanonickeho tvaru (pritom obsahuje stejne prvky jako na zacatku)
    casova slozitost: O(n), kde 'n' je pocet prvku 'heap'
    """
    for i in range(heap.size // 2):
        left, right = get_children(i)
        if right < heap.size and heap.array[left] > heap.array[right]:
            heap.array[left], heap.array[right] = heap.array[right], heap.array[left]
            min_heapify(right, heap)


# min_heap = MinHeap()
# min_heap.size = 100000
# for _ in range(min_heap.size):
#     min_heap.array.append(randint(0, 100))
# # min_heap.array = [-1, 0, -1, 0, 0, -1]
#
# print(min_heap.array)
# build_heap(min_heap)
# print(min_heap.array)
# canonise_min_heap(min_heap)
# print(min_heap.array)
# print(is_canonical_min_heap(min_heap))
# print(counter)