print("Welcome to Tic-Tac-Toe!")
print("Player 1 is X")
print("Player 2 is O")

pos = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def display_board():
    board = (f'\n\t{pos[0]}\t|\t{pos[1]}\t|\t{pos[2]} '
             f'\n\t{pos[3]}\t|\t{pos[4]}\t|\t{pos[5]} '
             f'\n\t{pos[6]}\t|\t{pos[7]}\t|\t{pos[8]}\n')
    print(board)

display_board()
game_session = True
player1_turn = True
p1_selections = []
p2_selections = []

while game_session:
    try:
        if player1_turn:
            current_selection = int(input("Player 1's turn. Please select a cell number: ")) - 1

            if current_selection in p2_selections:
                print(f"Box number {current_selection + 1} was already chosen by player 2!")
            elif current_selection in p1_selections:
                print(f"Silly goose! You've already chosen box number {current_selection + 1}!")
            else:
                p1_selections.append(current_selection)
                pos[current_selection] = "X"
                display_board()
                player1_turn = False
        else:
            current_selection = int(input("Player 2's turn. Please select a cell number: ")) - 1

            if current_selection in p1_selections:
                print(f"Box number {current_selection + 1} was already chosen by player 1!")
            elif current_selection in p2_selections:
                print(f"Silly goose! You've already chosen box number {current_selection + 1}!")
            else:
                p2_selections.append(current_selection)
                pos[current_selection] = "O"
                display_board()
                player1_turn = True

    except ValueError:
        print("OOPS! You forgot to type something in!")
    except IndexError:
        print("OOPS! Please type in a number between 1 and 9!")

    if (pos[0] == pos[1] == pos[2]) or (pos[3] == pos[4] == pos[5]) or (pos[6] == pos[7] == pos[8]) or \
            (pos[0] == pos[3] == pos[6]) or (pos[1] == pos[4] == pos[7]) or (pos[2] == pos[5] == pos[8]) or \
            (pos[0] == pos[4] == pos[8]) or (pos[2] == pos[4] == pos[6]):
        if player1_turn:
            print("Player 2 has won the game!")
            game_session = False
            player1_turn = False
        else:
            print("Player 1 has won the game!")
            game_session = False
            player1_turn = False
    elif len(p1_selections) == 9:
        print("Draw")
        game_session = False
        player1_turn = False