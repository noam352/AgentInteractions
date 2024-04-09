import time
import numpy as np
import random
from Agent import Agent
import pygame


class World:
    # x_size = 250
    # y_size = 250
    num_agents = 200
    # num_resources = 200
    agents_left = num_agents

    def __init__(self, x_size, y_size, screen):
        # track population in the population dict
        self.x_size = x_size
        self.y_size = y_size
        self.screen = screen

        self.population = {}
        self.shrink_requested = False
        # create the grid
        self.grid = np.array(
            [[set() for i in range(self.x_size)] for p in range(self.y_size)]
        )
        # print(self.grid.size)
        # TO DO populate the world with resources

        # Populate the grid with agents
        population_positions = zip(
            [
                random.randint(
                    0,
                    self.x_size - 1,
                    # int(self.x_size / 4),
                    # int(3 * self.x_size / 4),
                )
                for i in range(self.num_agents)
            ],
            [
                random.randint(
                    0,
                    self.y_size - 1,
                    # int(self.y_size / 4),
                    # int(3 * self.y_size / 4),
                )
                for i in range(self.num_agents)
            ],
        )

        for id, (x, y) in enumerate(population_positions):
            # print(x, y)
            agent = Agent(str(id))
            agent.set_pos(x, y)

            self.population[str(id)] = agent  # might not need this

            self.grid[x][y].add(str(id))
            # print(self.grid[x][y])
        # print(self.grid)

    def agents_interact(self, agent1_id, agent2_id):
        """
        return the loser of the fight
        """
        agent1 = self.population[agent1_id]
        agent2 = self.population[agent2_id]
        healths = [agent1.health, agent2.health]
        strengths = [agent1.strength, agent2.strength]
        turn = 0
        while all([health > 0 for health in healths]) > 0:
            # ATTACK
            healths[turn] = healths[turn] - strengths[(turn + 1) % 2]
            turn = (turn + 1) % 2
            # Perform other action instead of attack (TODO)

        # if healths[0] <= 0:
        if agent1.radius <= agent2.radius:
            agent2.kills += 1
            agent2.radius = ((agent2.radius**2) + (agent1.radius**2)) ** (1 / 2)
            return agent1_id
        else:
            agent1.kills += 1
            agent1.radius = ((agent2.radius**2) + (agent1.radius**2)) ** (1 / 2)
            return agent2_id

    def evaluate_world(self):
        # Step 1: Have all agents interact with eachother if they share the same block
        for agent_id in list(self.population.keys()):
            # Skip over killed agents
            if agent_id not in self.population:
                continue
            agent = self.population[agent_id]
            agent_pos_x, agent_pos_y = agent.get_pos()

            # interact agents that lay in their kill grid
            next_potential_point = True

            for potential_point in agent.get_kill_grid(self.x_size, self.y_size):
                if next_potential_point:
                    for discovered_agent in list(
                        self.grid[potential_point[0]][potential_point[1]]
                    ):
                        if discovered_agent == agent_id:
                            continue
                        loser = self.agents_interact(agent_id, discovered_agent)
                        if loser == agent_id:
                            self.grid[agent_pos_x][agent_pos_y].remove(loser)
                            del self.population[loser]
                            self.agents_left -= 1
                            next_potential_point = False
                            break
                        else:
                            self.grid[potential_point[0]][potential_point[1]].remove(
                                loser
                            )
                            del self.population[loser]
                            self.agents_left -= 1
                else:
                    break

        # Step 2: Have all agents interact with a resource if they share the same square

    def walk_agents(self):
        # get center of mass

        for agent_id in self.population:
            agent = self.population[agent_id]
            agent_pos_x, agent_pos_y = agent.get_pos()

            # walk the agent with kinematic equations
            center, total = self.get_center_of_mass(besides_agent_id=agent_id)
            agent.update_pos(center, total)
            new_pos = agent.get_pos()
            new_pos = self.truncate_boundaries(new_pos, agent_id)
            agent.set_pos(new_pos[0], new_pos[1])

            # Update the grid and population dict
            self.grid[agent_pos_x][agent_pos_y].remove(agent_id)
            self.grid[new_pos[0]][new_pos[1]].add(agent_id)
            self.population[agent_id].set_pos(new_pos[0], new_pos[1])

    def truncate_boundaries(self, point, agent_id):
        x, y = point
        agent = self.population[agent_id]

        if x <= 0:
            x += 5
            # x = int(agent.radius)
            agent.velocity_x *= -1
        if x >= self.x_size - 1:
            # x -= 5
            x = self.x_size - 5
            agent.velocity_x *= -1
        if y <= 0:
            y += 5
            # y = int(agent.radius)
            agent.velocity_y *= -1
        if y >= self.y_size - 1:
            # y -= 5
            y = self.y_size - 5
            agent.velocity_y *= -1
        return (x, y)

    def get_center_of_mass(self, besides_agent_id):
        x = 0
        y = 0
        total = 1
        for agent_id in self.population:
            if besides_agent_id == agent_id:
                continue
            agent = self.population[agent_id]
            x += agent.get_pos()[0] * agent.get_area()
            y += agent.get_pos()[1] * agent.get_area()
            total += agent.get_area()
        y = y / total
        x = x / total

        return (x, y), total
