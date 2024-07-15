from copy import deepcopy

from model.checker import Checker
from utils.constants import board


# Klasa predstavlja tablu
class Board(object):

    # Imamo trenutnu poziciju svih figura na tabli, kao i broj crnih i belih figura i dama
    def __init__(self):
        self.board = []
        self.black = 12
        self.white = 12
        self.black_queen = 0
        self.white_queen = 0
        self.create_board()

    # Kreiranje table
    def create_board(self):
        self.board = []
        for row in range(8):
            self.board.append([])
            for col in range(8):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Checker(row, col, False))
                    elif row > 4:
                        self.board[row].append(Checker(row, col, True))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    # Iscrtavanje figura na tabli
    def draw_checkers(self, screen):
        for checker in self.get_all_checkers():
            if checker != 0:
                checker.draw_checker(screen)

    # Iscrtavanje table
    def draw(self, screen):
        screen.blit(board, (100, 0))
        self.draw_checkers(screen)

    # Heuristika poteza, gledamo koliko svaki igrac ima figura, dama i figura na ivici table
    def calculate_value(self):
        value = 0
        value += self.black * 2 - self.white * 2 + (self.black_queen - self.white_queen) * 1.5
        for checker in self.get_all_checkers():
            if checker != 0:
                if checker.x == 0 or checker.x == 7 or checker.y == 0 or checker.y == 7:
                    if checker.color:
                        if checker.queen:
                            value -= 1
                        else:
                            value -= 0.5
                    else:
                        if checker.queen:
                            value += 1
                        else:
                            value += 0.5
        return value

    # Sve figure odredjene boje
    def get_checkers(self, color):
        checkers = []
        for row in self.board:
            for checker in row:
                if checker != 0 and checker.color == color:
                    checkers.append(checker)
        return checkers

    def __str__(self): # Str funckija vraca najjednostavniju predstavu table, za poredjenje tabli
        return ''.join(str(self.board[i][j]) for i in range(8) for j in range(8))

    # Sve figure na tabli
    def get_all_checkers(self):
        checkers = []
        for row in self.board:
            for checker in row:
                checkers.append(checker)
        return checkers

    # Resetovanje table
    def reset(self):
        self.black = 12
        self.white = 12
        self.black_queen = 0
        self.white_queen = 0
        self.create_board()

    # Pomeranje figure, ako stigne do kraja postaje kraljica i menjamo vrednost x i y u figuri
    def move(self, checker, row, col):
        if (not checker.queen) and (row == 7 or row == 0):
            checker.queen = True
            if checker.color:
                self.white_queen += 1
            else:
                self.black_queen += 1
        self.board[checker.x][checker.y], self.board[row][col] = 0, checker
        checker.move(row, col)

    # Uklanjanje figure
    def remove(self, checker):
        row, col = checker.x, checker.y
        if self.board[row][col] != 0:
            if self.board[row][col].color:
                if checker.queen:
                    self.white_queen -= 1
                self.white -= 1
            else:
                if checker.queen:
                    self.black_queen -= 1
                self.black -= 1
            self.board[row][col] = 0

    # Svi potencijalni potezi odredjene figure
    def get_moves(self, checker):
        moves = []

        if checker.color or checker.queen:
            moves += self.get_moves_up(checker)
        if not checker.color or checker.queen:
            moves += self.get_moves_down(checker)

        return moves

    # Svi potezi odredjene figure u kojom je ona pojela drugu figuru
    def get_moves_only_eat(self, checker):
        moves = []
        if checker.color or checker.queen:
            moves += self.moves_only_eat_up(checker)
        if not checker.color or checker.queen:
            moves += self.moves_only_eat_down(checker)
        return moves

    # Funkcija gleda sve poteze u kojima figura ide ka gore (za igraca i AI ako ima kraljicu)
    def get_moves_up(self, checker):
        moves = []

        if checker.x - 1 >= 0 and checker.y - 1 >= 0 and self.board[checker.x - 1][checker.y - 1] == 0: # Ako je polje slobodno, pravimo novu tablu i pomeramo figuru
            new_board = deepcopy(self)
            new_board.move(new_board.board[checker.x][checker.y], checker.x - 1, checker.y - 1)
            moves.append(new_board)

        # Ako se figura moze pojesti, pravimo novu tablu, pomeramo figuru i sklanjamo pojedenu figuru
        elif checker.x - 2 >= 0 and checker.y - 2 >= 0 and self.board[checker.x - 1][checker.y - 1].color == (not checker.color) and self.board[checker.x - 2][checker.y - 2] == 0:
            new_board = deepcopy(self)
            new_board.move(new_board.board[checker.x][checker.y], checker.x - 2, checker.y - 2)
            new_board.remove(new_board.board[checker.x - 1][checker.y - 1])
            moves.append(new_board)
            moves += new_board.moves_eat_up(new_board.board[checker.x - 2][checker.y - 2])
        if checker.x - 1 >= 0 and checker.y + 1 < 8 and self.board[checker.x - 1][checker.y + 1] == 0:
            new_board = deepcopy(self)
            new_board.move(new_board.board[checker.x][checker.y], checker.x - 1, checker.y + 1)
            moves.append(new_board)
        elif checker.x - 2 >= 0 and checker.y + 2 < 8 and self.board[checker.x - 1][checker.y + 1].color == (not checker.color) and self.board[checker.x - 2][checker.y + 2] == 0:
            new_board = deepcopy(self)
            new_board.move(new_board.board[checker.x][checker.y], checker.x - 2, checker.y + 2)
            new_board.remove(new_board.board[checker.x - 1][checker.y + 1])
            moves.append(new_board)
            moves += new_board.moves_eat_up(new_board.board[checker.x - 2][checker.y + 2])
        return moves

    # Ista funkcija kao i prethodna, samo sto gleda poteze ka dole
    def get_moves_down(self, checker):
        moves = []

        if checker.x + 1 < 8 and checker.y + 1 < 8 and self.board[checker.x + 1][checker.y + 1] == 0:
            new_board = deepcopy(self)
            new_board.move(new_board.board[checker.x][checker.y], checker.x + 1, checker.y + 1)
            moves.append(new_board)
        elif checker.x + 2 < 8 and checker.y + 2 < 8 and self.board[checker.x + 1][checker.y + 1].color == (not checker.color) and self.board[checker.x + 2][checker.y + 2] == 0:
            new_board = deepcopy(self)
            new_board.move(new_board.board[checker.x][checker.y], checker.x + 2, checker.y + 2)
            new_board.remove(new_board.board[checker.x + 1][checker.y + 1])
            moves.append(new_board)
            moves += new_board.moves_eat_down(new_board.board[checker.x + 2][checker.y + 2])
        if checker.x + 1 < 8 and checker.y - 1 >= 0 and self.board[checker.x + 1][checker.y - 1] == 0:
            new_board = deepcopy(self)
            new_board.move(new_board.board[checker.x][checker.y], checker.x + 1, checker.y - 1)
            moves.append(new_board)
        elif checker.x + 2 < 8 and checker.y - 2 >= 0 and self.board[checker.x + 1][checker.y - 1].color == (not checker.color) and self.board[checker.x + 2][checker.y - 2] == 0:
            new_board = deepcopy(self)
            new_board.move(new_board.board[checker.x][checker.y], checker.x + 2, checker.y - 2)
            new_board.remove(new_board.board[checker.x + 1][checker.y - 1])
            moves.append(new_board)
            moves += new_board.moves_eat_down(new_board.board[checker.x + 2][checker.y - 2])
        return moves

    # Rekurzivna funkcija za posmatranje svih poteza u kome igrac jede figuru, kako bi se moglo pojesti vise figura za redom
    def moves_eat_up(self, checker):
        moves = []
        if checker.x - 2 >= 0 and checker.y - 2 >= 0 and self.board[checker.x - 1][checker.y - 1] != 0 and self.board[checker.x - 1][checker.y - 1].color == (not checker.color) and self.board[checker.x - 2][checker.y - 2] == 0:
            new_board = deepcopy(self)
            new_board.move(new_board.board[checker.x][checker.y], checker.x - 2, checker.y - 2)
            new_board.remove(new_board.board[checker.x - 1][checker.y - 1])
            moves.append(new_board)
            moves += new_board.moves_eat_up(new_board.board[checker.x - 2][checker.y - 2])
        if checker.x - 2 >= 0 and checker.y + 2 < 8 and self.board[checker.x - 1][checker.y + 1] != 0 and self.board[checker.x - 1][checker.y + 1].color == (not checker.color) and self.board[checker.x - 2][checker.y + 2] == 0:
            new_board = deepcopy(self)
            new_board.move(new_board.board[checker.x][checker.y], checker.x - 2, checker.y + 2)
            new_board.remove(new_board.board[checker.x - 1][checker.y + 1])
            moves.append(new_board)
            moves += new_board.moves_eat_up(new_board.board[checker.x - 2][checker.y + 2])
        return moves

    def moves_only_eat_up(self, checker):  # Ako moze da pojede vise figura, ne moze stati nakon jedne, nego jede do kraja
        moves = []
        if checker.x - 2 >= 0 and checker.y - 2 >= 0 and self.board[checker.x - 1][checker.y - 1] != 0 and self.board[checker.x - 1][checker.y - 1].color == (not checker.color) and self.board[checker.x - 2][checker.y - 2] == 0:
            new_board = deepcopy(self)
            new_board.move(new_board.board[checker.x][checker.y], checker.x - 2, checker.y - 2)
            new_board.remove(new_board.board[checker.x - 1][checker.y - 1])
            potential_moves = new_board.moves_only_eat_up(new_board.board[checker.x - 2][checker.y - 2])
            if not potential_moves:
                moves.append(new_board)
            moves += potential_moves
        if checker.x - 2 >= 0 and checker.y + 2 < 8 and self.board[checker.x - 1][checker.y + 1] != 0 and self.board[checker.x - 1][checker.y + 1].color == (not checker.color) and self.board[checker.x - 2][checker.y + 2] == 0:
            new_board = deepcopy(self)
            new_board.move(new_board.board[checker.x][checker.y], checker.x - 2, checker.y + 2)
            new_board.remove(new_board.board[checker.x - 1][checker.y + 1])
            potential_moves = new_board.moves_only_eat_up(new_board.board[checker.x - 2][checker.y + 2])
            if not potential_moves:
                moves.append(new_board)
            moves += potential_moves
        return moves

    def moves_eat_down(self, checker):
        moves = []
        if checker.x + 2 < 8 and checker.y + 2 < 8 and self.board[checker.x + 1][checker.y + 1] != 0 and self.board[checker.x + 1][checker.y + 1].color == (not checker.color) and self.board[checker.x + 2][checker.y + 2] == 0:
            new_board = deepcopy(self)
            new_board.move(new_board.board[checker.x][checker.y], checker.x + 2, checker.y + 2)
            new_board.remove(new_board.board[checker.x + 1][checker.y + 1])
            moves.append(new_board)
            moves += new_board.moves_eat_down(new_board.board[checker.x + 2][checker.y + 2])
        if checker.x + 2 < 8 and checker.y - 2 >= 0 and self.board[checker.x + 1][checker.y - 1] != 0 and self.board[checker.x + 1][checker.y - 1].color == (not checker.color) and self.board[checker.x + 2][checker.y - 2] == 0:
            new_board = deepcopy(self)
            new_board.move(new_board.board[checker.x][checker.y], checker.x + 2, checker.y - 2)
            new_board.remove(new_board.board[checker.x + 1][checker.y - 1])
            moves.append(new_board)
            moves += new_board.moves_eat_down(new_board.board[checker.x + 2][checker.y - 2])
        return moves

    def moves_only_eat_down(self, checker):
        moves = []
        if checker.x + 2 < 8 and checker.y + 2 < 8 and self.board[checker.x + 1][checker.y + 1] != 0 and self.board[checker.x + 1][checker.y + 1].color == (not checker.color) and self.board[checker.x + 2][checker.y + 2] == 0:
            new_board = deepcopy(self)
            new_board.move(new_board.board[checker.x][checker.y], checker.x + 2, checker.y + 2)
            new_board.remove(new_board.board[checker.x + 1][checker.y + 1])
            potential_moves = new_board.moves_only_eat_down(new_board.board[checker.x + 2][checker.y + 2])
            if not potential_moves:
                moves.append(new_board)
            moves += potential_moves
        if checker.x + 2 < 8 and checker.y - 2 >= 0 and self.board[checker.x + 1][checker.y - 1] != 0 and self.board[checker.x + 1][checker.y - 1].color == (not checker.color) and self.board[checker.x + 2][checker.y - 2] == 0:
            new_board = deepcopy(self)
            new_board.move(new_board.board[checker.x][checker.y], checker.x + 2, checker.y - 2)
            new_board.remove(new_board.board[checker.x + 1][checker.y - 1])
            potential_moves = new_board.moves_only_eat_down(new_board.board[checker.x + 2][checker.y - 2])
            if not potential_moves:
                moves.append(new_board)
            moves += potential_moves
        return moves


    # Svi potezi za boju
    def get_all_moves(self, color):
        moves = []
        for checker in self.get_checkers(color):
            moves += self.get_moves(checker)
        return moves

    # Svi potezi za boju u kojima se jede, ili ako nema takvih poteza, svi potezi
    def get_eat_moves(self, color):
        moves = []
        for checker in self.get_checkers(color):
            moves += self.get_moves_only_eat(checker)
        if len(moves) == 0:
            return self.get_all_moves(color)
        return moves

    # Samo potezi u kojima jede
    def get_only_eat_moves(self, color):
        moves = []
        for checker in self.get_checkers(color):
            moves += self.get_moves_only_eat(checker)
        return moves

    # Samo potezi u kojima jede, ali samo za jednu figuru
    def get_only_eat_moves_checker(self, checker):
        moves = []
        moves += self.moves_after_only_eat(checker, [])
        return moves

    # Svi potezi za igraca
    def get_moves_player(self, checker):
        moves = []
        if checker.x - 1 >= 0 and checker.y - 1 >= 0 and self.board[checker.x - 1][checker.y - 1] == 0:
            new_checker = deepcopy(checker)
            new_checker.move(checker.x - 1, checker.y - 1)
            moves.append([new_checker])
        elif checker.x - 2 >= 0 and checker.y - 2 >= 0 and self.board[checker.x - 1][checker.y - 1].color == (not checker.color) and self.board[checker.x - 2][checker.y - 2] == 0:
            new_checker = deepcopy(checker)
            new_checker.move(checker.x - 2, checker.y - 2)
            moves.append([new_checker, self.board[checker.x - 1][checker.y - 1]])
            moves += self.moves_after_eat(new_checker, [self.board[checker.x - 1][checker.y - 1]])
        if checker.x - 1 >= 0 and checker.y + 1 < 8 and self.board[checker.x - 1][checker.y + 1] == 0:
            new_checker = deepcopy(checker)
            new_checker.move(checker.x - 1, checker.y + 1)
            moves.append([new_checker])
        elif checker.x - 2 >= 0 and checker.y + 2 < 8 and self.board[checker.x - 1][checker.y + 1].color == (not checker.color) and self.board[checker.x - 2][checker.y + 2] == 0:
            new_checker = deepcopy(checker)
            new_checker.move(checker.x - 2, checker.y + 2)
            moves.append([new_checker, self.board[checker.x - 1][checker.y + 1]])
            moves += self.moves_after_eat(new_checker, [self.board[checker.x - 1][checker.y + 1]])
        if checker.queen:
            if checker.x + 1 < 8 and checker.y + 1 < 8 and self.board[checker.x + 1][checker.y + 1] == 0:
                new_checker = deepcopy(checker)
                new_checker.move(checker.x + 1, checker.y + 1)
                moves.append([new_checker])
            elif checker.x + 2 < 8 and checker.y + 2 < 8 and self.board[checker.x + 1][checker.y + 1].color == (
                    not checker.color) and self.board[checker.x + 2][checker.y + 2] == 0:
                new_checker = deepcopy(checker)
                new_checker.move(checker.x + 2, checker.y + 2)
                moves.append([new_checker, self.board[checker.x + 1][checker.y + 1]])
                moves += self.moves_after_eat(new_checker, [self.board[checker.x + 1][checker.y + 1]])
            if checker.x + 1 < 8 and checker.y - 1 >= 0 and self.board[checker.x + 1][checker.y - 1] == 0:
                new_checker = deepcopy(checker)
                new_checker.move(checker.x + 1, checker.y - 1)
                moves.append([new_checker])
            elif checker.x + 2 < 8 and checker.y - 2 >= 0 and self.board[checker.x + 1][checker.y - 1].color == (
                    not checker.color) and self.board[checker.x + 2][checker.y - 2] == 0:
                new_checker = deepcopy(checker)
                new_checker.move(checker.x + 2, checker.y - 2)
                moves.append([new_checker, self.board[checker.x + 1][checker.y - 1]])
                moves += self.moves_after_eat(new_checker, [self.board[checker.x + 1][checker.y - 1]])

        return moves

    # Svi potezi za igraca nakon jedenja
    def moves_after_eat(self, checker, eaten):
        moves = []

        if checker.x - 2 >= 0 and checker.y - 2 >= 0 and self.board[checker.x - 1][checker.y - 1] != 0 and self.board[checker.x - 1][checker.y - 1].color == (not checker.color) and self.board[checker.x - 2][checker.y - 2] == 0:
            new_checker = deepcopy(checker)
            new_checker.move(checker.x - 2, checker.y - 2)
            moves.append([new_checker, self.board[checker.x - 1][checker.y - 1]] + eaten)
            moves += self.moves_after_eat(new_checker, eaten + [self.board[checker.x - 1][checker.y - 1]])
        if checker.x - 2 >= 0 and checker.y + 2 < 8 and self.board[checker.x - 1][checker.y + 1] != 0 and self.board[checker.x - 1][checker.y + 1].color == (
                not checker.color) and self.board[checker.x - 2][checker.y + 2] == 0:
            new_checker = deepcopy(checker)
            new_checker.move(checker.x - 2, checker.y + 2)
            moves.append([new_checker, self.board[checker.x - 1][checker.y + 1]] + eaten)
            moves += self.moves_after_eat(new_checker, eaten + [self.board[checker.x - 1][checker.y + 1]])
        if checker.queen:
            if checker.x + 2 < 8 and checker.y + 2 < 8 and self.board[checker.x + 1][checker.y + 1] != 0 and self.board[checker.x + 1][checker.y + 1].color == (
                    not checker.color) and self.board[checker.x + 2][checker.y + 2] == 0:
                new_checker = deepcopy(checker)
                new_checker.move(checker.x + 2, checker.y + 2)
                moves.append([new_checker, self.board[checker.x + 1][checker.y + 1]] + eaten)
                moves += self.moves_after_eat(new_checker, eaten + [self.board[checker.x + 1][checker.y + 1]])
            if checker.x + 2 < 8 and checker.y - 2 >= 0 and self.board[checker.x + 1][checker.y - 1] != 0 and self.board[checker.x + 1][checker.y - 1].color == (
                    not checker.color) and self.board[checker.x + 2][checker.y - 2] == 0:
                new_checker = deepcopy(checker)
                new_checker.move(checker.x + 2, checker.y - 2)
                moves.append([new_checker, self.board[checker.x + 1][checker.y - 1]] + eaten)
                moves += self.moves_after_eat(new_checker, eaten + [self.board[checker.x + 1][checker.y - 1]])

        return moves

    def moves_after_only_eat(self, checker, eaten):  # Ako se moze jesti vise figura, uzimamo samo te poteze
        moves = []

        if checker.x - 2 >= 0 and checker.y - 2 >= 0 and self.board[checker.x - 1][checker.y - 1] != 0 and self.board[checker.x - 1][checker.y - 1].color == (not checker.color) and self.board[checker.x - 2][checker.y - 2] == 0:
            new_checker = deepcopy(checker)
            new_checker.move(checker.x - 2, checker.y - 2)
            potential_moves = self.moves_after_only_eat(new_checker, eaten + [self.board[checker.x - 1][checker.y - 1]])
            if not potential_moves:
                moves.append([new_checker, self.board[checker.x - 1][checker.y - 1]] + eaten)
            moves += self.moves_after_eat(new_checker, eaten + [self.board[checker.x - 1][checker.y - 1]])
        if checker.x - 2 >= 0 and checker.y + 2 < 8 and self.board[checker.x - 1][checker.y + 1] != 0 and self.board[checker.x - 1][checker.y + 1].color == (
                not checker.color) and self.board[checker.x - 2][checker.y + 2] == 0:
            new_checker = deepcopy(checker)
            new_checker.move(checker.x - 2, checker.y + 2)
            potential_moves = self.moves_after_only_eat(new_checker, eaten + [self.board[checker.x - 1][checker.y + 1]])
            if not potential_moves:
                moves.append([new_checker, self.board[checker.x - 1][checker.y + 1]] + eaten)
            moves += self.moves_after_eat(new_checker, eaten + [self.board[checker.x - 1][checker.y + 1]])
        if checker.queen:
            if checker.x + 2 < 8 and checker.y + 2 < 8 and self.board[checker.x + 1][checker.y + 1] != 0 and self.board[checker.x + 1][checker.y + 1].color == (
                    not checker.color) and self.board[checker.x + 2][checker.y + 2] == 0:
                new_checker = deepcopy(checker)
                new_checker.move(checker.x + 2, checker.y + 2)
                potential_moves = self.moves_after_only_eat(new_checker, eaten + [self.board[checker.x + 1][checker.y + 1]])
                if not potential_moves:
                    moves.append([new_checker, self.board[checker.x + 1][checker.y + 1]] + eaten)
                moves += self.moves_after_eat(new_checker, eaten + [self.board[checker.x + 1][checker.y + 1]])
            if checker.x + 2 < 8 and checker.y - 2 >= 0 and self.board[checker.x + 1][checker.y - 1] != 0 and self.board[checker.x + 1][checker.y - 1].color == (
                    not checker.color) and self.board[checker.x + 2][checker.y - 2] == 0:
                new_checker = deepcopy(checker)
                new_checker.move(checker.x + 2, checker.y - 2)
                potential_moves = self.moves_after_only_eat(new_checker, eaten + [self.board[checker.x + 1][checker.y - 1]])
                if not potential_moves:
                    moves.append([new_checker, self.board[checker.x + 1][checker.y - 1]] + eaten)
                moves += self.moves_after_eat(new_checker, eaten + [self.board[checker.x + 1][checker.y - 1]])

        return moves

    # Proveravamo da li ima pobednika (ako nije ostalo figura ili ne moze da se napravi potez)
    def get_winner(self):
        if self.black <= 0:
            return True
        elif self.white <= 0:
            return False
        moves = self.get_all_moves(True)
        if len(moves) == 0:
            return False
        return None

    # Gledamo varijabilnu dubinu, posto ce vise kalkulacija trebati da se izvrso ako ima vise figura i ako ima vise dama
    def get_recommended_depth(self):
        depth = 4
        if self.black + self.white < 10:
            depth += 2
        elif self.black + self.white < 15:
            depth += 1
        if self.black_queen + self.white_queen > 2:
            depth -= 1
        return depth
