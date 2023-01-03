from enum import Enum


class CodeBlock(Enum):
    """Code block enum. Each code block represents a command for the agent."""
    EMPTY = 'empty'
    MOVE_FORWARD = 'move_forward'
    TURN_LEFT = 'turn_left'
    TURN_RIGHT = 'turn_right'
