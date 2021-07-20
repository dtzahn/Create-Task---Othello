
import tkinter
import othello
import othello_gui_dialog_boxes
import point

class OthelloGui:
    '''Gui for the Othello application.'''
    
    def __init__(self):
        input_window = othello_gui_dialog_boxes.InputDialog()
        input_window.show()

        self.root_window = tkinter.Tk()

        self.state = othello.OthelloGame(input_window.input_num_columns,
            input_window.input_num_rows, input_window.input_first_player,
            input_window.input_win_type, input_window.input_corner_tile)
        self.state.begin_game()

        title = tkinter.Label(
            master = self.root_window, text = 'OTHELLO', height = 1,
            font = ('Arial', 16, 'bold'), foreground = '#FFFFFF',
            background = '#000000')

        title.grid(
            row = 0, column = 0, padx = 0, pady = 0,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self.info_board = tkinter.Frame(
            master = self.root_window, width = 500, height = 20)

        self.info_board.grid(
            row = 1, column = 0, padx = 0, pady = 0,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self.info_board.grid_propagate(5)

        self._update_info_board()

        self.game_board = tkinter.Canvas(
            master = self.root_window, width = 500, height = 500,
            background = '#179A47') #005200

        self.game_board.grid(
            row = 2, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self.game_board.bind('<Configure>', self._on_resize)
        self.game_board.bind('<Button-1>', self._on_click)

        self.root_window.rowconfigure(0, weight = 0)
        self.root_window.columnconfigure(0, weight = 1)
        self.root_window.rowconfigure(1, weight = 0)
        self.root_window.rowconfigure(2, weight = 1)

        self._draw_board(self.state._get_num_columns(),
            self.state._get_num_rows())
        self._draw_tiles_from_game_state()

    def start(self) -> None:
        '''Initiates the tkinter mainloop n order to run the Othello
        Game application with the OthelloGui class.'''

        self.root_window.mainloop()


    def _draw_board(self, num_columns: int, num_rows: int) -> None:
        '''Draws the game board.'''

        canvas_width = self.game_board.winfo_width()
        canvas_height = self.game_board.winfo_height()

        self.row_pixel_size = canvas_height/num_rows
        self.column_pixel_size = canvas_width/num_columns

        origin = point.Point(0, 0)
        vertical_end = point.Point(0, 1)
        horizontal_end = point.Point(1, 0)

        origin_x, origin_y = origin.pixel(canvas_width, canvas_height)
        vert_x, vert_y = vertical_end.pixel(canvas_width, canvas_height)
        for column in range(num_columns):
            self.game_board.create_line(origin_x, origin_y, vert_x, vert_y)
            origin_x += self.column_pixel_size
            vert_x += self.column_pixel_size

        origin_x, origin_y = origin.pixel(canvas_width, canvas_height)
        hori_x, hori_y = horizontal_end.pixel(canvas_width, canvas_height)
        for column in range(num_rows):
            self.game_board.create_line(origin_x, origin_y, hori_x, hori_y)
            origin_y += self.row_pixel_size
            hori_y += self.row_pixel_size

    def _update_info_board(self) -> None:
        '''Updates the info board with appropriate items.'''

        whose_turn = tkinter.Label(
            master = self.info_board,
            text = 'Turn: ' + self.state.get_string_turn(),
            font = ('Arial', 12),
            height = 1)

        whose_turn.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        white_score = tkinter.Label(
            master = self.info_board,
            text = 'White: ' + str(self.state.get_score()[0]),
            font = ('Arial', 12),
            height = 1)

        white_score.grid(
            row = 0, column = 1, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        black_score = tkinter.Label(
            master = self.info_board,
            text = 'Black: ' + str(self.state.get_score()[1]),
            font = ('Arial', 12),
            height = 1)

        black_score.grid(
            row = 0, column = 2, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self.info_board.rowconfigure(0, weight = 0)
        self.info_board.columnconfigure(0, weight = 1)
        self.info_board.columnconfigure(1, weight = 1)
        self.info_board.columnconfigure(2, weight = 1)

    def _on_click(self, event: tkinter.Event) -> None:
        '''Draws a tile on the game board when the board is clicked.
        Also, manages the players turn, by checking if the next player
        has any possible moves, if the game is over, and updating the
        info board.'''

        canvas_width = self.game_board.winfo_width()
        canvas_height = self.game_board.winfo_height()

        column = int(event.x/self.column_pixel_size) + 1
        row = int(event.y/self.row_pixel_size) + 1

        try:
            self.state.execute_move((column, row))
            self._draw_tiles_from_game_state()
            self._manage_turn()
        except othello.InvalidMoveError:
            invalid_move_dialog_window = othello_gui_dialog_boxes.InvalidMoveDialog(
                self.root_window)
            invalid_move_dialog_window.show()
            

    def _draw_tile(self, column: int, row: int, tile_type: str) -> None:
        '''Draws a tile on the game board given a column and row number.'''
        
        radius_x = self.column_pixel_size/2
        radius_y = self.row_pixel_size/2

        center_x = (self.column_pixel_size * (column - 1)) + radius_x
        center_y = (self.row_pixel_size * (row - 1)) + radius_y

        if tile_type == 'W':
            color = '#FFFFFF'        
        if tile_type == 'B':
            color = '#000000'
        if tile_type == '-':
            return
            
        self.game_board.create_oval(
            center_x - radius_x, center_y - radius_y,
            center_x + radius_x, center_y + radius_y,
            fill = color, outline = '#000000') 

    def _draw_tiles_from_game_state(self) -> None:
        '''Draws tiles on the board from the game state data.'''

        tile_list = self.state

        column_index = 0
        row_index = 0

        for column in tile_list.state:
            column_index += 1
            for tile in column:
                row_index += 1
                self._draw_tile(column_index, row_index,
                    tile_list._return_tile(column_index, row_index))
            row_index = 0
                
    def _on_resize(self, event: tkinter.Event) -> None:
        '''Redraws the canvas when the window is resized.'''

        self.game_board.delete(tkinter.ALL)
        self._draw_board(self.state._get_num_columns(),
            self.state._get_num_rows())
        self._draw_tiles_from_game_state()

    def _manage_turn(self) -> None:
        '''Manages turn related verifications and state updates.'''
              
        if self.state.check_if_player_can_move() == False:
            if self.state.check_if_game_over() == True:
                winner_dialog_window = othello_gui_dialog_boxes.WinDialog(
                    self.root_window, self.state.return_winner())
                winner_dialog_window.show()
                
        self._update_info_board()
            
if __name__ == '__main__':

    OthelloGui().start()
