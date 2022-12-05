from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from random import choice, uniform
from direction import DirectionEnum
import numpy as np

from agent import Agent
from level import LevelMap, Tile
import logging


@dataclass_json
@dataclass
class Trial:
    """
    The experiment trial

    Attributes:
        id: An integer Trail ID 
        map_size: An integer specifying the grid size (int x int)
        num_agents: An integer to count total number of agents in a map
        score: An integer to indicate total score for the trial

    """
    id: int = field(default=1)
    map_size: int = field(default=5)
    num_agents: int = field(default=3)
    score: int = field(default=0)
    __grid: list[LevelMap] = field(default_factory=list, repr=False)
    __agents: List[Agent] = field(default_factory=list, repr=False)

    def generate_map(self, mutation=False, **kwargs):

        if not mutation:
            level = LevelMap(self.map_size)
            level.generate_map(**kwargs)
            self.__grid.append(level)
            for id in range(1, self.num_agents + 1):
                logging.info(f'creating agent {id}')
                self.__agents.append(
                    Agent(id, level, choice(list(DirectionEnum))))
        else:
            for id in range(1, self.num_agents + 1):
                level = LevelMap(self.map_size)
                method = choice([
                    {
                        'method': 'cellular',
                        'complexity': uniform(0.1, 0.3),
                        'density': uniform(0.1, 0.3)
                    },
                    {
                        'method': 'eller',
                        'xskew': uniform(0.8, 1.0),
                        'yskew': uniform(0.1, 0.3)
                    },
                    {
                        'method': 'eller',
                        'xskew': uniform(0.1, 0.3),
                        'yskew': uniform(0.8, 1.0)
                    },
                ])

                level.generate_map(**method)
                self.__grid.append(level)
                self.__agents.append(
                    Agent(id, level, choice(list(DirectionEnum))))

    def _gen_rand_location(self, locations, r_min, r_max, c_min, c_max):
        _r, _c = choice([(r, c)
                         for r, c in zip(locations[0], locations[1])
                         if ((r >= r_min) and (r <= r_max) and (c >= c_min) and
                             (c <= c_max) and r % 2 != 0 and c % 2 != 0)])
        return (_r, _c)

    def _get_end_location(self, locations, r, c):
        direction = choice([
            DirectionEnum.SOUTH, DirectionEnum.NORTH, DirectionEnum.WEST,
            DirectionEnum.EAST
        ])

        end_r, end_c = 0, 0
        if direction == DirectionEnum.SOUTH:
            end_r, end_c = self._gen_rand_location(locations, r // 2, r, 0, c)
        elif direction == DirectionEnum.NORTH:
            end_r, end_c = self._gen_rand_location(locations, 0, r // 2, 0, c)
        elif direction == DirectionEnum.EAST:
            end_r, end_c = self._gen_rand_location(locations, 0, r, c // 2, c)
        elif direction == DirectionEnum.WEST:
            end_r, end_c = self._gen_rand_location(locations, 0, r, 0, c // 2)
        end_tile = Tile(int(end_r), int(end_c))

        return end_tile

    def start_agent_walk(self, id=None, random_start=False):

        grid = self.__grid[0].maze.grid
        r, c = grid.shape
        locations = np.where(grid == 0)
        start_r, start_c = self._gen_rand_location(locations, r // 2 - 1,
                                                   r // 2 + 1, c // 2 - 1,
                                                   c // 2 + 1)
        start_tile = Tile(int(start_r), int(start_c))

        end_tile = self._get_end_location(locations, r, c)

        while start_tile == end_tile:
            end_tile = self._get_end_location(locations, r, c)

        logging.info(f'start location  {start_tile}')
        logging.info(f'end location {end_tile}')

        if id is not None:
            for agent in self.__agents:
                if id == agent.id:
                    agent.start_walk(start_tile, end_tile)
                    break
        else:
            for agent in self.__agents:
                if random_start:
                    start_tile = self._get_end_location(locations, r, c)
                end_tile = self._get_end_location(locations, r, c)

                while start_tile == end_tile:
                    end_tile = self._get_end_location(locations, r, c)
                agent.start_walk(start_tile, end_tile)

    def generate_custom_map(self, custom_map):
        """
        Generate trial based on given numpy maze array
        """
        level = LevelMap(custom_map.shape[0] // 2 - 1)
        level.generate_map(custom_map)

        for id in range(1, self.num_agents + 1):
            self.__agents.append(Agent(id, level, choice(list(DirectionEnum))))
        for agent in self.__agents:
            agent.start_walk()

        self.__grid = level

    def show_map_with_agents(self):
        """Generate a simple image of the maze."""

        nrows = 1
        ncols = self.num_agents

        if ncols > 1:
            fig, axes = plt.subplots(nrows,
                                     ncols,
                                     sharex=False,
                                     sharey=False,
                                     squeeze=True)
            for agent_id, ax in enumerate(axes.flatten()):
                ax.imshow(self.__agents[agent_id].grid.maze.grid,
                          cmap=plt.cm.binary,
                          interpolation='nearest')
                colors = [
                    'maroon', 'royalblue', 'darkgray', 'coral', 'steelblue'
                ]
                for path in self.__agents[agent_id].path:
                    entrance_colors = ['dimgray', 'darkgray']
                    for i, tile in enumerate(path):
                        if i == 0 or i == len(path) - 1:
                            color = entrance_colors.pop()
                        else:
                            color = colors[agent_id]
                        patch = patches.Circle((tile.col, tile.row),
                                               0.5,
                                               linewidth=3,
                                               edgecolor=color,
                                               facecolor=color)
                        ax.add_patch(patch)
        else:
            fig, ax = plt.subplots(nrows,
                                   ncols,
                                   sharex=False,
                                   sharey=False,
                                   squeeze=True)
            ax.imshow(self.__agents[agent_id].grid.maze.grid,
                      cmap=plt.cm.binary,
                      interpolation='nearest')
            colors = ['maroon', 'royalblue', 'darkgray', 'coral', 'steelblue']

            for idx, agent in enumerate(self.__agents):
                for path in agent.path:
                    entrance_colors = ['dimgray', 'darkgray']
                    for i, tile in enumerate(path):
                        if i == 1 or i == len(path) - 1:
                            color = entrance_colors.pop()
                        else:
                            color = colors[idx]
                        patch = patches.Circle((tile.col, tile.row),
                                               0.5,
                                               linewidth=3,
                                               edgecolor=color,
                                               facecolor=color)
                        ax.add_patch(patch)

        plt.show()
