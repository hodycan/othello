import point
import othello_game_logic as othello
from tkinter import *

BOARD_BACKGROUND = '#409030'
BOARD_GRID_COLOR = '#999999'
BOARD_GRID_THICKNESS = 2
DISC_PADDING = .08
WHITE_COLOR = '#EEEEEE'
BLACK_COLOR = '#101010'
GHOST_PIECE_COLOR = '#30DDCC'
SCORE_FONT = ('Tahoma', 15)
TURN_FONT = ('Tahoma', 15)



class OthelloApp(Frame):
    """
    Class inherited from Frame, containing an Othello game board
    and status bar.

    Public methods:
	    refresh_statusbar
	    refresh_board
    """
    
    def __init__(self, master, init_width: int,
                 init_height: int, game: 'OthelloGame', inversemode: bool):
        """Initializes Board given a parent widget and board width and height."""
        Frame.__init__(self, master)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self._game = game
        self._cells = []
        self._inversemode = inversemode
        self._rows = len(game.board)
        self._columns = len(game.board[0])
        
        board_width, board_height = init_width, .9*init_height
        statusbar_width, statusbar_height = init_width, .1*init_height
        
        # initialize canvas (aka board)
        self._board = Canvas(self, width=board_width,
                              height=board_height, bg=BOARD_BACKGROUND)
        self._board.grid(row=1, column=0, sticky='nswe')
        
        self._board.bind('<Button-1>', self._on_click)

        # initialize statusbar
        self._build_statusbar()

        self.refresh_board(board_width, board_height)
        self.refresh_statusbar(statusbar_width, statusbar_height)
        

    def _on_click(self, event) -> None:
        """
        Given click event object, finds the cell that the click is in and with
        the corresponding row and column, tries the move on the Othello game.
        """
        for cell in self._cells:
            if cell.contains(event.x, event.y,
                             self._board_width, self._board_height):
                try:
                    self._game.trymove(cell._row, cell._column)

                    self._refresh_app()
                    
                    self._update_dynamicmessage('')
                    
                    if self._game.gameover:
                        self._endgame()
                        
                except othello.OccupiedSquare:
                   self._update_dynamicmessage('That cell is occupied! Try again.')
               
                except othello.InvalidMove:
                   self._update_dynamicmessage('Invalid move! Try again.')
                   # self._on_invalidmove(cell)
                   
                except othello.NoMovesForCurrentTurn:
                   message = 'Other turn has no valid moves! '
                   message += 'Current turn gets to go again.'
                   self._update_dynamicmessage(message)
                   
                break


    def _refresh_app(self) -> None:
        """refresh app on placed move"""
        board_width, board_height = self.master.winfo_width(), .9*self.master.winfo_height()
        statusbar_width, statusbar_height = self.master.winfo_width(), .1*self.master.winfo_height()

        self.refresh_board(board_width, board_height)
        self.refresh_statusbar(statusbar_width, statusbar_height)


    def _endgame_prompt(self, winner) -> str:
            """returns user input of 'yes' or 'no'."""
            message = '{} won! \n Play again?'.format(winner.upper())
            return messagebox.askquestion('Othello', message)


    def _endgame(self):
            """
            Handles the end of the game.
            
            Determines the winner and asks user if they want to play again.
            """
            winner = self._determine_winner()
            print('WINNER IS', winner)
            playagain = self._endgame_prompt(winner)  # either 'yes' or 'no'
            
            if playagain == 'yes':
                    self.master.playagain = True
            elif playagain == 'no':
                    self.master.playagain = False
                    
            self.master.quit()  # exit mainloop
            
            
    def _determine_winner(self) -> str:
            """
            Determine and returns the winner as 'black' or 'white'.
            """
            print("black: {} white: {}".format(self._game.blackscore,
                                               self._game.whitescore))
            print('inverse:', self._inversemode)
            if self._inversemode:
                    if self._game.blackscore > self._game.whitescore:
                            return 'white'
                    elif self._game.whitescore > self._game.blackscore:
                            return 'black'
            else:
                    if self._game.blackscore > self._game.whitescore:
                            return 'black'
                    elif self._game.whitescore > self._game.blackscore:
                            return 'white'

			
    def _othellomessage(self, message: str) -> None:
        """Create Othello related pop up message box."""
        messagebox.showinfo('Othello', message)
 

    def _on_invalidmove(self, cell):
        cell_width = self._board_width/self._columns
        cell_height = self._board_height/self._rows
        row_y = cell.getrow() * cell_height
        column_x = cell.getcolumn() * cell_width
        x1 = column_x + cell_width*DISC_PADDING
        y1 = row_y + cell_height*DISC_PADDING
        x2 = (column_x + cell_width) - cell_width*DISC_PADDING
        y2 = (row_y + cell_height) - cell_height*DISC_PADDING
        id_ = self._board.create_oval(x1, y1, x2, y2, fill='#AA4040',
                                       outline='#AA4040')
        self._board.delete(id_)


    def _build_statusbar(self):
        """create the status bar."""
        self._statusbar = Frame(self)
        self._blackscorelabel = Label(self._statusbar,
                                      text='Black: {}'.format(2),
                                      font=SCORE_FONT, bg='white',
                                      anchor=SW)
        self._whitescorelabel = Label(self._statusbar,
                                      text='White: {}'.format(2),
                                      font=SCORE_FONT, bg='white',
                                      anchor=SE)
        self._turnlabel = Label(self._statusbar,
                                font=TURN_FONT, bg='white',
                                anchor=S)
        # for error messages and such
        self._dynamicmessage = Label(self._statusbar, font=SCORE_FONT)
        
        self._blackscorelabel.grid(row=0, column=0)
        self._whitescorelabel.grid(row=0, column=1)
        self._turnlabel.grid(row=0, column=2)
        self._dynamicmessage.grid(row=1, column=0, columnspan=3)

        self._statusbar.grid(row=0, column=0)
      
    
    def _update_dynamicmessage(self, message):
        """Update the dynamic message label in the status bar."""
        self._dynamicmessage['text'] = message


    def refresh_statusbar(self, statusbar_width: int, statusbar_height: int):

        self._blackscorelabel['text'] = 'Black: {}'.format(self._game.blackscore)
        self._whitescorelabel['text'] = 'White: {}'.format(self._game.whitescore)
        self._turnlabel['text'] = "{}'s turn".format(self._game.turn.capitalize())
        

    def refresh_board(self, board_width, board_height) -> None:
        """Given board width and height, draws the board."""
        self._board.delete('all')
        self._board_width, self._board_height = board_width, board_height
        
        cell_width = board_width/self._columns
        cell_height = board_height/self._rows
        
        for r in range(self._rows):
            row_y = r * cell_height     # row_x and column_y are in pixels

            # create the horizontal line
            self._board.create_line(0, row_y, board_width, row_y,
                                     fill=BOARD_GRID_COLOR,
                                     width=BOARD_GRID_THICKNESS)
            
            for c in range(self._columns):
                column_x = c * cell_width

                # create the vertical line
                self._board.create_line(column_x, 0, column_x, board_height,
                                         fill=BOARD_GRID_COLOR,
                                         width=BOARD_GRID_THICKNESS)
            
                # create the discs
                x1 = column_x + cell_width*DISC_PADDING
                y1 = row_y + cell_height*DISC_PADDING
                x2 = (column_x + cell_width) - cell_width*DISC_PADDING
                y2 = (row_y + cell_height) - cell_height*DISC_PADDING
                
                # draw game piece
                gamepiece = self._game.board[r][c]
                
                if gamepiece in ('W', 'B'):
                    gamepiece_to_color = {'W': WHITE_COLOR, 'B': BLACK_COLOR}
                    color = gamepiece_to_color[gamepiece]                    
                    self._board.create_oval(x1, y1, x2, y2,
                                             fill=color, outline=color)

                else:   # draw ghost disc in unoccupied cells in the grid
                    self._board.create_oval(x1, y1, x2, y2,
                                             fill=BOARD_BACKGROUND,
                                             outline=BOARD_BACKGROUND,
                                             activefill=GHOST_PIECE_COLOR)
                
                # create cell object
                cell_frac_radius = cell_width/board_width/2
                cell_frac_x = column_x / board_width + cell_frac_radius
                cell_frac_y = row_y / board_height + cell_frac_radius
                                 
                cell = Cell(r, c, cell_frac_x, cell_frac_y, cell_frac_radius)
                self._cells.append(cell)


class Cell(object):
    """
    Container for each cell in the board grid.

    For keeping track of the cell's row, column, fractional coordinates for the center,
    and the fractional radius.
    
    Public methods:
        contains:
            returns bool of whether or not the given Point object is within the radius
            of the disc.
        getrow
        getcolumn
    """
    def __init__(self, row: int, column: int,
                 frac_x: int, frac_y: int, frac_radius: int):
        """Initializes the Cell, given row, column, and fractional coordinates."""
        # center frac coordinate
        self._frac_x, self._frac_y = frac_x, frac_y
        self._frac_radius = frac_radius
        self._row = row
        self._column = column


    def getrow(self) -> int:
        """returns cell row."""
        return self._row


    def getcolumn(self) -> int:
        """returns cell column"""
        return self._column


    def contains(self, click_x, click_y, board_width, board_height) -> bool:
        """
        Returns whether or not the given pixel coordinates are within the radius
        of the center of the cell/disc.
        """
        click = point.from_pixel(click_x, click_y, board_width, board_height)
        center = point.from_frac(self._frac_x, self._frac_y)
        
        distance = click.frac_distance_from(center)
        return distance <= self._frac_radius

        
    def __repr__(self) -> str:
        """Returns string representation of Cell."""
        return 'Cell({}, {})'.format(self._row, self._column)
