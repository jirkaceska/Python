#!/usr/bin/python3

# UCO: 469507
# Povolene knihovny: copy, math, collections
from collections import deque
from math import inf
# --- Implementacni test 24. 5. 2018: Bludiste ---
#
# V tomto prikladu budeme pracovat s bludistem reprezentovanym ctvercovou siti.
# Bludiste je objekt typu Maze, viz nize.
# Pohyb v bludisti je mozny nejvyse ctyrmi smery (nahoru, dolu, doleva,
# doprava). Zdi nejsou pruchozi.

# Nasledujici konstanty reprezentuji ruzne druhy mist v bludisti.
# Muzete je pouzit ve svem kodu pro lepsi citelnost a prehlednost.
# Znaky START, TREASURE a PATH se pouzivaji jen v poslednim ukolu.

WALL = "#"      # tento znak reprezentuje zed (neni pruchozi)
EMPTY = "."     # tento znak reprezentuje chodbu (pruchozi misto)
START = "?"     # tento znak reprezentuje pocatecni pozici (jen pro 4. ukol)
TREASURE = "$"  # tento znak reprezentuje poklad (jen pro 4. ukol)
PATH = "*"      # timto znakem budete ve 4. ukolu znacit cestu

NOT_VISITED = 0
FOUND = 1
# V ukolech 1, 2 a 3 bude zadane bludiste vzdy obsahovat jen znaky WALL a
# EMPTY. V ukolu 4 bude zadane bludiste navic obsahovat prave jeden znak START
# a libovolny pocet znaku TREASURE.


class Maze:
    """Trida Maze slouzi k reprezentaci bludiste. Nijak ji nemodifikujte.

    Atributy:
        rows   pocet radku ctvercove site (vzdy alespon 3)
        cols   pocet sloupcu ctvercove site (vzdy alespon 3)
        map    2D matice s obsahem bludiste

    Rozmer matice map je rows krat cols.
    Pro lepsi praci s bludistem bude zaruceno, ze okrajova mista jsou zdi,
    tedy na souradnicich [0][x], [rows - 1][x], [y][0] a [y][cols - 1] je vzdy
    zed (WALL) pro vsechna x, y.

    K textovemu vykreslovani bludiste muzete pouzit funkci print_maze
    (definovanou na zacatku testu nize); funkce bere jeden parametr typu Maze.
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.map = [[EMPTY] * cols for row in range(rows)]
        for row in range(rows):
            self.map[row][0] = WALL
            self.map[row][cols - 1] = WALL
        for col in range(cols):
            self.map[0][col] = WALL
            self.map[rows - 1][col] = WALL

# Priklad bludiste s indexy:
# Nasledujici bludiste ma rows = 9, cols = 17, matice ma tedy rozmery 9x17 a
# obsahuje indexy radku 0..8 a indexy sloupcu 0..16. Na indexech [0][.],
# [8][.], [.][0], [.][16] se tedy zarucene nachazeji zdi.
#
#           sloupce
#                 1111111
#       01234567890123456
#     0 #################
#     1 #.......#.......#
#   r 2 #.#######.##.##.#
#   a 3 #.#.....#.#..$#.#     na pozici [3][13] se nachazi znak TREASURE
#   d 4 #.#.###.#.##.##.#
#   k 5 #.#...#.#.......#
#   y 6 #.#####.#######.#
#     7 #.......#..?....#     na pozici [7][11] se nachazi znak START
#     8 #################

# Pripomenuti prace s dvourozmernymi maticemi a dvojicemi:
# - indexovani 2D matice:
#     maze.map[y][x]    # prvni souradnice je radek, druha sloupec
# - vytvoreni 2D matice obsahujici same hodnoty False
#     [[False] * pocet_sloupcu for y in range(pocet_radku)]
#   nebo
#     [[False for x in range(pocet_sloupcu)] for y in range(pocet_radku)]
# - ulozeni dvojice hodnot do promenne
#     x = (a, b)        # zavorky je mozno vynechat
# - rozbaleni dvojice (predpokladame, ze x obsahuje dvojici hodnot)
#     (a, b) = x        # zavorky je mozno vynechat
#   (misto x muze byt i volani funkce f(), indexovani seznamu s[i] apod.)
# - vytvoreni seznamu obsahujiciho dvojici
#     s = [(a, b)]      # zde jsou zavorky nutne
# - pridani dvojice na konec seznamu
#     s.append((a, b))  # zde jsou zdvojene zavorky nutne!


# Ukol 1. (15 bodu)
# Implementujte funkce neigbours (5 bodu) a count_directions (10 bodu).
# Funkce neighbours vrati k zadanym souradnicim seznam souradnic vsech
# sousedu, napr. sousede (1, 3) jsou (0, 3), (1, 2), (2, 3), (1, 4);
# ve vyslednem seznamu mohou byt v libovolnem poradi.
# Funkce count_directions kazde prazdne misto (EMPTY) v matici bludiste nahradi
# cislem od 0 do 4 reprezentujicim pocet smeru, kterymi se z daneho mista da
# odejit.
#
# Priklad:
#   vstup       vysledne bludiste
#  #######          #######
#  #...###   --->   #231###
#  #..##.#          #22##0#
#  #######          #######

def neighbours(row, col):
    """
    vstup: souradnice row (radek) a col (sloupec)
           zadane souradnice zarucene neoznacuji okrajove misto bludiste
    vystup: seznam souradnic vsech ctyr sousedu
            (Pythonovsky seznam dvojic, na poradi nezalezi)
    casova slozitost: O(1)

    Poznamka: Tato funkce se vam hodi i v dalsich ukolech.
    """
    return [(row, col - 1), (row + 1, col), (row, col + 1), (row - 1, col)]


def count_directions(maze):
    """
    vstup: maze - korektni bludiste typu Maze
    vystup: zadna navratova hodnota,
            v bludisti maze se zmeni vsechna prazdna mista
            na cislo reprezentujici pocet moznych odchozich smeru (0 az 4)
    casova slozitost: O(n), kde n je celkovy pocet pozic v bludisti
        (tedy n = rows * cols)
    extrasekvencni prostorova slozitost: O(1)
        (nepocitame velikost vstupniho bludiste, ktere zaroven modifikujeme)
    """
    for y in range(maze.rows):
        for x in range(maze.cols):
            if maze.map[y][x] == EMPTY:
                maze.map[y][x] = 0
                adj = neighbours(y, x)
                for (row, col) in adj:
                    if maze.map[row][col] != WALL:
                        maze.map[y][x] += 1


# Ukol 2. (20 bodu)
# Implementuje funkci separate_areas, ktera vrati pocet oddelenych oblasti
# bludiste, tj. takovych, mezi kterymi se vzajemne neda prechazet.
#
# Priklad:
#  jedna oddelena oblast     dve oddelene oblasti     zadna oddelena oblast
#        ########                ########                   ########
#        #.###..#                #...#.##                   ########
#        #......#                #.#.#.##                   ########
#        #.#.##.#                #...#..#                   ########
#        ########                ########                   ########

def separate_areas(maze):
    """
    vstup: maze - korektni bludiste typu Maze
    vystup: pocet oddelenych oblasti v bludisti
            (vstupni bludiste nijak nemodifikujte)
    casova slozitost: O(n), kde n je celkovy pocet pozic v bludisti
        (tedy n = rows * cols)
    """
    maze_inner = [[NOT_VISITED] * maze.cols for row in range(maze.rows)]
    queue = deque()
    areas = 0

    for row in range(maze.rows):
        for col in range(maze.cols):
            if maze.map[row][col] != WALL and maze_inner[row][col] == NOT_VISITED:
                maze_inner[row][col] = FOUND
                queue.append((row, col))
                areas += 1
            while len(queue) != 0:
                (y, x) = queue.pop()
                adj = neighbours(y, x)
                for (a_row, a_col) in adj:
                    if maze_inner[a_row][a_col] == NOT_VISITED and maze.map[a_row][a_col] != WALL:
                        maze_inner[a_row][a_col] = FOUND
                        queue.append((a_row, a_col))

    return areas  # TODO


# Ukol 3. (30 bodu)
# Implementujte funkci has_loop, ktera zjisti, zda bludiste obsahuje smycku.
# Smyckou v bludisti zde nazyvame situaci, kdy muzeme vyjit z nektereho volneho
# mista a zase se do nej vratit, pricemz po ceste nenavstivime zadne misto
# vicekrat. Za smycku ovsem nepovazujeme pouhy krok na vedlejsi misto a zpet.
#
# Priklady:                                     #####  #####
#                                  ####  #####  #...#  #...#
# Tato bludiste neobsahuji smycku: #..#  #...#  #.#.#  ##.##
#                                  ####  #####  #####  #...#
#                                                      #####
#                                  #####        #####
#                                  #...#  ####  #.###
# Tato bludiste obsahuji smycku:   #.#.#  #..#  #..##
#                                  #...#  #..#  #...#
#                                  #####  ####  #####

def has_loop(maze):
    """
    vstup: maze - korektni bludiste typu Maze
    vystup: True/False, podle toho, zda ma zadane bludiste smycku
            (vstupni bludiste nijak nemodifikujte)
    casova slozitost: O(n), kde n je celkovy pocet pozic v bludisti
        (tedy n = rows * cols)
    """
    maze_inner = [[NOT_VISITED] * maze.cols for row in range(maze.rows)]
    default = None

    def deep_search(row, col, source):
        maze_inner[row][col] = FOUND

        for (y, x) in neighbours(row, col):
            if maze_inner[y][x] == FOUND and (y, x) != source:
                return True
            if maze_inner[y][x] == NOT_VISITED and maze.map[y][x] == EMPTY:
                if deep_search(y, x, (row, col)):
                    return True
        return False

    for row in range(maze.rows):
        for col in range(maze.cols):
            if maze_inner[row][col] == NOT_VISITED and maze.map[row][col] != WALL:
                if deep_search(row, col, (row, col)):
                    return True
    return False  # TODO


# Ukol 4. (15 + 20 bodu)
# Implementuje funkci find_treasure, ktera v bludisti najde nejkratsi cestu
# od pocatecni pozice (zadane znakem START) k nejblizsimu pokladu (zadanemu
# znakem TREASURE).
# Bludiste zarucene obsahuje presne jeden znak START a muze obsahovat libovolny
# (vcetne 0) pocet znaku TREASURE.
# Zadana funkce jednak vrati delku cesty (15 bodu), jednak cestu do bludiste
# vykresli (20 bodu).
#
# K vykresleni cesty pouzijte symbol PATH, pricemz tento symbol piste pouze do
# volnych mist na nejkratsi ceste z pocatecniho mista k pokladu, symboly START
# a TREASURE ponechte v puvodnim stavu.
# Pokud zadna cesta k pokladu neexistuje, funkce vrati None.
#
# Priklad:
#     vstup        vysledne bludiste
#   #########          #########
#   #.?..##.#          #.?**##.#
#   #.##.#.$#   --->   #.##*#.$#    navratova hodnota je 10
#   #..#.##.#          #..#*##*#
#   ##......#          ##..****#
#   #########          #########

def find_start(maze):
    for row in range(maze.rows):
        for col in range(maze.cols):
            if maze.map[row][col] == START:
                return (row, col)
    return None

class Node:
    def __init__(self):
        self.found = 0
        self.dist = inf
        self.p = None

def find_treasure(maze):
    """
    vstup: maze - korektni bludiste typu Maze, ktere navic obsahuje
           prave jednu pozici se znakem START
           0 nebo vice pozic se znakem TREASURE
    vystup: delka nejkratsi cesty od START k nejblizsimu TREASURE
            nebo None, pokud zadna takova cesta neexistuje;
            v bludisti 'maze' se vykresli nejkratsi cesta od znaku START
            k nejblizsimu znaku TREASURE; vykreslena bude pomoci znaku PATH
            (vstupni bludiste nijak nemodifikujte)
    casova slozitost: O(n), kde n je celkovy pocet pozic v bludisti
        (tedy n = rows * cols)
    """
    start = find_start(maze)
    if start is None:
        return None

    (row, col) = start

    maze_inner = [[inf] * maze.cols for row in range(maze.rows)]
    queue = deque()
    dist = inf

    maze_inner[row][col] = 0
    queue.append((row, col))
    while len(queue) != 0:
        (row, col) = queue.popleft()
        for (y, x) in neighbours(row, col):
            if maze_inner[row][col] + 1 < maze_inner[y][x] and maze.map[y][x] != WALL:
                maze_inner[y][x] = maze_inner[row][col] + 1
                # maze.map[y][x] = PATH
                queue.append((y, x))
                if maze.map[y][x] == TREASURE and maze_inner[y][x] < dist:
                    dist = maze_inner[y][x]

    if dist == inf:
        return None  # TODO
    return dist


########################################################################
#               Nasleduje kod testu, NEMODIFIKUJTE JEJ                 #
#######################################################################
test_maze = Maze(3, 4)
test_maze.map[1][1] = EMPTY
test_maze.map[1][2] = EMPTY

has_loop(test_maze)


def print_maze(maze):
    """
    Funkce print_maze textove vykresli bludiste na standardni vystup
    vcetne indexu radku a sloupcu.
    """
    if maze.cols > 10:
        print(" " * 14 +
              "".join(str(x // 10) for x in range(10, maze.cols)))
    print(" " * 4 + "".join(str(x % 10) for x in range(maze.cols)) +
          "  rows = {}, cols = {}".format(maze.rows, maze.cols))
    for y, row in enumerate(maze.map):
        print(" {:2} ".format(y) + "".join(map(str, row)))


class Ib002TestCase:
    from copy import deepcopy as _copy

    def __init__(self, rows, cols, areas, loop, maze_code, dir_code):
        self.maze, self.dir_maze = \
            Ib002TestCase._decode(rows, cols, maze_code, dir_code)
        self.areas = areas
        self.loop = loop
        self.t_cases = []

    @staticmethod
    def _decode(rows, cols, code, dir_code):
        import base64
        code, dir_code = map(base64.b85decode, (code, dir_code))
        pos = dir_pos = 0
        maze, dir_maze = Maze(rows, cols), Maze(rows, cols)

        for row in range(1, rows - 1):
            for col in range(1, cols - 1):
                place = EMPTY if code[pos // 8] & (1 << (pos % 8)) else WALL
                dir_maze.map[row][col] = maze.map[row][col] = place

                if place == EMPTY:
                    dir_maze.map[row][col] = \
                        dir_code[dir_pos // 3] // (5 ** (dir_pos % 3)) % 5
                    dir_pos += 1

                pos += 1

        return maze, dir_maze

    def add_treasure_case(self, path_len, *t_case):
        start, *treasures = map(lambda x: divmod(x, self.maze.cols), t_case)
        self.t_cases.append((path_len, start, treasures))
        return self  # allow chaining

    def clone_maze(self):
        return Ib002TestCase._copy(self.maze)

    def treasure_cases(self):
        for path_len, *t_case in self.t_cases:
            maze = self.clone_maze()
            Ib002TestCase.apply_treasure_case(maze, *t_case)
            clone = Ib002TestCase._copy(maze)
            yield maze, clone, path_len

    @staticmethod
    def apply_treasure_case(maze, start, treasures):
        row, col = start
        maze.map[row][col] = START
        for row, col in treasures:
            maze.map[row][col] = TREASURE


IB002_CASES = [
    Ib002TestCase(9, 17, 2, True, b'fB%4FU$-dP^$!C6{Q&',
                  b'ySqI@K0ZD^Yq~zWCA&jIySuwRyMF')
    .add_treasure_case(12, 130, 64)
    .add_treasure_case(None, 24, 62),
    Ib002TestCase(4, 7, 2, True, b'X95', b'Dhv'),
    Ib002TestCase(3, 4, 1, False, b'0{', b'1^'),
    Ib002TestCase(3, 5, 1, False, b'2L', b'Bm'),
    Ib002TestCase(4, 5, 1, False, b'F8', b'J_Y'),
    Ib002TestCase(5, 5, 1, False, b'*8u', b'rq2N'),
    Ib002TestCase(5, 5, 1, True, b'?*R', b'ySoe'),
    Ib002TestCase(4, 4, 1, True, b'4*', b'J^}'),
    Ib002TestCase(5, 5, 1, True, b'*#Q', b'LMi'),
    Ib002TestCase(5, 8, 1, True, b'@m~S', b'y474C'),
    Ib002TestCase(5, 8, 2, True, b'S9Jp', b'yShFl'),
    Ib002TestCase(6, 9, 1, True, b'&-Bs{', b'yS7q3K0g8')
    .add_treasure_case(10, 11, 25),
    Ib002TestCase(4, 4, 1, True, b'4*', b'J^}')
    .add_treasure_case(2, 5, 10)
    .add_treasure_case(2, 6, 9),
    Ib002TestCase(8, 16, 1, True, b'|NsC0`~Uv`|Njp',
                  b'+1g!QSbSrAeDi$seA|3p`QZ3``1wU$U0q!Q')
    .add_treasure_case(4, 54, 17, 25, 60, 67, 88, 98)
    .add_treasure_case(6, 20, 42, 46, 81, 91, 101)
    .add_treasure_case(6, 109, 28, 33),
    Ib002TestCase(11, 11, 4, True, b'{`&5|{{H&zzWx9',
                  b'*xERJQgByEZ}TGHN$f;Or}v~=+I|')
    .add_treasure_case(None, 16, 57, 63, 93)
    .add_treasure_case(None, 104, 27, 58, 62)
    .add_treasure_case(None, 56, 38, 61, 82)
    .add_treasure_case(None, 64, 49, 59, 71)
    .add_treasure_case(6, 31, 13, 19, 23, 25, 29, 35, 37, 39, 47, 69, 79, 81,
                       83, 89, 91, 95, 97, 101, 107),
    Ib002TestCase(8, 16, 2, True, b'{r>`3|8ARY>+KH',
                  b'&bvN7Dm^?zE2me$KD#PDw%EV|')
    .add_treasure_case(19, 17, 19, 51, 92, 101)
    .add_treasure_case(30, 36, 34, 102),
    Ib002TestCase(5, 7, 0, False, b'000', b''),
    Ib002TestCase(3, 3, 1, False, b'0R', b'00')
    .add_treasure_case(None, 4),
    Ib002TestCase(3, 4, 1, False, b'0{', b'1^')
    .add_treasure_case(1, 5, 6),
    Ib002TestCase(3, 3, 0, False, b'00', b''),
    Ib002TestCase(3, 16, 0, False, b'000', b''),
    Ib002TestCase(16, 3, 0, False, b'000', b''),
    Ib002TestCase(12, 17, 1, True, b'|NsC0|NsC0|NsC0|NsC0|NlP',
                  b'+1g!QM0<REeBgWeeEDO0`T6-{`1yQ%V|#pjeBgWeeEDO0`T6-{`1'
                  b'yQ%V_aQbUBL')
    .add_treasure_case(23, 18, 185)
    .add_treasure_case(7, 32, 61, 88, 128, 158)
    .add_treasure_case(10, 171, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                       30, 31, 49, 66, 83, 100, 117, 134, 151, 168),
    Ib002TestCase(12, 17, 1, False, b'KJRgzhG~A?z`d_>)kj-?>E$l',
                  b'yP`iJKRrWMJ-a@(KGQx!z`MIS)V5JRSVKNJJ-i_')
    .add_treasure_case(63, 42, 55)
    .add_treasure_case(43, 62, 40, 89),
    Ib002TestCase(12, 17, 2, False, b'*Y&>ZvbL7`daYHj^LnZ&@B11',
                  b'ySh0(Tth!9J<cV%J?>URy3U<f&bvfwDj+#=J)%OQ3j')
    .add_treasure_case(53, 98, 173)
    .add_treasure_case(12, 181, 139, 151, 167, 183),
    Ib002TestCase(12, 17, 1, False, b'z169|UvjBh|1DMd%A>tsmGV6',
                  b'wVoh7Qe0SAShgjiJ<eTSox7bvywo{9SVBJ_Aip7_')
    .add_treasure_case(25, 100, 171)
    .add_treasure_case(21, 137, 18, 32, 151, 185),
    Ib002TestCase(12, 17, 1, True, b'+}=C??#Po=PU`o6+kXTn{_i~',
                  b'yS7ADTwGmONV`|OB-B4#^X~Fo;M7-jURNwwMA;y_Tz>')
    .add_treasure_case(42, 25, 185)
    .add_treasure_case(22, 138, 116),
    Ib002TestCase(12, 17, 8, True, b'|Nji2et#g4*DnZGb*qL&)cz{',
                  b'yTLv_K3h3ICA&VNCAK~}yS1S{y1FGKK0`hR')
    .add_treasure_case(28, 146, 62)
    .add_treasure_case(None, 53, 35, 55),
    Ib002TestCase(12, 17, 1, True, b'{r!S+e>T-xGVQ+>K>NRe!2dr',
                  b'y1PDCJ~=;FL%KPkKDs|cz}dP!ySqa^K0ZD^Kf4S')
    .add_treasure_case(44, 45, 23)
    .add_treasure_case(29, 18, 24, 63, 79),
    Ib002TestCase(19, 19, 1, True,
                  b'|NjF3_WvzFTK}~IYW3ABs#RC3s8(OCf?EHz0BHZ;Ab|h>0R',
                  b'ySqL<K0ZD^KGZ(DKD$0Xyt}(TySqL<K0ZEHKD$1<SGztwySuwTyS'
                  b'qL<K0iJ_KD$1^KD#~')
    .add_treasure_case(82, 28, 180)
    .add_treasure_case(74, 144, 20, 36)
    .add_treasure_case(26, 140, 60, 72, 288, 300),
]

IB002_N_CASES = [(18, 1, 17, 35, 19), (27, 10, 26, 44, 28),
                 (171, 154, 170, 188, 172), (180, 163, 179, 197, 181),
                 (60, 43, 59, 77, 61), (209, 192, 208, 226, 210),
                 (128, 111, 127, 145, 129), (62, 45, 61, 79, 63),
                 (77, 60, 76, 94, 78), (179, 162, 178, 196, 180),
                 (183, 166, 182, 200, 184), (243, 226, 242, 260, 244),
                 (151, 134, 150, 168, 152), (182, 165, 181, 199, 183),
                 (27, 10, 26, 44, 28), (105, 88, 104, 122, 106),
                 (173, 156, 172, 190, 174), (202, 185, 201, 219, 203)]


def ib002_test_report(ok, basic):
    if ok:
        print("[ OK ] {} prosel.".format("Zakladni test" if basic else "Test"))
    elif basic:
        print("[FAIL] Zakladni test neprosel.",
              "Tato cast bude automaticky hodnocena 0 body.")
    else:
        print("[FAIL] Test neprosel.")


def ib002_test_header(msg, basic):
    print("\n*** {} {}:".format("Zakladni test" if basic else "Test", msg))


def ib002_report_mazes(orig=None, result=None, correct=None):
    if orig is not None:
        print("Vstupni bludiste:")
        print_maze(orig)

    if result is not None:
        print("Bludiste po spusteni Vaseho kodu:")
        print_maze(result)

    if correct is not None:
        print("Spravne reseni melo vypadat takto:")
        print_maze(correct)


def ib002_test_neighbours():
    ib002_test_header("neighbours", basic=True)
    print("    (tato funkce ma pouze zakladni testy)")

    ok = True
    for pos, *npos in IB002_N_CASES:
        ok = False
        pos = divmod(pos, 17)
        npos = set(divmod(x, 17) for x in npos)

        result = neighbours(*pos)

        if not isinstance(result, list):
            print("Volani neighbours{} nevraci seznam.".format(pos))
            break

        if set(result) != npos:
            print("Volani neigbours{} vraci {}, coz neni seznam sousedu."
                  .format(pos, result))
            break

        ok = True

    ib002_test_report(ok, basic=True)


def ib002_test_count_directions(case):
    maze = case.clone_maze()
    count_directions(maze)
    for y, row in enumerate(maze.map):
        for x, place in enumerate(row):
            correct_place = case.dir_maze.map[y][x]
            if place != correct_place:
                print("Spatna hodnota na pozici {}.".format((y, x)))
                ib002_report_mazes(orig=case.maze,
                                   result=maze, correct=case.dir_maze)
                return False
    return True


def ib002_test_template(case, fun, correct):
    maze = case.clone_maze()
    result = fun(maze)
    if maze.map != case.maze.map:
        print("Chyba! Doslo k modifikaci vstupniho bludiste.")
        ib002_report_mazes(orig=case.maze, result=maze)
        return False

    if result != correct:
        print("Spatna odpoved {}, spravna mela byt {}."
              .format(result, correct))
        ib002_report_mazes(orig=case.maze)
        return False

    return True


def ib002_test_has_loop(case):
    return ib002_test_template(case, has_loop, case.loop)


def ib002_test_separate_areas(case):
    return ib002_test_template(case, separate_areas, case.areas)


def ib002_test_find_treasure_len(case):
    for maze, clone, path_len in case.treasure_cases():
        result = find_treasure(maze)
        if result != path_len:
            print("Funkce vraci {}, ale mela vratit {}."
                  .format(result, path_len))
            ib002_report_mazes(orig=clone)
            return False

    return True


def ib002_test_find_treasure_draw(case):
    ok = True
    for maze, clone, path_len in case.treasure_cases():
        find_treasure(maze)
        if path_len is None and clone.map != maze.map:
            print("Doslo k modifikaci vstupniho bludiste v situaci,",
                  "kdy zadna cesta k pokladu neexistuje.")
            ok = False
            break
        elif path_len is not None and \
                not ib002_check_shortest_path(clone, maze, path_len):
            ok = False
            break

    if not ok:
        ib002_report_mazes(orig=clone, result=maze)

    return ok


def ib002_check_shortest_path(orig_maze, maze, path_len):
    count, specials = 0, 0

    for y, row in enumerate(maze.map):
        for x, place in enumerate(row):
            orig_place = orig_maze.map[y][x]
            if place != PATH:
                if place != orig_place:
                    print("Doslo ke zmene mista na pozici {}.".format((y, x)))
                    return False
                continue

            if orig_place != EMPTY:
                print("{} na pozici {}.".format(
                    "Cesta vede pres zed" if orig_place == WALL else
                    "Poklad je prepsan znakem cesty" if orig_place == TREASURE
                    else "Pocatecni misto je prepsano znakem cesty", (y, x)))
                return False

            count += 1
            connects = 0

            for dy, dx in (0, -1), (0, 1), (-1, 0), (1, 0):
                n = maze.map[y + dy][x + dx]
                if n in (PATH, START, TREASURE):
                    connects += 1
                    if n != PATH:
                        specials += 1

            if connects != 2:
                print("Cesta {} na pozici {}."
                      .format("se vetvi" if connects > 2 else "je slepa",
                              (y, x)))
                return False

    if path_len != 1 and count == 0:
        print("V bludisti neni zakreslena zadna cesta.")
        return False

    if specials != 2 and path_len != 1:
        print("Cesta nespojuje pocatecni pozici s pokladem.")
        return False

    if count != path_len - 1:
        print("Zakreslena cesta neni nejkratsi cestou k nejblizsimu pokladu.")
        return False

    return True


def ib002_run_test(test, msg):
    # basic
    ib002_test_header(msg, basic=True)
    result = ib002_try_test(test, IB002_CASES[0])
    ib002_test_report(ok=result, basic=True)

    if not result:
        return

    # extended
    ib002_test_header(msg, basic=False)
    for i in range(1, len(IB002_CASES)):
        if not ib002_try_test(test, IB002_CASES[i]):
            ib002_test_report(ok=False, basic=False)
            return

    ib002_test_report(ok=True, basic=False)


def ib002_try_test(test, *args):
    import traceback
    import sys
    try:
        return test(*args)
    except Exception:
        print("Test vyhodil vyjimku:")
        traceback.print_exc(file=sys.stdout)
        return False


def ib002_main():
    ib002_test_neighbours()  # basic only
    for test, msg in ((ib002_test_count_directions, "count_directions"),
                      (ib002_test_separate_areas, "separate_areas"),
                      (ib002_test_has_loop, "has_loop"),
                      (ib002_test_find_treasure_len,
                       "find_treasure (delka cesty)"),
                      (ib002_test_find_treasure_draw,
                       "find_treasure (nakresleni cesty)")):
        ib002_run_test(test, msg)


if __name__ == '__main__':
    ib002_main()
