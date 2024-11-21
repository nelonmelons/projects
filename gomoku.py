"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Nov. 1, 2023
"""

def is_empty(board):
    """
    Checks if the board is completely empty.
    """
    for row in board:
        for cell in row:
            if cell != " ":
                return False
    return True
    
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    """
    Checks if a sequence of stones is bounded.
    """
    color = board[y_end][x_end]
    opp_color = "b" if color == "w" else "w"

    # Calculate the coordinates of the squares beyond the sequence on both ends
    y1, x1 = y_end + d_y, x_end + d_x
    y2, x2 = y_end - d_y * (length + 1), x_end - d_x * (length + 1)

    # Check if both ends are out of bounds or blocked by opponent's stone
    if not (0 <= y1 < len(board) and 0 <= x1 < len(board[0])) or board[y1][x1] == opp_color:
        if not (0 <= y2 < len(board) and 0 <= x2 < len(board[0])) or board[y2][x2] == opp_color:
            return "CLOSED"

    # Check if both ends are open
    if (0 <= y1 < len(board) and 0 <= x1 < len(board[0]) and board[y1][x1] == " ") and \
            (0 <= y2 < len(board) and 0 <= x2 < len(board[0]) and board[y2][x2] == " "):
        return "OPEN"

    # Otherwise, it is semi-open
    return "SEMIOPEN"

    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    """
    Detects open and semi-open sequences of a given length for a specific color.
    """
    open_seq_count, semi_open_seq_count = 0, 0
    y, x = y_start, x_start
    count = 0

    while 0 <= y < len(board) and 0 <= x < len(board[0]):
        if board[y][x] == col:
            count += 1
        else:
            count = 0

        if count == length:
            # Check if the sequence is bounded
            if is_bounded(board, y, x, length, d_y, d_x) == "OPEN":
                open_seq_count += 1
            elif is_bounded(board, y, x, length, d_y, d_x) == "SEMIOPEN":
                semi_open_seq_count += 1
            count = 0

        y += d_y
        x += d_x

    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):
    """
    Counts open and semi-open sequences of stones for a specific player.
    """
    open_seq_count, semi_open_seq_count = 0, 0

    # Check all rows, columns, and diagonals
    for i in range(len(board)):
        # Check rows (horizontal)
        open_row, semi_open_row = detect_row(board, col, i, 0, length, 0, 1)
        open_seq_count += open_row
        semi_open_seq_count += semi_open_row

        # Check columns (vertical)
        open_col, semi_open_col = detect_row(board, col, 0, i, length, 1, 0)
        open_seq_count += open_col
        semi_open_seq_count += semi_open_col

    # Check diagonals
    for i in range(len(board)):
        open_diag1, semi_open_diag1 = detect_row(board, col, i, 0, length, 1, 1)
        open_diag2, semi_open_diag2 = detect_row(board, col, 0, i, length, 1, 1)
        open_seq_count += open_diag1 + open_diag2
        semi_open_seq_count += semi_open_diag1 + semi_open_diag2

        open_diag3, semi_open_diag3 = detect_row(board, col, i, 0, length, 1, -1)
        open_diag4, semi_open_diag4 = detect_row(board, col, len(board) - 1, i, length, -1, 1)
        open_seq_count += open_diag3 + open_diag4
        semi_open_seq_count += semi_open_diag3 + semi_open_diag4

    return open_seq_count, semi_open_seq_count
    
def search_max(board):
    """
    Searches for the best move for the computer by maximizing the score.
    """
    best_score = -float('inf')
    move_y, move_x = 0, 0

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == " ":
                board[i][j] = "b"
                current_score = score(board)
                board[i][j] = " "

                if current_score > best_score:
                    best_score = current_score
                    move_y, move_x = i, j

    return move_y, move_x
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

    
def is_win(board):
    """
    Checks the current state of the board to determine if there is a winner.
    """
    if detect_rows(board, 'b', 5)[0] > 0 or detect_rows(board, 'b', 5)[1] > 0:
        return "Black won"
    elif detect_rows(board, 'w', 5)[0] > 0 or detect_rows(board, 'w', 5)[1] > 0:
        return "White won"

    # Check if the board is full (draw)
    for row in board:
        if " " in row:
            return "Continue playing"
    return "Draw"



def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
        
    
    

        
    
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
            
        
        
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
            
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
            
if __name__ == '__main__':
    play_gomoku(8)
    

















