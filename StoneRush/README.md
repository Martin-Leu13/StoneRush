# StoneRush

Ein 2D Side-Scroller Platformer in Python/Pygame - portiert vom Java/LibGDX Original.

## Beschreibung

StoneRush ist ein Platformer-Spiel, in dem du einen Stein-Charakter steuerst, der springen und rammen kann, um durch Level zu navigieren, Hindernisse zu zerstören und Gegner zu besiegen.

## Features

- **Spieler-Charakter**: Grauer Stein mit Animation
- **Bewegung**: Links/Rechts bewegen mit 200 px/s
- **Springen**: Sprungkraft von 400 px/s
- **Ramm-Angriff**: 500 px/s Geschwindigkeit für 0,3 Sekunden
- **Leben-System**: 3 Herzen mit 1,5 Sekunden Unverwundbarkeit nach Schaden
- **Gegner**: 5 rote Quadrat-Gegner, die patrouillieren
- **Blöcke**:
  - Normale Blöcke (braun) - unzerstörbar
  - Gebrochene Blöcke (dunkelbraun) - zerstörbar durch Rammen
- **Ziel**: Grünes Rechteck mit Flagge am Ende des Levels
- **Kamera**: Smooth-Follow-Kamera mit Offset

## Installation

1. Stelle sicher, dass Python 3.7+ installiert ist
2. Installiere die Dependencies:
```bash
pip install -r requirements.txt
```

## Spiel starten

```bash
python main.py
```

## Steuerung

| Taste | Aktion |
|-------|--------|
| ← → | Links/Rechts bewegen |
| Leertaste | Springen (nur wenn auf dem Boden) |
| Shift | Ramm-Angriff (nur wenn auf dem Boden) |
| Escape | Spiel beenden |

## Spielmechanik

### Ziel
Erreiche das grüne Ziel am Ende des Levels!

### Rammen
- Drücke Shift, um einen Ramm-Angriff zu starten
- Während des Rammens kannst du:
  - Gebrochene Blöcke (dunkelbraun) zerstören
  - Gegner eliminieren
- Der Ramm-Angriff dauert 0,3 Sekunden

### Gegner
- Rote Quadrate mit Augen
- Patrouillieren 128 Pixel hin und her
- Berührung verursacht Schaden (außer beim Rammen)
- Können durch Ramm-Angriff zerstört werden

### Leben
- Du startest mit 3 Leben
- Nach Schaden bist du 1,5 Sekunden lang unverwundbar (Blink-Effekt)
- Game Over bei 0 Leben

## Level 1 Layout

- **Größe**: 100 Blöcke breit × 20 Blöcke hoch (3200 × 640 Pixel)
- **Boden**: 3 Reihen am unteren Rand
- **Plattformen**: Mehrere Plattformen in verschiedenen Höhen
- **Hindernisse**: Gebrochene Blöcke zum Durchrammen
- **Gegner**: 5 Gegner verteilt im Level
- **Ziel**: Bei Position (3100, 96)

## Projektstruktur

```
StoneRush/
├── main.py                      # Haupteinstiegspunkt
├── requirements.txt             # Python-Dependencies
├── config.py                    # Konstanten & Einstellungen
├── enums.py                     # Enumerationen
├── entities/                    # Spielobjekte
│   ├── game_object.py          # Basisklasse
│   ├── player.py               # Spieler
│   ├── enemy.py                # Gegner
│   └── block.py                # Blöcke
├── systems/                     # Spielsysteme
│   ├── physics_system.py       # Physik
│   ├── collision_system.py     # Kollisionen
│   └── input_system.py         # Eingabe
├── world/                       # Level-Verwaltung
│   ├── level_data.py           # Level-Daten
│   ├── level.py                # Level-Logik
│   └── camera.py               # Kamera
└── screens/                     # Bildschirm-Management
    ├── base_screen.py          # Basisklasse
    └── game_screen.py          # Spiel-Screen
```

## Technische Details

- **Auflösung**: 800 × 600 Pixel
- **FPS**: 60 FPS
- **Schwerkraft**: -800 px/s²
- **Terminal Velocity**: -1000 px/s
- **Kollisionserkennung**: AABB (Axis-Aligned Bounding Box)
- **Rendering**: Pygame Shape Drawing (keine Sprites)

## Portierung

Dieses Spiel wurde vom Java/LibGDX Original portiert:
- Original: Java + LibGDX Framework
- Portiert nach: Python + Pygame
- Identische Spielmechanik und Level-Design
- Gleiche Physik-Werte

## Credits

Portiert von Java/LibGDX nach Python/Pygame
