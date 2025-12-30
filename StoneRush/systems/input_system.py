"""
Input system for keyboard handling
Ported from InputSystem.java
"""
import pygame


class InputSystem:
    """Handles keyboard input for player control"""

    def __init__(self, player):
        self.player = player

    def update(self, delta):
        """Process keyboard input"""
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT]:
            self.player.move_right()
        else:
            self.player.stop_horizontal_movement()

        # Jump (Space)
        if keys[pygame.K_SPACE]:
            self.player.jump()

        # Ram (Shift)
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.player.start_ram()
