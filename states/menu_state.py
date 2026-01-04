"""
Menu State - Main menu screen.
"""

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_DARK_BLUE


class MenuState:
    """
    Main menu with title and start prompt.
    """

    def __init__(self, game):
        self.game = game
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)

    def enter(self) -> None:
        """Called when state becomes active."""
        pass

    def exit(self) -> None:
        """Called when state is deactivated."""
        pass

    def pause(self) -> None:
        """Called when another state is pushed on top."""
        pass

    def resume(self) -> None:
        """Called when returning to this state."""
        pass

    def handle_event(self, event) -> None:
        """Handle pygame events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Import here to avoid circular import
                from .playing_state import PlayingState
                self.game.change_state(PlayingState(self.game))
            elif event.key == pygame.K_ESCAPE:
                self.game.running = False

    def update(self, dt: float) -> None:
        """Update menu logic."""
        pass

    def render(self, screen) -> None:
        """Render the menu."""
        screen.fill(COLOR_DARK_BLUE)

        # Title
        title = self.font_large.render("SIDE SHOOTER", True, COLOR_WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title, title_rect)

        # Instructions
        start_text = self.font_small.render("Press ENTER to Start", True, COLOR_WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(start_text, start_rect)

        # Controls
        controls = [
            "Controls:",
            "A/D or Arrows - Move",
            "W or Space - Jump",
            "F - Shoot",
            "ESC - Pause"
        ]

        y_offset = SCREEN_HEIGHT * 0.65
        for line in controls:
            text = self.font_small.render(line, True, COLOR_WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 30
