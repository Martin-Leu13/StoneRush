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

        # Jump (Space OR Up Arrow)
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.player.jump()

        # Ram (Shift) - continuous while held
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.player.start_ram()
            # Keep ramming while shift is held
            self.player.keep_ramming()
        else:
            # Stop ramming when shift is released
            self.player.stop_ram_if_active()
