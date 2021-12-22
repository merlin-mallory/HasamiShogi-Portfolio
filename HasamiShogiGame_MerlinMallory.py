# Author: Merlin Mallory
# Date: 12/03/2021
# Description: This program models Variant 1 of the Hasami Shogi Game.

class HasamiShogiGame:
    """Represents a single instance of the Hasami Shogi Game (Variant 1), see:
    https://en.wikipedia.org/wiki/Hasami_shogi"""

    def __init__(self):
        """Initializes the following data members: game_board_array, game_state, active_player,
        blacks_number_of_captured_pieces, reds_number_of_captured_pieces."""
        self._game_board_array = list()
        self._game_state = 'UNFINISHED'
        self._active_player = 'BLACK'
        self._blacks_number_of_captured_pieces = int(0)
        self._reds_number_of_captured_pieces = int(0)

        for square in range(81):
            self._game_board_array.append("_")
        for red_pieces in range(0, 9):
            self._game_board_array[red_pieces] = "R"
        for black_pieces in range(72, 81):
            self._game_board_array[black_pieces] = "B"

    def get_game_state(self):
        """Takes no parameters and returns a str indicating the state of the game - 'UNFINISHED', 'RED_WON',
        or 'BLACK WON''"""
        return self._game_state

    def get_active_player(self):
        """Takes no parameters and returns a str indicating whose turn it is - either 'RED' or 'BLACK'"""
        return self._active_player

    def get_num_captured_pieces(self, whose_number_of_captured_pieces):
        """Takes a str (either 'RED' or 'BLACK'), and returns an int indicating the number of that color that have been
        captured."""
        if whose_number_of_captured_pieces == "RED":
            return int(self._reds_number_of_captured_pieces)
        elif whose_number_of_captured_pieces == "BLACK":
            return int(self._blacks_number_of_captured_pieces)

    def get_square_occupant(self, search_alg_notation):
        """Takes one string (algebraic notion) that represents a square on the board. Returns 'RED', 'BLACK',
        or 'NONE' depending upon whether the specified square is occupied by a red piece, a black piece, or neither."""
        desired_index = self.convert_notation(search_alg_notation)
        result = self._game_board_array[desired_index]
        if result == "_":
            return "NONE"
        elif result == "R":
            return "RED"
        elif result == "B":
            return "BLACK"

    def print_board(self):
        """Takes no parameters, and prints out game_board_array with the appropriate labels. Used primarily for
        testing purposes. Returns nothing."""
        # Labeling the x-axis
        print("  1 2 3 4 5 6 7 8 9")
        row = ""
        for rows in range(0, 9):
            for squares in range(0, 9):
                row = row + self._game_board_array[rows*9 + squares]
                row = row + " "
            y_label = ""
            if rows == 0:
                y_label = "a"
            elif rows == 1:
                y_label = "b"
            elif rows == 2:
                y_label = "c"
            elif rows == 3:
                y_label = "d"
            elif rows == 4:
                y_label = "e"
            elif rows == 5:
                y_label = "f"
            elif rows == 6:
                y_label = "g"
            elif rows == 7:
                y_label = "h"
            elif rows == 8:
                y_label = "i"

            print(y_label, row)
            row = ""

    def convert_notation(self, alg_notation):
        """Takes a string referring to a board location in algebraic notation (str), and converts the algebraic
        notation into the corresponding index (int) in the game_board_array."""
        row, col = alg_notation
        col = int(col)
        col = col - 1
        row_num = int()
        if row == "a":
            row_num = 0
        elif row == "b":
            row_num = 1
        elif row == "c":
            row_num = 2
        elif row == "d":
            row_num = 3
        elif row == "e":
            row_num = 4
        elif row == "f":
            row_num = 5
        elif row == "g":
            row_num = 6
        elif row == "h":
            row_num = 7
        elif row == "i":
            row_num = 8

        desired_index = row_num*9 + col
        return desired_index

    def clear_board(self):
        """Clears the game_board_array (only used for testing purposes)"""
        for square in range(81):
            self._game_board_array[square] = "_"

    def place_black(self, alg_notation):
        """Takes a location (algebraic notation) as a parameter, and places a black stone at that location. (only
        used for testing purposes)"""
        desired_index = self.convert_notation(alg_notation)
        self._game_board_array[desired_index] = "B"

    def place_red(self, alg_notation):
        """Takes a location (algebraic notation) as a parameter, and places a red stone at that location. (only used
        for testing purposes)"""
        desired_index = self.convert_notation(alg_notation)
        self._game_board_array[desired_index] = "R"

    def place_space(self, alg_notation):
        """Takes a location (algebraic notation) as a parameter, and empties that location. (only used for testing
        purposes)"""
        desired_index = self.convert_notation(alg_notation)
        self._game_board_array[desired_index] = "_"

    def make_move(self, move_origin_alg, move_target_alg):
        """1. Takes two strings (algebraic notation) that represent the square moved from and the square moved to.
        2. Calls the convert_notation function to create move_origin_index (int) and move_target_index (int) variables
        that correspond to the appropriate index in game_board_array.
        3. Calls the legal_move_check function to see if the player's move is possible. If legal_move_check returns
        False, then make_move also returns False.
        4. Otherwise the make_move function calls the appropriate removal_for function, which analyzes if any nearby
        enemy pieces need to be removed from the board.
        5. After removal_check completes, make_move switches the active_player turn, updates the game_state,
        and returns True."""
        if self._game_state == "BLACK_WON":
            return False
        if self._game_state == "RED_WON":
            return False

        move_origin_index = self.convert_notation(move_origin_alg)
        move_target_index = self.convert_notation(move_target_alg)

        if self._active_player == "BLACK" and self._game_board_array[move_origin_index] != "B":
            return False
        elif self._active_player == "RED" and self._game_board_array[move_origin_index] != "R":
            return False

        is_move_legal = self.legal_move_check(move_origin_index, move_target_index)
        if is_move_legal is False:
            return False

        self.removal_check(move_target_index)

        if self._active_player == "BLACK":
            self._active_player = "RED"
        elif self._active_player == "RED":
            self._active_player = "BLACK"

        if self._blacks_number_of_captured_pieces == 8 or self._blacks_number_of_captured_pieces == 9:
            self._game_state = "BLACK_WON"
        elif self._reds_number_of_captured_pieces == 8 or self._reds_number_of_captured_pieces == 9:
            self._game_state = "RED_WON"

        return True

    def legal_move_check(self, move_origin_index, move_target_index):
        """Called by the make_move function. Takes two strings (index notation) that represent the square moved
        from and the square moved to. Compiles a set of all the legal moves possible for move_origin in the up, down,
        left, and, right directions. If move_target is included in the set, then this function returns True.
        Otherwise this function returns False."""
        legal_move_set = set()

        # Vertical up search
        up_current_square = "_"
        up_current_square_index = move_origin_index
        while up_current_square == "_" and up_current_square_index >= 0:
            # print("Here's the vert up legal_move_set this iteration:", legal_move_set)
            up_current_square_index -= 9
            try:
                up_current_square = self._game_board_array[up_current_square_index]
            except IndexError:
                up_current_square = "X"
            if up_current_square == "_" and up_current_square_index >= 0:
                legal_move_set.add(up_current_square_index)

        # Vertical down search
        down_current_square = "_"
        # print("move_origin_index is now:", move_origin_index, "in vertical down search")
        down_current_square_index = move_origin_index
        while down_current_square == "_" and down_current_square_index <= 80:
            # print("Here's the vert down legal_move_set this iteration:", legal_move_set)
            down_current_square_index += 9
            try:
                down_current_square = self._game_board_array[down_current_square_index]
            except IndexError:
                down_current_square = "X"
            if down_current_square == "_" and down_current_square_index <= 80:
                legal_move_set.add(down_current_square_index)

        # Horizontal left search
        left_current_square = "_"
        # print("move_origin_index is now:", move_origin_index, "in horizontal left search")
        left_current_square_index = move_origin_index
        while left_current_square == "_" and (left_current_square_index % 9) != 0 and \
                left_current_square_index >= 0:
            # print("Here's the horizontal left legal_move_set this iteration:", legal_move_set)
            left_current_square_index -= 1
            try:
                left_current_square = self._game_board_array[left_current_square_index]
            except IndexError:
                left_current_square = "X"
            if left_current_square == "_" and ((left_current_square_index + 1) % 9) != 0 and \
                    left_current_square_index >= 0:
                legal_move_set.add(left_current_square_index)

        # Horizontal right search
        right_current_square = "_"
        # print("move_origin_index is now:", move_origin_index, "in horizontal right search")
        right_current_square_index = move_origin_index
        while right_current_square == "_" and ((right_current_square_index+1) % 9) != 0 and \
                right_current_square_index <= 80:
            # print("Here's the horizontal right legal_move_set this iteration:", legal_move_set)
            right_current_square_index += 1
            try:
                right_current_square = self._game_board_array[right_current_square_index]
            except IndexError:
                right_current_square = "X"
            if right_current_square == "_" and (right_current_square_index % 9) != 0 and right_current_square_index <=\
                    80:
                legal_move_set.add(right_current_square_index)

        if move_target_index in legal_move_set:
            if self._active_player == "BLACK":
                self._game_board_array[move_target_index] = "B"
            elif self._active_player == "RED":
                self._game_board_array[move_target_index] = "R"

            self._game_board_array[move_origin_index] = "_"
            return True
        else:
            return False

    def removal_check(self, move_target_index):
        """Called by the make_move function. Takes one string (index notation) that represents the square moved
        to. Checks for enemy pieces for capture, and compiles a candidates_for_removal_list. Checks for custodial
        capture to the right, left, up, and down from the move_target_index.  Also checks for corner capture.
        At the end of the function, removes the candidates_for_removal, and increments the appropriate
        num_captured_pieces variable appropriately."""
        candidates_for_removal_list = list()
        ally_color = str()
        enemy_color = str()

        if self._active_player == "BLACK":
            ally_color = "B"
            enemy_color = "R"
        if self._active_player == "RED":
            ally_color = "R"
            enemy_color = "B"

        # Searching for vertical up removal
        mini_list = list()
        up_flag = int(0)
        red_found = False
        current_square_index = int(move_target_index)

        while current_square_index >= 0 and up_flag == 0:
            current_square_index -= 9
            if red_found is True and current_square_index >= 0:
                if self._game_board_array[current_square_index] == ally_color:
                    for squares in mini_list:
                        candidates_for_removal_list.append(squares)
                    up_flag = 1
                elif self._game_board_array[current_square_index] == "_":
                    up_flag = 1
            if current_square_index >= 0 and self._game_board_array[current_square_index] == enemy_color and up_flag == 0:
                red_found = True
                mini_list.append(current_square_index)
            else:
                up_flag = 1

        # Searching for vertical down removal
        mini_list = list()
        down_flag = int(0)
        red_found = False
        current_square_index = int(move_target_index)

        while current_square_index <= 80 and down_flag == 0:
            current_square_index += 9
            if red_found is True and current_square_index <= 80:
                if self._game_board_array[current_square_index] == ally_color:
                    for squares in mini_list:
                        candidates_for_removal_list.append(squares)
                    down_flag = 1
                elif self._game_board_array[current_square_index] == "_":
                    down_flag = 1
            if current_square_index <= 80 and self._game_board_array[current_square_index] == enemy_color and \
                    down_flag == 0:
                red_found = True
                mini_list.append(current_square_index)
            else:
                down_flag = 1

        # Searching for horizontal left removal
        mini_list = list()
        left_flag = int(0)
        red_found = False
        current_square_index = int(move_target_index)

        while current_square_index >= 0 and left_flag == 0 and (current_square_index % 9) != 0:
            current_square_index -= 1
            if red_found is True and current_square_index >= 0:
                if self._game_board_array[current_square_index] == ally_color:
                    for squares in mini_list:
                        candidates_for_removal_list.append(squares)
                    left_flag = 1
                elif self._game_board_array[current_square_index] == "_":
                    left_flag = 1
            if current_square_index >= 0 and (current_square_index % 9) != 0 and \
                    self._game_board_array[current_square_index] == enemy_color and left_flag == 0:
                red_found = True
                mini_list.append(current_square_index)
            else:
                left_flag = 1

        # Searching for horizontal right removal
        mini_list = list()
        right_flag = int(0)
        red_found = False
        current_square_index = int(move_target_index)

        while current_square_index <= 80 and right_flag == 0 and ((current_square_index+1) % 9) != 0:
            current_square_index += 1
            if red_found is True and current_square_index <= 80:
                if self._game_board_array[current_square_index] == ally_color:
                    for squares in mini_list:
                        candidates_for_removal_list.append(squares)
                    right_flag = 1
                elif self._game_board_array[current_square_index] == "_":
                    right_flag = 1
            if current_square_index <= 80 and ((current_square_index+1) % 9) != 0 \
                    and self._game_board_array[current_square_index] == enemy_color and right_flag == 0:
                red_found = True
                mini_list.append(current_square_index)
            else:
                right_flag = 1

        # Searching for corner removal
        # print("Current move_target_index:", move_target_index)
        if self._game_board_array[0] == enemy_color:
            if move_target_index == 1:
                if self._game_board_array[9] == ally_color:
                    candidates_for_removal_list.append(0)
            if move_target_index == 9:
                if self._game_board_array[1] == ally_color:
                    candidates_for_removal_list.append(0)

        if self._game_board_array[8] == enemy_color:
            if move_target_index == 7:
                if self._game_board_array[17] == ally_color:
                    candidates_for_removal_list.append(8)
            if move_target_index == 17:
                if self._game_board_array[7] == ally_color:
                    candidates_for_removal_list.append(8)

        if self._game_board_array[72] == enemy_color:
            if move_target_index == 63:
                if self._game_board_array[73] == ally_color:
                    candidates_for_removal_list.append(72)
            if move_target_index == 73:
                if self._game_board_array[63] == ally_color:
                    candidates_for_removal_list.append(72)

        if self._game_board_array[80] == enemy_color:
            if move_target_index == 71:
                if self._game_board_array[79] == ally_color:
                    candidates_for_removal_list.append(80)
            if move_target_index == 79:
                if self._game_board_array[71] == ally_color:
                    candidates_for_removal_list.append(80)

        # Removing the candidates
        # print("Here's candidates_for_removal right before action", candidates_for_removal_list)

        for square in candidates_for_removal_list:
            self._game_board_array[square] = "_"
            if self._active_player == "BLACK":
                self._blacks_number_of_captured_pieces += 1
            elif self._active_player == "RED":
                self._reds_number_of_captured_pieces += 1
