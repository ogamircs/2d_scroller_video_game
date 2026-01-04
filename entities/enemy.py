"""
Enemy - Flying enemy that tracks toward the player.
"""

import pygame
from config import (
    ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_COLOR,
    ENEMY_SPEED, ENEMY_HEALTH, ENEMY_DAMAGE
)
from core.event_manager import EventManager, GameEvent


class FlyingEnemy(pygame.sprite.Sprite):
    """
    Flying enemy that moves toward the player.
    """

    def __init__(self, x: int, y: int, player, event_manager: EventManager):
        """
        Args:
            x, y: Starting position
            player: Reference to player (for tracking)
            event_manager: For emitting death events
        """
        super().__init__()

        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect(center=(x, y))

        self.player = player
        self.event_manager = event_manager

        self.speed = ENEMY_SPEED
        self.health = ENEMY_HEALTH
        self.damage = ENEMY_DAMAGE

        self.velocity = pygame.math.Vector2(0, 0)
        self.facing_right = False

    def update(self, dt: float) -> None:
        """Move toward the player."""
        if not self.player or not self.player.alive():
            return

        # Calculate direction to player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery

        # Normalize direction
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance > 0:
            dx /= distance
            dy /= distance

        # Move toward player
        self.rect.x += dx * self.speed * dt
        self.rect.y += dy * self.speed * dt

        # Track facing direction
        self.facing_right = dx > 0

    def take_damage(self, amount: int) -> None:
        """Take damage and check for death."""
        self.health -= amount

        if self.health <= 0:
            self.event_manager.emit(GameEvent.ENEMY_KILLED, {
                'position': self.rect.center
            })
            self.kill()
