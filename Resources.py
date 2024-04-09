import random
import math

class Resources:
    def __init__(self, mean) -> None:
        # Follows a folded normal distribution
        self.resource_level = math.abs(random.normalvariate(mean, 1))
        self.pos_x = None
        self.pos_y = None

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y
    
    def get_pos(self):
        return (self.pos_x, self.pos_y)
    
    def get_weapon(self):
        return self.resource_level
