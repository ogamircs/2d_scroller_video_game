"""
Camera - Scrolling viewport that follows the player.
"""

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, LEVEL_WIDTH, LEVEL_HEIGHT


class Camera:
    """
    Handles viewport scrolling for the side-scroller.
    Centers on target (player) with level boundary clamping.
    """

    def __init__(self, level_width: int = LEVEL_WIDTH, level_height: int = LEVEL_HEIGHT):
        self.camera_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.level_width = level_width
        self.level_height = level_height

    def apply(self, entity) -> pygame.Rect:
        """Offset an entity's rect by camera position for rendering."""
        return entity.rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def apply_rect(self, rect: pygame.Rect) -> pygame.Rect:
        """Offset a rect by camera position."""
        return rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def apply_pos(self, pos: tuple) -> tuple:
        """Offset a position by camera position."""
        return (pos[0] - self.camera_rect.x, pos[1] - self.camera_rect.y)

    def update(self, target) -> None:
        """Center camera on target, clamped to level boundaries."""
        # Center on target
        x = target.rect.centerx - SCREEN_WIDTH // 2
        y = target.rect.centery - SCREEN_HEIGHT // 2

        # Clamp to level boundaries
        x = max(0, min(x, self.level_width - SCREEN_WIDTH))
        y = max(0, min(y, self.level_height - SCREEN_HEIGHT))

        self.camera_rect.x = x
        self.camera_rect.y = y

    @property
    def left(self) -> int:
        return self.camera_rect.left

    @property
    def right(self) -> int:
        return self.camera_rect.right

    @property
    def top(self) -> int:
        return self.camera_rect.top

    @property
    def bottom(self) -> int:
        return self.camera_rect.bottom
