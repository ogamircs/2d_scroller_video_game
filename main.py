"""
Side-Scrolling Shooter Game
Entry point - initializes and runs the game.

Controls:
    A/D or Left/Right - Move
    W or Space - Jump
    F - Shoot
    ESC - Pause
    ENTER - Start/Select
"""

from core.game import Game
from states.menu_state import MenuState


def main():
    """Initialize and run the game."""
    game = Game()

    # Start at menu
    initial_state = MenuState(game)
    game.push_state(initial_state)

    # Run game loop
    game.run()


if __name__ == "__main__":
    main()
