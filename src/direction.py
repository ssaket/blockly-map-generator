from enum import Enum


class DirectionEnum(Enum):
    """Direction enum. Each direction represents a delta coordinate for the agent."""
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)
    NONE = (0, 0)
