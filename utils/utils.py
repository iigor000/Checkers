from time import time


def black_move(board, must_eat): # AI odigrava svoj potez, poziva odgovarajucu minimax funkciju i vraca to stanje ili False, ako nema poteza
    start = time()
    depth = board.get_recommended_depth()
    memo = {}
    board, _ = minimax(board, depth, -10000, 10000, True, memo, must_eat)
    end = time()
    print("Time: ", end - start)
    if board is None:
        return False
    return board

def minimax(board, depth, alpha, beta, player, memo, must_eat): # Minimax algoritam, vraca najbolji potez i njegovu vrednost
    board_hash = str(board) # U hashmapi cuvamo table koje su vec uracunate, da se ne bi cuvale vise puta

    if board_hash in memo: # Ako je pronadjena vrednost trenutne mape, vracamo je
        return memo[board_hash]

    if depth == 0 or board.get_winner() is not None: # Ako smo dosli do kraja stavbla ili imamo pobednika, vracamo vrednost poteza
        value = board.calculate_value()
        memo[board_hash] = (None, value) # Dodajemo trenutnu vrednost u mapu
        return None, value

    if player:
        max_value = -10000 # Maksimalna vrednost krece kao -10000, sto simulira -beskonacno, jer svakako vrednost table ne moze biti manja od te vrednosti
        best_move = None # Najbolji potez je inicijalno None
        if must_eat:
            moves = board.get_eat_moves(False) # Uzimamo samo poteze gde jede
        else:
            moves = board.get_all_moves(False) # Uzimamo potencijalne poteze za AI
        for move in moves:
            _, value = minimax(move, depth - 1, alpha, beta, False, memo, must_eat) # Rekurzivno pozivamo minimax za svaki potez
            max_value = max(max_value, value) # Ako je vrednost trenutnog poteza veca od maksimalne, postavljamo je kao maksimalnu
            if value == max_value: # Ako je vrednost trenutnog poteza jednaka maksimalnoj, postavljamo taj potez kao najbolji, onda ga vracamo
                best_move = move
            alpha = max(alpha, value) # Postavljamo alfu kao maksimum izmedju alfe i vrednosti trenutnog poteza
            if alpha >= beta: # Ako je alfa veca ili jednaka beti, mozemo zanemariti ostatak poteza, jer nece uticati na rezultat
                break

    else: # Igracev potez se odigrava isto, samo sto trazimo najmanju vrednost
        min_value = 10000
        best_move = None
        if must_eat:
            moves = board.get_eat_moves(True)
        else:
            moves = board.get_all_moves(True)
        for move in moves:
            _, value = minimax(move, depth - 1, alpha, beta, True, memo, must_eat)
            min_value = min(min_value, value)
            if value == min_value:
                best_move = move
            beta = min(beta, value)
            if alpha >= beta:
                break

    memo[board_hash] = (best_move, max_value if player else min_value) # Dodajemo trenutnu vrednost u mapu
    return best_move, max_value if player else min_value # Vracamo najbolji potez i njegovu vrednost


def get_checker_difference(old_board, new_board):
    diff_checkers = []
    new_checkers = []
    for i in range(8):  # Assuming the board is 8x8
        for j in range(8):
            old_checker = old_board.board[i][j]
            new_checker = new_board.board[i][j]
            if new_checker == 0 and old_checker != 0:
                diff_checkers.append(old_checker)
            if old_checker == 0 and new_checker != 0:
                new_checkers.append(new_checker)
    return diff_checkers, new_checkers

