"""
Particle system for visual effects
"""
import pygame
import random
import math


class Particle:
    """Single particle with position, velocity, and lifetime"""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-150, 150)  # Random horizontal velocity
        self.vy = random.uniform(-200, -50)  # Random upward velocity
        self.color = color
        self.lifetime = 0.5  # 0.5 seconds
        self.max_lifetime = 0.5
        self.size = random.uniform(2, 4)  # Random size between 2-4 pixels

    def update(self, delta):
        """Update particle position and lifetime"""
        # Apply velocity
        self.x += self.vx * delta
        self.y += self.vy * delta

        # Apply gravity
        self.vy += 400 * delta  # Gravity effect

        # Reduce lifetime
        self.lifetime -= delta

    def is_dead(self):
        """Check if particle should be removed"""
        return self.lifetime <= 0

    def render(self, surface, camera_offset):
        """Render the particle"""
        screen_x = self.x - camera_offset[0]
        screen_y = self.y - camera_offset[1]

        # Calculate alpha based on remaining lifetime (fade out)
        alpha_ratio = self.lifetime / self.max_lifetime
        alpha = int(255 * alpha_ratio)

        # Create a surface with alpha for transparency
        particle_surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        color_with_alpha = (*self.color, alpha)
        pygame.draw.circle(particle_surface, color_with_alpha,
                         (int(self.size), int(self.size)), int(self.size))

        surface.blit(particle_surface, (int(screen_x - self.size), int(screen_y - self.size)))


class ParticleSystem:
    """Manages all particles in the game"""

    def __init__(self):
        self.particles = []

    def spawn_ram_particles(self, x, y, direction):
        """Spawn particles when player rams

        Args:
            x: X position to spawn particles
            y: Y position to spawn particles
            direction: Direction player is facing (1 for right, -1 for left)
        """
        # Spawn 5-8 particles
        num_particles = random.randint(5, 8)

        # Colors: gray and brown particles
        colors = [
            (128, 128, 128),  # Gray
            (153, 102, 51),   # Brown
            (127, 76, 25),    # Dark brown
            (100, 100, 100),  # Dark gray
        ]

        for _ in range(num_particles):
            # Random offset around the spawn point
            offset_x = random.uniform(-10, 10)
            offset_y = random.uniform(-10, 10)

            particle = Particle(x + offset_x, y + offset_y, random.choice(colors))

            # Adjust velocity based on direction
            # Particles should fly in the direction of movement
            particle.vx = random.uniform(50, 200) * direction

            self.particles.append(particle)

    def update(self, delta):
        """Update all particles"""
        # Update each particle
        for particle in self.particles:
            particle.update(delta)

        # Remove dead particles
        self.particles = [p for p in self.particles if not p.is_dead()]

    def render(self, surface, camera_offset):
        """Render all particles"""
        for particle in self.particles:
            particle.render(surface, camera_offset)

    def clear(self):
        """Remove all particles"""
        self.particles.clear()
