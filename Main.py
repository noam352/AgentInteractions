import time

# from Agent import Agent
from World import World

import pygame
import numpy as np
import sys

x_size = 1000
y_size = 1000


def main():
    start_time = time.time()
    walks = 0

    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    screen = pygame.display.set_mode((x_size, y_size))
    world = World(x_size=x_size, y_size=y_size, screen=screen)

    # Colors
    background_color = (255, 255, 255)  # White background
    # agent_color = (0, 0, 255)  # Blue agents

    # FPS control
    clock = pygame.time.Clock()

    while world.agents_left > 1:
        # Check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                # running = False

        walks += 1
        world.evaluate_world()
        world.walk_agents()
        # world.shrink_boundaries()
        # print(world.agents_left)
        # Fill the screen with background color
        world.screen.fill(background_color)

        for agent_id in world.population:
            agent = world.population[agent_id]
            position = agent.get_pos()
            kills = agent.get_kills()
            agent_color = agent.get_color()
            pygame.draw.circle(world.screen, agent_color, position, agent.radius)

        # Update the display
        pygame.display.flip()

        # Limit frames per second
        clock.tick(60)

    for agent in world.population:
        print(
            f"Health: {world.population[agent].health}",
            f"Strength: {world.population[agent].strength}",
            f"kills: {world.population[agent].get_kills()}",
            # f"killed_agent_stats: {world.population[agent].killed_agent_stats}"
        )
    print(f"Total walks: {walks}")

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The function took {execution_time} seconds to complete.")


main()

### What did i accomplish?
"""
Got a simulation to work with traits for strength and health.

What can i change?

Reproduction?

new traits for cooperation and resourcefulness 
    (if 1 guy ends up dying but he has higher cooperation than the other he can give up a resource to stay alive)

VISUALIZATION!!

How can i shrink the arena to speed up the proccess??
Maybe give speed?
maybe use distance function to others, and give kills to others.
"""
