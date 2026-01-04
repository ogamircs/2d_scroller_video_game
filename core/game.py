"""
Game - Main game class with game loop and state management.
"""

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from .event_manager import EventManager


class Game:
    """
    Main game controller.
    Manages the game loop and state stack.
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.event_manager = EventManager()

        # State stack for managing game states
        self.state_stack = []

    def push_state(self, state) -> None:
        """Push a new state onto the stack."""
        if self.state_stack:
            self.state_stack[-1].pause()
        self.state_stack.append(state)
        state.enter()

    def pop_state(self):
        """Remove and return the current state."""
        if self.state_stack:
            state = self.state_stack.pop()
            state.exit()
            if self.state_stack:
                self.state_stack[-1].resume()
            return state
        return None

    def change_state(self, state) -> None:
        """Replace current state with a new one."""
        while self.state_stack:
            self.state_stack.pop().exit()
        self.push_state(state)

    def current_state(self):
        """Get the active state."""
        return self.state_stack[-1] if self.state_stack else None

    def handle_events(self) -> None:
        """Process all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # Pass event to current state
            if self.current_state():
                self.current_state().handle_event(event)

    def update(self, dt: float) -> None:
        """Update current state."""
        if self.current_state():
            self.current_state().update(dt)

    def render(self) -> None:
        """Render current state."""
        if self.current_state():
            self.current_state().render(self.screen)
        pygame.display.flip()

    def run(self) -> None:
        """Main game loop."""
        while self.running:
            # Delta time in seconds
            dt = self.clock.tick(FPS) / 1000.0

            self.handle_events()
            self.update(dt)
            self.render()

        pygame.quit()
