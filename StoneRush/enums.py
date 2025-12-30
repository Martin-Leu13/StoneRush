from enum import Enum


class PlayerState(Enum):
    IDLE = "idle"
    WALKING = "walking"
    JUMPING = "jumping"
    FALLING = "falling"
    RAMMING = "ramming"


class Direction(Enum):
    LEFT = -1
    RIGHT = 1
    NONE = 0

    def get_value(self):
        return self.value


class BlockType(Enum):
    EMPTY = "empty"
    GROUND = "ground"
    CRACKED = "cracked"
