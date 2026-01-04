"""
Player - Main player character with movement, jumping, and shooting.
"""

import os
import pygame
from config import (
    PLAYER_SPEED, JUMP_VELOCITY, GRAVITY, TERMINAL_VELOCITY,
    PLAYER_MAX_HEALTH, PLAYER_INVINCIBILITY_TIME,
    SHOOT_COOLDOWN, LEVEL_WIDTH, ASSETS_DIR
)
from core.event_manager import EventManager, GameEvent
from .bullet import Bullet


class Player(pygame.sprite.Sprite):
    """
    Player character with movement, jumping, health, and shooting.
    """

    def __init__(self, x: int, y: int, event_manager: EventManager):
        super().__init__()

        # Load sprites
        self.sprites = {
            'stand': self._load_sprite('player_stand.png'),
            'jump': self._load_sprite('player_jump.png'),
            'walk': [
                self._load_sprite('player_walk1.png'),
                self._load_sprite('player_walk2.png'),
            ]
        }

        # Animation
        self.animation_timer = 0
        self.animation_frame = 0
        self.animation_speed = 0.1  # seconds per frame

        # Set initial image
        self.image = self.sprites['stand']
        self.rect = self.image.get_rect(topleft=(x, y))

        self.event_manager = event_manager

        # Physics
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False

        # Direction
        self.facing_right = True

        # Health
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health
        self.invincible = False
        self.invincible_timer = 0

        # Shooting
        self.shoot_cooldown = 0
        self.bullet_group = None  # Set by PlayingState

    def _load_sprite(self, filename: str) -> pygame.Surface:
        """Load a sprite image and scale it appropriately."""
        path = os.path.join(ASSETS_DIR, filename)
        try:
            image = pygame.image.load(path).convert_alpha()
            # Scale to reasonable size (original Kenney sprites are 70x70ish)
            return pygame.transform.scale(image, (48, 48))
        except pygame.error:
            # Fallback to colored rectangle
            surface = pygame.Surface((48, 48))
            surface.fill((0, 200, 100))
            return surface

    def handle_input(self, keys) -> None:
        """Process keyboard input for movement."""
        # Horizontal movement
        self.velocity.x = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED
            self.facing_right = False

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED
            self.facing_right = True

        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
            self.velocity.y = JUMP_VELOCITY
            self.on_ground = False

    def shoot(self) -> None:
        """Fire a bullet if cooldown allows."""
        if self.shoot_cooldown > 0 or self.bullet_group is None:
            return

        # Spawn bullet at gun position
        direction = 1 if self.facing_right else -1
        bullet_x = self.rect.right if self.facing_right else self.rect.left
        bullet_y = self.rect.centery

        bullet = Bullet(bullet_x, bullet_y, direction)
        self.bullet_group.add(bullet)

        self.shoot_cooldown = SHOOT_COOLDOWN
        self.event_manager.emit(GameEvent.BULLET_FIRED)

    def take_damage(self, amount: int) -> None:
        """Take damage if not invincible."""
        if self.invincible:
            return

        self.health -= amount
        self.invincible = True
        self.invincible_timer = PLAYER_INVINCIBILITY_TIME

        self.event_manager.emit(GameEvent.PLAYER_DAMAGED, self.health)

        if self.health <= 0:
            self.health = 0
            self.event_manager.emit(GameEvent.PLAYER_DIED)

    def _update_animation(self, dt: float) -> None:
        """Update sprite animation based on state."""
        # Determine which sprite to use
        if not self.on_ground:
            sprite = self.sprites['jump']
        elif abs(self.velocity.x) > 0:
            # Walking animation
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % len(self.sprites['walk'])
            sprite = self.sprites['walk'][self.animation_frame]
        else:
            sprite = self.sprites['stand']

        # Flip sprite based on direction
        if self.facing_right:
            self.image = sprite
        else:
            self.image = pygame.transform.flip(sprite, True, False)

    def update(self, dt: float) -> None:
        """Update player physics and timers."""
        # Apply gravity
        self.velocity.y += GRAVITY * dt
        if self.velocity.y > TERMINAL_VELOCITY:
            self.velocity.y = TERMINAL_VELOCITY

        # Apply velocity
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

        # Keep player in level bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LEVEL_WIDTH:
            self.rect.right = LEVEL_WIDTH

        # Update shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        # Update animation
        self._update_animation(dt)

        # Update invincibility
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False

            # Flash effect - toggle visibility
            if int(self.invincible_timer * 10) % 2 == 0:
                self.image.set_alpha(100)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)
