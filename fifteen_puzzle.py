"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods
    def right_below_invariant(self, target_row, target_col):
        """
        Check the tiles at the right size and below are placed in the target position
        Returns a boolean
        """
        # check the tile to the right of position of tile0
        for col_index in range(target_col+1, self._width):
            if self.current_position(target_row, col_index) != (target_row, col_index):
                return False
        # check the tiles below the tile0
        for row_index in range(target_row+1, self._height):
            for col_index in range(self._width):
                if self.current_position(row_index, col_index) != (row_index, col_index):
                    return False
        return True

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self._grid[target_row][target_col] == 0:
            if target_row == self._height-1 and target_col == self._width-1:
                return True
            # check the tile to the right of position of tile0
            return self.right_below_invariant(target_row, target_col)
        else:
            return False

    def move_zero_to_pos(self, zero, target):
        """
        Place zero tile at target position
        returns a move string
        """
        move_string = ""
        if zero[0] == target[0]:
            if zero[1] > target[1]:
                move_string += "l"
            else:
                move_string += "r"
        elif zero[1] == target[1]:
            if zero[0] > target[0]:
                move_string += "u"
            else:
                move_string += "d"
        elif zero[0] > target[0]:
            move_string += "u"
        elif zero[1] < target[1]:
            move_string += "d"
        else:
            move_string += "l"
        return move_string

#    def move_tile_to_position_parallel(self, zero, target_tem, target, target_value):
#        """
#        Place target tile to target position
#        returns a move string
#        for the situation
#                  target_temp zero
#        target_pos
#        """
#        move_string = ""
#        zero_col = zero[1]
#        target_tem_row = target_tem[0]
#        target_tem_col = target_tem[1]
#        target_col = target[1]
#
#
    def move_tile_to_target_position(self, zero, target_tem, target, target_value):
        """
        Place target tile at target position
        returns a move string
        """
        zero_row = zero[0]
        zero_col = zero[1]
        target_tem_row = target_tem[0]
        target_tem_col = target_tem[1]
        target_row = target[0]
        target_col = target[1]
        move_string = ""
        #for the situation
        # zero  target_temp  target_pos
        if zero_row == target_tem_row and target_tem_row == target_row and target_tem_col < target_col:
            move_string = "u"+ (target_col -zero_col) * "r" + "d" + (target_col-target_tem_col) *"l"
        #for the situation
        # zero  target_pos target_temp
        elif zero_row == target_tem_row and target_tem_row == target_row and target_tem_col > target_col:
            move_string = (self._width -1- zero_col)*"r"+ "u" + (self._width-1) * "l" + "d" + zero_col*"r"
        #for the situation
        #zero target_temp
        #target_pos
        elif zero_row == target_tem_row and target_tem_col > zero_col:
            move_string += "dru"
        #for the situation
        #target_temp zero
        #
        #target_pos
        elif zero_row == target_tem_row and target_tem_col < zero_col and (abs(target_tem_row-target_row) > 1 or zero_row == 0):
            move_string += "dlu"
        #for the situation
        #      target_temp zero
        #target_pos
        elif zero_row == target_tem_row and target_tem_col < zero_col and abs(target_tem_row-target_row) == 1:
            grid_tem = self.clone()
            # target actual col is not equal to target col
            # move target to (target_tem_row, target_col)
            while grid_tem.get_number(target_tem_row,target_col)!= target_value:
                move_string_target = (self._width -1- zero_col)*"r"+ "u" + (self._width-1) * "l" + "d" + zero_col*"r"
                grid_tem.update_puzzle(move_string_target)
                move_string += move_string_target
            # move zero to (target_tem_row-1, target_col)
            while grid_tem.get_number(target_tem_row-1,target_col)!= 0:
                zero = grid_tem.current_position(0, 0)
                move_string_target = grid_tem.move_zero_to_pos(zero,(target_tem_row-1,target_col))
                grid_tem.update_puzzle(move_string_target)
                move_string += move_string_target
#            move_string += self.move_tile_to_position_parallel(zero, target_tem, target, target_value)
        #for the situation
        #target_temp zero
        #
        #                target_pos
        elif zero_col == target_tem_col  and zero_row < target_tem_row and target_tem_row < target_row\
            and zero_col <= target_col:
            move_string += "lddru"
        #for the situation
        #zero
        #target_temp
        #for the situation
        #            zero
        # target_pos target_temp
        #                target_pos
        elif (zero_col == target_tem_col  and zero_row < target_tem_row and target_tem_row < target_row) or\
            (zero_col == target_tem_col and target_tem_row == target_row and target_tem_col > target_col):
            move_string += "ldr"
        #for the situation
        #target_temp
        #zero
        #                target_pos
        elif zero_col == target_tem_col  and zero_row  > target_tem_row and target_tem_row < target_row and\
            target_tem_col == 0:
            move_string += "rul"
        elif zero_col == target_tem_col  and zero_row  > target_tem_row and target_tem_row < target_row:
            move_string += "lur"
        #for the situation
        # zero
        # target_temp   target_pos
        elif zero_col == target_tem_col and target_tem_row == target_row and target_tem_col < target_col:
            move_string += "rdl"
        return move_string

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        move_string = ""
        if target_row <= 1 or target_col == 0:
            return ""
        assert self.lower_row_invariant(target_row, target_col)
        # move zero to the target's position
        tile = self.current_position(target_row, target_col)
        solved_value = target_col + self._width * target_row
        while self.get_number(tile[0],tile[1]) != 0:
            zero = self.current_position(0, 0)
            move_string_target = self.move_zero_to_pos(zero,tile)
            self.update_puzzle(move_string_target)
            move_string += move_string_target
        # move target to the target position
        zero = self.current_position(0, 0)
        while self.get_number(target_row,target_col) != solved_value:
            target_temp = self.current_position(target_row, target_col)
            move_string_target = self.move_tile_to_target_position(zero,target_temp,(target_row, target_col),solved_value)
            move_string += move_string_target
            self.update_puzzle(move_string_target)
            zero = self.current_position(0, 0)
        # move zero to (target_row, target_col-1)
        while self.get_number(target_row,target_col-1)!= 0:
            zero = self.current_position(0, 0)
            move_string_target = self.move_zero_to_pos(zero,(target_row,target_col-1))
            self.update_puzzle(move_string_target)
            move_string += move_string_target
        assert self.lower_row_invariant(target_row, target_col-1)
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        if target_row == 0:
            return ""
        assert self.lower_row_invariant(target_row, 0)
        solved_value = self._width * target_row
        # move the zero tile from (i,0) to (i−1,1)
        move_string = "ur"
        self.update_puzzle(move_string)
        zero = self.current_position(0,0)
        if self.get_number(target_row,0) == solved_value:
            while self.get_number(target_row-1,self._width-1) != 0:
                zero = self.current_position(0,0)
                move_string_target = self.move_zero_to_pos(zero,(target_row-1,self._width-1))
                move_string += move_string_target
                self.update_puzzle(move_string_target)
        else:
            # move zero to the target's position
            tile = self.current_position(target_row,0)
            while self.get_number(tile[0],tile[1]) != 0:
                zero = self.current_position(0, 0)
                move_string_target = self.move_zero_to_pos(zero,tile)
                move_string += move_string_target
                self.update_puzzle(move_string_target)
            # move target to the target position(row-1,1)
            while self.get_number(target_row-1,1) != solved_value:
                zero = self.current_position(0, 0)
                target_temp = self.current_position(target_row, 0)
                move_string_target = self.move_tile_to_target_position(zero,target_temp,(target_row-1, 1),solved_value)
                move_string += move_string_target
                self.update_puzzle(move_string_target)
            # move zero to the target position(row-1,0)
            while self.get_number(target_row-1,0) != 0:
                zero = self.current_position(0, 0)
                if zero[0] == target_row-1:
                    move_string += "u"
                    self.update_puzzle("u")
                else:
                    move_string_target = self.move_zero_to_pos(zero,(target_row-1,0))
                    self.update_puzzle(move_string_target)
                    move_string += move_string_target
            # move fix move
            self.update_puzzle("ruldrdlurdluurddlur")
            move_string += "ruldrdlurdluurddlur"
            # move zero to the target position(row-1,width-1)
            while self.get_number(target_row-1,self._width-1) != 0:
                zero = self.current_position(0, 0)
                move_string_target = self.move_zero_to_pos(zero,(target_row-1,self._width-1))
                move_string += move_string_target
                self.update_puzzle(move_string_target)
        assert self.lower_row_invariant(target_row-1, self._width-1)
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[0][target_col] == 0:
            if self.current_position(1, target_col) == (1, target_col):
                # check the tile to the right of position of tile0
                for col_index in range(target_col+1, self._width):
                    if self.current_position(0, col_index) != (0, col_index):
                        return False
            else:
                return False
            return self.right_below_invariant(1, target_col)
        else:
            return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        return self.lower_row_invariant(1, target_col)

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        if target_col < 1:
            return ""
        solved_value = target_col
        # move the zero tile from (0,j) to (1,j-1)
        move_string = "ld"
        self.update_puzzle(move_string)
        zero = self.current_position(0,0)
        if self.get_number(0,target_col) == solved_value:
            while self.get_number(1,target_col-1) != 0:
                move_string_target = self.move_zero_to_pos(zero,(1,target_col-1))
                move_string += move_string_target
                self.update_puzzle(move_string_target)
        else:
            # move zero to the target's position
            tile = self.current_position(0,target_col)
            while self.get_number(tile[0],tile[1]) != 0:
                zero = self.current_position(0, 0)
                move_string_target = self.move_zero_to_pos(zero,tile)
                move_string += move_string_target
                self.update_puzzle(move_string_target)
            # move target to the target position(1,col-1)
            while self.get_number(1,target_col-1) != solved_value:
                zero = self.current_position(0, 0)
                target_temp = self.current_position(0, target_col)
                move_string_target = self.move_tile_to_target_position(zero,target_temp,(1,target_col-1),solved_value)
                move_string += move_string_target
                self.update_puzzle(move_string_target)
            # move zero to the target position(1,col-2)
            while self.get_number(1,target_col-2) != 0:
                zero = self.current_position(0, 0)
                move_string_target = self.move_zero_to_pos(zero,(1,target_col-2))
                self.update_puzzle(move_string_target)
                move_string += move_string_target
            # move fix move
            self.update_puzzle("urdlurrdluldrruld")
            move_string += "urdlurrdluldrruld"
            # move zero to the target position(1,col-1)
            while self.get_number(1,target_col-1) != 0:
                zero = self.current_position(0, 0)
                move_string_target = self.move_zero_to_pos(zero,(1,target_col-1))
                move_string += move_string_target
                self.update_puzzle(move_string_target)
        assert self.row1_invariant(target_col-1)
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        if target_col < 1:
            return ""
        assert self.row1_invariant(target_col)
        move_string = ""
        # move zero to the target's position
        tile = self.current_position(1, target_col)
        solved_value = target_col + self._width
        while self.get_number(tile[0],tile[1]) != 0:
            zero = self.current_position(0, 0)
            move_string_target = self.move_zero_to_pos(zero,tile)
            move_string += move_string_target
            self.update_puzzle(move_string_target)
        # move target to the target position (1, target_col)
        zero = self.current_position(0, 0)
        while self.get_number(1,target_col) != solved_value:
            target_temp = self.current_position(1, target_col)
            move_string_target = self.move_tile_to_target_position(zero,target_temp,(1, target_col),solved_value)
            move_string += move_string_target
            self.update_puzzle(move_string_target)
            zero = self.current_position(0, 0)
        # move zero to (0, target_col)
        while self.get_number(0,target_col) != 0:
            zero = self.current_position(0, 0)
            move_string_target = self.move_zero_to_pos(zero,(0,target_col))
            move_string += move_string_target
            self.update_puzzle(move_string_target)
        assert self.row0_invariant(target_col)
        return move_string

    ###########################################################
    # Phase 3 methods
    def validate_puzzle_solved(self, row, col):
        """
        Check the upper left 2x2 part of the puzzle solved
        """
        # check the tiles below the tile0
        for row_index in range(row-1,-1,-1):
            for col_index in range(col-1,-1,-1):
                if self.current_position(row_index, col_index)!=(row_index, col_index):
                    return False,(row_index, col_index)
        return True,(0, 0)

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1)
        move_string = ""
        called = 0
        # move zero to the (0,0)
        while self.get_number(0,0) != 0:
            zero = self.current_position(0, 0)
            move_string_target = self.move_zero_to_pos(zero,(0,0))
            move_string += move_string_target
            self.update_puzzle(move_string_target)
        while called <= 3 and not self.validate_puzzle_solved(2,2)[0]:
            self.update_puzzle("drul")
            move_string += "drul"
            called +=1
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        called_time = 0
        result = self.validate_puzzle_solved(self._height,self._width)
        if not result[0]:
            tile = result[1]
            # move zero to the untarget position
            while self.get_number(tile[0],tile[1]) != 0:
                zero = self.current_position(0, 0)
                move_string_target = self.move_zero_to_pos(zero,tile)
                self.update_puzzle(move_string_target)
                move_string += move_string_target
            zero = self.current_position(0, 0)
            while called_time <20 and not self.validate_puzzle_solved(self._height,self._width)[0]:
                if zero[0] > 1 and zero[1] > 0:
                    move_string += self.solve_interior_tile(zero[0], zero[1])
                    zero = self.current_position(0, 0)
                elif zero[0] > 1 and zero[1] == 0:
                    move_string += self.solve_col0_tile(zero[0])
                    zero = self.current_position(0, 0)
                elif zero[0] == 1 and zero[1] >= 2:
                    move_string += self.solve_row1_tile(zero[1])
                    zero = self.current_position(0, 0)
                elif zero[0] == 0 and zero[1] >= 0:
                    move_string += self.solve_row0_tile(zero[1])
                    zero = self.current_position(0, 0)
                elif (zero[0] == 0 or zero[0] == 1) and (zero[1] == 0 or zero[1] == 1):
                    move_string += self.solve_2x2()
                    zero = self.current_position(0, 0)
        return move_string

#Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]]))
poc_fifteen_gui.FifteenGUI(Puzzle(5, 5, [[24, 23, 22,21,20], [19, 18, 17,16,15], [14, 13, 12,11,10],[9,8,7,6,5],[4,3,2,1,0]]))
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, [[15, 14, 13, 12], [11,10,9,8],[7, 6,5,4], [3,2, 1, 0]]))
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 5, [[12, 11, 9, 3, 4], [7, 11, 5, 14, 13], [1, 6, 8, 15, 0], [2, 16, 17, 18, 19]]))
