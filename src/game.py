from board import SantoriniBoard
from player_factory import make_player
from memento import Originator, Caretaker
# from player_iterator import PlayerIterator

class Game():
    """
    Sets up the Santorini game by creating a board and players
    """
    def __init__(self, *args):
        self._players = []
        self._white_player_id = 0
        self._blue_player_id = 1
        self._board = SantoriniBoard()
        self._white_player = make_player(self._white_player_id, args[0], self._board)
        self._blue_player = make_player(self._blue_player_id, args[1], self._board)
        self._enable_undo = args[2]
        self._enable_score = args[3]
        self._players.append(self._white_player)
        self._players.append(self._blue_player)
        self._turn_num = 1
        self._current_player = 0

    def play_game(self):
        """
        Starts the game
        """
        originator = Originator(self._board, self._turn_num)
        caretaker = Caretaker(originator)
        caretaker.backup()
        while(True):
            self._board.display()

            # cur_player = player_iterator.next_player()
            # prev_player = player_iterator.previous_player()

            cur_player = self._players[self._current_player]
            prev_player = self._players[(self._current_player - 1) % 2]

            if self._enable_score:
                print(f"Turn: {self._turn_num}, {cur_player.format()}, ({cur_player.print_move_score()})")
            else:
                print(f"Turn: {self._turn_num}, {cur_player.format()}")

            choice = None

            if self._enable_undo:
                print("undo, redo, or next")
                choice = input()

            if choice == "undo":
                caretaker.undo()
                self._restore_game(originator)
            elif choice == "redo":
                caretaker.redo()
                self._restore_game(originator)
            else:
                if not cur_player.next_move_possible() or prev_player.win():
                    print(f"{prev_player.color} has won")
                    break
                
                while(True):
                    worker = cur_player.select_worker()
                    if self._board.is_possible_next_turn(worker):
                        break
                    else:
                        print("That worker cannot move")

                move_dir = cur_player.select_move_direction(worker)
                self._board.move(worker, move_dir)
                build_dir = cur_player.select_build_direction(worker)
                self._board.build(worker, build_dir)

                if self._enable_score:
                    print(f"{worker},{move_dir},{build_dir} ({cur_player.print_move_score()})")
                else:
                    print(f"{worker},{move_dir},{build_dir}")
                
                self._current_player = self._turn_num % 2
                # cur_player = player_iterator.next_player()
                self._turn_num += 1

                originator.set_state(self._board, self._turn_num)
                caretaker.backup()
    
    def _restore_game(self, originator):
        old_state = originator.get_state()
        self._board = old_state[0]
        self._turn_num = old_state[1]
        self._current_player = (self._turn_num - 1) % 2




    
