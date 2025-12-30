"""
Collision system for AABB collision detection
Ported from CollisionSystem.java
"""
import pygame
from enums import BlockType


class CollisionSystem:
    """Handles all collision detection and resolution"""

    def __init__(self, level):
        self.level = level

    def update(self, delta):
        """Update all collisions"""
        player = self.level.get_player()

        # Player vs Blocks
        self._handle_player_block_collisions(player)

        # Player vs Enemies
        self._handle_player_enemy_collisions(player)

        # Enemies vs Blocks (for grounding)
        for enemy in self.level.get_enemies():
            self._handle_enemy_block_collisions(enemy)

    def _handle_player_block_collisions(self, player):
        """Handle collisions between player and blocks"""
        player_bounds = player.get_bounds()

        # Expand search area slightly
        search_area = pygame.Rect(
            player_bounds.x - 32,
            player_bounds.y - 32,
            player_bounds.width + 64,
            player_bounds.height + 64
        )

        nearby_blocks = self.level.get_blocks_in_range(search_area)

        # Check if player is grounded with tolerance
        # Instead of setting to False immediately, check if there's a block below
        grounded = False
        ground_tolerance = 3.0  # Pixels of tolerance for ground detection

        # First check if player is on or very close to ground
        for block in nearby_blocks:
            b_bounds = block.get_bounds()
            # Check if player is standing on top of this block (with small tolerance)
            if (player_bounds.x + player_bounds.width > b_bounds.x and
                player_bounds.x < b_bounds.x + b_bounds.width and
                player_bounds.y + player_bounds.height >= b_bounds.y - ground_tolerance and
                player_bounds.y + player_bounds.height <= b_bounds.y + ground_tolerance):
                grounded = True
                break

        # Debug: Track grounded status changes
        old_grounded = player.is_grounded
        player.set_grounded(grounded)
        if old_grounded != grounded:
            print(f"Grounded changed: {old_grounded} → {grounded}")

        # Now handle collisions
        for block in nearby_blocks:
            if player_bounds.colliderect(block.get_bounds()):
                self._resolve_player_block_collision(player, block)

    def _resolve_player_block_collision(self, player, block):
        """Resolve collision between player and block using AABB"""
        p_bounds = player.get_bounds()
        b_bounds = block.get_bounds()

        # Calculate overlap on each side
        overlap_left = (p_bounds.x + p_bounds.width) - b_bounds.x
        overlap_right = (b_bounds.x + b_bounds.width) - p_bounds.x
        overlap_top = (p_bounds.y + p_bounds.height) - b_bounds.y
        overlap_bottom = (b_bounds.y + b_bounds.height) - p_bounds.y

        # Find minimum overlap
        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        pos = player.get_position()
        vel = player.get_velocity()

        if min_overlap == overlap_top and vel.y >= 0:  # Changed > to >= for better ground detection
            # Collision from top (player landing on block from above)
            # In Pygame: positive y velocity = falling down
            pos.y = b_bounds.y - p_bounds.height
            vel.y = 0  # Stop all downward movement
            player.set_grounded(True)
            player.update_bounds()  # Update bounds immediately
        elif min_overlap == overlap_bottom and vel.y < 0:
            # Collision from bottom (player hitting head while jumping)
            # In Pygame: negative y velocity = going up
            pos.y = b_bounds.y + b_bounds.height
            vel.y = 0
        elif min_overlap == overlap_left and vel.x > 0:
            # Collision from left
            pos.x = b_bounds.x - p_bounds.width

            # If ramming, destroy cracked blocks
            if player.is_ramming() and block.get_type() == BlockType.CRACKED:
                block.destroy()
            else:
                vel.x = 0
        elif min_overlap == overlap_right and vel.x < 0:
            # Collision from right
            pos.x = b_bounds.x + b_bounds.width

            # If ramming, destroy cracked blocks
            if player.is_ramming() and block.get_type() == BlockType.CRACKED:
                block.destroy()
            else:
                vel.x = 0

        player.update_bounds()

    def _handle_player_enemy_collisions(self, player):
        """Handle collisions between player and enemies"""
        player_bounds = player.get_bounds()

        for enemy in self.level.get_enemies():
            if enemy.is_dead:
                continue

            if player_bounds.colliderect(enemy.get_bounds()):
                if player.is_ramming():
                    # Destroy enemy
                    enemy.die()
                else:
                    # Player takes damage
                    player.take_damage()

        # Clean up dead enemies
        self.level.remove_dead_enemies()

    def _handle_enemy_block_collisions(self, enemy):
        """Handle collisions between enemy and blocks (for grounding)"""
        enemy_bounds = enemy.get_bounds()

        search_area = pygame.Rect(
            enemy_bounds.x - 16,
            enemy_bounds.y - 16,
            enemy_bounds.width + 32,
            enemy_bounds.height + 32
        )

        nearby_blocks = self.level.get_blocks_in_range(search_area)

        for block in nearby_blocks:
            if enemy_bounds.colliderect(block.get_bounds()):
                self._resolve_enemy_block_collision(enemy, block)

    def _resolve_enemy_block_collision(self, enemy, block):
        """Resolve collision between enemy and block (simple ground collision)"""
        e_bounds = enemy.get_bounds()
        b_bounds = block.get_bounds()

        # Calculate overlap on each side
        overlap_left = (e_bounds.x + e_bounds.width) - b_bounds.x
        overlap_right = (b_bounds.x + b_bounds.width) - e_bounds.x
        overlap_top = (e_bounds.y + e_bounds.height) - b_bounds.y
        overlap_bottom = (b_bounds.y + b_bounds.height) - e_bounds.y

        # Find minimum overlap
        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        vel = enemy.get_velocity()
        pos = enemy.get_position()

        # Ground collision - enemy landing on top of block
        if min_overlap == overlap_top and vel.y > 0:
            # In Pygame: positive y velocity = falling down
            pos.y = b_bounds.y - e_bounds.height
            vel.y = 0
            enemy.update_bounds()
        # Side collisions - reverse direction for patrolling
        elif min_overlap == overlap_left and vel.x > 0:
            pos.x = b_bounds.x - e_bounds.width
            vel.x = -vel.x  # Reverse direction
            enemy.update_bounds()
        elif min_overlap == overlap_right and vel.x < 0:
            pos.x = b_bounds.x + b_bounds.width
            vel.x = -vel.x  # Reverse direction
            enemy.update_bounds()
