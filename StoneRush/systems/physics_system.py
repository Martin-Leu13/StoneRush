"""
Physics system for gravity and velocity
Ported from PhysicsSystem.java
"""
import config


class PhysicsSystem:
    """Applies physics (gravity) to game objects"""

    def update(self, delta, game_object):
        """Apply physics to a game object

        Args:
            delta: Time delta in seconds
            game_object: GameObject to apply physics to
        """
        # Apply gravity
        game_object.velocity.y += config.GRAVITY * delta

        # Terminal velocity (in Pygame, positive y = falling down)
        if game_object.velocity.y > 1000.0:
            game_object.velocity.y = 1000.0
