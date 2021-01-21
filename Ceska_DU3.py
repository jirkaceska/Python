from random import randint


class Stone:
    def __init__(self, path, start, owner, home):
        self.__coor = None
        self.__position = None
        self.__distance_to_home = len(path)
        self.__start = start
        self.__path = path
        self.__home = home
        self.__owner = owner
        self.__value = 0

    def __get_endangered_stone(self, new_coor):
        for player in self.__owner.board.get_players():
            for stone in player.get_stones_in_game():
                if self != stone and new_coor == stone.get_coors():
                    return stone
        return None

    def __get_end_coors(self, new_pos):
        return self.__path[(self.__start + self.__position + new_pos) % len(self.__path)]

    def __go_to_home(self, dice_sum):
        home_i = self.__position + dice_sum - self.__distance_to_home
        self.set_coors(self.__home[home_i])
        self.__owner.move_stone_to_home(self)

    def count_move_value(self, dice_sum):
        value = self.__position
        if self.can_go_home(dice_sum):
            value += 1000
        endangered_stone = self.__get_endangered_stone(self.__get_end_coors(dice_sum))
        if endangered_stone:
            if endangered_stone in self.__owner.get_stones_in_game():
                value -= 100
            else:
                value += 100
        self.__value = value

    def stone_move(self, dice_sum):
        if self.can_go_home(dice_sum):
            self.__go_to_home(dice_sum)
            return
        if self.can_follow_path(dice_sum):
            self.__position += dice_sum
            self.set_coors(self.__path[(self.__start + self.__position) % len(self.__path)])

    def can_follow_path(self, dice_sum):
        return self.__position + dice_sum - self.__distance_to_home < 0

    def can_go_home(self, dice_sum):
        diff = self.__position + dice_sum - self.__distance_to_home
        if len(self.__home) > diff >= 0:
            for stone in self.__owner.finished_stones:
                if stone.get_coors() == self.__home[diff]:
                    return False
            return True
        return False

    def set_coors(self, new_coor):
        self.__coor = new_coor
        if new_coor:
            deleted = self.__get_endangered_stone(new_coor)
            if deleted:
                deleted.remove_from_game()
                print(self.__owner.get_name(), "removed", deleted.get_owner().get_name())

    def get_to_game(self):
        self.set_coors(self.__path[self.__start])
        self.set_position(0)

    def remove_from_game(self):
        self.set_coors(None)
        self.set_position(None)
        self.__owner.remove_stone_from_game(self)

    def get_coors(self):
        return self.__coor

    def set_position(self, new_pos):
        self.__position = new_pos

    def get_position(self):
        return self.__position

    def get_owner(self):
        return self.__owner

    def get_value(self):
        return self.__value


class Player:
    colors = ["\033[1;31m", "\033[1;34m", "\033[1;36m", "\033[0;32m"]
    reverse_color = "\033[0m"

    def __init__(self, stones_count, start, player_num, size, path, game_board):
        self.__board_size = size
        self.board = game_board
        self.__start = start
        self.__color = Player.colors[player_num]
        self.__char = chr(ord("A") + player_num)
        self.__path = path
        self.__stone_on_start = False
        self.stones_in_game = []
        self.finished_stones = []
        self.shift = 0
        self.waiting_stones = [Stone(path, start, self, self.__home()) for _ in range(stones_count)]

    def get_name(self):
        return self.__color + self.__char + Player.reverse_color

    def __sort_stones_by_value(self):
        if len(self.stones_in_game) > 1:
            for stone in self.stones_in_game:
                stone.count_move_value(self.shift)
            self.stones_in_game.sort(key=lambda i: i.get_value(), reverse=True)

    def __get_stone_index(self, stone):
        if stone in self.stones_in_game:
            return self.stones_in_game.index(stone)

    def __home(self):
        end = self.__path[self.__start - 1]
        if end[0] == self.__board_size - 1 or end[0] == 0:
            if end[0] == self.__board_size - 1:
                home = [(i, end[1]) for i in range(self.__board_size - 2, self.__board_size // 2, - 1)]
            else:
                home = [(i, end[1]) for i in range(1, self.__board_size // 2)]
        else:
            if end[1] == self.__board_size - 1:
                home = [(end[0], i) for i in range(self.__board_size - 2, self.__board_size // 2, - 1)]
            else:
                home = [(end[0], i) for i in range(1, self.__board_size // 2)]
        return home

    def __roll_dice(self):
        dice_num = randint(1, 6)
        print(self.get_name(), "rolled", dice_num)
        self.shift += dice_num

    def __move_with_stone(self):
        if self.__stone_on_start:
            self.stones_in_game[-1].stone_move(self.shift)
        else:
            self.__sort_stones_by_value()
            for stone in self.stones_in_game:
                if stone.can_go_home(self.shift) or stone.can_follow_path(self.shift):
                    stone.stone_move(self.shift)
                    break
        self.shift = 0
        self.__stone_on_start = False

    def roll_six(self):
        if len(self.waiting_stones) > 0 and not self.__stone_on_start:
            stone_in_game = self.waiting_stones.pop()
            stone_in_game.get_to_game()
            self.stones_in_game.append(stone_in_game)
            self.__stone_on_start = True
            self.shift = 0
            return True
        else:
            self.player_move()

    def player_move(self):
        self.__roll_dice()
        if self.shift == 6:
            if self.roll_six():
                self.player_move()
            return
        elif len(self.stones_in_game) > 0:
            if self.shift % 6 == 0:
                # Roll again on 6
                self.player_move()
                return
            else:
                self.__move_with_stone()
        elif len(self.waiting_stones) > 0:
            # All stones were throw up or are in home
            for i in range(2):
                self.shift = 0
                self.__roll_dice()
                if self.shift == 6:
                    if self.roll_six():
                        self.player_move()
                        return
            self.shift = 0
            print(self.get_name(), "must wait for 6 to next turn!")
            return
        if len(self.stones_in_game) + len(self.waiting_stones) == 0:
            # End of game
            self.board.finished = True
            print(self.get_name(), "HAS WON!")

    def remove_stone_from_game(self, stone):
        self.waiting_stones.append(self.stones_in_game.pop(self.__get_stone_index(stone)))

    def move_stone_to_home(self, stone):
        self.finished_stones.append(self.stones_in_game.pop(self.__get_stone_index(stone)))

    def get_stones_in_game(self):
        return self.stones_in_game

    def get_stones_coors(self):
        coors = []
        for stone in self.stones_in_game + self.finished_stones:
            coors.append(stone.get_coors())
        return coors


class GameBoard:
    def __init__(self, size, player_count=0):
        self.finished = False
        self.__size = size
        self.__path = []
        self.__move_counter = 0
        self.__gen_path()
        self.__end = False
        self.__player_count = player_count
        self.__players = [
            # Player(stones_count,          start,                     player_num, size, path,        game_board)
            Player(size // 2 - 1, 2 + int(i * len(self.__path) / player_count), i, size, self.__path, self)
            for i in range(player_count)
        ]

    def get_players(self):
        return self.__players

    def __gen_path(self):
        counter = 0
        self.__path.append((0, self.__size // 2 - 1))
        while not ((1, self.__size // 2 - 1) in self.__path):
            if counter % 3 == 0:
                self.__edge(self.__path[-1], counter)
            else:
                self.__leg(self.__size, self.__path[-1], counter)
            counter += 1

    def __edge(self, start, counter):
        # Ensure correct direction
        alter = 1 if (counter // 6) % 2 == 0 else -1
        for i in range(3):
            if counter % 2 == 0:
                self.__append_to_path((start[0], start[1] + alter * i))
            else:
                self.__append_to_path((start[0] + alter * i, start[1]))

    def __leg(self, n, start, counter):
        # Ensure correct direction
        alter = -1 if ((counter + 4) // 6) % 2 == 0 else 1
        # Odd/even leg
        alter *= -1 if counter % 3 == 1 else 1
        for i in range(n // 2):
            if counter % 2 == 0:
                self.__append_to_path((start[0], start[1] + alter * i))
            else:
                self.__append_to_path((start[0] + alter * i, start[1]))

    def __append_to_path(self, el):
        if el not in self.__path:
            self.__path.append(el)

    def start(self):
        for player in self.__players:
            player.roll_six()

        while not self.finished:
            self.__board_move()
            self.print_path()
            input("Press Enter to continue...")

    def __board_move(self):
        player = self.__players[self.__move_counter % self.__player_count]
        player.player_move()
        self.__move_counter += 1

    def print_path(self):
        middle = self.__size // 2
        for i in range(self.__size):
            for j in range(self.__size):
                if (i, j) in self.__path:
                    if not self.print_player(i, j):
                        print("*", end="")
                elif (i == middle and not j == middle) or (j == middle and not i == middle):
                    if not self.print_player(i, j):
                        print("D", end="")
                else:
                    print(" ", end="")
            print()

    def print_player(self, i, j):
        player_printed = False
        for player in self.__players:
            if (i, j) in player.get_stones_coors():
                print(player.get_name(), end="")
                player_printed = True
        return player_printed


board = GameBoard(11, 3)
board.start()
