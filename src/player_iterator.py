class PlayerIterator:
    """
    A two-player iterator that facilitates the game progression.
    """
    def __init__(self, players):
        self._players = players
        self._current_index = -1

    def next_player(self):
        """Moves to the next player and returns them."""
        self._current_index = (self._current_index + 1) % len(self._players)
        return self._players[self._current_index]

    def current_player(self):
        """Returns the current player."""
        return self._players[self._current_index]

    def previous_player(self):
        """Returns the previous player."""
        if self._current_index == -1:
            return None
        prev_index = (self._current_index - 1) % len(self._players)
        return self._players[prev_index]