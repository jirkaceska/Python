from random import *

def place_row(distance, position, places):
    print(places[0], end=" ")
    for i in range(distance):
        if i == position:
            print("*", end=" ")
        else:
            print(".", end=" ")
    print(places[1])

def end_message(places, index):
    print("Succesful arrival to", places[0 if index == 0 else 1] + "!")
            
def drunk_simulator(distance, steps):
    position = distance // 2
    places = ["home", "pub"]

    for i in range(steps):
        #place_row(length, position, places)
        if position == 0:
            return places[0]
        if position == distance - 1:
            return places[1]
            #end_message(places, position)
        position += (randint(0,1)-0.5)*2
    #print("Lost in night!")
    return 0
    


def drunk_travelling(repeat, distance, steps):
    home = 0
    pub = 0
    for i in range(repeat):
        if drunk_simulator(distance, steps) == "home":
            home += 1
        if drunk_simulator(distance, steps) == "pub":
            pub += 1
    print(home/repeat, pub/repeat, sep="; ")

#drunk_travelling(20, 30, 100)

def rnd_row(length, minimum, maximum):
    row = []
    for j in range(length):
        row.append(randint(minimum, maximum))
    return row

def rnd_matrix(length, minimum, maximum):
    table = []
    for i in range(length):
        table.append(rnd_row(length, minimum, maximum))
    return table

def print_table(table):
    for i in range(len(table)):
        for j in range(len(table[i])):
            print(table[i][j], end=" ")
        print()
        
#print_table(rnd_matrix(3, 0, 9))

def gen_pool(n):
    pool = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(".")
        pool.append(row)
    return pool

def drunk_move(pool, pos, old_pos = [0, 0]):
    pool[old_pos[0]][old_pos[1]] = "."
    pool[pos[0]][pos[1]] = "*"

def in_range(number, low, high):
    if number >= low and number <= high:
        return True
    else:
        return False
            

def drunk_pool(n, repeat):
    pool = gen_pool(n)
    pos = [n//2, n//2]
    drunk_move(pool, pos)

    for _ in range(repeat):
        direction = randint(0,1)
        step = int((randint(0,1) - 0.5)*2)
        if direction == 1: #vertical move
            new_pos = [pos[0] + step, pos[1]]
        else: #horizontal move
            new_pos = [pos[0], pos[1] + step]
        if in_range(new_pos[0], 0, n-1) and in_range(new_pos[1], 0, n-1):
            #drunk_move(pool, new_pos, pos)
            pos = new_pos
        else:
            print("end")
            print(new_pos)
            return
        #print_table(pool)
        #print()
    

drunk_pool(3, 10)
