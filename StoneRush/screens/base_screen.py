"""
Base screen class
Ported from BaseScreen.java
"""
from abc import ABC, abstractmethod


class BaseScreen(ABC):
    """Abstract base class for game screens"""

    def __init__(self):
        pass

    @abstractmethod
    def show(self):
        """Called when this screen becomes active"""
        pass

    @abstractmethod
    def update(self, delta):
        """Update screen logic

        Args:
            delta: Time delta in seconds
        """
        pass

    @abstractmethod
    def render(self, surface):
        """Render the screen

        Args:
            surface: Pygame surface to render to
        """
        pass

    def resize(self, width, height):
        """Handle window resize

        Args:
            width: New window width
            height: New window height
        """
        pass

    def dispose(self):
        """Clean up resources"""
        pass
