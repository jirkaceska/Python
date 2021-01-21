from random import randint


def transposition(string, n):
    output = ""
    for j in range(n):
        #print((len(string) - j - 1) // n)
        for i in range((len(string) - j + j%n) // n):
            output += string[j+i*n]
            print(output)
    print(output)


for i in range(2,10):
    print(i, ":")
    transposition("ABCDEFGH", i)
    print()


def Caesar_cipher_encrypt(string, step):
    string = string.upper()
    a = ord("A")
    output = ""
    for char in string:
        output += chr(a + (ord(char) - a + step) % 26)
    return output


def Ceaser_cipher_decrpyt(string, step):
    string = string.upper()
    a = ord("A")
    output = ""
    for char in string:
        output += chr(a + (ord(char) - a - step) % 26)
    print(output)


def gen_permutation():
    alphabet = []
    output = []
    a = ord("A")
    for i in range(26):
        alphabet.append(chr(a + i))

    while len(alphabet) > 0:
        rand = randint(0, len(alphabet) - 1)
        output.append(alphabet[rand])
        del alphabet[rand]
    return output


def substituion(string, perm):
    a = ord("A")
    output = ""
    for char in string:
        output += perm[(a - ord(char)) % len(perm)]

    print(output)


substituion("ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789", gen_permutation())
