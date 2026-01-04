"""
Platform - Static solid surfaces for the player to stand on.
"""

import os
import pygame
from config import PLATFORM_COLOR, ASSETS_DIR


class Platform(pygame.sprite.Sprite):
    """
    Static platform that player and enemies can stand on.
    Uses tiled sprites for visual appearance.
    """

    def __init__(self, x: int, y: int, width: int, height: int, color=PLATFORM_COLOR):
        super().__init__()

        # Load tile sprites
        self.tile_left = self._load_sprite('platform_left.png')
        self.tile_mid = self._load_sprite('platform_mid.png')
        self.tile_right = self._load_sprite('platform_right.png')

        # Get tile dimensions
        tile_width = self.tile_mid.get_width()
        tile_height = self.tile_mid.get_height()

        # Calculate how many tiles we need
        num_tiles = max(1, width // tile_width)

        # Create surface for the full platform
        self.image = pygame.Surface((num_tiles * tile_width, tile_height), pygame.SRCALPHA)

        # Tile the platform
        if num_tiles == 1:
            self.image.blit(self.tile_mid, (0, 0))
        elif num_tiles == 2:
            self.image.blit(self.tile_left, (0, 0))
            self.image.blit(self.tile_right, (tile_width, 0))
        else:
            # Left edge
            self.image.blit(self.tile_left, (0, 0))
            # Middle tiles
            for i in range(1, num_tiles - 1):
                self.image.blit(self.tile_mid, (i * tile_width, 0))
            # Right edge
            self.image.blit(self.tile_right, ((num_tiles - 1) * tile_width, 0))

        self.rect = self.image.get_rect(topleft=(x, y))

    def _load_sprite(self, filename: str) -> pygame.Surface:
        """Load a sprite image."""
        path = os.path.join(ASSETS_DIR, filename)
        try:
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, (70, 70))
        except pygame.error:
            # Fallback to colored rectangle
            surface = pygame.Surface((70, 70))
            surface.fill(PLATFORM_COLOR)
            return surface

    def update(self, dt: float) -> None:
        """Platforms are static - no update needed."""
        pass
