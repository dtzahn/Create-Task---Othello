
import tkinter

class InputDialog:
    '''Pop up dialog box which takes in the input for the Otheelo game.'''

    def __init__(self):
        self.dialog_window = tkinter.Tk()
        self.dialog_window.resizable(width = False, height = False)

        col_row_option_list = ['8', '4', '5', '6', '7', '9', '10', '11', '12',
                       '13', '14', '15', '16']

        player_option_list = ['Black', 'White']

        top_left_option_list = ['White', 'Black']

        win_type_option_list = ['Most', 'Least']

        title = tkinter.Label(
            master = self.dialog_window, text = 'OTHELLO SET-UP', height = 1,
            font = ('Arial', 16, 'bold'), foreground = '#FFFFFF',
            background = '#000000')

        title.grid(
            row = 0, column = 0, columnspan = 2, padx = 0, pady = 0,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self.column_text = tkinter.Label(master = self.dialog_window,
            text = 'Please choose the number of columns for the game board:')

        self.column_text.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self.column_input = tkinter.IntVar()
        self.column_input.set(col_row_option_list[0])

        self.column_input_menu = tkinter.OptionMenu(self.dialog_window,
            self.column_input, *col_row_option_list)

        self.column_input_menu.grid(
            row = 1, column = 1, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self.row_text = tkinter.Label(master = self.dialog_window,
            text = 'Please choose the number of rows for the game board:')

        self.row_text.grid(
            row = 2, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self.row_input = tkinter.IntVar()
        self.row_input.set(col_row_option_list[0])

        self.row_input_menu = tkinter.OptionMenu(self.dialog_window,
            self.row_input, *col_row_option_list)

        self.row_input_menu.grid(
            row = 2, column = 1, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self.first_player_text = tkinter.Label(master = self.dialog_window,
            text = 'Please choose who will be the first player: ')

        self.first_player_text.grid(
            row = 3, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self.first_player_input = tkinter.StringVar()
        self.first_player_input.set(player_option_list[0])

        self.first_player_menu = tkinter.OptionMenu(self.dialog_window,
            self.first_player_input, *player_option_list)

        self.first_player_menu.grid(
            row = 3, column = 1, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self.corner_tile_text = tkinter.Label(master = self.dialog_window,
            text = 'Please choose which color tile will be placed in the top_left: ')

        self.corner_tile_text.grid(
            row = 4, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self.corner_tile_input = tkinter.StringVar()
        self.corner_tile_input.set(top_left_option_list[0])

        self.corner_tile_menu = tkinter.OptionMenu(self.dialog_window,
            self.corner_tile_input, *top_left_option_list)

        self.corner_tile_menu.grid(
            row = 4, column = 1, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self.win_type_text = tkinter.Label(master = self.dialog_window,
            text = 'Please choose how the winner will be determined: ')

        self.win_type_text.grid(
            row = 5, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self.win_type_input = tkinter.StringVar()
        self.win_type_input.set(win_type_option_list[0])

        self.win_type_menu = tkinter.OptionMenu(self.dialog_window,
            self.win_type_input, *win_type_option_list)

        self.win_type_menu.grid(
            row = 5, column = 1, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        submit_button = tkinter.Button(
            master = self.dialog_window, text = 'Submit',
            font = ('Arial', 14), command = self._on_click)

        submit_button.grid(
                row = 6, column = 0, columnspan = 2, padx = 10, pady = 10,
                sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

    def show(self):
        '''Turns control over to the dilog window until it is destroyed.'''

        self.dialog_window.grab_set()
        self.dialog_window.wait_window()

    def _on_click(self):
        '''When the button in the dialog window is clicked, the window
        is destroyed.'''
        
        self.input_num_columns = self.column_input.get()
        self.input_num_rows = self.row_input.get()
        self.input_first_player = self.first_player_input.get().upper()
        self.input_corner_tile = self.corner_tile_input.get().upper()
        self.input_win_type = self.win_type_input.get().upper()
        self.dialog_window.destroy()

class WinDialog:
    '''Pop up dialog box for when a player wins the game.'''

    def __init__(self, root_window: 'root window', winner: str):
        self.dialog_window = tkinter.Toplevel()
        self.dialog_window.resizable(width = False, height = False)

        if winner != 'TIE':

            win_label = tkinter.Label(
                master = self.dialog_window, text = winner + ' Wins!',
                font = ('Arial', 20, 'bold'), height = 1)

            win_label.grid(
                row = 0, column = 0, padx = 10, pady = 10,
                sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        if winner == 'TIE':

            win_label = tkinter.Label(
                master = self.dialog_window, text = "It's a " + winner,
                font = ('Arial', 20, 'bold'), height = 1)

            win_label.grid(
                row = 0, column = 0, padx = 10, pady = 10,
                sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        win_button = tkinter.Button(
            master = self.dialog_window, text = 'Close',
            font = ('Arial', 14), command = self._on_click)

        win_button.grid(
                row = 1, column = 0, padx = 10, pady = 10,
                sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

    def show(self):
        '''Turns control over to the dilog window until it is destroyed.'''

        self.dialog_window.grab_set()
        self.dialog_window.wait_window()

    def _on_click(self):
        '''When the button in the dialog window is clicked, the window
        is destroyed.'''

        self.dialog_window.destroy()

class InvalidMoveDialog:
    '''Pop up dialog box for when a player wins the game.'''

    def __init__(self, root_window: 'root_window'):
        self.dialog_window = tkinter.Toplevel()
        self.dialog_window.resizable(width = False, height = False)

        win_label = tkinter.Label(
            master = self.dialog_window,
            text = 'Invalid Move. Please click another square.',
            font = ('Arial', 14, 'bold'), height = 1)

        win_label.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        win_button = tkinter.Button(
            master = self.dialog_window, text = 'Close',
            font = ('Arial', 14), command = self._on_click)

        win_button.grid(
                row = 1, column = 0, padx = 10, pady = 10,
                sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

    def show(self):
        '''Turns control over to the dilog window until it is destroyed.'''

        self.dialog_window.grab_set()
        self.dialog_window.wait_window()

    def _on_click(self):
        '''When the button in the dialog window is clicked, the window
        is destroyed.'''

        self.dialog_window.destroy()

'''if __name__ == '__main__':
    input_window = WinDialog('White')
    input_window.show()'''
