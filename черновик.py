#координаты
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y ==other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'

#исключения

class BoardException(Exception):
    def __str__(self):
        return "Вы стреляете по берегу!"
    def __str__(self):
        return "Сюда уже стреляли"

class BoardWrongShipException(Exception):
    pass

#кораблик и попадания
class Ship:
    def __init__(self, bow, i, o):
        self.bow = bow
        self.i = i
        self.o = o
        self.lives =1
    @property
    def dots(self):
        ship_dots = []
        for i  in range(self.i):
            cur_x = self.bow.x
            cur_y = self.bow.y
            if self.o == 0:
                cur_x += 1
            elif self.o == 1
                cur_y += 1
        return  ship_dots

    def shooten(self, shot):
        return shot in self.dots

# вывод доски через класс
class Board:
    def __init__(self, hid = False, size = 6 ):
        self.size = size
        self.hid = hid
        #количество кораблей
        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.buzy= []
        self.ships =[]
    def __str__(self):
        res =""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1 } | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace("■", "O")
        return  res




