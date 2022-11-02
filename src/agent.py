#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List, Union
from direction import DirectionEnum
from level import LevelMap, Tile, Point
from random import choice

# actions
ACTION = ['move_forward', 'turn_left', 'turn_right', 'turn_left$move_forward',
          'turn_right$move_forward', 'move_forward$move_forward']

@dataclass
class Agent:
    id: int
    level_map: LevelMap
    current_location: Union[Point, None] = None
    direction: DirectionEnum = choice(list(DirectionEnum))
    path: List[Tile] = field(default_factory=list)

    def perform_action(self, action):
        del_x, del_y = self.direction.value
        new_tile = self.level_map.find_tile(self.current_location)
        new_tile.visited_agent = self.id
        new_tile.code_block = action
        if action == 'move_forward':
            # isValid(move)
            new_location = self.current_location + Point(del_x, del_y)
            new_tile = self.level_map.find_tile(new_location)
            self.current_location = new_location
            new_tile.visited_agent = self.id
            new_tile.code_block = action
            self.path.append(new_tile)
        elif action == 'turn_left':
            if self.direction == DirectionEnum.SOUTH:
                self.direction = DirectionEnum.EAST
            elif self.direction == DirectionEnum.NORTH:
                self.direction = DirectionEnum.WEST
            elif self.direction == DirectionEnum.EAST:
                self.direction = DirectionEnum.NORTH
            elif self.direction == DirectionEnum.WEST:
                self.direction = DirectionEnum.SOUTH
        elif action == 'turn_right':
            if self.direction == DirectionEnum.SOUTH:
                self.direction = DirectionEnum.WEST
            elif self.direction == DirectionEnum.NORTH:
                self.direction = DirectionEnum.EAST
            elif self.direction == DirectionEnum.EAST:
                self.direction = DirectionEnum.SOUTH
            elif self.direction == DirectionEnum.WEST:
                self.direction = DirectionEnum.NORTH
        # self.path.append(new_tile)

    def __post_init__(self):
        start_tile = self.level_map.start_location
        start_tile.visited_agent = self.id
        self.current_location = Point(start_tile.x, start_tile.y)
        self.path.append(start_tile)