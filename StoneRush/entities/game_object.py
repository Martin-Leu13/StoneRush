"""
Base GameObject class
Ported from GameObject.java
"""
import pygame
from abc import ABC, abstractmethod


class GameObject(ABC):
    """Abstract base class for all game entities"""

    def __init__(self, x, y, width, height):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.width = width
        self.height = height
        self.bounds = pygame.Rect(x, y, width, height)

    def update(self, delta):
        """Update position based on velocity"""
        self.position.x += self.velocity.x * delta
        self.position.y += self.velocity.y * delta
        self.update_bounds()

    def update_bounds(self):
        """Update collision bounds to match position"""
        self.bounds.x = self.position.x
        self.bounds.y = self.position.y

    @abstractmethod
    def render(self, surface, camera_offset):
        """Render the entity to the screen

        Args:
            surface: Pygame surface to render to
            camera_offset: Tuple (x, y) for camera offset
        """
        pass

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def get_bounds(self):
        return self.bounds
