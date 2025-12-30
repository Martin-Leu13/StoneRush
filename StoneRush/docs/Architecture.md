# StoneRush - Architektur

## Überblick

StoneRush ist ein 2D-Platformer in Python/Pygame, portiert von LibGDX (Java). Das Spiel verwendet eine **Entity-Component-System (ECS)** ähnliche Architektur mit klarer Trennung von Logik, Rendering und Datenhaltung.

## Technologie-Stack

- **Sprache**: Python 3.13
- **Game Engine**: Pygame 2.6.1
- **Bildverarbeitung**: Pillow (PIL)
- **Koordinatensystem**: Y=0 oben, positive Y = nach unten (Pygame Standard)

## Architektur-Komponenten

### 1. Core Game Loop (`main.py`)

```
┌─────────────────────────────────────┐
│          Main Game Loop             │
├─────────────────────────────────────┤
│  - Window/Display Management        │
│  - Screen State Management          │
│  - Delta Time Calculation           │
│  - Event Handling                   │
└─────────────────────────────────────┘
```

**Verantwortlichkeiten**:
- Initialisiert Pygame und das Fenster
- Verwaltet Screen-States (Menu, Game, etc.)
- Ruft Update/Render in jedem Frame auf

### 2. Screens (`screens/`)

```
┌─────────────────────────────────────┐
│        Screen Management            │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │     GameScreen                │  │
│  │  - Level Management           │  │
│  │  - System Orchestration       │  │
│  │  - Camera/UI Rendering        │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**GameScreen** ist der zentrale Screen-State:
- Lädt und verwaltet Level
- Initialisiert alle Systeme
- Koordiniert Update-Reihenfolge
- Verwaltet Kamera und UI-Rendering

### 3. Entities (`entities/`)

```
┌─────────────────────────────────────┐
│           GameObject (Base)         │
│  - Position, Velocity, Bounds       │
│  - update(), render()               │
└─────────────────────────────────────┘
           ▲         ▲         ▲
           │         │         │
    ┌──────┴──┐ ┌────┴────┐ ┌─┴─────┐
    │ Player  │ │ Enemy   │ │ Block │
    └─────────┘ └─────────┘ └───────┘
```

**GameObject** (Abstract Base Class):
- `position`: pygame.Vector2
- `velocity`: pygame.Vector2
- `bounds`: pygame.Rect (AABB collision box)
- `update(delta)`: Update-Logik
- `render(surface, camera_offset)`: Rendering

**Player**:
- State Machine (IDLE, WALKING, JUMPING, FALLING, RAMMING)
- Dash-Energy System (100 max, drain/regen rates)
- Lives System (3 Leben)
- Invulnerability Timer
- Animation Controller
- Particle System Integration

**Enemy**:
- Patrol Behavior (Hin- und Her-Bewegung)
- Platform-Edge Detection
- Death State

**Block**:
- BlockType (GROUND, CRACKED)
- Sprite-basiertes Rendering
- Destroyed State (für rissige Blöcke)

### 4. Systems (`systems/`)

```
┌─────────────────────────────────────────────────┐
│              Systems (Game Logic)               │
├─────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐             │
│  │ InputSystem │  │PhysicsSystem │             │
│  │             │  │              │             │
│  │ - Keyboard  │  │ - Gravity    │             │
│  │ - Controls  │  │ - Terminal   │             │
│  └─────────────┘  │   Velocity   │             │
│                   └──────────────┘             │
│  ┌──────────────────────────────┐              │
│  │    CollisionSystem           │              │
│  │                              │              │
│  │ - AABB Detection             │              │
│  │ - Overlap Resolution         │              │
│  │ - Player vs Blocks           │              │
│  │ - Player vs Enemies          │              │
│  │ - Enemy Edge Detection       │              │
│  │ - Boundary Walls             │              │
│  └──────────────────────────────┘              │
└─────────────────────────────────────────────────┘
```

**InputSystem**:
- Verarbeitet Tastatur-Input (Pfeiltasten, Space, Shift)
- Ruft entsprechende Player-Methoden auf
- Dash-Blockierung bei Wandkollision

**PhysicsSystem**:
- Wendet Gravitation an (800 px/s²)
- Terminal Velocity (1000 px/s max)
- Delta-basierte Bewegung

**CollisionSystem**:
- AABB (Axis-Aligned Bounding Box) Kollisionserkennung
- Minimum Overlap Resolution
- Spezielle Logik für:
  - Ground Detection mit Toleranz (3px)
  - Dash-Stopp bei Wänden
  - Cracked Block Destruction
  - Enemy Edge Detection
  - Invisible Boundary Walls (links, rechts, oben)

### 5. World Management (`world/`)

```
┌─────────────────────────────────────┐
│          Level                      │
├─────────────────────────────────────┤
│  - Player Instance                  │
│  - Enemies List                     │
│  - Blocks Grid/List                 │
│  - Goal Position                    │
│  - Spatial Queries                  │
└─────────────────────────────────────┘
```

**Level**:
- Prozedural generierte Levels (10 Stück)
- Schwierigkeitsgrad steigt mit Level-Nummer
- Spatial Queries für Collision Detection
- Block Management (Add/Remove)

### 6. Sprite Management (`sprite_manager.py`)

```
┌─────────────────────────────────────┐
│       SpriteManager (Singleton)     │
├─────────────────────────────────────┤
│  - player_idle, player_walk         │
│  - block_ground, block_cracked      │
│  - background                       │
│  - Sprite Caching                   │
└─────────────────────────────────────┘
```

**Design Pattern**: Singleton
- Lädt alle Sprites einmal beim Start
- Bietet `get_sprite(name)` und `get_flipped_sprite()`
- Convert_alpha() für Performance

### 7. Particle System (`particle_system.py`)

```
┌─────────────────────────────────────┐
│        ParticleSystem               │
├─────────────────────────────────────┤
│  - Particle Pool                    │
│  - spawn_particle(x, y, vx, vy)    │
│  - Physics Simulation               │
│  - Rendering                        │
└─────────────────────────────────────┘
```

**Features**:
- Dash-Effekt Partikel
- Gravitation und Lifetime
- Optimiert durch Pooling

## Update-Reihenfolge (Game Loop)

```
1. InputSystem.update(delta)
   └─> Player Input Processing

2. Player.update(delta)
   ├─> State Machine Updates
   ├─> Dash Energy Drain/Regen
   ├─> Animation Updates
   └─> Invulnerability Timer

3. Enemy.update(delta) (für alle Enemies)

4. PhysicsSystem.update(delta, game_object)
   └─> Gravity + Velocity Application

5. CollisionSystem.update(delta)
   ├─> Boundary Collisions
   ├─> Player vs Blocks
   ├─> Player vs Enemies
   └─> Enemy vs Blocks

6. ParticleSystem.update(delta)

7. GameObject Movement Application
   └─> position += velocity * delta
```

## Rendering-Pipeline

```
1. Background Rendering
2. Blocks (mit Sprites)
3. Enemies
4. Player (mit Animation)
5. Particles
6. UI Layer:
   ├─> Lives Counter
   ├─> Level Counter
   └─> Dash Energy Bar
```

## Dateistruktur

```
StoneRush/
├── main.py                 # Entry Point
├── config.py               # Konstanten
├── enums.py                # Enumerations
├── sprite_manager.py       # Sprite Loading
├── particle_system.py      # Partikel-Effekte
├── animation_controller.py # Walk Animation
│
├── entities/
│   ├── game_object.py      # Base Class
│   ├── player.py           # Spieler
│   ├── enemy.py            # Gegner
│   └── block.py            # Blöcke
│
├── systems/
│   ├── input_system.py     # Input Handling
│   ├── physics_system.py   # Physik
│   └── collision_system.py # Kollisionen
│
├── screens/
│   └── game_screen.py      # Haupt-Screen
│
├── world/
│   └── level.py            # Level Management
│
├── assets/
│   ├── player_idle.png
│   ├── player_walk.png
│   ├── block_ground.png
│   ├── block_cracked.png
│   └── background.png
│
└── docs/
    ├── Architecture.md
    ├── Decision.md
    └── Progress.md
```

## Design Patterns

1. **Singleton**: SpriteManager
2. **State Pattern**: Player State Machine
3. **Observer Pattern**: Particle System
4. **Component Pattern**: GameObject + Systems
5. **Factory Pattern**: Level Generation

## Performance-Optimierungen

- Spatial Queries für Collision Detection
- Sprite Caching (SpriteManager)
- Particle Pooling
- Bounds Update nur nach Positionsänderung
- Debug-Output Reduktion (frame counter)

## Koordinatensystem

```
(0,0) ───────────────────> X
  │
  │    ┌──────────────┐
  │    │              │
  │    │   Spielfeld  │
  │    │              │
  │    └──────────────┘
  │
  ↓ Y (positive = nach unten)
```

- Y=0: Oben
- Positive Y: Nach unten (Fallrichtung)
- Positive X: Nach rechts
- Velocity.y > 0: Fallen
- Velocity.y < 0: Springen/Aufwärts
