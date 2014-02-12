from Position import Position

class Zone:
    def __init__(self, name, start, end):
        self._bounds = [range(start[0],end[0]),range(start[1],end[1]),range(start[2],end[2])]
        self._lower = start
        self._upper = end
        self._name = name
        self._subzones = []
        
    def __contains__(self, other):
        """
        The input of other will be a Position object or another zone.
        """
        if isinstance(other, Zone):
            for axis in range(3):
                if other._upper[axis]-1 not in self._bounds[axis]:
                    # -1 on this boundary because upper range is not inclusive
                    print(other._upper[axis], self._bounds[axis])
                    return False
                if other._lower[axis] not in self._bounds[axis]:
                    other._lower[axis], self._bounds[axis]                    
                    return False
        else:
            for axis in range(3):
                if other[axis] not in self._bounds[axis]:
                    return False
        return True
       
    def set_description(self, description):
        self._description = description
        
    def get_description(self):
        return self._description
        
    def __str__(self):
        return self._name
    
    def create_subzone(self, name, start, end):
        subzone = Zone(name, start, end)
        if subzone in self:
            self._subzones.append(subzone)
        else:
            raise Exception("Tried to build zone '" + name + "' outside parent zone '" + str(self) + "'.")

def initialize_zones():
    """
    Calling this function generates the world and returns the generated Zones as
    a list.
    """
    pass

World = Zone("World", Position([-10,-10,0]), Position([10,10,2]))