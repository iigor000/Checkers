import copy

import pygame

from model.board import Board
from utils import utils
from utils.constants import (square_size, title, button_on, button_off, start_button, winner_txt, loser_txt, width,
                             height)

pygame.init()

window = pygame.display.set_mode((width, height))

# Varijable koje ce se koristiti u igri, da li AI treba da jede kad moze, ko je pobednik, tabla, moguci potezi, selektovana figura
must_eat = False
winner = None
board = Board()
possible_moves = []
selected_checker = None
old_board = None
selectable_checkers = []

# Funckija koja iscrtava glavni meni, na sebi ima naslov, fugme koje menja da li AI mora da jede i dugme koje zapocinje igru
def main_menu():
    while True:
        global must_eat
        global winner
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 400 <= mouse_x <= 600 and 500 <= mouse_y <= 600:
                    winner = None
                    board.reset()
                    main(0)
                elif 250 <= mouse_x <= 750 and 300 <= mouse_y <= 400:
                    must_eat = not must_eat

        window.fill((255, 200, 255))
        window.blit(title, (275, 0))
        if must_eat:
            window.blit(button_on, (250, 300))
        else:
            window.blit(button_off, (250, 300))
        window.blit(start_button, (400, 500))
        if winner is not None:
            if winner:
                window.blit(winner_txt, (375, 650))
            else:
                window.blit(loser_txt, (375, 650))
        pygame.display.flip()


# Glavna funckija kroz koju se igra
def main(counter):
    global selected_checker
    global possible_moves
    global winner
    global board
    global old_board
    global selectable_checkers

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP: # Ako igrac pritisne na mis, gleda se pozicija misa i tako odredjuje na koju figuru je kluknuo
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row = (mouse_y - 10) // square_size
                col = (mouse_x - 110) // square_size

                if selected_checker:
                    for situation in possible_moves:
                        if situation[0].x == row and situation[0].y == col: # Ako je igrac kliknuo na jedan od mogucih poteza, pomeramo figuru i brisemo figure koje je pojeo
                            selectable_checkers = []
                            board.move(selected_checker, row, col)
                            if len(situation) > 1:
                                for checker in situation[1:]:
                                    board.remove(checker)
                            selected_checker = None
                            possible_moves = []
                            if board.get_winner() is not None: # Provera da li je igrac sa ovim potezom pobedio
                                winner = board.get_winner()
                                running = False
                                main_menu()
                                board.reset()
                                break
                            old_board = copy.deepcopy(board)
                            potential_board = utils.black_move(board, must_eat) # Ako igrac nije pobedio, AI pravi svoj potez, ako funkcija ne vraca nista, znaci da AI nema mogucuh poteza
                            if potential_board:
                                board = potential_board
                                checker_difference, new_checkers = utils.get_checker_difference(old_board, board)  # Proveravamo koje figure su se pojele
                            else:
                                winner = True
                                running = False
                                board.reset()
                                main_menu()
                            if must_eat:  # Ako je pravilo da mora da se jede, proveravamo da li ima potez gde igrac moze da jede
                                possible_moves = board.get_only_eat_moves(True)
                                if possible_moves:
                                    diff = []
                                    for move in possible_moves:
                                        checks, _ = utils.get_checker_difference(board, move)
                                        diff += checks
                                    for check in diff:
                                        if check.color == True:
                                            selectable_checkers.append(check)
                                    possible_moves = []
                                    selected_checker = None
                                else:
                                    if board.get_winner() is not None:
                                        winner = board.get_winner()
                                        running = False
                                        main_menu()
                                        board.reset()
                                        break
                            if board.get_winner() is not None: # Proveramo da li je AI pobedio
                                winner = board.get_winner()
                                running = False
                                main_menu()
                                board.reset()
                                break
                            break
                possible_moves = []  # Ako je igrac kliknuo negde osim na figuru, ili na poteze, brisu se moguci potezi i ako je kliknuo na firguru prave novi
                selected_checker = None
                if board.board[row][col] != 0 and board.board[row][col].color:
                    if must_eat:
                        if selectable_checkers:
                            for checker in selectable_checkers:
                                if checker.x == row and checker.y == col:
                                    selected_checker = checker
                                    possible_moves = board.get_only_eat_moves_checker(selected_checker)
                        else:
                            selected_checker = board.board[row][col]
                            possible_moves = board.get_moves_player(selected_checker)
                    else:
                        selected_checker = board.board[row][col]
                        possible_moves = board.get_moves_player(selected_checker)

        counter += 1
        board.draw(window)  # Iscrtavamo sve poterebne elemente

        for checker in selectable_checkers:  # Crtamo figure koje igrac moze da odabere
            checker.draw_selectable(window)

        if old_board:  # Crtamo prethodan potez
            if counter > 200:
                for checker in checker_difference:
                    if checker.color:
                        checker.draw_eaten(window)
                    else:
                        checker.draw_last(window)
            else:
                for checker in new_checkers:
                    checker.draw_last(window)
            if counter > 400:
                counter = 0

        for situation in possible_moves:  # Crtamo moguce poteze
            situation[0].draw_hint(window)

        if selected_checker:  # Crtamo selektovanu figuru
            selected_checker.draw_high(window)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main_menu()