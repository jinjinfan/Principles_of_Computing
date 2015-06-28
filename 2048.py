"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

SQUARE_VALUE = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
TILE_INTIALIZED = 2
# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    output = list(line)
    return_list = list(line)
    for output_index in range(len(line)):
        output[output_index] = 0
        return_list[output_index] = 0
    output_valuenum = 0
    # create an output list that has all of the non-zero tiles slid over 
    # to the beginning of the list with the appropriate number of zeroes 
    # at the end of the list.
    for line_value in line:
        if line_value != 0:
            output[output_valuenum] = line_value
            output_valuenum += 1
    
    # Iterate over the list created in the previous step and create another new list
    # in which pairs of tiles in the first list are replaced with a tile of twice 
    # the value and a zero tile.
    return_list_index = 0
    for output_index in range(len(output)):
        if output[output_index] == 0:
            continue
        else:    
            if output_index != len(output)-1 and output[output_index] == output[output_index+1]:
                return_list[return_list_index] = 2 * output[output_index]
                output[output_index+1] = 0
                return_list_index += 1  
            else:
                return_list[return_list_index] = output[output_index]
                return_list_index += 1    
    return return_list

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self.reset()
        
        # create indices for UP, DOWN, LEFT, RIGHT
        grid_by_row = [[(dummy_row, dummy_col) for dummy_col in range(self._width)]
                                               for dummy_row in range(self._height)]
        grid_by_col = [[(dummy_row, dummy_col) for dummy_row in range(self._height)]
                                               for dummy_col in range(self._width)]
        self._indices = {UP: grid_by_row[0],
                         DOWN: grid_by_row[self._height-1],
                         LEFT: grid_by_col[0],
                         RIGHT: grid_by_col[self._width-1]}
        # get the len of tiles to be merged for UP, DOWN, LEFT, RIGHT
        self._mergelist_len = {UP: self._height,
                               DOWN: self._height,
                               LEFT: self._width,
                               RIGHT: self._width}
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[ 0 for dummy_col in range(self._width)]
                          for dummy_row in range(self._height)]
        for dummy_index in range(TILE_INTIALIZED):
            self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        tile_changed = False
        offset = OFFSETS[direction]
        indice =  self._indices[direction]
        tem_list =[0 for dummy_row in range(self._mergelist_len[direction])]
        # iterate over the entries of the associated row or column starting at the 
        # specified initial tile according to the direction
        for square in indice:
            # store the tile values into a temporary list
            for index in range(self._mergelist_len[direction]):
                row = square[0] + index * offset[0]
                col = square[1] + index * offset[1]
                tem_list[index] = self.get_tile(row, col)
            # merge the temporary list    
            merged_list = merge(tem_list)
            # store the merged tile values back into the grid
            for index in range(self._mergelist_len[direction]):
                row = square[0] + index * offset[0]
                col = square[1] + index * offset[1]
                if self._grid[row][col]!= merged_list[index]:
                    tile_changed = True
                self.set_tile(row, col,merged_list[index])
        if tile_changed:
            self.new_tile()
                
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        row_random = random.randrange(0, self._height)
        col_random = random.randrange(0, self._width)
        if self._grid[row_random][col_random] == 0:
            self._grid[row_random][col_random] = random.choice(SQUARE_VALUE)
        else:
            self.new_tile()

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 5))

