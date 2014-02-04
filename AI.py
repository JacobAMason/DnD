# AI.py

import time
from threading import Thread
from Mob import Mob


class Clock(Thread):
    def __init__(self):
        Thread.__init__(self) 
        
    def run(self):
        self._timeIn = int(time.time())
        
        def move_mob(speed):
            print("Moving mobs of speed", speed)
            for mob in Mob.instances:
                if mob.get_speed() == speed:
                    mob.move()
                    
        def current_time():
            return int(time.time())-self._timeIn

        while True:
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