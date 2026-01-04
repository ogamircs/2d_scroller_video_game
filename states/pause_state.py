"""
Pause State - Pause overlay during gameplay.
"""

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE


class PauseState:
    """
    Pause overlay that renders on top of the game.
    """

    def __init__(self, game):
        self.game = game
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)

        # Semi-transparent overlay
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(150)

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
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                # Unpause - go back to playing
                self.game.pop_state()
            elif event.key == pygame.K_q:
                # Quit to menu
                from .menu_state import MenuState
                self.game.change_state(MenuState(self.game))

    def update(self, dt: float) -> None:
        """Update pause logic."""
        pass

    def render(self, screen) -> None:
        """Render pause overlay on top of game."""
        # Draw overlay
        screen.blit(self.overlay, (0, 0))

        # Pause text
        pause_text = self.font_large.render("PAUSED", True, COLOR_WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(pause_text, pause_rect)

        # Instructions
        resume_text = self.font_small.render("Press ESC or ENTER to Resume", True, COLOR_WHITE)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(resume_text, resume_rect)

        quit_text = self.font_small.render("Press Q to Quit to Menu", True, COLOR_WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        screen.blit(quit_text, quit_rect)
