from tkinter import *

class OthelloSettingsGUI:
    """
    Contains the Othello setup GUI.
    
    Public Methods:
        get_settings
    
    Public Attributes:
        rows, columns, firstplayer, topleftpiece
    """
    def __init__(self):
        """Initializes the settings menu."""
        self._settingswindow = Tk()
        self._settingswindow.title('Othello Setup')
        self._settingswindow.resizable(0, 0)
        
        self._buildall()
        
        self.rows, self.columns = None, None
        self.firstplayer, self.topleftpiece = None, None
        
        self._settingswindow.mainloop()

    def get_settings(self) -> set:
        """Returns a tuple containing settings variables."""
        return (self.rows, self.columns,
                self.firstplayer, self.topleftpiece, self.inversemode)

                
    def _start(self) -> None:
        """Sets the class instance variables to the user selected options and then closes the window."""
        self.rows, self.columns = self._rows_var.get(), self._columns_var.get()
        self.firstplayer = self._firstplayer_var.get()
        self.topleftpiece = self._topleftoption_var.get()

        stringtobool = {'yes': True, 'no': False}
        self.inversemode = stringtobool[self._inversemode_var.get()]
        self._settingswindow.destroy()


    def _gridall(self) -> None:
        """grids each child widget of self._settingswindow."""
        self._row_scale.grid(row=1, column=0, rowspan=4)
        self._columns_scale.grid(row=1, column=1, rowspan=4)
        self._firstplayeroption_frame.grid(row=1, column=2)
        self._topleftoption_frame.grid(row=1, column=3)
        self._inversemode_frame.grid(row=3, column=2, columnspan=2)

        self._rows_label.grid(row=0, column=0)
        self._columns_label.grid(row=0, column=1)
        self._firstplayer_label.grid(row=0, column=2)
        self._topleftpiece_label.grid(row=0, column=3)
        self._inversemode_label.grid(row=2, column=2, columnspan=2)        


    def _buildall(self) -> None:
        """Builds the menu."""
        self._buildsliders()
        self._buildfirstplayeroptions()
        self._buildtopleftoptions()
        self._buildinversemodeoptions()
        self._buildlabels()
        
        self._start_button = Button(self._settingswindow, text='Start Othello',
                              command=self._start,
                              width=15, height=7)
        self._gridall()
        self._start_button.grid(row=0, column=4, rowspan=4)
        
        
    def _buildsliders(self) -> None:
        """self explanatory"""
        # rows
        self._rows_var = IntVar()
        self._row_scale = Scale(self._settingswindow, variable=self._rows_var,
                          from_=16, to=4, length=200,
                          resolution=2, tickinterval=2,
                          showvalue=0)
        self._row_scale.set(8)

        # columns
        self._columns_var = IntVar()
        self._columns_scale = Scale(self._settingswindow, variable=self._columns_var,
                              from_=16, to=4, length=200,
                              resolution=2, tickinterval=2,
                              showvalue=0)
        self._columns_scale.set(8)


    def _buildfirstplayeroptions(self) -> None:
        """self explanatory"""
        self._firstplayer_var = StringVar()
        self._firstplayeroption_frame = Frame(self._settingswindow)

        black_radiobutton = Radiobutton(self._firstplayeroption_frame, text='Black',
                                        variable=self._firstplayer_var,
                                        value='black')
        white_radiobutton = Radiobutton(self._firstplayeroption_frame, text='White',
                                        variable=self._firstplayer_var,
                                        value='white')
        black_radiobutton.select()
        black_radiobutton.grid(row=1, column=0)
        white_radiobutton.grid(row=0, column=0)


    def _buildtopleftoptions(self) -> None:
        """self explanatory"""
        self._topleftoption_var = StringVar()
        self._topleftoption_frame = Frame(self._settingswindow)

        blacktopleft_radiobutton = Radiobutton(self._topleftoption_frame, text='Black',
                                        variable=self._topleftoption_var,
                                               value='black')
        whitetopleft_radiobutton = Radiobutton(self._topleftoption_frame, text='White',
                                        variable=self._topleftoption_var,
                                               value='white')
        whitetopleft_radiobutton.select()
        blacktopleft_radiobutton.grid(row=1, column=0)
        whitetopleft_radiobutton.grid(row=0, column=0)

        
    def _buildinversemodeoptions(self) -> None:
        """self explanatory"""
        self._inversemode_var = StringVar()
        self._inversemode_frame = Frame(self._settingswindow)
        noinverse_radiobutton = Radiobutton(self._inversemode_frame, text='no',
                                            variable=self._inversemode_var,
                                            value='no')
        yesinverse_radiobutton = Radiobutton(self._inversemode_frame, text='yes',
                                            variable=self._inversemode_var,
                                            value='yes')
        noinverse_radiobutton.select()
        noinverse_radiobutton.grid(row=1, column=0)
        yesinverse_radiobutton.grid(row=0, column=0)
        
        
    def _buildlabels(self) -> None:
        """self explanatory"""
        self._rows_label = Label(self._settingswindow, text='Rows')
        self._columns_label = Label(self._settingswindow, text='Columns')
        self._firstplayer_label = Label(self._settingswindow, text='First turn')
        self._topleftpiece_label = Label(self._settingswindow, text='Top left piece')
        self._inversemode_label = Label(self._settingswindow,
                                  text='Inverse mode \n(least amount of points win)')
                                  

