# Cody Han 80197269
# othello game logic

from random import shuffle

BLANKCELL = '.'

class OthelloGame:
    """
    Represents an Othello game, including game logic and class methods to
    manipulate the game.

    attributes:
        board: two dimensional list
        turn: either 'white' or 'black'
        gameover: bool
        blackscore: int
        whitescore: int

    public methods:
        trymove(self, row, column)
    """
    def __init__(self, rows=8, columns=8,
                 firstturn="black", topleftpiece="white"):
        """Initializes the Othello game."""
        topleftpiece = self._playerpiece(topleftpiece)
        
        if rows%2 != 0 or columns%2 != 0:
            raise InvalidCoordinate("number rows and columns must both be even")

        self.board = self._blankboard(rows, columns, topleftpiece)
        self.turn = firstturn
        self.gameover = False
        self.blackscore = 2
        self.whitescore = 2


    def trymove(self, row, column):
        """
        Scans the board in all directions from the given coordinate and
        either applies the move if it's valid or raises exception InvalidMove.
        """
        if self.board[row][column] != BLANKCELL:
            raise OccupiedSquare

        piece = self._playerpiece(self.turn) # convert player string to piece string
        
        all_pieces_to_flip = self._get_pieces_to_flip(piece, row, column)
        # list elements are two element tuples
        # each containing row and column coordinates
        
        # calling self._applymove implies that the move is valid.
        if len(all_pieces_to_flip) > 0:
            self._applymove(piece, row, column, all_pieces_to_flip)

        else:
            raise InvalidMove        


    def _scanline(self, piece, row, column, r_delta, c_delta):
        """
        Scans the line in the given direction and returns a list of pieces
        to flip if the move is valid, else returns an empty list.
        """
        opposite = self._opposite(piece)
        pieces_to_flip = []
        r_cursor, c_cursor = 0, 0

        while True:

            r_cursor += r_delta
            c_cursor += c_delta
            
            try:
                r, c = row + r_cursor, column + c_cursor
                cursor = self.board[r][c]
                if r < 0 or c < 0:
                    break
                  
                if (cursor == piece or cursor == BLANKCELL) \
                    and (abs(r_cursor) == 1 or abs(c_cursor) == 1):
                    break
                
                if cursor == opposite:
                    pieces_to_flip.append((r, c))
                    
                if cursor == piece and (abs(r_cursor) > 1 or abs(c_cursor) > 1):
                    return pieces_to_flip
    
            except IndexError:
                break
            
        return []


    def _applymove(self, piece: str, row: int,
                   column: int, all_pieces_to_flip: list):
        """
        In the event of a valid move, actually add the piece to the move and
        flip all the pieces.
        """
        # add the new piece
        self.board[row][column] = piece

        # flip pieces
        for pair in all_pieces_to_flip:
            cursor = self.board[pair[0]][pair[1]]
            self.board[pair[0]][pair[1]] = self._opposite(cursor)

        # after making the move
        self._recount_scores()

        if self._has_valid_moves(self._opposite(self.turn)):
            self._nextturn()
        elif self._has_valid_moves(self.turn):
            
            pass # current player gets to go again
        else:
            self.gameover = True

    
    def _nextturn(self):
        """Changes whose turn it is in the game."""
        self.turn = self._opposite(self.turn)


    def _recount_scores(self):
        """Updates the score attributes."""
        blackscore = 0
        whitescore = 0
        
        for row in self.board:
            for column in row:
                if column == 'B':
                    blackscore += 1
                elif column == 'W':
                    whitescore += 1
                elif column == BLANKCELL:
                    pass

        self.blackscore = blackscore
        self.whitescore = whitescore
                

    def _playerpiece(self, player) -> 'piece':
        """
        Given a player string, returns a piece string.

        e.g. parameter 'white' returns 'W'
        """
        strings = {"white": "W", "black": "B"}
        return strings[player]


    def _has_valid_moves(self, player) -> bool:
        """
        Given a player, returns a bool representing whether or not
        the player has any valid moves.
        """
        
        piece = self._playerpiece(player)
        
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if self.board[row][column] == BLANKCELL:
                    
                    # see if there is a valid move for this square
                    if len(self._get_pieces_to_flip(piece, row, column)) > 0:
                        return True # there are available moves
                        

        # if there are no valid moves.
        return False
                    
                    
    def _get_pieces_to_flip(self, piece, row, column) -> [list]:
        """
        Given a coordinate and a piece, returns a list of all the pieces
        that will be flipped when the piece is applied to the board.

        Returns an empty list if the move is not valid.
        """
        all_pieces_to_flip = []
        # list elements are two element tuples
        # each containing row and column coordinates
        
        deltas = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                  (1, 0), (1, -1), (0, -1), (-1, -1)]

        for pair in deltas:
            all_pieces_to_flip.extend(self._scanline(piece, row, column,
                                                     pair[0], pair[1]))
            
        return all_pieces_to_flip


    def getAImove(self, turn) -> tuple:
        """Returns a coordinate tuple of the move of an AI."""
        blankcells = [] # list of 2 element tuples
        
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if self.board[row][column] == BLANKCELL:
                    blankcells.append((row, column))

        shuffle(blankcells)
        
        for blankcell in blankcells:
            coordinate = self._findAImove(turn, blankcell[0], blankcell[1])
            if coordinate != (-1, -1):
                return coordinate
            else:
                pass
                    
        # if there are no valid moves.
        return 'No moves found'

    
    def _findAImove(self, turn, row, column):
        """returns either a coordinate set or (-1, -1)"""
        
        piece = self._playerpiece(self.turn) # convert player string to piece string

        all_pieces_to_flip = []
        # list elements are two element tuples
        # each containing row and column coordinates
        
        deltas = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                  (1, 0), (1, -1), (0, -1), (-1, -1)]

        for pair in deltas:
            all_pieces_to_flip.extend(self._scanline(piece, row, column,
                                                     pair[0], pair[1]))
            
        if len(all_pieces_to_flip) != 0:
            return (row, column) # there are valid moves available.
        else:
            return (-1, -1) # there are no valid moves.


    def _pieceplayer(self, piece) -> 'player':
        """Given a piece string, returns a player string.

        e.g. parameter 'B' returns 'black'
        """
        strings = {'W': 'white', 'B': 'black'}
        return strings[piece]

    
    def _opposite(self, string) -> str:
        """Given player or piece, returns the opposite player or piece."""
        
        strings = {"white": "black", "black": "white",
                "W": "B", "B": "W"}
        return strings[string]


    def _blankboard(self, rows, columns, topleftpiece) -> [list]:
        """Returns a starting othello game board."""
        board = []
        
        # each sublist will be a row.
        # accessing a point: board[r][c]
        
        for r in range(rows):
            row = []
            for c in range(columns):
                row.append(BLANKCELL)
            board.append(row)

        r = int(rows/2 - 1)
        c = int(columns/2 - 1)
        board[r][c] = topleftpiece
        board[r][c+1] = self._opposite(topleftpiece)
        board[r+1][c] = self._opposite(topleftpiece)
        board[r+1][c+1] = topleftpiece

        return board



class InvalidCoordinate(Exception):
    """Raised when row and column user input are invalid."""
    pass

class OccupiedSquare(Exception):
    """Self explanatory."""
    pass

class InvalidMove(Exception):
    """Raised when the move is not valid."""
    pass

class NoMovesForCurrentTurn(Exception):
    """"""
    pass
                            

    
        
                
        
        
