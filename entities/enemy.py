"""
Enemy - Flying enemy that tracks toward the player.
"""

import os
import pygame
from config import (
    ENEMY_SPEED, ENEMY_HEALTH, ENEMY_DAMAGE, ASSETS_DIR
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

        # Load sprites
        self.sprites = {
            'idle': self._load_sprite('enemy.png'),
            'fly': self._load_sprite('enemy_fly.png'),
        }

        # Animation
        self.animation_timer = 0
        self.animation_speed = 0.15

        self.image = self.sprites['idle']
        self.rect = self.image.get_rect(center=(x, y))

        self.player = player
        self.event_manager = event_manager

        self.speed = ENEMY_SPEED
        self.health = ENEMY_HEALTH
        self.damage = ENEMY_DAMAGE

        self.velocity = pygame.math.Vector2(0, 0)
        self.facing_right = False

    def _load_sprite(self, filename: str) -> pygame.Surface:
        """Load a sprite image and scale it appropriately."""
        path = os.path.join(ASSETS_DIR, filename)
        try:
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, (40, 40))
        except pygame.error:
            # Fallback to colored rectangle
            surface = pygame.Surface((40, 40))
            surface.fill((200, 50, 50))
            return surface

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

        # Animate
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            # Toggle between idle and fly
            if self.image == self.sprites['idle']:
                sprite = self.sprites['fly']
            else:
                sprite = self.sprites['idle']

            # Flip based on direction
            if self.facing_right:
                self.image = sprite
            else:
                self.image = pygame.transform.flip(sprite, True, False)

    def take_damage(self, amount: int) -> None:
        """Take damage and check for death."""
        self.health -= amount

        if self.health <= 0:
            self.event_manager.emit(GameEvent.ENEMY_KILLED, {
                'position': self.rect.center
            })
            self.kill()
