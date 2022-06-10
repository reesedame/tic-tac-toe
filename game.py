import random
import copy

MAP_POS = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]


def new_game():
    player_1 = user_pick_player_type(1)
    player_2 = user_pick_player_type(2)
    board = new_board()

    print("Here are the available positions on the board:")
    render(MAP_POS)

    turn = 0
    while turn < 9:
        if turn % 2 == 0:
            current_player = "X"
            move = player_1(board, current_player)
        else:
            current_player = "O"
            move = player_2(board, current_player)

        board = make_move(board, move, current_player)
        render(board)

        winner = get_winner(board)
        if winner != None:
            print("The winner is " + winner + "!")
            break
        turn += 1
    if turn == 9:
        print("There is no winner, it's a draw.")


def new_board():
    board = []
    for _ in range(3):
        column = []
        for _ in range(3):
            column.append(" ")
        board.append(column)
    return board


def render(board):
    print("-" * 10)
    for i in range(3):
        row = " | ".join(board[i])
        print(row)
        print("-" * 10)
    print("\n")


def get_move():
    moves_dict = {
        1: (0, 0),
        2: (0, 1),
        3: (0, 2),
        4: (1, 0),
        5: (1, 1),
        6: (1, 2),
        7: (2, 0),
        8: (2, 1),
        9: (2, 2),
    }
    try:
        key = int(input("What is your move? "))
    except ValueError:
        print("Key must be an integer, try again.")
        get_move()
    move = moves_dict.get(key)
    if move:
        return move
    else:
        print("Invalid move, try again.")
        get_move()


def make_move(board, move, player):
    if is_valid_move(board, move):
        updated_board = board
        i = move[0]
        j = move[1]
        updated_board[i][j] = player
        return updated_board
    else:
        print("Invalid move, try again.")


def is_valid_move(board, move):
    i = move[0]
    j = move[1]
    if board[i][j] == " ":
        return True
    else:
        return False


def get_winner(board):
    winner = None
    # check each row
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] != " ":
                winner = board[i][0]
    # check each column
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j]:
            if board[0][j] != " ":
                winner = board[0][j]
    # check diagnols
    if (
        board[0][0] == board[1][1] == board[2][2]
        or board[0][2] == board[1][1] == board[2][0]
    ):
        if board[1][1] != " ":
            winner = board[1][1]
    return winner


def is_board_full(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == " ":
                return False
    return True


def valid_moves_list(board):
    valid_moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if is_valid_move(board, (i, j)):
                valid_moves.append((i, j))
    return valid_moves


# Randomly picks a move
def random_ai(board, player):
    valid_moves = valid_moves_list(board)
    move = random.choice(valid_moves)
    return move


# Picks a winning move
# If winning move is not available, randomly picks a move
def finds_winning_moves_ai(board, player):
    valid_moves = valid_moves_list(board)
    chosen_move = random_ai(board, player)
    for move in valid_moves:
        potential_board = copy.deepcopy(board)
        potential_board = make_move(potential_board, move, player)
        if get_winner(potential_board):
            chosen_move = move
            break
    return chosen_move


# Picks a winning move or blocks opponent's winning move
def finds_winning_and_losing_moves_ai(board, player):
    opp_player = get_opposing_player(player)
    move_1 = finds_winning_moves_ai(board, player)
    potential_board = copy.deepcopy(board)
    potential_board = make_move(potential_board, move_1, player)
    if get_winner(potential_board):
        return move_1
    else:
        move_2 = finds_winning_moves_ai(board, opp_player)
        return move_2


# Humans pick their own move
def human_player(board, player):
    move = get_move()
    return move


def user_pick_player_type(player_num):
    print("Choose a player type for player " + str(player_num))
    player_type_dict = {
        1: human_player,
        2: random_ai,
        3: finds_winning_moves_ai,
        4: finds_winning_and_losing_moves_ai,
        5: minimax_ai,
    }
    try:
        key = int(
            input(
                " 1: Human player \n 2: Random AI \n 3: Winning Moves AI \n 4: Winning & Blocking Moves AI \n 5: Minimax AI"
            )
        )
    except ValueError:
        print("Player type must be an integer from the provided list, try again.")
        user_pick_player_type(player_num)
    player_type = player_type_dict.get(key)
    if player_type:
        print("\n")
        return player_type
    else:
        print("Player type must be an integer from the provided list, try again.")
        user_pick_player_type(player_num)


def get_opposing_player(player):
    if player == "X":
        opp_player = "O"
    elif player == "O":
        opp_player = "X"
    return opp_player


def minimax_score(board, current_player, player_to_optimize):
    winner = get_winner(board)
    if winner != None:
        if winner == player_to_optimize:
            return 10
        else:
            return -10
    elif is_board_full(board):
        return 0
    else:
        valid_moves = valid_moves_list(board)
        scores = []
        for move in valid_moves:
            potential_board = copy.deepcopy(board)
            potential_board = make_move(potential_board, move, current_player)
            opp_player = get_opposing_player(current_player)
            opp_best_score = minimax_score(
                potential_board, opp_player, player_to_optimize
            )
            scores.append(opp_best_score)
    if current_player == player_to_optimize:
        return max(scores)
    else:
        return min(scores)


# Picks move which maximizes its score & minimizes the opponent's score
def minimax_ai(board, player):
    best_move = None
    best_score = None
    valid_moves = valid_moves_list(board)
    for move in valid_moves:
        potential_board = copy.deepcopy(board)
        potential_board = make_move(potential_board, move, player)

        opp_player = get_opposing_player(player)
        score = minimax_score(potential_board, opp_player, player)

        if best_score is None or score > best_score:
            best_move = move
            best_score = score
    return best_move


new_game()
