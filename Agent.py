import math
import random

from deap import base
from deap import creator
from deap import tools

"""
Let's define traits:
Health
Attack (damage)
Reproductive appeal -> force reproduction
Cooperation (i scratch your back you scratch mine)

Crazier cool idea:
build a world that can have resources.
the world is a grid. people can randomly walk around on each frame
people can interract with resources, or other people

we need a way for people to have people interact with others

we need a way for people to interact with the world

we need a way for people to procreate

is there a way to simulate technology increasing? Through resource collection?

allow parents to give there kids weapons to the next generation


Define agents
Define the world
define the way agents intereact with the world 


"""
HEALTH_MIN, HEALTH_MAX = 1, 20
STRENGTH_MIN, STRENGTH_MAX = 1, 5
COOPERATION_MIN, COOPERATION_MAX = 1, 5
# SEDUCTION_MIN, SEDUCTION_MAN = 1, 5
RESOURCEFULNESS_MIN, RESOURCEFULNESS_MAX = 1, 5
CONSTITUTION_MIN, CONSTITUTION_MAX = 1, 5


class Agent:
    def __init__(self, id) -> None:
        self.health = 10 + random.randint(0, 40)
        self.strength = 1 + random.randint(0, 9)
        # self.cooperation = 1 + random()
        # self.resourcefulness = 1 + random()
        # self.seduction = 1 + random()
        # self.speed =

        self.id = id
        self.bounces = 1
        self.pos_x = None
        self.pos_y = None
        self.kills = 0
        self.killed_agent_stats = []
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        self.radius = 2
        self.velocity_x = (random.random() - 0.5) * 1
        self.velocity_y = (random.random() - 0.5) * 1

    def get_pos(self):
        return (self.pos_x, self.pos_y)

    def get_color(self):
        return self.color

    def get_kills(self):
        return self.kills

    def get_kill_grid(self, max_x, max_y):
        radius = int(self.radius)
        point_deltas = list(range(-radius, radius + 1))
        points = [
            (self.pos_x + i, self.pos_y + j) for i in point_deltas for j in point_deltas
        ]
        points = [(max(0, x), max(0, y)) for (x, y) in points]
        points = [(min(x, max_x - 1), min(y, max_y - 1)) for (x, y) in points]
        return list(set(points))

    def bounce(self):
        self.bounces *= 2
        return self.bounces // 2

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def get_area(self):
        return math.pi * (self.radius**2)

    def gravity_acceleration(self):
        return 9.81

    def update_pos(self, center_of_mass, total):
        center_of_mass_x, center_of_mass_y = center_of_mass
        direction_x = center_of_mass_x - self.pos_x
        direction_y = center_of_mass_y - self.pos_y
        magnitude = math.sqrt(direction_x**2 + direction_y**2) 

        if magnitude == 0:
            return (0, 0)  # Prevent division by zero if points are the same

        unit_dx = direction_x / magnitude
        unit_dy = direction_y / magnitude

        # Scale the unit vector by the acceleration magnitude
        ax = unit_dx * (0.1) 
        ay = unit_dy * (0.1) 

        self.pos_x = int(self.pos_x + self.velocity_x + (0.5 * ax))
        self.pos_y = int(self.pos_y + self.velocity_y + (0.5 * ay))

        self.velocity_x = self.velocity_x + 0.5 * ax
        self.velocity_y = self.velocity_y + 0.5 * ay
