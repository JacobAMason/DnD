# MapGenerator.py
"""
MapGenerator keeps all the coordinate positions of all entities in the same location.
It offers methods for determining the location of other entities in any given entity's radius.
MapGenerator is mostly used to determine a Player's visible range, but it can also be used
by mobs to determine what is in proximity to them.
"""
import logging

logger = logging.getLogger("MapGen")

class MapGenerator:
    def __init__(self):
        self._entities = []

    def track(self, entity):
        """
        Pass this method an entity and MapGenerator will track it.
        """
        self._entities.append(entity)
        logger.debug('Appended entity "%s"', entity)

    def look(self, radius):
        """
        Returns map data based on an Entity's visible radius.
        """
        pass

MapGen = MapGenerator()