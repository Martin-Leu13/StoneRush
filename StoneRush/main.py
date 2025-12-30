"""
StoneRush - Main entry point
A 2D platformer game ported from Java/LibGDX to Python/Pygame

Controls:
- Arrow Keys: Move left/right
- Space: Jump
- Shift: Ram attack
- Escape: Quit game
"""
import pygame
import sys
from screens.game_screen import GameScreen
import config


class StoneRushGame:
    """Main game class"""

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Create window
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption(config.GAME_TITLE)

        # Game clock
        self.clock = pygame.time.Clock()

        # Current screen
        self.current_screen = None

        # Running flag
        self.running = True

    def run(self):
        """Main game loop"""
        # Start with game screen
        self.current_screen = GameScreen()
        self.current_screen.show()

        while self.running:
            # Calculate delta time (in seconds)
            delta = self.clock.tick(config.TARGET_FPS) / 1000.0

            # Handle events
            self._handle_events()

            # Update
            if self.current_screen:
                self.current_screen.update(delta)

            # Render
            if self.current_screen:
                self.current_screen.render(self.screen)

            # Update display
            pygame.display.flip()

        # Cleanup
        self._quit()

    def _handle_events(self):
        """Handle Pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def _quit(self):
        """Clean up and quit"""
        if self.current_screen:
            self.current_screen.dispose()
        pygame.quit()
        sys.exit()


def main():
    """Entry point"""
    game = StoneRushGame()
    game.run()


if __name__ == "__main__":
    main()
