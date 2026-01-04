"""
Playing State - Main gameplay state.
"""

import pygame
import random
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, LEVEL_WIDTH, LEVEL_HEIGHT,
    COLOR_SKY_BLUE, SPAWN_INTERVAL, SPAWN_MARGIN
)
from core.camera import Camera
from core.event_manager import GameEvent
from entities.player import Player
from entities.enemy import FlyingEnemy
from entities.platform import Platform
from systems.collision import CollisionSystem
from ui.hud import HUD


class PlayingState:
    """
    Active gameplay - manages all entities and systems.
    """

    def __init__(self, game):
        self.game = game

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        # Create player
        self.player = Player(100, SCREEN_HEIGHT - 150, game.event_manager)
        self.player.bullet_group = self.bullets
        self.all_sprites.add(self.player)

        # Create level
        self._create_level()

        # Systems
        self.collision_system = CollisionSystem()
        self.camera = Camera(LEVEL_WIDTH, LEVEL_HEIGHT)

        # UI
        self.hud = HUD(self.player)

        # Enemy spawning
        self.spawn_timer = 0
        self.spawn_interval = SPAWN_INTERVAL

        # Score tracking
        self.score = 0

        # Subscribe to events
        game.event_manager.subscribe(GameEvent.PLAYER_DIED, self._on_player_died)
        game.event_manager.subscribe(GameEvent.ENEMY_KILLED, self._on_enemy_killed)

    def _create_level(self) -> None:
        """Create platforms for the level."""
        # Ground
        ground = Platform(0, SCREEN_HEIGHT - 40, LEVEL_WIDTH, 40)
        self.platforms.add(ground)
        self.all_sprites.add(ground)

        # Floating platforms
        platform_data = [
            (200, 480, 150, 20),
            (450, 400, 150, 20),
            (700, 320, 150, 20),
            (950, 400, 150, 20),
            (1200, 480, 150, 20),
            (1400, 350, 200, 20),
            (1700, 420, 150, 20),
            (100, 350, 100, 20),
            (350, 250, 120, 20),
            (600, 180, 100, 20),
            (900, 220, 150, 20),
            (1100, 280, 120, 20),
            (1500, 200, 150, 20),
        ]

        for x, y, w, h in platform_data:
            p = Platform(x, y, w, h)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def enter(self) -> None:
        """Called when state becomes active."""
        pass

    def exit(self) -> None:
        """Called when state is deactivated."""
        # Unsubscribe from events
        self.game.event_manager.unsubscribe(GameEvent.PLAYER_DIED, self._on_player_died)
        self.game.event_manager.unsubscribe(GameEvent.ENEMY_KILLED, self._on_enemy_killed)

    def pause(self) -> None:
        """Called when another state is pushed on top."""
        pass

    def resume(self) -> None:
        """Called when returning to this state."""
        pass

    def handle_event(self, event) -> None:
        """Handle pygame events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from .pause_state import PauseState
                self.game.push_state(PauseState(self.game))
            elif event.key == pygame.K_f:
                self.player.shoot()

    def update(self, dt: float) -> None:
        """Update all game logic."""
        # Handle continuous input
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

        # Update player
        self.player.update(dt)

        # Update enemies
        self.enemies.update(dt)

        # Update bullets
        self.bullets.update(dt)

        # Add new sprites to all_sprites for rendering
        for enemy in self.enemies:
            if enemy not in self.all_sprites:
                self.all_sprites.add(enemy)

        for bullet in self.bullets:
            if bullet not in self.all_sprites:
                self.all_sprites.add(bullet)

        # Handle collisions
        self.collision_system.update(
            self.player,
            self.enemies,
            self.bullets,
            self.platforms
        )

        # Update camera
        self.camera.update(self.player)

        # Spawn enemies
        self._update_spawning(dt)

        # Remove off-screen bullets
        self._cleanup_bullets()

    def _update_spawning(self, dt: float) -> None:
        """Spawn enemies periodically."""
        self.spawn_timer += dt

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self._spawn_enemy()

    def _spawn_enemy(self) -> None:
        """Spawn a flying enemy off-screen."""
        # Spawn from right side of camera view
        spawn_x = self.camera.right + SPAWN_MARGIN
        spawn_y = random.randint(100, SCREEN_HEIGHT - 150)

        enemy = FlyingEnemy(spawn_x, spawn_y, self.player, self.game.event_manager)
        self.enemies.add(enemy)

    def _cleanup_bullets(self) -> None:
        """Remove bullets that are too far off-screen."""
        for bullet in self.bullets:
            if bullet.rect.right < self.camera.left - 100:
                bullet.kill()
            elif bullet.rect.left > self.camera.right + 100:
                bullet.kill()

    def _on_player_died(self, data) -> None:
        """Handle player death."""
        from .game_over_state import GameOverState
        self.game.change_state(GameOverState(self.game, self.score))

    def _on_enemy_killed(self, data) -> None:
        """Handle enemy death."""
        self.score += 1

    def render(self, screen) -> None:
        """Render the game world."""
        # Clear screen with sky color
        screen.fill(COLOR_SKY_BLUE)

        # Draw all sprites with camera offset
        for sprite in self.all_sprites:
            screen.blit(sprite.image, self.camera.apply(sprite))

        # Draw HUD (fixed to screen)
        self.hud.render(screen, self.score)
