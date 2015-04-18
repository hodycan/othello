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
SCORE_FONT = ('consolas', 15)
TURN_FONT = ('consolas', 15)



class OthelloApp(Frame):
    """
    Class inherited from Frame, containing an Othello game board
    and status bar.

    Public methods:
    refresh_statusbar
    refresh_board
    """
    
    def __init__(self, master, board_width: int,
                 board_height: int, game: 'OthelloGame',
                 inversemode: bool):
        """Initializes Board given a parent widget and board width and height."""
        Frame.__init__(self, master)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._game = game
        self._cells = []
        self._inversemode = inversemode
        self._rows = len(game.board)
        self._columns = len(game.board[0])
        self._board_width, self._board_height = board_width, board_height
        self.playagain = False
        self._invalid_is_active = False
        self._current_invalid_circle = 0
        
        self._board = Canvas(self, width=board_width, 
                             height=board_height, bg=BOARD_BACKGROUND)
        self._board.grid(row=0, column=0, sticky='nswe')
        self._board.bind('<Button-1>', self._on_click)

        self._build_statusbar()

        self._statusbar.protocol('WM_DELETE_WINDOW', self._on_close)

        self.refresh_board(board_width, board_height)
        self.refresh_statusbar()
        

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
                    self._after_move()
                        
                except othello.OccupiedSquare:
                    self._update_dynamicmessage('That cell is occupied!')
               
                except othello.InvalidMove:
                    self._update_dynamicmessage('Invalid move!')
                    self._on_invalidmove(cell)
                   
                except othello.NoMovesForNextTurn:
                    self._after_move()
                    message = 'Other turn has no valid moves! '
                    message += 'Current turn gets to go again.'
                    messagebox.showinfo('Othello', message)

                break


    def _after_move(self) -> None:
        """refreshes the move and check if the game is over."""
        self.refresh_board(self._board_width, self._board_height)
        self.refresh_statusbar()
        
        self._update_dynamicmessage('')
        
        if self._game.gameover:
            self._endgame()


    def _endgame_prompt(self, winner) -> str:
        """returns user input of 'yes' or 'no'."""
        message = '{} won! \n Play again?'.format(winner.upper())
        return messagebox.askquestion('Othello', message)


    def _endgame(self) -> None:
        """
        Handles the end of the game.
        
        Determines the winner and asks user if they want to play again.
        """
        winner = self._determine_winner()
        playagain = self._endgame_prompt(winner)  # either 'yes' or 'no'
        
        if playagain == 'yes':
            self.playagain = True
                
        self.master.quit()  # exit mainloop
            
            
    def _determine_winner(self) -> str:
        """
        Determine and returns the winner as 'black' or 'white'.
        """
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


    def _on_invalidmove(self, cell) -> None:
        """flashes a red circle on an invalid move cell."""

        if self._invalid_is_active:
            self._remove_invalid_circle()

        cell_width = self._board_width/self._columns
        cell_height = self._board_height/self._rows
        row_y = cell.getrow() * cell_height
        column_x = cell.getcolumn() * cell_width
        x1 = column_x + cell_width*DISC_PADDING
        y1 = row_y + cell_height*DISC_PADDING
        x2 = (column_x + cell_width) - cell_width*DISC_PADDING
        y2 = (row_y + cell_height) - cell_height*DISC_PADDING

        self._current_invalid_circle = self._board.create_oval(x1, y1, x2, y2, fill='#CC1515',
                                       outline=BOARD_BACKGROUND)
        self._invalid_is_active = True
        self._board.after(500, self._remove_invalid_circle)


    def _remove_invalid_circle(self) -> None:
        """deletes the current invalid red game piece."""
        self._board.delete(self._current_invalid_circle)
        self._invalid_is_active = False


    def _build_statusbar(self) -> None:
        """Create the status bar"""        
        self._statusbar = Toplevel()
        self._statusbar.title('Othello')
        self._blackscorelabel = Label(self._statusbar,
                                      text='Black: {}'.format(2),
                                      font=SCORE_FONT, relief=SUNKEN, bg='white')
        self._whitescorelabel = Label(self._statusbar,
                                      text='White: {}'.format(2),
                                      font=SCORE_FONT, relief=SUNKEN, bg='white')
        self._turnlabel = Label(self._statusbar,
                                font=TURN_FONT, relief=SUNKEN, bg='white')
        # for error messages and such
        self._dynamicmessage = Label(self._statusbar, font=SCORE_FONT, relief=FLAT)
        
        self._blackscorelabel.grid(row=0, column=0)
        self._whitescorelabel.grid(row=0, column=1)
        self._turnlabel.grid(row=0, column=2)
        self._dynamicmessage.grid(row=1, column=0, columnspan=3)

        x = int(self._statusbar.winfo_screenwidth()/2)
        y = int(self._statusbar.winfo_screenheight()/4)
        string = '326x58+{}+{}'.format(x, y)
        self._statusbar.geometry(string)



    def _on_close(self) -> None:
        """asks if the user wants to quit"""
        text = 'Are you sure you want to exit Othello?'
        answer = messagebox.askquestion('Othello',
                                        message=text)
        if answer == 'yes':
            self.master.quit()
      
    
    def _update_dynamicmessage(self, message) -> None:
        """Update the dynamic message label in the status bar."""
        self._dynamicmessage['text'] = message


    def refresh_statusbar(self) -> None:
        """updates statusbar labels"""
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
