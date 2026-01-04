"""
Event Manager - Pub/Sub system for decoupled game events.
"""

from enum import Enum, auto
from typing import Callable, Dict, List, Any


class GameEvent(Enum):
    """All game events that can be broadcast."""
    PLAYER_DIED = auto()
    PLAYER_DAMAGED = auto()
    ENEMY_KILLED = auto()
    BULLET_FIRED = auto()
    GAME_PAUSED = auto()
    GAME_RESUMED = auto()


class EventManager:
    """
    Mediator pattern for decoupled event handling.
    Objects can communicate without direct references.
    """

    def __init__(self):
        self._listeners: Dict[GameEvent, List[Callable]] = {}

    def subscribe(self, event_type: GameEvent, callback: Callable) -> None:
        """Register a listener for an event type."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: GameEvent, callback: Callable) -> None:
        """Remove a listener."""
        if event_type in self._listeners and callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)

    def emit(self, event_type: GameEvent, data: Any = None) -> None:
        """Broadcast an event to all listeners."""
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                callback(data)

    def clear(self) -> None:
        """Remove all listeners."""
        self._listeners.clear()
