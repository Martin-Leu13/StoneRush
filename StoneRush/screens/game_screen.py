"""
Main game screen
Ported from GameScreen.java
"""
import pygame
from screens.base_screen import BaseScreen
from world.level import Level
from world.camera import Camera
from systems.physics_system import PhysicsSystem
from systems.collision_system import CollisionSystem
from systems.input_system import InputSystem
from sprite_manager import SpriteManager
from particle_system import ParticleSystem
import config


class GameScreen(BaseScreen):
    """Main gameplay screen"""

    def __init__(self):
        super().__init__()
        self.level = None
        self.player = None
        self.camera = None
        self.physics_system = None
        self.collision_system = None
        self.input_system = None
        self.particle_system = None
        self.game_over = False
        self.level_complete = False
        self.font = None
        self.sprite_manager = SpriteManager()
        self.background = None

    def show(self):
        """Initialize the game screen"""
        # Initialize level (this creates the player too)
        self.level = Level()
        self.player = self.level.get_player()

        # Initialize systems
        self.physics_system = PhysicsSystem()
        self.collision_system = CollisionSystem(self.level)
        self.input_system = InputSystem(self.player)
        self.particle_system = ParticleSystem()

        # Set particle system for player
        self.player.set_particle_system(self.particle_system)

        # Initialize camera
        self.camera = Camera(self.player)

        # Load background and scale it to window size
        bg_image = self.sprite_manager.get_sprite("background")
        self.background = pygame.transform.scale(bg_image, (config.WINDOW_WIDTH, config.WINDOW_HEIGHT))

        # Initialize font for UI
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

        self.game_over = False
        self.level_complete = False

    def update(self, delta):
        """Update game logic"""
        if self.game_over or self.level_complete:
            return

        # Handle input
        self.input_system.update(delta)

        # Update player
        self.player.update(delta)

        # Update enemies
        for enemy in self.level.get_enemies():
            enemy.update(delta)

        # Apply physics
        self.physics_system.update(delta, self.player)
        for enemy in self.level.get_enemies():
            self.physics_system.update(delta, enemy)

        # Check collisions
        self.collision_system.update(delta)

        # Update camera
        self.camera.update(delta)

        # Update particle system
        self.particle_system.update(delta)

        # Check win/lose conditions
        self._check_game_state()

    def _check_game_state(self):
        """Check if game is over or level is complete"""
        # Check if player reached goal
        if self.player.get_bounds().colliderect(self.level.get_goal_bounds()):
            self.level_complete = True

        # Check if player is dead
        if self.player.get_lives() <= 0:
            self.game_over = True

    def render(self, surface):
        """Render the game screen"""
        # Draw background image
        surface.blit(self.background, (0, 0))

        # Get camera offset
        camera_offset = self.camera.get_offset()

        # Render level (blocks and goal)
        self.level.render(surface, camera_offset)

        # Render enemies
        for enemy in self.level.get_enemies():
            enemy.render(surface, camera_offset)

        # Render player
        self.player.render(surface, camera_offset)

        # Render particles
        self.particle_system.render(surface, camera_offset)

        # Render UI
        self._render_ui(surface)

    def _render_ui(self, surface):
        """Render UI elements (lives, game over, etc.)"""
        # Render lives
        lives_text = self.font.render(f"Lives: {self.player.get_lives()}", True, config.COLOR_BLACK)
        surface.blit(lives_text, (10, 10))

        # Render game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, config.COLOR_BLACK)
            text_rect = game_over_text.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2))
            surface.blit(game_over_text, text_rect)

        # Render level complete message
        if self.level_complete:
            complete_text = self.font.render("LEVEL COMPLETE!", True, config.COLOR_BLACK)
            text_rect = complete_text.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2))
            surface.blit(complete_text, text_rect)
