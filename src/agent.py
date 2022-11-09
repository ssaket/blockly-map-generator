from enum import Enum
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import List, Union
from direction import DirectionEnum
from level import LevelMap, Tile, Point, showPNGMark
from random import choice
from blocks import CodeBlock
import numpy as np

# actions
TURN_LEFT = [
    [DirectionEnum.SOUTH, DirectionEnum.EAST],
    [DirectionEnum.NORTH, DirectionEnum.WEST],
    [DirectionEnum.EAST, DirectionEnum.NORTH],
    [DirectionEnum.WEST, DirectionEnum.SOUTH],
]

TURN_RIGHT = [
    [DirectionEnum.SOUTH, DirectionEnum.WEST],
    [DirectionEnum.NORTH, DirectionEnum.EAST],
    [DirectionEnum.EAST, DirectionEnum.SOUTH],
    [DirectionEnum.WEST, DirectionEnum.NORTH],
]

TURN_AROUND = [
    [DirectionEnum.SOUTH, DirectionEnum.NORTH],
    [DirectionEnum.EAST, DirectionEnum.WEST],
    [DirectionEnum.NORTH, DirectionEnum.SOUTH],
    [DirectionEnum.WEST, DirectionEnum.EAST]
]

# direction coords for actions
class ActionEnum(Enum):
    MOVE = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)


@dataclass_json
@dataclass
class Agent:
    id: int
    level_map: LevelMap
    current_location: Union[Point, None] = None
    direction: DirectionEnum = choice(list(DirectionEnum))
    path: List[Tile] = field(default_factory=list,
                             metadata=config(exclude=lambda x: False))

    def _gen_rand_location(self, locations, r_min, r_max, c_min, c_max):
        end_r, end_c = choice([(r, c) for r, c in zip(locations[0], locations[1]) if (
            r >= r_min) and (r <= r_max) and (c > c_min) and (c < c_max)])
        return (end_r, end_c)

    def start_walk(self):
        grid = self.level_map.maze.grid
        r, c = grid.shape
        locations = np.where(grid == 0)
        start_r, start_c = self._gen_rand_location(
            locations, r // 2 - 1, r // 2 + 1, c // 2 - 1, c // 2 + 1)
        start_tile = Tile(int(start_r), int(start_c))
        self.level_map.start_location = start_tile
        start_tile.direction = self.direction.name

        if self.direction == DirectionEnum.SOUTH:
            end_r, end_c = self._gen_rand_location(locations, r // 2, r, 0, c)
        elif self.direction == DirectionEnum.NORTH:
            end_r, end_c = self._gen_rand_location(locations, 0, r // 2, 0, c)
        elif self.direction == DirectionEnum.EAST:
            end_r, end_c = self._gen_rand_location(locations, 0, r, c // 2, c)
        elif self.direction == DirectionEnum.WEST:
            end_r, end_c = self._gen_rand_location(locations, 0, r, 0, c // 2)
        end_tile = Tile(end_r, end_c)

        paths = self.level_map.auto_solver(start_tile, end_tile)
        showPNGMark(self.level_map.maze.grid,
                    self.level_map.maze.start, self.level_map.maze.end)

        for path in paths:
            old_tile = start_tile
            old_direction = self.direction
            tiles = [start_tile]
            for location in path:
                x, y = location
                new_tile = Tile(int(x), int(y))
                delta = old_tile - new_tile
                new_direction = DirectionEnum((delta.row, delta.col))
                new_tile.direction = new_direction.name

                if old_direction == new_direction:
                    new_tile.code_block = CodeBlock.MOVE_FORWARD.value
                elif [old_direction, new_direction] in TURN_AROUND:
                    new_tile.code_block = '#'.join(
                        [CodeBlock.TURN_LEFT.value, CodeBlock.TURN_LEFT.value, CodeBlock.MOVE_FORWARD.value])
                elif [old_direction, new_direction] in TURN_LEFT:
                    new_tile.code_block = '#'.join(
                        [CodeBlock.TURN_LEFT.value, CodeBlock.MOVE_FORWARD.value])
                elif [old_direction, new_direction] in TURN_RIGHT:
                    new_tile.code_block = '#'.join(
                        [CodeBlock.TURN_RIGHT.value, CodeBlock.MOVE_FORWARD.value])

                old_tile = new_tile
                old_direction = new_direction
                tiles.append(new_tile)
            self.path.append(tiles)
