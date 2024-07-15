import pygame

# Ucitavamo sve slike koje se koriste
white_check = pygame.image.load('assets/checkWhite.png')
black_check = pygame.image.load('assets/checkBlack.png')
hint_check = pygame.image.load('assets/checkHint.png')
high_check = pygame.image.load('assets/checkHigh.png')
board = pygame.image.load('assets/board.jpg')
queen_white = pygame.image.load('assets/queenWhite.png')
queen_black = pygame.image.load('assets/queenBlack.png')
title = pygame.image.load("assets/title.png")
start_button = pygame.image.load("assets/startButton.png")
button_on = pygame.image.load("assets/buttonOn.png")
button_off = pygame.image.load("assets/buttonOff.png")
winner_txt = pygame.image.load("assets/winnerTxt.png")
loser_txt = pygame.image.load("assets/loserTxt.png")
checker_eaten = pygame.image.load("assets/checkEaten.png")
checker_last = pygame.image.load("assets/checkLast.png")
checker_selectable = pygame.image.load("assets/checkSel.png")
queen_selectable = pygame.image.load("assets/queenSel.png")

queen_black = pygame.transform.scale(queen_black, (80, 80))
queen_white = pygame.transform.scale(queen_white, (80, 80))
white_check = pygame.transform.scale(white_check, (80, 80))
black_check = pygame.transform.scale(black_check, (80, 80))
hint_check = pygame.transform.scale(hint_check, (80, 80))
high_check = pygame.transform.scale(high_check, (80, 80))
checker_eaten = pygame.transform.scale(checker_eaten, (80, 80))
checker_last = pygame.transform.scale(checker_last, (80, 80))
checker_selectable = pygame.transform.scale(checker_selectable, (80, 80))
queen_selectable = pygame.transform.scale(queen_selectable, (80, 80))
board = pygame.transform.scale(board, (800, 800))


# Velicina ekrana i velicina kvadrata
square_size = 100
width = 1000
height = 800
