import random

class BoardOutException(Exception):
    pass

class Dot:
    def __init__(self, x, y):
        if not(x<=6 and x>=1 and y<=6 and y>=1):
            print(f'Координаты должны быть от 1 до 6. Вы ввели {x} и {y}')
            raise BoardOutException('Координаты должны быть от 1 до 6')
        self.x = x
        self.y = y

    def __eq__(self, other):
        if (self.x == other.x and self.y == other.y):
            return True
        else:
            return False

class Ship:
    def __init__(self, length, dot, direct, life):
        self.length = length
        self.dot = dot
        self.direct = direct
        self.life = life

    def dots(self):
        L=[]
        for i in range(self.length):
            if self.direct == 0:
                L.append(Dot(self.dot.x+i,self.dot.y))
            else:
                L.append(Dot(self.dot.x, self.dot.y + i))
        return L

class Board:
    def __init__(self, board_all, list_ships, hid, list_life):
        self.board_all = board_all
        self.list_ships = list_ships
        self.hid = hid
        self.list_life = list_life


    def add_ship(self, len):
        while True:
            x, y = random.randint(0,5), random.randint(0,5)
            gor_vert = random.randint(0,1)
            if gor_vert == 0:
                if x+len-1 > 5:
                    continue
            else:
                if y+len-1 > 5:
                    continue
            ship = Ship(len,Dot(x+1, y+1), gor_vert, len)
            if self.check_ship_free(ship) == True:

                break
        return ship


    def check_ship_free(self, ship):
        l = ship.dots()

        for dot in l:
            if self.board_all[dot.x-1][dot.y-1] != 'O':
                return False
        return True


    def contur(self, ship):
        l = ship.dots()
        for dot in l:
            x = dot.x -1
            y = dot.y -1
            if x >0:
                self.board_all[x-1][y] = 'T'
                if y > 0:
                    self.board_all[x - 1][y - 1] = 'T'
            if y >0:
                self.board_all[x][y-1] = 'T'
                if x < 5:
                    self.board_all[x+1][y -1] = 'T'
            if x <5:
                self.board_all[x+1][y] = 'T'
                if y < 5:
                    self.board_all[x + 1][y + 1] = 'T'
            if y <5:
                self.board_all[x][y+1] = 'T'
                if x > 0:
                    self.board_all[x - 1][y+1] = 'T'
        l = ship.dots()
        for d in l:
            self.board_all[d.x - 1][d.y - 1] = 'X'


    def show_board(self):
        l_ships_dots = []
        if self.hid == True:
            for sh in self.list_ships:
                l_ships_dots+=sh.dots()

        print('  |1|2|3|4|5|6|')
        for i in range(1,7):
            print(i , '|', end='')
            for j in range(1,7):
                if (Dot(i, j) in l_ships_dots) and (self.board_all[i-1][j-1] == 'O'):
                    print('■'+ '|', end='')
                else:
                    print(self.board_all[i-1][j-1] + '|', end='')
            print()


    def shot(self, d):
        try:
            l_ships_dots = []
            for sh in self.list_ships:
                l_ships_dots += sh.dots()

            x, y = d.x,d.y

            if (d in l_ships_dots) and self.board_all[x-1][y-1] == 'O':
                self.board_all[x - 1][y - 1] = 'X'
                for sh in self.list_ships:
                     if d in sh.dots():
                        sh.life-=1
                        if sh.life == 0:
                            self.list_life-=1
                            self.contur(sh)
                            print('Корабль убит!')
                            return True
                        else:
                            print('Корабль ранен!')
                            return True
                        break
            elif (d in l_ships_dots) and self.board_all[x-1][y-1] == 'X':
                raise BoardOutException
            elif self.board_all[x-1][y-1] == 'T':
                raise BoardOutException
            else:
                self.board_all[x - 1][y - 1] = 'T'
                print('Мимо!')
        except BoardOutException:
            print('Сюда уже был выстрел')
            return True
        return False

class Player:
    def __init__(self, board1, board2):
        self.board1 = board1
        self.board2 = board2

    def ask(self):
        pass

    def move(self):

        dot = self.ask()
        trueFalse = self.board2.shot(dot)
        return trueFalse


class AI(Player):
    def ask(self):
        x, y = random.randint(1,6), random.randint(1,6)
        return Dot(x, y)


class User(Player):
    def ask(self):
        while True:
            try:
                d = input('Введите координаты. Два числа через пробел: ').split()
                if len(d) != 2:
                    print(f'Ввели всего один элемент {d[0]}. Нужно два.')
                    raise BoardOutException
                if not (d[0].isdigit() and d[1].isdigit()):
                    print(f'Нужно ввести два числа. А у вас: {d[0]} и {d[1]}')
                    raise BoardOutException
                x, y = map(int, d)
                dot =Dot(x, y)

            except BoardOutException:
                print('Давайте еще раз!')
            else:
                break
        return dot


class Game:
    def __init__(self, pl_user, board_user, pl_ai, board_ai):
        self.pl_user = pl_user
        self.board_user = board_user
        self.pl_ai = pl_ai
        self.board_ai = board_ai

    @classmethod
    def random_board(cls, brd):

        while True:
            brd.board_all = [['O'] * 6 for _ in range(6)]

            list_sh =[]

            sh = brd.add_ship(3)
            list_sh.append(sh)

            brd.contur(sh)

            for _ in range(2):
                sh = brd.add_ship(2)
                list_sh.append(sh)
                brd.contur(sh)
            k = 0

            for _ in range(4):
                k+=1
                sh = brd.add_ship(1)
                list_sh.append(sh)
                brd.contur(sh)
                t = 0
                for i in range(6):
                    t += brd.board_all[i].count('T')+brd.board_all[i].count('X')
                if t == 36 and k!=4:
                    break

            if k==4:
                break
        brd.board_all = [['O'] * 6 for _ in range(6)]
        brd.list_ships = list_sh


    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    Морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
        print("-------------------")
        print('\n Поле игрока')
        self.board_user.show_board()
        print('\n Поле компьютера')
        self.board_ai.show_board()


    def loop(self):
        t_f = True
        while t_f:
            true_false = True
            while true_false:
                print('Выстрел игрока')
                true_false = pl_user.move()
                print('\n Поле компьютера')
                self.board_ai.show_board()
                if self.board_ai.list_life == 0:
                    print('Игрок победил! Поздравляем!')
                    t_f = False
                    break

            if not t_f:
                break

            true_false = True
            while true_false:
                print('Выстрел компьютера')
                true_false = pl_ai.move()
                print('\n Поле игрока')
                self.board_user.show_board()
                if self.board_user.list_life == 0:
                    print('Компьютер победил! Попробуй еще раз!')
                    t_f = False
                    break

    def start(self):
        Game.greet(self)
        Game.loop(self)



board1 = Board([], 0, True, 7)
board2 = Board([], 0, False, 7)

Game.random_board(board1)
Game.random_board(board2)

pl_user = User(board1, board2)
pl_ai = AI(board2, board1)

game1 = Game(pl_user, board1, pl_ai, board2)

game1.start()





