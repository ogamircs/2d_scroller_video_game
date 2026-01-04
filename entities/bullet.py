"""
Bullet - Projectile fired by the player.
"""

import pygame
from config import (
    BULLET_WIDTH, BULLET_HEIGHT, BULLET_COLOR,
    BULLET_SPEED, BULLET_DAMAGE, BULLET_LIFETIME
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

        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect(center=(x, y))

        self.direction = direction
        self.speed = BULLET_SPEED
        self.damage = BULLET_DAMAGE
        self.lifetime = BULLET_LIFETIME

    def update(self, dt: float) -> None:
        """Move bullet and check lifetime."""
        # Move in direction
        self.rect.x += self.speed * self.direction * dt

        # Decrease lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
