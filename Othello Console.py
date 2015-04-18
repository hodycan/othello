# Cody Han 80197269
# othello game on console

import othello_game_logic as othello

# todo:
# fix printgameboard for rows/columns over 9 DONE
# implement entering moves for rows and columns with 2 digits DONE
# make othello unique exceptions for indexerror and valueerror  DONE
# finish menu DONE
# documentation DONE

AI_MODE = False

def main() -> None:
    """Runs everything."""

    printmenu()
    
    while True:

        cmd = input("Default or custom setup? \n").lower()
        
        if cmd == "default":
            game = othello.OthelloGame()
            rungame(game)

        elif cmd == "custom":
            
            setup = get_custom_setup()

            rows, columns = setup[0], setup[1]
            firstturn, topleftpiece = setup[2], setup[3]
            
            inversemode = setup[4]
            yesno_to_bool = {"yes": True, "no": False}
            inversemode = yesno_to_bool[inversemode]

            game = othello.OthelloGame(rows, columns, firstturn, topleftpiece)

            rungame(game, inversemode)
            
        else:
            continue
        
        cmd = input("Play again?").lower()
        if not cmd.startswith('y'):
            break

    
def rungame(game: othello.OthelloGame, inversemode: bool = False) -> None:
    """Runs the game of Othello, invoking methods on the othello game object."""

    global AI_MODE
    
    while True:
        
        try:
            print('_'*80)
            printgameboard(game.board)
            print()
            print("Black: {} White: {}".format(game.blackscore,
                                               game.whitescore))
            print()
            print("{}'s turn".format(game.turn.upper()))

            if AI_MODE == False:
                row = input("Enter row: ")
                column = input("Enter column: ")
                print()
                
            if AI_MODE == True:
                coordinate = game.getAImove(game.turn)
                row, column = coordinate[0], coordinate[1]
            
            try:
                row, column = int(row), int(column)
            except:
                raise othello.InvalidCoordinate
            
            game.trymove(row, column)
            
            if game.gameover:
                if not inversemode:
                    endgame(game)
                elif inversemode:
                    endinversegame(game)
                return


        except othello.InvalidCoordinate:
            print("Invalid row or column. Please try again.")

        except othello.OccupiedSquare:
            print("This square is occupied. Please try again.")

        except othello.InvalidMove:
            print("Invalid move. Please try again.")

        except othello.NoMovesForCurrentTurn:
            print("Next player has no valid moves.")
            print("{} goes again.".format(game.turn))


 
def endgame(game) -> None:
    """Prints the final score and the winner."""
    
    printgameboard(game.board)
    print("Black: {} - White: {}".format(game.blackscore,
                                         game.whitescore))
    if game.blackscore > game.whitescore:
        print("Black won!")
    elif game.whitescore > game.blackscore:
        print("White won!")

def endinversegame(game) -> None:
    """Prints the final score and the winner for inverse othello."""
    
    printgameboard(game.board)
    print("Black: {} - White: {}".format(game.blackscore,
                                         game.whitescore))
    if game.blackscore > game.whitescore:
        print("White won!")
    elif game.whitescore > game.blackscore:
        print("Black won!")


def printmenu() -> None:
    """Prints the menu."""
    lines = ["Welcome to Othello! (console based)"]
    # add rules and stuff i guess
    for line in lines:
        print(line)

def printgameboard(board) -> None:
    """Prints the game board in a readable format."""
    
    print()
    print(' ', end='')
    for c in range(len(board[0])):
        print('{:>3}'.format(c), end='')
        
    print()
    
    for r in range(len(board)):
        print('{:>2}'.format(r), end=' ') # numbering 
        for c in board[r]:
            print(c, end='  ') # filling in grid

        print()
        print()


def get_custom_setup() -> set:
    """Gets user preferences and returns them in a set."""
    
    while True:
        try:
            rows = input('Enter an even number of rows between 4 and 16:\n')
            
            rows = int(rows)
            if rows%2 == 0 and 4 <= rows <= 16:
                break
        except:
            pass
        
    while True:
        try:
            columns = input('Enter an even number of columns between 4 and 16:\n')
            columns = int(columns)
            if columns%2 == 0 and 4 <= columns <= 16:
                break
        except:
            pass
        
    while True:
        firstturn = input('Enter what color goes first (black/white):\n')
        if firstturn in ("black", "white"):
            break
        
    while True:
        topleftpiece = input('Enter what color piece will be in the top'
                             ' left center of the board\n(black/white):\n')
        if topleftpiece in ("black", "white"):
            break
        
    while True:
        inversemode = input('Do you want to play inverse Othello?'
                            '\n\tyes - the player with the fewest pieces wins'
                            '\n\tno - the player with the most pieces win:\n')
        if inversemode in ("yes", "no"):
            break
        
    return (rows, columns, firstturn, topleftpiece, inversemode)


if __name__ == '__main__':
    main()

