from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from random import choice
from direction import DirectionEnum
import numpy as np


from agent import Agent
from level import LevelMap, Tile


@dataclass_json
@dataclass
class Trial:
    """
    Generate a trial for the experiment
    """
    id: int = field(default=1)
    map_size: int = field(default=5)
    num_agents: int = field(default=3)
    grid: LevelMap = field(init=False, repr=False)
    agents: List[Agent] = field(default_factory=list, repr=False)
    score: int = field(default=0)

    def generate_map(self, **kwargs):
        level = LevelMap(self.map_size)
        level.generate_map(**kwargs)
        self.grid = level
        for id in range(1, self.num_agents + 1):
            self.agents.append(Agent(id, self.grid))
    
    def _gen_rand_location(self, locations, r_min, r_max, c_min, c_max):
        _r, _c = choice([(r, c) for r, c in zip(locations[0], locations[1]) if (
            (r >= r_min) and (r <= r_max) and (c >= c_min) and (c <= c_max) and r % 2 != 0 and c % 2 != 0)])
        return (_r, _c)

    def _get_end_location(self, locations, r, c):
        direction = choice([DirectionEnum.SOUTH, DirectionEnum.NORTH, DirectionEnum.WEST, DirectionEnum.EAST])
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

    def start_agent_walk(self, id=None, random_start=False, random_end=False):

        grid = self.grid.maze.grid
        r, c = grid.shape
        locations = np.where(grid == 0)
        start_r, start_c = self._gen_rand_location(
            locations, r // 2 - 1, r // 2 + 1, c // 2 - 1, c // 2 + 1)
        start_tile = Tile(int(start_r), int(start_c))

        end_tile = self._get_end_location(locations, r, c)

        while start_tile == end_tile:
            end_tile = self._get_end_location(locations, r, c)

        print('start location', start_tile)
        print('end location', end_tile)

        if id is not None:
            for agent in self.agents:
                if id == agent.id:
                    agent.start_walk(start_tile, end_tile)
                    break
        else:
            for agent in self.agents:
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
            self.agents.append(Agent(id, level))
        for agent in self.agents:
            agent.start_walk()

        self.grid = level

    def show_map_with_agents(self):
        """Generate a simple image of the maze."""

        nrows = 1
        ncols = self.num_agents

        if ncols > 1:
            fig, axes = plt.subplots(
                nrows, ncols, sharex=False, sharey=False, squeeze=True)
            for agent_id, ax in enumerate(axes.flatten()):
                ax.imshow(self.grid.maze.grid, cmap=plt.cm.binary, interpolation='nearest')
                colors = ['maroon', 'royalblue',
                          'darkgray', 'coral', 'steelblue']
                for path in self.agents[agent_id].path:
                    entrance_colors = ['dimgray', 'darkgray']
                    for i, tile in enumerate(path):
                        if i == 0 or i == len(path) - 1:
                            color = entrance_colors.pop()
                        else:
                            color = colors[agent_id]
                        patch = patches.Circle((tile.col, tile.row), 0.5, linewidth=3,
                                            edgecolor=color, facecolor=color)
                        ax.add_patch(patch)
        else:
            fig, ax = plt.subplots(nrows, ncols, sharex=False,
                                   sharey=False, squeeze=True)
            ax.imshow(self.grid.maze.grid, cmap=plt.cm.binary, interpolation='nearest')
            colors = ['maroon', 'royalblue', 'darkgray', 'coral', 'steelblue']

            for idx, agent in enumerate(self.agents):
                for path in agent.path:
                    entrance_colors = ['dimgray', 'darkgray']
                    for i, tile in enumerate(path):
                        if i == 1 or i == len(path) - 1:
                            color = entrance_colors.pop()
                        else:
                            color = colors[idx]
                        patch = patches.Circle((tile.col, tile.row), 0.5, linewidth=3,
                                            edgecolor=color, facecolor=color)
                        ax.add_patch(patch)

        plt.show()
