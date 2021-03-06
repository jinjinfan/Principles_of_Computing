"""
Zombie Apocalypse
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None,
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human

    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        grid_width = poc_grid.Grid.get_grid_width(self)
        grid_height = poc_grid.Grid.get_grid_height(self)
        visited  = poc_grid.Grid(grid_height,grid_width)
        distance_field = [[grid_width*grid_height for dummy_col in range(grid_width)]
                                for dummy_row in range(grid_height)]
        boundary = poc_queue.Queue()

        # For cells in the queue, initialize visited to be FULL and distance_field to be zero
        if entity_type == ZOMBIE:
            for item in self._zombie_list:
                boundary.enqueue(item)
        elif entity_type == HUMAN:
            for item in self._human_list:
                boundary.enqueue(item)
        for item in boundary:
            visited.set_full(item[0], item[1])
            distance_field[item[0]][item[1]] = 0

        while len(boundary)!= 0:
            cell = boundary.dequeue()
            neighbors = self.four_neighbors(cell[0], cell[1])
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]) and visited.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[cell[0]][cell[1]] + 1
        return distance_field

    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        results = []
        for human_ in self.humans():
            human_move = []
            max_distance = float('-inf')
            neighbors = self.eight_neighbors(human_[0], human_[1])
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]):
                    if max_distance < zombie_distance[neighbor[0]][neighbor[1]]:
                        max_distance = zombie_distance[neighbor[0]][neighbor[1]]
            if max_distance < zombie_distance[human_[0]][human_[1]]:
                max_distance = zombie_distance[human_[0]][human_[1]]
                human_move.append(human_)
            else:
                for neighbor in neighbors:
                    if max_distance == zombie_distance[neighbor[0]][neighbor[1]]:
                        human_move.append(neighbor)
            results.append(random.choice(human_move))
        self._human_list = results

    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        results = []
        for zombie_ in self.zombies():
            zombie_move = []
            min_distance = float('inf')
            neighbors = self.four_neighbors(zombie_[0], zombie_[1])
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]):
                    if min_distance > human_distance[neighbor[0]][neighbor[1]]:
                        min_distance = human_distance[neighbor[0]][neighbor[1]]
            if min_distance > human_distance[zombie_[0]][zombie_[1]]:
                min_distance = human_distance[zombie_[0]][zombie_[1]]
                zombie_move.append(zombie_)
            else:
                for neighbor in neighbors:
                    if min_distance == human_distance[neighbor[0]][neighbor[1]]:
                        zombie_move.append(neighbor)
            results.append(random.choice(zombie_move))
        self._zombie_list = results

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40))