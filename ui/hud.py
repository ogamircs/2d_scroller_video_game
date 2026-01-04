"""
HUD - Heads-up display showing health bar and score.
"""

import pygame
from config import (
    HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT,
    HEALTH_BAR_X, HEALTH_BAR_Y,
    HEALTH_BAR_BG, HEALTH_BAR_FG, HEALTH_BAR_LOW,
    COLOR_WHITE
)


class HUD:
    """
    Displays player health bar and score.
    """

    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 28)

    def render(self, screen, score: int = 0) -> None:
        """Render HUD elements to screen."""
        self._render_health_bar(screen)
        self._render_score(screen, score)

    def _render_health_bar(self, screen) -> None:
        """Draw the health bar."""
        # Background bar
        bg_rect = pygame.Rect(
            HEALTH_BAR_X, HEALTH_BAR_Y,
            HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT
        )
        pygame.draw.rect(screen, HEALTH_BAR_BG, bg_rect)

        # Health percentage
        health_percent = self.player.health / self.player.max_health

        # Foreground bar (changes color when low)
        fg_color = HEALTH_BAR_FG if health_percent > 0.3 else HEALTH_BAR_LOW
        fg_width = int(HEALTH_BAR_WIDTH * health_percent)

        if fg_width > 0:
            fg_rect = pygame.Rect(
                HEALTH_BAR_X, HEALTH_BAR_Y,
                fg_width, HEALTH_BAR_HEIGHT
            )
            pygame.draw.rect(screen, fg_color, fg_rect)

        # Border
        pygame.draw.rect(screen, COLOR_WHITE, bg_rect, 2)

        # Health text
        health_text = self.font.render(
            f"{self.player.health}/{self.player.max_health}",
            True, COLOR_WHITE
        )
        text_x = HEALTH_BAR_X + HEALTH_BAR_WIDTH + 10
        text_y = HEALTH_BAR_Y + (HEALTH_BAR_HEIGHT - health_text.get_height()) // 2
        screen.blit(health_text, (text_x, text_y))

    def _render_score(self, screen, score: int) -> None:
        """Draw the score."""
        score_text = self.font.render(f"Score: {score}", True, COLOR_WHITE)
        score_x = HEALTH_BAR_X + HEALTH_BAR_WIDTH + 100
        score_y = HEALTH_BAR_Y + (HEALTH_BAR_HEIGHT - score_text.get_height()) // 2
        screen.blit(score_text, (score_x, score_y))
