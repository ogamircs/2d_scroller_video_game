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
        Resolve player-platform collisions using separate X and Y passes.
        """
        # Reset ground state
        player.on_ground = False

        # Get player's feet position for ground check
        feet_rect = pygame.Rect(player.rect.x + 5, player.rect.bottom, player.rect.width - 10, 5)

        # Check if standing on any platform
        for platform in platforms:
            if feet_rect.colliderect(platform.rect) and player.velocity.y >= 0:
                # Player is on top of this platform
                player.rect.bottom = platform.rect.top
                player.velocity.y = 0
                player.on_ground = True
                break

        # Handle horizontal collisions (walls)
        for platform in platforms:
            if player.rect.colliderect(platform.rect):
                # Determine overlap
                overlap_left = player.rect.right - platform.rect.left
                overlap_right = platform.rect.right - player.rect.left
                overlap_top = player.rect.bottom - platform.rect.top
                overlap_bottom = platform.rect.bottom - player.rect.top

                # Find smallest horizontal overlap
                min_horizontal = min(overlap_left, overlap_right)
                min_vertical = min(overlap_top, overlap_bottom)

                # Only resolve horizontal if it's a side collision (not standing on top)
                if min_horizontal < min_vertical and not player.on_ground:
                    if overlap_left < overlap_right:
                        player.rect.right = platform.rect.left
                    else:
                        player.rect.left = platform.rect.right

        # Handle hitting head on platform from below
        if player.velocity.y < 0:
            head_rect = pygame.Rect(player.rect.x + 5, player.rect.top - 2, player.rect.width - 10, 4)
            for platform in platforms:
                if head_rect.colliderect(platform.rect):
                    player.rect.top = platform.rect.bottom
                    player.velocity.y = 0
                    break

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
