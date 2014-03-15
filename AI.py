"""
AI.py

This Module contains a clock that moves mob groups of a certain speed on their
respective speed markings.
Example: a mob with speed 20 will move every 20 seconds.

This module will also save every player account every minute.

This Module uses threading and will not crash if the server crashes.
Start the clock by calling Clock.start() (This is inside the threading module.)
Stop the clock by calling Clock.stop()
"""

import time, logging
from threading import Thread
from Mob import Mob
from Player import Player
from MapGenerator import MapGen

logger = logging.getLogger("AI")

class Clock(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        logger.info("[!] AI clock started.")
        self._alive = True
        self._timeIn = int(time.time())
        
        def move_mob(speed):
            logger.debug("Moving mobs of speed %s", speed)
            for mob in Mob.instances:
                if mob.get_speed() == speed:
                    mob.move()
                    
        def current_time():
            return int(time.time())-self._timeIn

        try:
            while self._alive:
                move_mob(10)

                for mob in Mob.instances:
                    # Dump the following list after movements, forcing it to rebuild before every check.
                    mob.unfollow()

                if current_time()%20 == 0:
                    move_mob(20)
                    
                if current_time()%30 == 0:
                    move_mob(30)            
                
                if current_time() >= 60:
                    move_mob(60)
                    for p in Player.instances:
                        p.save()
                    self._timeIn = int(time.time())

                MapGen.refresh_view(Player.instances)
                    
                logger.debug("Timer active: %s", current_time())
                time.sleep(10)
        finally:
            logger.warn("[!] AI clock stopped.")
            
    def stop(self):
        self._alive = False
        self.join()