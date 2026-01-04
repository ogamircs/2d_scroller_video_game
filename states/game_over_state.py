"""
Game Over State - Death screen with restart option.
"""

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_DARK_GRAY


class GameOverState:
    """
    Game over screen shown when player dies.
    """

    def __init__(self, game, score: int = 0):
        self.game = game
        self.score = score
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
                # Restart game
                from .playing_state import PlayingState
                self.game.change_state(PlayingState(self.game))
            elif event.key == pygame.K_ESCAPE:
                # Return to menu
                from .menu_state import MenuState
                self.game.change_state(MenuState(self.game))

    def update(self, dt: float) -> None:
        """Update game over logic."""
        pass

    def render(self, screen) -> None:
        """Render game over screen."""
        screen.fill(COLOR_DARK_GRAY)

        # Game Over text
        game_over = self.font_large.render("GAME OVER", True, (200, 50, 50))
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(game_over, game_over_rect)

        # Score
        score_text = self.font_small.render(f"Enemies Defeated: {self.score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_text, score_rect)

        # Instructions
        restart_text = self.font_small.render("Press ENTER to Play Again", True, COLOR_WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.65))
        screen.blit(restart_text, restart_rect)

        menu_text = self.font_small.render("Press ESC for Menu", True, COLOR_WHITE)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.65 + 40))
        screen.blit(menu_text, menu_rect)
