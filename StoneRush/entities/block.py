"""
Block entity
Ported from Block.java
"""
import pygame
from entities.game_object import GameObject
from enums import BlockType
from sprite_manager import SpriteManager
import config


class Block(GameObject):
    """Represents a platform block in the level"""

    # Class-level sprite manager and sprites (shared by all blocks)
    _sprite_manager = None
    _sprite_ground = None
    _sprite_cracked = None

    @classmethod
    def _load_sprites(cls):
        """Load sprites once for all blocks"""
        if cls._sprite_manager is None:
            print("[BLOCK] Lade Block-Sprites vom SpriteManager...")
            cls._sprite_manager = SpriteManager()
            cls._sprite_ground = cls._sprite_manager.get_sprite("block_ground")
            cls._sprite_cracked = cls._sprite_manager.get_sprite("block_cracked")

            # Scale to block size
            target_size = (int(config.BLOCK_SIZE), int(config.BLOCK_SIZE))
            if cls._sprite_ground:
                print(f"[BLOCK] Ground-Sprite gefunden, skaliere auf {target_size}")
                cls._sprite_ground = pygame.transform.scale(cls._sprite_ground, target_size)
            else:
                print("[WARNUNG] Ground-Sprite NICHT gefunden!")

            if cls._sprite_cracked:
                print(f"[BLOCK] Cracked-Sprite gefunden, skaliere auf {target_size}")
                cls._sprite_cracked = pygame.transform.scale(cls._sprite_cracked, target_size)
            else:
                print("[WARNUNG] Cracked-Sprite NICHT gefunden!")

    def __init__(self, x, y, block_type):
        super().__init__(x, y, config.BLOCK_SIZE, config.BLOCK_SIZE)
        self.block_type = block_type
        self.is_destroyed = False

        # Load sprites on first block creation
        Block._load_sprites()

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

        # Choose sprite based on block type
        sprite = None
        if self.block_type == BlockType.GROUND:
            sprite = Block._sprite_ground
        elif self.block_type == BlockType.CRACKED:
            sprite = Block._sprite_cracked

        # Draw sprite if available
        if sprite:
            surface.blit(sprite, (int(screen_x), int(screen_y)))
        else:
            # Fallback to colored rectangles if sprites not loaded
            if self.block_type == BlockType.GROUND:
                color = config.COLOR_GROUND
            elif self.block_type == BlockType.CRACKED:
                color = config.COLOR_CRACKED_BLOCK
            else:
                return

            pygame.draw.rect(surface, color, (screen_x, screen_y, self.width, self.height))

            # Draw border for cracked blocks
            if self.block_type == BlockType.CRACKED:
                pygame.draw.rect(surface, config.COLOR_BLACK,
                               (screen_x, screen_y, self.width, self.height), 2)
