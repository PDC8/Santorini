class Tile():
    """This is an abstract class for tiles. Provides accessor function for row and col.
    """
    def __init__(self, row, col):
        self._row = row
        self._col = col

    def _get_row(self):
        return self._row

    row = property(_get_row)

    def _get_col(self):
        return self._col

    col = property(_get_col)

class SantoriniTile(Tile):
    """
    Concrete Tile class with added accessor and mutator functionality for a new height attribute
    """
    def __init__(self, row, col):
        super().__init__(row, col)
        self._height = 0
    
    def _get_height(self):
        return self._height
    
    def _set_height(self, height):
        self._height = height
    
    height = property(_get_height, _set_height)
    
    def __str__(self):
        """Prints the height
        """
        return f"{self._height}"
    

    
   