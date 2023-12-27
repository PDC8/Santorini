import random

class Player():
    """
    This is an abstract class for players. Provides select worker, move, and build 
    capabilities, checks terminal conditions, and handles output
    """
    def __init__(self, id, board):
        self._board = board
        self._id = id
        self._worker_list = [['A', 'B'], ['Y', 'Z']]
        if id == 0:
            self._workers = self._worker_list[0]
            self._color = "white"
        else:
            self._workers = self._worker_list[1]
            self._color = "blue"

        self._center_score = 0
        self._height_score = 0
        self._distance_score = 0

    def _get_color(self):
        return self._color
    
    color = property(_get_color)

    def select_worker(self):
        pass
    def select_move_direction(self):
        pass

    #put this in parent since both random and heurtistic choose build_direction this way
    def select_build_direction(self, worker): 
        """
        Select a valid build direction. Utilized in the random and heuristic classes.
        """
        lst = self._board.build_list(worker)
        if len(lst) != 0:
            return random.choice(lst)
    
    # terminal conditions
    def win(self):
        """
        Checks if a player has a worker with height 3 in which case they win
        """
        for w in self._workers:
            if self._board.get_worker_height(w) == 3:
                return True
        return False
    
    def next_move_possible(self):
        """
        Checks if there is a possible next move
        """
        for w in self._workers:
            if self._board.is_possible_next_turn(w):
                return True
        return False

    # output
    def format(self):
        """
        Outputs according to the spec
        """
        return f"{self._color} ({self._workers[0]}{self._workers[1]})"

    def print_move_score(self):
        """
        Prints out the scores
        """
        self._height_score = self._board.height_score(self._workers)
        self._center_score = self._board.center_score(self._workers)
        self._distance_score = self._board.distance_score(self._workers)
        return f"{self._height_score}, {self._center_score}, {self._distance_score}"
    
class RandomPlayer(Player):
    """
    Concrete class for the random player implementation
    """
    def __init__(self, id, board):
        super().__init__(id, board)

    def select_worker(self):
        """
        Selects a valid worker randomly
        """
        worker1 = self._board.is_possible_next_turn(self._workers[0])
        worker2 = self._board.is_possible_next_turn(self._workers[1])

        if(worker1 and worker2):
            worker = random.choice(self._workers)
        elif(worker1 and not worker2):
            worker = self._workers[0]
        else:
            worker = self._workers[1]
        return worker
    
    def select_move_direction(self, worker):
        """
        Selects a valid move randomly
        """
        lst = self._board.move_list(worker)
        if len(lst) != 0:
            return random.choice(lst)
    
class HeuristicPlayer(Player):
    """
    Concrete class for the heuristic player implementation
    """
    def __init__(self, id, board):
        super().__init__(id, board)
        self._result = None
    
    def select_worker(self):
        """
        Selects a worker with the highest move score
        """
        self._result = self._move_score()
        worker = self._result[0]
        return worker

    def select_move_direction(self, worker):
        """
        Selects a move with the highest move score
        """
        dir = self._result[1]
        return dir
    
    def _move_score(self):
        score_dict = {}
        c1 = 3
        c2 = 2
        c3 = 1
        opp_directions = {'n':'s', 'ne':'sw', 'e':'w', 'se':'nw', 's':'n', 'sw':'ne', 'w':'e', 'nw':'se'}
        for w in self._workers:
            if self._board.is_possible_next_turn(w):
                move_list = self._board.move_list(w)
                for m in move_list:
                    self._board.move(w, m)
                    height_score = self._board.height_score(self._workers)
                    center_score = self._board.center_score(self._workers)
                    distance_score = self._board.distance_score(self._workers)
                    if self.win():
                        move_score = 1000000000
                    else:
                        move_score = c1*height_score + c2*center_score + c3*distance_score
                    self._board.move(w, opp_directions[m])
                    score_dict[move_score] = [w, m]
        max_score = max(score_dict.keys())
        scores_worker_move = []
        for move_score in score_dict:
            if move_score == max_score:
                scores_worker_move.append(score_dict[move_score])
        result = random.choice(scores_worker_move)
        return result
        
class HumanPlayer(Player):
    """
    Concrete class for the human player. It takes in user input.
    """
    def __init__(self, id, board):
        super().__init__(id, board)

    def select_worker(self):
        """
        Selects a worker based on user input and checks for valid input
        """
        flag = False
        while not flag:
            print("Select a worker to move")
            worker = input()
            if worker not in "ABYZ":
                print("Not a valid worker")
            elif worker not in self._workers:
                print("That is not your worker")
            else:
                flag = True
        return worker
    
    def select_move_direction(self, worker):
        """
        Selects a move based on user input, checks for valid input and for feasibility
        """
        flag = False
        while not flag:
            print("Select a direction to move (n, ne, e, se, s, sw, w, nw)")
            move_direction = input()
            if not self._board.valid_direction(move_direction):
                print("Not a valid direction")
            elif not self._board.valid_move(worker, move_direction):
                print(f"Cannot move {move_direction}")
            else:
                flag = True
        return move_direction
            
    def select_build_direction(self, worker):
        """
        Selects a build based on user input, checks for valid input and for feasibility
        """
        flag = False
        while not flag:
            print("Select a direction to build (n, ne, e, se, s, sw, w, nw)")
            build_direction = input()
            if not self._board.valid_direction(build_direction):
                print("Not a valid direction")
            elif not self._board.valid_build(worker, build_direction):
                print(f"Cannot build {build_direction}")
            else:
                flag = True
        return build_direction


