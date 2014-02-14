from Position import Position

class Zone:
    def __init__(self, name, start, end, parent=None, description=None):
        self._bounds = [range(start[0],end[0]),range(start[1],end[1]),range(start[2],end[2])]
        self._lower = start
        self._upper = end
        self._name = name
        self._subzones = []
        self._parent = parent
        self._description = description
        if parent is not None:
            self.create_subzone(parent)
            
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
        
    def get_description(self):
        return self._description
    
    def get_subzones(self):
        return self._subzones
        
    def __str__(self):
        return self._name
    
    def create_subzone(self, parent):
        if self in parent:
            # TODO: check for sister Zones and disallow any overlaps.
            parent._subzones.append(self)
            return
        raise Exception("Tried to build zone '" + str(self) + "' outside parent zone '" + str(parent) + "'.")


# All the Zones are generated below. The global scope zone "World" is generated
# first, and then all it's subzones are instantiated.

World = Zone("World", Position([-10,-10,0]), Position([10,10,3]))

def initialize_zones():
    """
    This is a container for the zones since the temporary variables need to expire
    once zoning is completed. The subzones will remain in existence as long as
    World remains in scope.
    """
    Hull = Zone("Hull Hall", Position([-10,-10,0]), Position([10,10,3]), World)
    Zone("2B", Position([0,0,1]), Position([3,10,2]), Hull)
    
initialize_zones()