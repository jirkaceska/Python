from random import randint
letters = ["h", "d", "s", "c"]
values = [2, 3, 4, 5, 6, 7, 8, 9, "T", "J", "Q", "K", "A"]
LENGTH = 1000

def get_card():
    return randint(0, 51)


def gen_card(card):
    suit = card // 13
    val = card % 13
    return str(values[val]) + letters[suit]


def gen_set():
    set_c = []
    for i in range(9):
        card = get_card()
        while card in set_c:
            card = get_card()
        set_c.append(card)
    return set_c


def print_set():
    set_c = gen_set()
    for i in range(len(set_c)):
        set_c[i] = gen_card(set_c[i])
    print(*set_c[:2])
    print(*set_c[2:4])
    print(*set_c[4:])

def print_set_r():
    set_c = gen_set()
    for i in range(len(set_c)):
        set_c[i] = gen_card(set_c[i])
    print(*set_c[:2])
    print(*set_c[2:6])


for i in range(LENGTH):
    #print_set()
    print_set_r()
