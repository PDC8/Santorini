from player import RandomPlayer, HumanPlayer, HeuristicPlayer

class PlayerFactory():
    """
    Establishes a class to handle the creation of players
    """
    def create_player(self, id, type, board):
        if type == 'human':
            return HumanPlayer(id, board)
        elif type == 'random':
            return RandomPlayer(id, board)
        else:
            return HeuristicPlayer(id, board)
        
def make_player(player_type, *args):
    factory = PlayerFactory()
    return factory.create_player(player_type, *args)