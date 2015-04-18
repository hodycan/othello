from tkinter import *
from tkinter import messagebox
from settings_menu import OthelloSettingsGUI
from othello_gui_board import *
import othello_game_logic

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500


class OthelloGUI:
    """
    Graphical user interface for Othello game.

    public attributes:
        playagain: bool

    """
     
    def __init__(self, init_width: int, init_height: int, game: 'OthelloGame', inversemode: bool):
        """Initializes the Othello GUI given initial width and height."""

        self._root = Tk()
        self._root.title('Othello')
        self._root.rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)

        self._game = game
        self._inversemode = inversemode
        self._initialize_app(init_width, init_height)
        self.playagain = False
        
        self._root.mainloop()


    def _initialize_app(self, init_width: int, init_height: int) -> None:
        """initialize the app."""
        self._app = OthelloApp(self._root, init_width, init_height,
                               self._game, self._inversemode)

        self._app.grid(row=0, column=0, sticky='nswe')
        self._app.bind('<Configure>', self._resize_app)


    def _resize_app(self, event) -> None:
        """tkinter resize event handler."""
        board_width, board_height = self._root.winfo_width(), .9*self._root.winfo_height()
        statusbar_width, statusbar_height = self._root.winfo_width(), .1*self._root.winfo_height()

        self._app.refresh_board(board_width, board_height)
        self._app.refresh_statusbar(statusbar_width, statusbar_height)


class FakeError(Exception):
    pass

if __name__ == '__main__':

    while True:
        try:
            # ask thornton why this works:
            # Once the settings GUI is initialized, the mainloop is not closed
            # until the user hits start.
            # however, calling get_settings() works
            settingsgui = OthelloSettingsGUI()
            settings = settingsgui.get_settings()
            rows, columns, first_turn, top_left, inversemode = settings

            # rows, columns, first_turn, top_left = 4, 4, 'black', 'white'
            # inversemode = False
            
            game = othello_game_logic.OthelloGame(rows=rows, columns=columns,
                                                  firstturn=first_turn,
                                                  topleftpiece=top_left)
            
            gui = OthelloGUI(WINDOW_WIDTH, WINDOW_HEIGHT, game, inversemode)
            
            playagain = gui._root.playagain
            
            gui._root.destroy()
            
            if not playagain:
                break
            
        except FakeError:
            e = sys.exc_info()
            print(e[0], e[1])
            input()
            break
    input()        
        

