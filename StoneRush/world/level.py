"""
Level management
Ported from Level.java
"""
import pygame
from entities.block import Block
from entities.enemy import Enemy
from entities.player import Player
from enums import BlockType
from world.level_data import LevelData
import config


class Level:
    """Manages level layout, entities, and rendering"""

    def __init__(self):
        self.blocks = []
        self.enemies = []
        self.player = None
        self.goal_bounds = None
        self.level_data = None

        # Create and build level
        self.level_data = self._create_level_1_data()
        self._build_level()

    def _create_level_1_data(self):
        """Create Level 1 data (identical to Java version)"""
        data = LevelData(config.LEVEL_WIDTH_BLOCKS, config.LEVEL_HEIGHT_BLOCKS)

        # Create ground (bottom 3 rows)
        for x in range(data.get_width()):
            data.set_block(x, 0, BlockType.GROUND)
            data.set_block(x, 1, BlockType.GROUND)
            data.set_block(x, 2, BlockType.GROUND)

        # Add platforms
        for x in range(10, 20):
            data.set_block(x, 5, BlockType.GROUND)

        for x in range(25, 35):
            data.set_block(x, 8, BlockType.GROUND)

        for x in range(40, 50):
            data.set_block(x, 6, BlockType.GROUND)

        for x in range(70, 80):
            data.set_block(x, 7, BlockType.GROUND)

        # Add cracked blocks (obstacles to ram through)
        data.set_block(20, 3, BlockType.CRACKED)
        data.set_block(20, 4, BlockType.CRACKED)
        data.set_block(45, 3, BlockType.CRACKED)
        data.set_block(60, 3, BlockType.CRACKED)
        data.set_block(60, 4, BlockType.CRACKED)
        data.set_block(60, 5, BlockType.CRACKED)

        # Set spawn points
        data.set_player_spawn(64, 96)  # 2 blocks up from ground (2 * 32)
        data.add_enemy_spawn(320, 96)
        data.add_enemy_spawn(480, 96)
        data.add_enemy_spawn(640, 96)
        data.add_enemy_spawn(800, 96)
        data.add_enemy_spawn(1120, 96)

        # Set goal at end of level
        data.set_goal_position(3100, 96)

        return data

    def _build_level(self):
        """Build level from data"""
        # Create blocks from data
        for x in range(self.level_data.get_width()):
            for y in range(self.level_data.get_height()):
                block_type = self.level_data.get_block(x, y)
                if block_type != BlockType.EMPTY:
                    # Flip y-coordinate: LibGDX has y=0 at bottom, Pygame has y=0 at top
                    pixel_y = (config.LEVEL_HEIGHT_BLOCKS - 1 - y) * config.BLOCK_SIZE
                    self.blocks.append(
                        Block(x * config.BLOCK_SIZE, pixel_y, block_type)
                    )

        # Create player (flip y-coordinate from LibGDX to Pygame)
        player_spawn = self.level_data.get_player_spawn()
        player_y = config.WINDOW_HEIGHT - player_spawn.y - config.PLAYER_SIZE
        self.player = Player(player_spawn.x, player_y)

        # Create enemies (flip y-coordinate from LibGDX to Pygame)
        for spawn in self.level_data.get_enemy_spawns():
            enemy_y = config.WINDOW_HEIGHT - spawn.y - config.ENEMY_SIZE
            self.enemies.append(Enemy(spawn.x, enemy_y))

        # Create goal (flip y-coordinate from LibGDX to Pygame)
        goal_pos = self.level_data.get_goal_position()
        goal_y = config.WINDOW_HEIGHT - goal_pos.y - 96  # Goal height is 96
        self.goal_bounds = pygame.Rect(goal_pos.x, goal_y, 64, 96)

    def render(self, surface, camera_offset):
        """Render level blocks and goal"""
        # Render blocks
        for block in self.blocks:
            block.render(surface, camera_offset)

        # Render goal (green rectangle with flag pole)
        screen_x = self.goal_bounds.x - camera_offset[0]
        screen_y = self.goal_bounds.y - camera_offset[1]

        pygame.draw.rect(surface, config.COLOR_GOAL,
                        (screen_x, screen_y, self.goal_bounds.width, self.goal_bounds.height))

        # Draw flag pole
        pygame.draw.rect(surface, config.COLOR_DARK_GRAY,
                        (screen_x + 10, screen_y, 4, self.goal_bounds.height))

    def get_blocks_in_range(self, area):
        """Get blocks that overlap with the given area

        Args:
            area: pygame.Rect representing the search area

        Returns:
            List of blocks that are solid and overlap with the area
        """
        result = []
        for block in self.blocks:
            if block.is_solid() and area.colliderect(block.get_bounds()):
                result.append(block)
        return result

    def remove_dead_enemies(self):
        """Remove dead enemies from the list"""
        self.enemies = [enemy for enemy in self.enemies if not enemy.is_dead]

    def get_player(self):
        return self.player

    def get_enemies(self):
        return self.enemies

    def get_blocks(self):
        return self.blocks

    def get_goal_bounds(self):
        return self.goal_bounds
