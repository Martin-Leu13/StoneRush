"""
Player entity
Ported from Player.java
"""
import pygame
import math
from entities.game_object import GameObject
from enums import PlayerState, Direction
from sprite_manager import SpriteManager
import config


class AnimationController:
    """Animation controller for sprite-based walk animation"""

    ANIMATION_SPEED = 6.0  # Animation speed (higher = faster)

    def __init__(self):
        self.walk_timer = 0.0
        self.current_frame = 0  # 0 = idle frame, 1 = walk frame

    def update(self, delta, state):
        """Update animation timer"""
        if state == PlayerState.WALKING:
            self.walk_timer += delta * self.ANIMATION_SPEED
            # Toggle between frame 0 and 1 every 1.0 units
            old_frame = self.current_frame
            self.current_frame = int(self.walk_timer) % 2
            # Print when frame changes
            if old_frame != self.current_frame:
                print(f"Animation Frame: {self.current_frame}")
        else:
            # Reset to idle frame when not walking
            self.walk_timer = 0.0
            if self.current_frame != 0:
                self.current_frame = 0
                print(f"Animation Frame: {self.current_frame} (stopped)")

    def get_current_frame(self):
        """Get current animation frame (0 or 1)"""
        return self.current_frame

    def is_walking_frame(self):
        """Returns True if currently showing walk frame"""
        return self.current_frame == 1


class Player(GameObject):
    """Player character with states, lives, and ramming ability"""

    INVULNERABILITY_DURATION = 1.5

    def __init__(self, x, y):
        super().__init__(x, y, config.PLAYER_SIZE, config.PLAYER_SIZE)
        self.state = PlayerState.IDLE
        self.facing_direction = Direction.RIGHT
        self.lives = config.PLAYER_MAX_LIVES
        self.is_grounded = False
        self.ram_timer = 0
        self.is_invulnerable = False
        self.invulnerability_timer = 0
        self.animation_controller = AnimationController()
        self.particle_system = None  # Will be set by game screen
        self.ram_particle_timer = 0  # Timer for spawning particles while ramming
        self.debug_frame_counter = 0  # Debug: Count frames for less verbose output
        self.last_sprite_shown = None  # Debug: Track last sprite shown

        # Load sprites
        self.sprite_manager = SpriteManager()
        self.sprite_idle = self.sprite_manager.get_sprite("player_idle")
        self.sprite_walk = self.sprite_manager.get_sprite("player_walk")

        # Target size for both sprites (must be exactly the same)
        target_size = (int(config.PLAYER_SIZE), int(config.PLAYER_SIZE))

        # Scale sprites to match player size
        if self.sprite_idle:
            original_size = self.sprite_idle.get_size()
            print(f"player_idle.png original size: {original_size}")
            self.sprite_idle = pygame.transform.scale(self.sprite_idle, target_size)
            final_size = self.sprite_idle.get_size()
            print(f"✓ player_idle.png scaled to: {final_size}")
        else:
            print("✗ ERROR: player_idle.png NOT loaded!")

        if self.sprite_walk:
            original_size = self.sprite_walk.get_size()
            print(f"player_walk.png original size: {original_size}")
            self.sprite_walk = pygame.transform.scale(self.sprite_walk, target_size)
            final_size = self.sprite_walk.get_size()
            print(f"✓ player_walk.png scaled to: {final_size}")
        else:
            print("✗ ERROR: player_walk.png NOT loaded!")

        # Verify both sprites are exactly the same size
        if self.sprite_idle and self.sprite_walk:
            if self.sprite_idle.get_size() == self.sprite_walk.get_size():
                print(f"✓ Both sprites are the same size: {target_size}")
            else:
                print(f"✗ WARNING: Sprite sizes don't match!")
                print(f"  idle: {self.sprite_idle.get_size()}")
                print(f"  walk: {self.sprite_walk.get_size()}")

    def update(self, delta):
        """Update player state and timers"""
        # Update ram timer
        if self.ram_timer > 0:
            self.ram_timer -= delta
            if self.ram_timer <= 0:
                self._stop_ramming()

        # Update invulnerability
        if self.is_invulnerable:
            self.invulnerability_timer -= delta
            if self.invulnerability_timer <= 0:
                self.is_invulnerable = False

        # Spawn particles while ramming
        if self.state == PlayerState.RAMMING and self.particle_system:
            self.ram_particle_timer += delta
            # Spawn particles every 0.05 seconds (20 times per second)
            if self.ram_particle_timer >= 0.05:
                self.ram_particle_timer = 0
                # Spawn particles at player's center
                spawn_x = self.position.x + self.width / 2
                spawn_y = self.position.y + self.height / 2
                self.particle_system.spawn_ram_particles(spawn_x, spawn_y, self.facing_direction.get_value())

        # Update state based on velocity and grounded status FIRST
        self._update_state()

        # THEN update animation with the new state
        self.animation_controller.update(delta, self.state)

        super().update(delta)

    def _update_state(self):
        """Update player state based on current conditions"""
        old_state = self.state

        if self.state == PlayerState.RAMMING:
            return  # Ramming overrides other states

        if not self.is_grounded:
            # In Pygame: negative y velocity = going up (jumping), positive = going down (falling)
            self.state = PlayerState.JUMPING if self.velocity.y < 0 else PlayerState.FALLING
        elif abs(self.velocity.x) > 10:
            self.state = PlayerState.WALKING
        else:
            self.state = PlayerState.IDLE

        # Debug: Print when state changes
        if old_state != self.state:
            print(f"State changed: {old_state.name} → {self.state.name}")

    def move_left(self):
        """Move player left"""
        if self.state != PlayerState.RAMMING:
            self.velocity.x = -config.PLAYER_SPEED
            self.facing_direction = Direction.LEFT

    def move_right(self):
        """Move player right"""
        if self.state != PlayerState.RAMMING:
            self.velocity.x = config.PLAYER_SPEED
            self.facing_direction = Direction.RIGHT

    def stop_horizontal_movement(self):
        """Stop horizontal movement"""
        if self.state != PlayerState.RAMMING:
            self.velocity.x = 0

    def jump(self):
        """Make player jump"""
        if self.is_grounded and self.state != PlayerState.RAMMING:
            self.velocity.y = config.PLAYER_JUMP_VELOCITY
            self.is_grounded = False

    def start_ram(self):
        """Start ramming attack"""
        if self.is_grounded and self.state != PlayerState.RAMMING:
            self.state = PlayerState.RAMMING
            self.ram_timer = config.PLAYER_RAM_DURATION
            self.velocity.x = self.facing_direction.get_value() * config.PLAYER_RAM_SPEED

    def _stop_ramming(self):
        """Stop ramming"""
        self.state = PlayerState.IDLE
        self.velocity.x = 0

    def take_damage(self):
        """Take damage (lose a life)"""
        if not self.is_invulnerable:
            self.lives -= 1
            self.is_invulnerable = True
            self.invulnerability_timer = self.INVULNERABILITY_DURATION

    def set_grounded(self, grounded):
        """Set grounded status"""
        self.is_grounded = grounded

    def is_ramming(self):
        """Returns True if player is ramming"""
        return self.state == PlayerState.RAMMING

    def get_state(self):
        return self.state

    def get_lives(self):
        return self.lives

    def get_facing_direction(self):
        return self.facing_direction

    def set_particle_system(self, particle_system):
        """Set the particle system for spawning particles"""
        self.particle_system = particle_system

    def render(self, surface, camera_offset):
        """Render the player with sprites"""
        # Calculate screen position with camera offset
        screen_x = self.position.x - camera_offset[0]
        screen_y = self.position.y - camera_offset[1]

        # Choose sprite based on state and animation frame
        sprite_name = ""
        if self.state == PlayerState.WALKING:
            # Alternate between idle and walk sprite when walking
            if self.animation_controller.is_walking_frame():
                current_sprite = self.sprite_walk.copy()
                sprite_name = "walk"
            else:
                current_sprite = self.sprite_idle.copy()
                sprite_name = "idle"
        else:
            # Use idle sprite for all non-walking states (idle, jumping, falling, ramming)
            current_sprite = self.sprite_idle.copy()
            sprite_name = "idle"

        # Debug: Print when sprite changes
        if sprite_name != self.last_sprite_shown:
            print(f"Showing: {sprite_name} sprite (state: {self.state.name})")
            self.last_sprite_shown = sprite_name

        if current_sprite:
            # Flip sprite if facing left
            if self.facing_direction == Direction.LEFT:
                current_sprite = pygame.transform.flip(current_sprite, True, False)

            # Apply flashing effect if invulnerable
            if self.is_invulnerable and int(self.invulnerability_timer * 10) % 2 == 0:
                # Create white tinted version for flash effect
                current_sprite.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_ADD)

            # Draw the sprite
            surface.blit(current_sprite, (int(screen_x), int(screen_y)))

            # Ram indicator (speed lines)
            if self.state == PlayerState.RAMMING:
                if self.facing_direction == Direction.RIGHT:
                    line_x = screen_x - 10
                else:
                    line_x = screen_x + self.width + 10

                pygame.draw.line(surface, config.COLOR_WHITE,
                               (line_x, screen_y + 10),
                               (line_x - self.facing_direction.get_value() * 8, screen_y + 10), 3)
                pygame.draw.line(surface, config.COLOR_WHITE,
                               (line_x, screen_y + 20),
                               (line_x - self.facing_direction.get_value() * 6, screen_y + 20), 3)
