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
        self.victory = False  # True when all 10 levels completed
        self.current_level = 1  # Track current level (1-10)
        self.font = None
        self.sprite_manager = SpriteManager()
        self.background = None
        self.transition_timer = 0  # Timer for level transition

    def show(self):
        """Initialize the game screen"""
        # Initialize level with current level number (this creates the player too)
        self.level = Level(self.current_level)
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

        # Initialize and play background music
        pygame.mixer.init()
        music_path = r"C:\@Martin\MADDIN\StoneRush\import\ovrworld.wav"
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # -1 = infinite loop

        self.game_over = False
        self.level_complete = False

    def update(self, delta):
        """Update game logic"""
        if self.game_over or self.victory:
            return

        # Handle level transition
        if self.level_complete:
            self.transition_timer += delta
            if self.transition_timer >= 2.0:  # Wait 2 seconds before next level
                if self.current_level >= 10:
                    # All levels complete - victory!
                    self.victory = True
                else:
                    # Advance to next level
                    self.current_level += 1
                    self.level_complete = False
                    self.transition_timer = 0
                    self.show()  # Reinitialize with new level
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

        # Check if player fell into abyss (below screen)
        if self.player.get_position().y > config.WINDOW_HEIGHT + 50:
            # Player fell off the map - instant death
            self.player.lives = 0

        # Check if player is dead - respawn instead of game over
        if self.player.get_lives() <= 0:
            # Respawn: reload the current level
            self.show()  # This resets the entire level

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
        # Render lives and level number
        lives_text = self.font.render(f"Lives: {self.player.get_lives()}", True, config.COLOR_BLACK)
        surface.blit(lives_text, (10, 10))

        level_text = self.font.render(f"Level: {self.current_level}/10", True, config.COLOR_BLACK)
        surface.blit(level_text, (10, 40))

        # Render dash energy bar
        bar_x = 10
        bar_y = 70
        bar_width = 200
        bar_height = 20
        energy_percentage = self.player.get_dash_energy() / self.player.get_max_dash_energy()
        filled_width = int(bar_width * energy_percentage)

        # Draw background (dark gray)
        pygame.draw.rect(surface, config.COLOR_DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))

        # Draw energy fill (orange/yellow)
        energy_color = (255, 165, 0)  # Orange
        pygame.draw.rect(surface, energy_color, (bar_x, bar_y, filled_width, bar_height))

        # Draw border (black)
        pygame.draw.rect(surface, config.COLOR_BLACK, (bar_x, bar_y, bar_width, bar_height), 2)

        # Render game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, config.COLOR_BLACK)
            text_rect = game_over_text.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2))
            surface.blit(game_over_text, text_rect)

        # Render level complete message
        if self.level_complete and not self.victory:
            if self.current_level < 10:
                complete_text = self.font.render(f"LEVEL {self.current_level} COMPLETE!", True, config.COLOR_BLACK)
            else:
                complete_text = self.font.render("LEVEL 10 COMPLETE!", True, config.COLOR_BLACK)
            text_rect = complete_text.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2))
            surface.blit(complete_text, text_rect)

        # Render victory screen after all 10 levels
        if self.victory:
            victory_text = self.font.render("VICTORY! ALL LEVELS COMPLETED!", True, config.COLOR_BLACK)
            text_rect = victory_text.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2))
            surface.blit(victory_text, text_rect)
