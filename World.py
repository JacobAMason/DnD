#from Position import Position

class World:
    def __init__(self, name, start, end):
        self._bounds = [range(start[0],end[0]),range(start[1],end[1]),range(start[2],end[2])]
        self._name = name
        
    def __contains__(self, other):
        """
        The input of other will be a Position object.
        """
        return (other[0] in self._bounds[0] and other[1] in self._bounds[1] and other[2] in self._bounds[2])
       
    def set_description(self, description):
        self._description = description
        
    def get_description(self):
        return self._description
        
    def __str__(self):
        return self._name
    
Earth = World("Earth", [-10,-10,0], [10,10,2])