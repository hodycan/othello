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

    def __init__(self, init_width: int, init_height: int, game, inversemode: bool):
        """Initializes the Othello GUI given initial width and height."""

        self._root = Tk()
        self._root.title('Othello')
        self._root.rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)
        self._root.minsize(50, 50)

        self._root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._game = game
        self._inversemode = inversemode
        self._initialize_app(init_width, init_height)
        self.playagain = False
        
        self._root.mainloop()


    def _on_close(self) -> None:
        """asks if the user wants to quit"""
        text = 'Are you sure you want to exit Othello?'
        answer = messagebox.askquestion('Othello',
                                        message=text)
        if answer == 'yes':
            self._root.quit()


    def _initialize_app(self, init_width: int, init_height: int) -> None:
        """initialize the app."""
        self._app = OthelloApp(self._root, init_width, init_height,
                               self._game, self._inversemode)

        self._app.grid(row=0, column=0, sticky='nswe')
        self._app.bind('<Configure>', self._on_resize)


    def _on_resize(self, event) -> None:
        """tkinter resize event handler."""
        self._app.refresh_board(self._root.winfo_width(),
                                self._root.winfo_height())



if __name__ == '__main__':

    while True:

        try:

            settingsgui = OthelloSettingsGUI()
            settings = settingsgui.get_settings()
            rows, columns, first_turn, top_left, inversemode = settings
            
            game = othello_game_logic.OthelloGame(rows=rows, columns=columns,
                                                  firstturn=first_turn,
                                                  topleftpiece=top_left)
            
            gui = OthelloGUI(WINDOW_WIDTH, WINDOW_HEIGHT, game, inversemode)
            
            playagain = gui._app.playagain
            
            gui._root.destroy()
            
            if not playagain:
                break
            
        except:
            e = sys.exc_info()
            print(e[0], e[1])
            input()
            break

        

