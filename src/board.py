from tile import SantoriniTile

class Board():
    """
    This is an abstract class that represents a game board characterized by a grid structure.
    """
    def __init__(self, rows, cols, tile_type):
        self._rows = rows
        self._cols = cols
        self._grid = [[tile_type(r, c) for c in range(self._cols)] for r in range(self._rows)]

    def _display(self):
        pass

class SantoriniBoard(Board):
    """
    Concrete board class that makes a 5x5 board and initializes four pieces (workers) for Santorini
    """
    def __init__(self):
        super().__init__(5, 5, SantoriniTile)

        self._worker = {} 
        self._worker['A'] = self._grid[3][1]
        self._worker['B'] = self._grid[1][3]
        self._worker['Y'] = self._grid[1][1]
        self._worker['Z'] = self._grid[3][3]

        self._direction_indices = {"n" : [-1, 0], "ne" : [-1, 1], "e" : [0, 1], "se" : [1, 1], "s" : [1, 0], "sw" : [1, -1], "w" : [0, -1], "nw" : [-1, -1]}

    def display(self):
        """
        Displays the current state of the board according the format in the spec
        """
        horizontal_border = '+--+--+--+--+--+'
        for row in self._grid:
            print(horizontal_border)
            row_str = "|"
            for tile in row:
                tile_str = str(tile.height)
                worker_on_tile = False
                for w in self._worker:
                    if self._worker[w] == tile:
                        tile_str += w
                        worker_on_tile = True
                        break
                if not worker_on_tile:
                    tile_str += " "
                row_str += tile_str + "|"
            print(row_str)
        print(horizontal_border)
                
    def valid_direction(self, direction):
        """
        Checks if a direction is n, s, e, w, ne, nw, se, sw
        """
        if direction in self._direction_indices:
            return True
        else:
            return False
    
    def _is_occupied(self, tile):
        """
        Checks if a tile is occupied by a worker
        """
        for w in self._worker:
            if self._worker[w] == tile:
                return True
        return False
    
    def _max_height(self, tile):
        """
        Returns whether or not a tile has a height of 4
        """
        if tile.height == 4:
            return True
        else:
            return False
        
    def valid_move(self, w, direction):
        """
        Returns whether or not a direction is a valid move for a given worker
        """
        row = self._worker[w].row + self._direction_indices[direction][0]
        col = self._worker[w].col + self._direction_indices[direction][1]
        
        if row < 0 or row >= 5 or col < 0 or col >= 5:
            return False
        temp_tile = self._grid[row][col]
        if self._is_occupied(temp_tile):
            return False
        if self._max_height(temp_tile):
            return False
        if temp_tile.height - self._worker[w].height  >  1:
            return False
        return True

    def move_list(self, w):
        """
        Returns a list of valid moves
        """
        lst = []
        for dir in self._direction_indices:
            if self.valid_move(w, dir):
                lst.append(dir)
        return lst
    
    def valid_build(self, w, direction):
        """
        Returns whether or not a direction is a valid build for a given worker
        """
        row = self._worker[w].row + self._direction_indices[direction][0]
        col = self._worker[w].col + self._direction_indices[direction][1]

        if row < 0 or row >= 5 or col < 0 or col >= 5:
            return False
        temp_tile = self._grid[row][col]
        if self._is_occupied(temp_tile):
            return False
        if self._max_height(temp_tile):
            return False
        return True
    
    def build_list(self, worker):
        """
        Returns a list of valid builds
        """
        lst = []
        for dir in self._direction_indices:
            if self.valid_build(worker, dir):
                lst.append(dir)
        return lst
    
    def move(self, w, direction):
        """
        Moves a worker to the specifed direction
        """
        row = self._worker[w].row + self._direction_indices[direction][0]
        col = self._worker[w].col + self._direction_indices[direction][1]
        self._worker[w] = self._grid[row][col]

    def build(self, w, direction):
        """
        Builds on a tile relative to the worker
        """
        row = self._worker[w].row + self._direction_indices[direction][0]
        col = self._worker[w].col + self._direction_indices[direction][1]
        self._grid[row][col].height += 1

    def get_worker_height(self, worker):
        """
        Gives the height of the structure that the worker is on
        """
        return self._worker[worker].height
    
    def is_possible_next_turn(self, worker):
        """
        Returns whether or not the a worker has a place to move to
        """
        move = []
        for dir in self._direction_indices:
            new_x = self._worker[worker].row + self._direction_indices[dir][0]
            new_y = self._worker[worker].col + self._direction_indices[dir][1]
            if self.valid_move(worker, dir):
                move.append(self._grid[new_x][new_y])
        if(len(move) == 0):
            return False
        return True

    def height_score(self, lst):
        """
        Calculates the height score according to the spec
        """
        sum = 0
        for w in lst:
            sum += self._worker[w].height
        return sum
    
    def center_score(self, lst):
        """
        Calculates the center score according to the spec
        """
        sum = 0
        for w in lst:
            row = self._worker[w].row 
            col = self._worker[w].col
            if (row == 2 and col == 2):
                sum +=2
            elif (1 <= row <= 3 and 1 <= col <= 3):
                sum +=1
            else:
                sum +=0
        return sum
    
    def _distance(self, worker1, worker2):
            return max(abs(worker1.row  - worker2.row), abs(worker1.col - worker2.col))
    
    def distance_score(self, cur_workers):
        """
        Calculates the distance score according to the spec
        """
        sum = 0
        for workers in [['A', 'B'], ['Y', 'Z']]:
            if workers != cur_workers:
                opponent_workers = workers
        for opponent_worker in opponent_workers:
                min_distance = min(self._distance(self._worker[cur_worker], self._worker[opponent_worker]) for cur_worker in cur_workers)
                sum += min_distance
        return 8 - sum

