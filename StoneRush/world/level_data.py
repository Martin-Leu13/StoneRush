"""
Level data structure
Ported from LevelData.java
"""
import pygame
from enums import BlockType
import config


class LevelData:
    """Data structure for level layout and spawn points"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Initialize grid with EMPTY blocks
        self.blocks = [[BlockType.EMPTY for _ in range(height)] for _ in range(width)]
        self.player_spawn = pygame.Vector2(0, 0)
        self.enemy_spawns = []
        self.goal_position = pygame.Vector2(0, 0)

    def set_block(self, x, y, block_type):
        """Set block type at grid position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.blocks[x][y] = block_type

    def get_block(self, x, y):
        """Get block type at grid position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.blocks[x][y]
        return BlockType.EMPTY

    def set_player_spawn(self, x, y):
        """Set player spawn position (in pixels)"""
        self.player_spawn = pygame.Vector2(x, y)

    def add_enemy_spawn(self, x, y):
        """Add enemy spawn position (in pixels)"""
        self.enemy_spawns.append(pygame.Vector2(x, y))

    def set_goal_position(self, x, y):
        """Set goal position (in pixels)"""
        self.goal_position = pygame.Vector2(x, y)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_player_spawn(self):
        return self.player_spawn

    def get_enemy_spawns(self):
        return self.enemy_spawns

    def get_goal_position(self):
        return self.goal_position
