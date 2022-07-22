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
    def __init__(self,ship_length, bow_ship, ship_direction):
        self.ship_lenght = ship_length
        self.bow_ship = bow_ship
        self.ship_direction = ship_direction
        self.hit_point = ship_length
    #декоратор для определения направления корабля, храниния списка всех точек и точки попадания
    @property
    def dots(self):
        ship_dots = []
            for i in range(self.ship_length)
                point_x = self.bow_ship.x
                point_y = self.bow_ship.y
                if self.ship_direction == 0:
                    point_x += i
                elif self.ship_direction == 1:
                    point_y += i
            ship_dots.append(Dot(point_x,point_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots

#доска
class Board:
    def __init__(self, hid=False, size_board = 6):
        #скрывает доску
        self.hid = hid
        #размер доски
        self.size_board = size_board
        self.count = 0
        #список строк поля
        self.field = [['O'] * size_board for _ in range(size_board)]
        #список занятых точек
        self.busy_point = []
        #список точек с кораблями
        self.ships_point = []
    def app_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy_point:
                return BoardWrongShipException()

