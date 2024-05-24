import random
import math

ROW = 6
COLUMN = 7

EMPTY = '_'
AI1_PIECE = 'X'
AI2_PIECE = 'O'

WINDOW_LENGTH = 4

def create_board():
    board = []
    for i in range(6):
        board.append(['_','_','_','_','_','_','_'])
    return board

def drop_piece(board, col, piece):
    for r in range(ROW-1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = piece
            return

def is_valid_location(board, col):
    return board[0][col] == EMPTY

def get_valid_locations(board, dice_no):
    valid_locations = []
    for col in range(dice_no+1):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def show_board(board):
    for row in board:
        print(' | '.join(row))
    print()

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN - 3):
        for r in range(ROW):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN):
        for r in range(ROW - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN - 3):
        for r in range(ROW - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN - 3):
        for r in range(3, ROW):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

def evaluate_window(window, piece):
    score = 0
    opp_piece = AI2_PIECE if piece == AI1_PIECE else AI1_PIECE

    if window.count(piece) == 4:
        score += 1000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80
    elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
        score -= 10

    return score

def score_position(board, piece):
    score = 0
    # Center Score
    center_column = [board[row][(COLUMN // 2)-1] for row in range(ROW)] \
        + [board[row][COLUMN // 2] for row in range(ROW)]
    center_count = center_column.count(piece)
    score += center_count * 5

    # Score Horizontal
    for r in range(ROW):
        for c in range(COLUMN - 3):
            window = board[r][c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN):
        for r in range(ROW - 3):
            window = [board[r + i][c] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score positively sloped diagonals
    for r in range(ROW - 3):
        for c in range(COLUMN - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negatively sloped diagonals
    for r in range(ROW - 3):
        for c in range(COLUMN - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_state(board):
    return winning_move(board, AI1_PIECE) or winning_move(board, AI2_PIECE) or is_full(board)

def is_full(board):
    for row in board:
        if EMPTY in row:
            return False
    return True

def random_number():
    return random.randint(0,6)


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)

    if depth == 0 or is_terminal_state(board):
        if is_terminal_state:
            if winning_move(board, AI1_PIECE):
                return (None, 1000000)
            elif winning_move(board, AI2_PIECE):
                return (None, -1000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI1_PIECE) - score_position(board, AI2_PIECE))

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = [row[:] for row in board]
            drop_piece(b_copy, col, AI1_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            elif new_score == value:
                if random.random() < 0.5:
                    column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = [row[:] for row in board]
            drop_piece(b_copy, col, AI2_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            elif new_score == value:
                if random.random() < 0.5:
                    column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
    
def expectimax(board, depth, maximizingPlayer, chanceNode, dice_no = None):
    valid_locations = get_valid_locations(board,6)

    if dice_no is not None:
        valid_locations = get_valid_locations(board,dice_no)

    # Probabilities for each column (assuming dice_no = 6)
    probabilities = {0:1, 1:6/7, 2:5/7, 3:4/7, 4:3/7, 5:2/7, 6:1/7}

    if depth == 0 or is_terminal_state(board):
        if is_terminal_state:
            if winning_move(board, AI1_PIECE):
                return (None, 1000000)
            elif winning_move(board, AI2_PIECE):
                return (None, -1000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI1_PIECE) - score_position(board, AI2_PIECE))
        
    if not valid_locations and dice_no is not None:
    # All columns are full but we rolled a specific dice_no
    # Need to reroll the dice and check for valid locations again
        new_dice = random_number()
        print("All columns are full. Rerolling the dice...")
        print("New dice number is:", new_dice)
        return expectimax(board, depth, maximizingPlayer, chanceNode, new_dice)

    if maximizingPlayer and not chanceNode:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = [row[:] for row in board]
            drop_piece(b_copy, col, AI1_PIECE)
            new_score = expectimax(b_copy, depth - 1, False, True)[1]
            if new_score > value:
                value = new_score
                column = col
            elif new_score == value:
                if random.random() < 0.5:
                    column = col
        return column, value
    
    elif not maximizingPlayer and not chanceNode:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = [row[:] for row in board]
            drop_piece(b_copy, col, AI2_PIECE)
            new_score = expectimax(b_copy, depth - 1, True, True)[1]
            if new_score < value:
                value = new_score
                column = col
            elif new_score == value:
                if random.random() < 0.5:
                    column = col
        return column, value

    else:  # Chance (averaging) node
        if maximizingPlayer and chanceNode:
            total_value = 0
            for  col in valid_locations:
                b_copy = [row[:] for row in board]
                drop_piece(b_copy, col, AI1_PIECE)
                # Multiply the expected value of the child node by the probability of choosing that column
                total_value += probabilities[col] * expectimax(b_copy, depth - 1, True, False)[1]
            return None, total_value
        else:
            total_value = 0
            for  col in valid_locations:
                b_copy = [row[:] for row in board]
                drop_piece(b_copy, col, AI2_PIECE)
                # Multiply the expected value of the child node by the probability of choosing that column
                total_value += probabilities[col] * expectimax(b_copy, depth - 1, False, False)[1]
            return None, total_value


def main():
    board = create_board()
    show_board(board)

    game_over = False
    turn = random.choice([AI1_PIECE, AI2_PIECE])
    max_depth = 5

    while not game_over:
        if turn == AI1_PIECE:
            # AI1's turn
            print("AI1's turn")
            dice = random_number()
            print("AI1's dice number is:",str(dice))
            col, _ = expectimax(board, max_depth, True, False, dice)
            if is_valid_location(board, col):
                drop_piece(board, col, AI1_PIECE)
                if winning_move(board, AI1_PIECE):
                    print("AI1 wins!")
                    game_over = True
                elif is_full(board):
                    print("Draw!")
                    game_over = True
                

                turn = AI2_PIECE

        else:
            # AI2's turn
            print("AI2's turn")
            dice = random_number()
            print("AI2's dice number is:",str(dice))
            col, _ = expectimax(board, max_depth, False, False, dice)
            if is_valid_location(board, col):
                drop_piece(board, col, AI2_PIECE)
                if winning_move(board, AI2_PIECE):
                    print("AI2 wins!")
                    game_over = True
                elif is_full(board):
                    print("Draw!")
                    game_over = True

                turn = AI1_PIECE

        show_board(board)

        if game_over:
            print("Game over!")

        
            

if __name__ == "__main__":
    main()

