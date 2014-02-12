"""
AI.py

This Module contains a clock that moves mob groups of a certain speed on their
respective speed markings.
Example: a mob with speed 20 will move every 20 seconds.

This Module uses threading and will not crash if the server crashes.
Start the clock by calling Clock.start() (This is inside the threading module.)
Stop the clock by calling Clock.stop()
"""

import time
from threading import Thread
from Mob import Mob


class Clock(Thread):
    def __init__(self):
        super().__init__()
        
    def run(self):
        self._alive = True

        self._timeIn = int(time.time())
        
        def move_mob(speed):
            print("Moving mobs of speed", speed)
            for mob in Mob.instances:
                if mob.get_speed() == speed:
                    mob.move()
                    
        def current_time():
            return int(time.time())-self._timeIn

        try:
            while self._alive:
                move_mob(10)
                if current_time()%20 == 0:
                    move_mob(20)
                    
                if current_time()%30 == 0:
                    move_mob(30)            
                
                if current_time() >= 60:
                    move_mob(60)
                    self._timeIn = int(time.time())
                    
                print("Timer active:", current_time())
                print()
                time.sleep(10)
        finally:
            print("!!! AI Clock has stopped.")
        
            
    def stop(self):
        self._alive = False
        self.join()