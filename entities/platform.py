"""
Platform - Static solid surfaces for the player to stand on.
"""

import pygame
from config import PLATFORM_COLOR


class Platform(pygame.sprite.Sprite):
    """
    Static platform that player and enemies can stand on.
    """

    def __init__(self, x: int, y: int, width: int, height: int, color=PLATFORM_COLOR):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt: float) -> None:
        """Platforms are static - no update needed."""
        pass
