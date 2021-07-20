
WHITE = 'W'
BLACK = 'B'
NONE = '-'

class BoardSizeError(Exception):
    pass

class OutsideBoardError(Exception):
    pass

class InvalidPlayerError(Exception):
    pass

class InvalidMoveError(Exception):
    pass

class InvalidWinTypeError(Exception):
    pass

class InvalidTileError(Exception):
    pass

class OthelloGame:
    def __init__(self, columns, rows, first_player: str, win_type: str,
                 center_tile: str):
        '''Creates an OthelloGame object with an empty board.'''

        self._generate_game_board(columns, rows)
        self._set_first_player(first_player)
        self._set_win_condition(win_type)
        self._set_center_tile(center_tile)
    
    def begin_game(self) -> None:
        '''Generates the starting state for an Othello game by placing
        the first for tiles, with the top left one specified by
        the user, in the center of the game board.'''

        tile_type = self.center_tile
        center = self._find_center()
        self._place_tile((center[0], center[1]), tile_type[0])
        self._place_tile((center[0], center[1] + 1), tile_type[1])
        self._place_tile((center[0] + 1, center[1]), tile_type[1])
        self._place_tile((center[0] + 1, center[1] + 1), tile_type[0])

    def display(self) -> None:
        '''Displays the current state of the OthelloGame object.'''

        num_columns = self._get_num_columns()
        num_rows = self._get_num_rows()
        column_nums = '  '

        for num in range(num_columns):
            column_nums += str(num + 1) + ' '
        print(column_nums)

        for num in range(num_rows):
            row = '' + str(num + 1) + ' '
            for column in self.state:
                row += column[num] + ' '
            print(row)

    def execute_move(self, move: tuple) -> None:
        '''Exceutes a move and then resets whose turn it is.'''

        self.verify_move(move)
        move_set_list = self._get_move_set(move)
        self._place_tile(move, self.get_turn())
        for move_set in move_set_list:
            self._flip_tiles(move_set)
        self.player_turn = self.player_turn * -1

    def verify_move(self, move: tuple) -> None:
        '''Checks if a move is valid, raises an InvalidMoveError
        if the move is invalid, otherwise returns nothing.'''

        possible_moves = self._return_possible_moves()
        move_locs = []
        
        for move_origin_set in possible_moves:
            move_locs.append(move_origin_set[0])

        if move not in move_locs:
            raise InvalidMoveError

    def check_if_player_can_move(self) -> bool:
        '''Checks if a player has any vaid moves. If so, returns True.
        If not, skips to next players turn and returns False.'''
        
        possible_moves = self._return_possible_moves()

        if len(possible_moves) == 0:
            self.player_turn = self.player_turn * -1
            return False
        else:
            return True

    def check_if_game_over(self) -> bool:
        '''Checks if the game is over, either because the board is full
        or there are no possible moves for both players.'''

        if not self.check_if_player_can_move():
            return not self.check_if_player_can_move()
        else:
            return False

    def return_winner(self) -> str:
        '''Returns who the winner of the current game state is.'''

        score = self.get_score()

        white_count = score[0]
        black_count = score[1]

        if self.win_condition == 'MOST':
            return _return_highest_count(white_count, black_count)
        if self.win_condition == 'LEAST':
            return _return_lowest_count(white_count, black_count)

    def get_turn(self) -> str:
        '''Returns whose turn it is.'''

        if self.player_turn == 1:
            return WHITE
        if self.player_turn == -1:
            return BLACK

    def get_string_turn(self) -> str:
        '''Returns the full turn name, ex. WHITE, instead of just the
        abbrevition.'''

        if self.get_turn() == 'W':
            return 'White'
        if self.get_turn() == 'B':
            return 'Black'

    def get_score(self) -> tuple:
        '''Returns the score in a tuple. (WHITE, BLACK).'''

        white_count = 0
        black_count = 0
        
        for column in self.state:
            for item in column:
                if item == 'W':
                    white_count += 1
                if item == 'B':
                    black_count += 1

        return (white_count, black_count)
            
    def _generate_game_board(self, columns, rows: int) -> None:
        '''Creates an othello game board with the specified number of
        rows and columns.'''

        board = []

        _verify_board_size(columns, rows)

        for column in range(columns):
            board.append([])
            for row in range(rows):
                board[column].append(NONE)
        
        self.state = board

    def _set_first_player(self, first_player: str) -> None:
        '''Verifies if the player entered is recognized as WHITE or BLACK and
        then sets which is the first player.'''

        if first_player == 'WHITE':
            self.player_turn = 1
        elif first_player == 'BLACK':
            self.player_turn = -1
        else:
            raise InvalidPlayerError()

    def _set_win_condition(self, win_type) -> None:
        '''Verifies if the win type is recognized and then assigns it.'''

        if win_type == 'MOST':
            self.win_condition = 'MOST'
        elif win_type == 'LEAST':
            self.win_condition = 'LEAST'
        else:
            raise InvalidWinTypeError()

    def _set_center_tile(self, tile_type) -> None:
        '''Verifies if the tile_type is recognized and then assignsit.'''

        if tile_type == 'WHITE':
            self.center_tile = ('W', 'B')
        elif tile_type == 'BLACK':
            self.center_tile = ('B', 'W')
        else:
            raise InvalidTileError()

    def _get_opposite_turn(self) -> str:
        '''Returns the opposite of whose turn it is .'''

        opposite_player_turn = self.player_turn * -1

        if opposite_player_turn == 1:
            return WHITE
        if opposite_player_turn == -1:
            return BLACK

    def _get_num_columns(self) -> int:
        '''Returns the number of columns in the game board.'''

        return len(self.state)

    def _get_num_rows(self) -> int:
        '''Returns the rumber of rows in the game board.'''

        return len(self.state[0])

    def _get_move_set(self, move) -> 'move_set':
        '''Returns a move_set which is a tuple containing where the
        the move will be made, the origin of the move, and the direction
        the move will be made in.'''

        possible_moves = self._return_possible_moves()
        move_list = []
        for move_set in possible_moves:
            if move == move_set[0]:
                move_list.append(move_set)
        return move_list

    def _place_tile(self, move: tuple, tile_type: str) -> None:
        '''Places a tile in a specified position on the board.'''

        new_board = self.state
        new_board[move[0] - 1][move[1] - 1] = tile_type
        self.state = new_board

    def _return_tile(self, column: int, row: int) -> tuple:
        '''Checks if there is a tile in a specified position on the board.
        Returns the type of tile if their is a tile in the specified
        position, returns '-' otherwise.'''

        try:
            return self.state[column - 1][ row - 1]
        except:
            raise OutsideBoardError()

    def _find_center(self) -> tuple:
        '''Locates the top left position of the four slot center of the
        game board of an OthelloGame object and return the indexed position
        in a tuple with rows first columns second; values are one greater than
        actual center positions.'''

        columns = self._get_num_columns()
        rows = self._get_num_rows()
        return (int(columns/2), int(rows/2))


    def _return_tiles_with_state(self, param: 'what to count') -> list:
        '''Returns a list of tuple objects which contain the values which
        represent a position on the game board.'''

        empty_tiles = []

        columns = self._get_num_columns()
        rows = self._get_num_rows()

        for column in range(1, columns + 1):
            for row in range(1, rows + 1):
                tile = self._return_tile(column, row)
                if tile == param:
                    empty_tiles.append((column, row))

        return empty_tiles
            
    def _return_possible_moves(self) -> None:
        '''Checks each tile from a list of empty tiles to see if it is a
        possible move for  specified player. Returns a list of move_sets.
        List will be empty if there are no possible moves.'''

        directions = {'up':(0, 1), 'up_left':(-1, 1), 'up_right':(1, 1),
                        'down':(0, -1), 'down_left':(-1, -1), 'down_right':(1, -1),
                      'left':(-1, 0), 'right':(1, 0)}
        empty_tiles = self._return_tiles_with_state(NONE)
        occupied_tiles = (self._return_tiles_with_state(WHITE) +
                          self._return_tiles_with_state(BLACK))
        possible_moves = []

        for move in empty_tiles:
            for direction in directions:
                origin = self._check_direction(move, directions[direction])
                if origin[0] != (-1, -1) and origin[0] in occupied_tiles:
                    possible_moves.append((move, origin[0], origin[1]))

        return possible_moves


    def _check_direction(self, move: tuple, direction: tuple) -> 'origin of move':
        '''Checks if a move if valid in a specified direction. If so,
        returns a tuple which includes the position of the orgin of the move
        and the direction which was checked. If not, returns
        (-1, -1) to represent a move is not possible in the specified
        direction and the direction which was checked.'''

        turn = self.get_turn()
        count = 0

        while(True):
            try:
                tile = self._return_tile(move[0] + direction[0],
                                    move[1] + direction[1])
                if tile == turn or tile == NONE:
                    break
                else:
                    move = (move[0] + direction[0], move[1] + direction[1])
                    count += 1
            except:
                return ((-1, -1), direction)
        try:
            origin_tile = self._return_tile(move[0] + direction[0],
                                           move[1] + direction[1])
            if count > 0 and origin_tile == turn:
                return ((move[0] + direction[0], move[1] + direction[1]), direction)
            else:
                raise OutsideBoardError()
        except:
            return ((-1, -1), direction)

    def _flip_tiles(self, move_set: tuple) -> None:
        '''Flips the tiles between two locations.'''

        move = move_set[0]
        origin = move_set[1]
        direction = move_set[2]
        turn = self.get_turn()

        while(True):
            tile = (move[0] + direction[0], move[1] + direction[1])
            if tile == origin:
                break
            else:
                self._place_tile(tile, turn)
                move = tile


#FUNCTIONS USED BY THE OTHELLO GAME CLASS:

def _verify_board_size(columns: int, rows: int) -> None:
    '''Verifies if the proposed board is composed of an even number of rows and columns
    between 4 and 16; returns an exception otherwise.'''

    _verify_size(rows)
    _verify_size(columns)

def _verify_size(size: int) -> None:
    '''Verifies row or column size is wihin constraints.'''

    if (size >= 4) and (size <= 16):
        pass
    else:
        raise BoardSizeError

def _return_highest_count(white_count:int, black_count: int) -> str:
    '''Returns whose count is higher, WHITE or BLACK.'''

    if white_count > black_count:
        return 'WHITE'
    if black_count > white_count:
        return 'BLACK'
    if white_count == black_count:
        return 'TIE'
        
def _return_lowest_count(white_count:int, black_count: int) -> str:
    '''Returns whose count is lower, WHITE or BLACK.'''

    if white_count < black_count:
        return 'WHITE'
    if black_count < white_count:
        return 'BLACK'
    if white_count == black_count:
        return 'TIE'

    
