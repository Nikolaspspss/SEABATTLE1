from random import  randint
#4 класса исключения
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass
#класс точки
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other and self.y == other
    def __repr__(self):
        return f'({self.x},{self.y})'
#корабль
class Ship:
    def __init__(self,bow_ship, ship_length, ship_direction):
        self.bow_ship = bow_ship
        self.ship_lenght = ship_length
        self.ship_direction = ship_direction
        self.hit_point = ship_length
#декоратор для определения направления корабля, храниния списка всех точек
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.ship_lenght):
            point_x = self.bow_ship.x
            point_y = self.bow_ship.y
            if self.ship_direction == 0:
                    point_x += i
            elif self.ship_direction == 1:
                    point_y += i
            ship_dots.append(Dot(point_x,point_y))

        return ship_dots

#точка попадания
    def shooten(self, shot):
        return shot in self.dots

#доска
class Board:
    def __init__(self, hid=False, size = 6):
        #скрывает доску
        self.hid = hid
        #размер доски
        self.size = size
        #пораженные корабли
        self.count = 0
        #список строк поля
        self.field = [['O'] * size for _ in range(size)]
        #список занятых точек
        self.busy_point = []
        #список точек с кораблями
        self.ships_point = []

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))
#контур корабля
    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy_point:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy_point.append(cur)
#добавление корабля
    def add_ship(self, ship):
        #проверка что точки не заняты и не выходят за поле
        for d in ship.dots:
            if self.out(d) or d in self.busy_point:
                raise BoardWrongShipException()

        # заняты точки заменяются символом и добавляются в список занятых
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy_point.append(d)

        self.ships_point.append(ship)
        self.contour(ship)
#выстрел мимо поля
    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
#повторный выстрел в ту же точку
        if  d in self.busy_point:
            raise BoardUsedException()
        self.busy_point.append(d)

        for ship in self.ships_point:
            if ship.shooten(d) :
                ship.hit_point -= 1
                self.field[d.x, d.y] = "X"
                if ship.hit_point == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print("Корабль уничтожен")
                    return False
                else:
                    print("Корабль ранен")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо")
        return False

    def begin(self):
        self.busy_point = []

class Gamer:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy
    def ask(self):
        raise NotImplementedError()
#цикл хода
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Gamer):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Gamer):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)

class Game:
#генерация 2х досок
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
#скрывает доску компьютера
        co.hid = True
#Создание двух играков
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board
# генерация доски случайной
    def random_board (self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("Морской бой")
        print("x - строка")
        print("y - столбец")


    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()

