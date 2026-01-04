"""
Collision System - Handles all collision detection and response.
"""

import pygame


class CollisionSystem:
    """
    Centralized collision detection using Pygame's sprite collision.
    """

    def __init__(self):
        pass

    def update(self, player, enemies, bullets, platforms) -> None:
        """
        Check all collisions each frame.
        Order matters for proper response.
        """
        self._handle_player_platform_collision(player, platforms)
        self._handle_bullet_enemy_collision(bullets, enemies)
        self._handle_enemy_player_collision(player, enemies)

    def _handle_player_platform_collision(self, player, platforms) -> None:
        """
        Resolve player-platform collisions for standing and blocking.
        """
        # Store original position for collision resolution
        original_y = player.rect.y

        # Reset ground state
        player.on_ground = False

        # Check each platform
        for platform in platforms:
            if not player.rect.colliderect(platform.rect):
                continue

            # Vertical collision (landing or hitting head)
            if player.velocity.y > 0:  # Falling
                # Check if player was above platform last frame
                if original_y + player.rect.height <= platform.rect.top + player.velocity.y * 0.1:
                    player.rect.bottom = platform.rect.top
                    player.velocity.y = 0
                    player.on_ground = True
            elif player.velocity.y < 0:  # Jumping up
                if player.rect.top < platform.rect.bottom:
                    player.rect.top = platform.rect.bottom
                    player.velocity.y = 0

        # Horizontal collision (after vertical is resolved)
        for platform in platforms:
            if not player.rect.colliderect(platform.rect):
                continue

            if player.velocity.x > 0:  # Moving right
                player.rect.right = platform.rect.left
            elif player.velocity.x < 0:  # Moving left
                player.rect.left = platform.rect.right

    def _handle_bullet_enemy_collision(self, bullets, enemies) -> None:
        """
        Check bullets hitting enemies.
        Uses groupcollide for efficiency.
        """
        # Get all collisions between bullets and enemies
        collisions = pygame.sprite.groupcollide(
            bullets,
            enemies,
            dokilla=True,   # Kill bullet on hit
            dokillb=False   # Don't auto-kill enemy
        )

        # Apply damage to hit enemies
        for bullet, hit_enemies in collisions.items():
            for enemy in hit_enemies:
                enemy.take_damage(bullet.damage)

    def _handle_enemy_player_collision(self, player, enemies) -> None:
        """
        Check enemies touching player.
        """
        if not player.alive():
            return

        hits = pygame.sprite.spritecollide(player, enemies, False)

        for enemy in hits:
            player.take_damage(enemy.damage)
