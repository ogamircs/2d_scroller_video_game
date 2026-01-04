"""
Bullet - Projectile fired by the player.
"""

import os
import pygame
from config import (
    BULLET_SPEED, BULLET_DAMAGE, BULLET_LIFETIME, ASSETS_DIR
)


class Bullet(pygame.sprite.Sprite):
    """
    Projectile that travels in a direction and damages enemies.
    """

    def __init__(self, x: int, y: int, direction: int):
        """
        Args:
            x, y: Starting position
            direction: 1 for right, -1 for left
        """
        super().__init__()

        # Load sprite
        self.image = self._load_sprite('bullet.png')

        # Flip if shooting left
        if direction < 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect(center=(x, y))

        self.direction = direction
        self.speed = BULLET_SPEED
        self.damage = BULLET_DAMAGE
        self.lifetime = BULLET_LIFETIME

    def _load_sprite(self, filename: str) -> pygame.Surface:
        """Load a sprite image and scale it appropriately."""
        path = os.path.join(ASSETS_DIR, filename)
        try:
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, (24, 24))
        except pygame.error:
            # Fallback to colored rectangle
            surface = pygame.Surface((12, 6))
            surface.fill((255, 255, 0))
            return surface

    def update(self, dt: float) -> None:
        """Move bullet and check lifetime."""
        # Move in direction
        self.rect.x += self.speed * self.direction * dt

        # Decrease lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
