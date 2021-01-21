#!/usr/bin/env python3


# IB002 Domaci uloha 3.
#
# Vasi ulohou bude s vyuzitim principu binarniho vyhledavani implementovat
# dve funkce, find_first_occurrence a find_first_greater. V obou pripadech
# musi casova slozitost vaseho algoritmu byt nejhure logaritmicka, tedy byt
# v O(log n). (Pozor, iterovani v poli ma linearni slozitost.)
# Funkce nesmi modifikovat vstupni pole.
#
# Ukol 1.
# Implementujte funkci find_first_occurrence, ktera vrati index prvniho
# vyskytu prvku key v serazenem poli numbers. Pokud se prvek v poli
# nevyskytuje, vrati -1.
#
# Priklady vstupu a vystupu:
# find_first_occurrence(2, [1, 2, 2, 2, 4]) -->  1
# find_first_occurrence(3, [1, 2, 4, 5])    --> -1

def find_first_occurrence(key, numbers):
    """
    vstup: 'key' hodnota hledaneho cisla, 'numbers' serazene pole cisel
    vystup: index prvniho vyskytu hodnoty 'key' v poli 'numbers',
            -1, pokud se tam tato hodnota nevyskytuje
    casova slozitost: O(log n), kde 'n' je pocet prvku pole 'numbers'
    """
    end = len(numbers) - 1
    start = 0

    # Test non-empty array
    if end >= 0:
        if numbers[start] == key:
            return start
        if numbers[start] > key or numbers[end] < key:
            return -1

        # Start points at value smaller than key and end at value greater than or equal to key
        while end - start > 1:
            index = (start + end) // 2
            if numbers[index] >= key:
                end = index
            else:
                start = index

        if numbers[end] == key:
            return end

    return -1


# Ukol 2.
# Implementujte funkci find_first_greater modifikaci predchozi funkce
# find_first_occurrence tak, ze find_first_greater vrati index prvniho prvku
# v poli vetsiho nez key. Neni-li v poli zadny takovy, vrati -1.
#
# Priklady vstupu a vystupu:
# find_first_greater(2, [1, 2, 4, 5]) -->  2
# find_first_greater(3, [1, 2, 4, 5]) -->  2
# find_first_greater(3, [1, 2, 3])    --> -1

def find_first_greater(key, numbers):
    """
    vstup: 'key' hodnota hledaneho cisla, 'numbers' serazene pole cisel
    vystup: index prvniho vyskytu prvku vetsiho nez hodnota 'key',
            -1, pokud tam zadny takovy prvek neni
    casova slozitost: O(log n), kde 'n' je pocet prvku pole 'numbers'
    """
    end = len(numbers) - 1
    start = 0

    # Test non-empty array
    if end >= 0:
        if numbers[start] > key:
            return start
        if numbers[end] <= key:
            return -1

        # Start points at value smaller than or equal to key and end at value greater than key
        while end - start > 1:
            index = (start + end) // 2
            if numbers[index] > key:
                end = index
            else:
                start = index

        if numbers[end] > key:
            return end

    return -1


# --------------- TESTS -------------- #
tested = [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
searched = 2
#print(find_first_occurrence(2, [1, 2, 2, 2, 4]))
print(find_first_occurrence(searched, tested))
print(find_first_greater(searched, tested))
print(find_first_greater(2, [1, 2, 4, 5]))
print(find_first_greater(3, [1, 2, 4, 5]))
print(find_first_greater(3, [1, 2, 3]))
