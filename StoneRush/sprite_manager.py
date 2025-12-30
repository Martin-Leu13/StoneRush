"""
Sprite Manager for loading and managing game sprites
"""
import pygame
import os


class SpriteManager:
    """Manages loading and caching of sprite images"""

    _instance = None
    _sprites = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SpriteManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._sprites:
            self._load_sprites()

    def _load_sprites(self):
        """Load all sprite images"""
        assets_path = os.path.join(os.path.dirname(__file__), "assets")

        # Load player sprites
        self._sprites["player_idle"] = pygame.image.load(
            os.path.join(assets_path, "player_idle.png")
        ).convert_alpha()

        self._sprites["player_walk"] = pygame.image.load(
            os.path.join(assets_path, "player_walk.png")
        ).convert_alpha()

        # Load block sprites
        print("[SPRITE MANAGER] Lade Block-Sprites...")
        block_ground_path = os.path.join(assets_path, "block_ground.png")
        block_cracked_path = os.path.join(assets_path, "block_cracked.png")

        self._sprites["block_ground"] = pygame.image.load(block_ground_path).convert_alpha()
        print(f"[OK] block_ground.png geladen: {self._sprites['block_ground'].get_size()}")

        self._sprites["block_cracked"] = pygame.image.load(block_cracked_path).convert_alpha()
        print(f"[OK] block_cracked.png geladen: {self._sprites['block_cracked'].get_size()}")

        # Load background
        self._sprites["background"] = pygame.image.load(
            os.path.join(assets_path, "background.png")
        ).convert()

    def get_sprite(self, name):
        """Get a sprite by name"""
        return self._sprites.get(name)

    def get_flipped_sprite(self, name, flip_x=False, flip_y=False):
        """Get a flipped version of a sprite"""
        sprite = self._sprites.get(name)
        if sprite:
            return pygame.transform.flip(sprite, flip_x, flip_y)
        return None
