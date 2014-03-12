# MapGenerator.py
"""
MapGenerator keeps all the coordinate positions of all entities in the same location.
It offers methods for determining the location of other entities in any given entity's radius.
MapGenerator is mostly used to determine a Player's visible range, but it can also be used
by mobs to determine what is in proximity to them.
"""
import logging
from BinaryEncodings import BE

# Future use for when the map should display other people and things.
# from Player import Player
# from Mob import Mob

logger = logging.getLogger("Mapper")

class MapGenerator:
    def __init__(self):
        logger.info("MapGen: Online")

    def start(self, entity):
        """
        Sends the "start" command to the client so the gui will initialize.
        """
        logger.debug("Sending MAP INIT.", entity)
        entity.request.send(BE.MAP + bytes("INIT", "utf-8"))
        self.update_position(entity)

    def update_position(self, entity):
        """
        Entity calls this when it has changed something about its positional data.

        Currently just returns its own position.
        """
        logger.debug("Sending %s MAP data.", entity)
        entity.request.send(BE.MAP + bytes(",".join(str(e) for e in entity.get_position()), "utf-8"))

    def look(self, radius):
        """
        Returns map data based on an Entity's visible radius.
        """
        pass

MapGen = MapGenerator()