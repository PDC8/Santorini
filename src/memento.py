from __future__ import annotations
from abc import ABC, abstractmethod
from copy import deepcopy

class Originator():
    """
    The Originator holds some important state that may change over time. It also
    defines a method for saving the state inside a memento and another method
    for restoring the state from it.
    """

    
    def __init__(self, board, turn) -> None:
        self._board = deepcopy(board)
        self._turn = turn

    def save(self) -> Memento:
        """
        Saves the current state inside a memento.
        """

        return ConcreteMemento(self._board, self._turn)
    
    def set_state(self, board, turn) -> None:
        """
        Alters the current state.
        """
        self._board = deepcopy(board)
        self._turn = turn  

    def get_state(self):
        """
        Returns the originator's current state
        """
        return [self._board, self._turn]

    def restore(self, memento: Memento) -> None:
        """
        Restores the Originator's state from a memento object.
        """

        self._state = memento.get_state()
        self._board = deepcopy(self._state[0])
        self._turn = self._state[1]  

class Memento(ABC):
    """
    The Memento interface provides a way to retrieve the memento's metadata,
    such as creation date or name. However, it doesn't expose the Originator's
    state.
    """

    @abstractmethod
    def get_state(self):
        pass


class ConcreteMemento(Memento):
    def __init__(self, board, turn) -> None:
        self._board = deepcopy(board)
        self._turn = turn

    def get_state(self):
        """
        The Originator uses this method when restoring its state.
        """
        return [self._board, self._turn]

class Caretaker():
    """
    The Caretaker doesn't depend on the Concrete Memento class. Therefore, it
    doesn't have access to the originator's state, stored inside the memento. It
    works with all mementos via the base Memento interface.
    """

    def __init__(self, originator: Originator) -> None:
        self._mementos = []
        self._originator = originator
        self._current_index = -1

    def backup(self) -> None:
        """
        Adds the latest state and nullfies all subsequent states
        """
        del self._mementos[self._current_index + 1:]
        self._mementos.append(self._originator.save())
        self._current_index = len(self._mementos) - 1

    def undo(self) -> None:
        """
        Roll back to a previous state
        """
        if self._current_index > 0:
            self._current_index -= 1
            memento = self._mementos[self._current_index]
            self._originator.restore(memento)
    
    def redo(self) -> None:
        """
        Reverses the most recent undo
        """
        if self._current_index < len(self._mementos) - 1:
            self._current_index += 1
            memento = self._mementos[self._current_index]
            self._originator.restore(memento)

        
