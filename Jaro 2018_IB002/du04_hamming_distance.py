#from random import randint
#!/usr/bin/env python3

# Povolene knihovny: copy, math
# Import jakekoli jine knihovny neprojde vyhodnocovaci sluzbou.

# IB002 Domaci uloha 4.
#
# Hammingovu vzdalenost dvou stejne dlouhych binarnich retezcu
# definujeme jako pocet bitu, ve kterych se retezce lisi.
#
# Vasim ukolem je implementovat funkci hamming_distance,
# ktera pro binarni retezec 'b' a nezaporne cele cislo 'k' vrati vsechny
# binarni retezce, jejichz Hammingova vzdalenost od 'b' bude prave 'k'.
#
# Priklady chovani:
# hamming_distance('100', 0) vrati vystup: ['100']
# hamming_distance('0001', 2) vrati vystup:
#         ['1101', '1011', '1000', '0111', '0100', '0010']


def reverse_bits(bin_str):
    output = ""
    for char in bin_str:
        output += "1" if char == "0" else "0"

    return output


def combine_arrays(arr1, arr2):
    output = []
    for a in arr1:
        for b in arr2:
            output.append(a + b)
    return output


def hamming_distance(b, k):
    """
    vstup: 'b' binarni retezec, 'k' nezaporne cele cislo
    vystup: pole vsech binarnich retezcu se vzdalenosti 'k' od 'b'
    casova slozitost: polynomialni vzhledem k delce binarniho retezce 'b'
        ( To znamena, ze pocet operaci je v O(n^j), kde 'n' je delka binarniho
          retezce 'b' a 'j' je nejake fixni cislo. Tedy pro slozitostni odhad
          'k' povazujeme za fixni. Vsimnete si, ze pokud budete generovat
          vsechny binarni retezce stejne delky jako 'b' a nasledne merit
          Hammingovu vzdalenost, tak se nevejdete do pozadovane slozitosti.
          Doporucejeme se zamyslet nad rekurzivnim pristupem. )
    """
    # Invalid => return empty array
    n = len(b)
    if k > n:
        return []

    # Return reversed
    if k == n:
        return [reverse_bits(b)]

    if k == 0:
        return [b]

    output = []

    for i in range(k + 1):
        left = b[:n//2]
        right = b[n//2:]

        if i <= len(left) and k - i <= len(right):
            output += combine_arrays(hamming_distance(left, i), hamming_distance(right, k - i))
        if i > len(left):
            break

    return output
# -----------------TESTS-------------#
# def count_xor(a, b):
#     output = 0
#     for j in range(len(a)):
#         if a[j] != b[j]:
#             output += 1
#     return output
#
#
# for i in range(7):
#     tested = ""
#     count = 0
#     for j in range(i + 1):
#         tested += str(randint(0, 1))
#     ham = randint(0, i)
#     ham_array = hamming_distance(tested, ham)
#     for bin_str in ham_array:
#         if count_xor(bin_str, tested) != ham:
#             print("ERROR:", end=" ")
#         print(tested, bin_str, ham)


# print("(", len(tested), ",", count, ",",len(tested)**3, ")")
print(hamming_distance("", 1))
# print("100"[-3:])
