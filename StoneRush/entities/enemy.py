"""
Enemy entity
Ported from Enemy.java
"""
import pygame
from entities.game_object import GameObject
from enums import Direction
import config


class Enemy(GameObject):
    """Enemy that patrols back and forth"""

    def __init__(self, x, y):
        super().__init__(x, y, config.ENEMY_SIZE, config.ENEMY_SIZE)
        self.start_x = x
        self.patrol_direction = Direction.RIGHT
        self.velocity.x = config.ENEMY_SPEED
        self.is_dead = False

    def update(self, delta):
        """Update enemy position and patrol logic"""
        if self.is_dead:
            return

        # Check if reached patrol boundary
        if abs(self.position.x - self.start_x) >= config.ENEMY_PATROL_DISTANCE:
            # Turn around
            if self.patrol_direction == Direction.RIGHT:
                self.patrol_direction = Direction.LEFT
            else:
                self.patrol_direction = Direction.RIGHT

            self.velocity.x = self.patrol_direction.get_value() * config.ENEMY_SPEED

        super().update(delta)

    def die(self):
        """Kill the enemy"""
        self.is_dead = True
        self.velocity.x = 0
        self.velocity.y = 0

    def render(self, surface, camera_offset):
        """Render the enemy"""
        if self.is_dead:
            return

        # Calculate screen position with camera offset
        screen_x = self.position.x - camera_offset[0]
        screen_y = self.position.y - camera_offset[1]

        # Draw red square body
        pygame.draw.rect(surface, config.COLOR_ENEMY,
                        (screen_x, screen_y, self.width, self.height))

        # Draw simple eyes (black circles)
        eye_radius = 3
        pygame.draw.circle(surface, config.COLOR_BLACK,
                         (int(screen_x + 8), int(screen_y + 20)), eye_radius)
        pygame.draw.circle(surface, config.COLOR_BLACK,
                         (int(screen_x + 24), int(screen_y + 20)), eye_radius)
