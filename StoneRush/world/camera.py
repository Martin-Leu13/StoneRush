"""
Camera controller with smooth following
Ported from Camera2DController.java
"""
import pygame
import config


class Camera:
    """Camera with smooth follow and bounds clamping"""

    def __init__(self, player):
        self.player = player
        self.position = pygame.Vector2(0, 0)
        self.lerp_speed = 0.1  # Smooth follow speed
        self.offset_x = 200  # Keep player left of center

        # Level bounds
        self.level_width = config.LEVEL_WIDTH_BLOCKS * config.BLOCK_SIZE
        self.level_height = config.LEVEL_HEIGHT_BLOCKS * config.BLOCK_SIZE

    def update(self, delta):
        """Update camera position to follow player smoothly"""
        # Target position: player position with offset
        target_x = self.player.position.x - self.offset_x
        target_y = self.player.position.y - config.WINDOW_HEIGHT / 2

        # Lerp towards target (smooth follow)
        self.position.x += (target_x - self.position.x) * self.lerp_speed
        self.position.y += (target_y - self.position.y) * self.lerp_speed

        # Clamp camera to level bounds
        # Don't go past left edge
        if self.position.x < 0:
            self.position.x = 0

        # Don't go past right edge
        max_x = self.level_width - config.WINDOW_WIDTH
        if self.position.x > max_x:
            self.position.x = max_x

        # Don't go past top edge
        if self.position.y < 0:
            self.position.y = 0

        # Don't go past bottom edge
        max_y = self.level_height - config.WINDOW_HEIGHT
        if self.position.y > max_y:
            self.position.y = max_y

    def get_offset(self):
        """Get camera offset as tuple (x, y)"""
        return (self.position.x, self.position.y)
