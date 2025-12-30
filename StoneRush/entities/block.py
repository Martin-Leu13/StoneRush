"""
Block entity
Ported from Block.java
"""
import pygame
from entities.game_object import GameObject
from enums import BlockType
import config


class Block(GameObject):
    """Represents a platform block in the level"""

    def __init__(self, x, y, block_type):
        super().__init__(x, y, config.BLOCK_SIZE, config.BLOCK_SIZE)
        self.block_type = block_type
        self.is_destroyed = False

    def is_solid(self):
        """Returns True if the block is solid (not destroyed)"""
        return not self.is_destroyed

    def destroy(self):
        """Mark block as destroyed"""
        self.is_destroyed = True

    def get_type(self):
        return self.block_type

    def render(self, surface, camera_offset):
        """Render the block"""
        if self.is_destroyed:
            return

        # Calculate screen position with camera offset
        screen_x = self.position.x - camera_offset[0]
        screen_y = self.position.y - camera_offset[1]

        # Choose color based on block type
        if self.block_type == BlockType.GROUND:
            color = config.COLOR_GROUND
        elif self.block_type == BlockType.CRACKED:
            color = config.COLOR_CRACKED_BLOCK
        else:
            return

        # Draw filled rectangle
        pygame.draw.rect(surface, color, (screen_x, screen_y, self.width, self.height))

        # Draw border for cracked blocks
        if self.block_type == BlockType.CRACKED:
            pygame.draw.rect(surface, config.COLOR_BLACK,
                           (screen_x, screen_y, self.width, self.height), 2)
