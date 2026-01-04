# Side-Scrolling Shooter

A 2D side-scrolling shooter game built with Python and Pygame.

## Installation

```bash
pip install pygame
```

Or using pygame-ce (community edition):
```bash
pip install pygame-ce
```

## Running the Game

```bash
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| A/D or Arrow Keys | Move left/right |
| W or Space | Jump |
| F | Shoot |
| ESC | Pause |
| ENTER | Start/Select |

## Gameplay

- Survive as long as possible against waves of flying enemies
- Shoot enemies before they reach you
- Each enemy defeated adds to your score
- Game ends when your health reaches zero

## Project Structure

```
simple_video_game/
├── main.py           # Entry point
├── config.py         # Game settings and constants
├── core/             # Core systems
│   ├── game.py       # Main game loop
│   ├── camera.py     # Scrolling camera
│   └── event_manager.py
├── entities/         # Game objects
│   ├── player.py
│   ├── enemy.py
│   ├── bullet.py
│   └── platform.py
├── systems/          # Game systems
│   └── collision.py
├── states/           # Game states
│   ├── menu_state.py
│   ├── playing_state.py
│   ├── pause_state.py
│   └── game_over_state.py
└── ui/               # User interface
    └── hud.py
```

## Configuration

Edit `config.py` to adjust game settings:

- `PLAYER_SPEED` - How fast the player moves
- `JUMP_VELOCITY` - Jump height
- `PLAYER_MAX_HEALTH` - Starting health
- `ENEMY_SPEED` - How fast enemies move
- `ENEMY_DAMAGE` - Damage per enemy hit
- `SPAWN_INTERVAL` - Seconds between enemy spawns
- `BULLET_DAMAGE` - Damage per bullet
