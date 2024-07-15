from utils.constants import (queen_white, queen_black, white_check, black_check, hint_check, high_check, square_size,
                             checker_eaten, checker_last, checker_selectable, queen_selectable)


# Checker predstavlja jednu figuru na tabli
class Checker(object):
    def __init__(self, x, y, color, queen=False):
        self._x = x
        self._y = y
        self._color = color
        self._queen = queen

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def queen(self):
        return self._queen

    @queen.setter
    def queen(self, value):
        self._queen = value

    def draw_checker(self, screen):  # Iscrtavanje figure
        if self.color:
            if self.queen:
                screen.blit(queen_white, (self.y * square_size + 110, self.x * square_size + 10))
            else:
                screen.blit(white_check, (self.y * square_size + 110, self.x * square_size + 10))
        else:
            if self.queen:
                screen.blit(queen_black, (self.y * square_size + 110, self.x * square_size + 10))
            else:
                screen.blit(black_check, (self.y * square_size + 110, self.x * square_size + 10))

    # Pomeranje figure
    def move(self, x, y):
        self.x = x
        self.y = y

    def draw_hint(self, screen):
        screen.blit(hint_check, (self.y * square_size + 110, self.x * square_size + 10))

    def draw_high(self, screen):
        screen.blit(high_check, (self.y * square_size + 110, self.x * square_size + 10))

    def draw_eaten(self, screen):
        screen.blit(checker_eaten, (self.y * square_size + 110, self.x * square_size + 10))

    def draw_last(self, screen):
        screen.blit(checker_last, (self.y * square_size + 110, self.x * square_size + 10))

    def draw_selectable(self, screen):
        if self.queen:
            screen.blit(queen_selectable, (self.y * square_size + 110, self.x * square_size + 10))
        else:
            screen.blit(checker_selectable, (self.y * square_size + 110, self.x * square_size + 10))

    def __str__(self):  # Vraca minimalnu reprezentaciju, kako bi poredjenje sa hash mapom bilo efikasnije
        return f"{self.color},{self.queen}"
