class Position:
    def __init__(self, coords):
        self._coords = coords
        
    def __getitem__(self, i):
        return self._coords[i]
    
    def __str__(self):
        return str(self._coords)
    
    def __add__(self, other):
        return Position([self[i] + other[i] for i in range(3)])
    
    def __iadd__(self, other):
        return self + other
    
    def __mul__(self, other):
        """
        This only works for scalars right now.
        """
        return Position([self[i] * other for i in range(3)])
    
    def __rmul__(self, other):
        return self * other
    
    def __imul__(self, other):
        return self * other
    
    def __sub__(self, other):
        return self + (-1 * other)
    
    def __isub__(self, other):
        return self - other
    
    def __rsub__(self, other):
        return self - other
    
    def __neg__(self):
        return self * -1
    
    def __eq__(self, other):
        return self._coords == other._coords
    
    def __ne__(self, other):
        return not self == other


# Used to adjust a position 
Unit = {"i": Position([1,0,0]), "j": Position([0,1,0]), "k": Position([0,0,1])} 