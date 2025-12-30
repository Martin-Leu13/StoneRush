# StoneRush - Design Decisions

## Technologie-Entscheidungen

### Warum Pygame statt LibGDX?

**Entscheidung**: Port von Java/LibGDX zu Python/Pygame

**Begründung**:
- Python ist einfacher zu lernen und zu lesen
- Pygame hat eine aktive Community
- Schnellere Iteration und Entwicklung
- Bessere Integration mit modernen Tools (PIL, etc.)

**Trade-offs**:
- ✅ Einfacherer Code
- ✅ Schnellere Prototyping
- ❌ Langsamere Performance als Java
- ❌ Weniger optimiert für große Spiele

---

### Warum Y=0 oben (Pygame Standard)?

**Entscheidung**: Pygame-Standard Koordinatensystem beibehalten

**Begründung**:
- Pygame arbeitet nativ mit Y=0 oben
- Weniger Konvertierungs-Overhead
- Einfacher zu debuggen (matches screen coordinates)

**Implementation**:
- Gravity: +800 (nach unten)
- Jump Velocity: -400 (nach oben)
- Collision Detection angepasst

---

## Architektur-Entscheidungen

### Warum ECS-ähnliche Architektur?

**Entscheidung**: System-basierter Ansatz statt OOP-Only

**Begründung**:
- Klare Trennung von Concerns
- InputSystem, PhysicsSystem, CollisionSystem
- Einfacher zu testen
- Bessere Wiederverwendbarkeit

**Alternative**: Rein OOP (alles in GameObject)
- ❌ Schwieriger zu warten
- ❌ Code-Duplikation
- ❌ Tight Coupling

---

### Warum State Machine für Player?

**Entscheidung**: Explizite PlayerState Enum

```python
class PlayerState(Enum):
    IDLE = 0
    WALKING = 1
    JUMPING = 2
    FALLING = 3
    RAMMING = 4
```

**Begründung**:
- Verhindert illegale State-Kombinationen
- Einfaches Debugging (aktueller State sichtbar)
- Klare State-Transitions

**Alternative**: Boolean Flags
```python
is_jumping = True
is_walking = False
is_ramming = True  # CONFLICT!
```
- ❌ Kann widersprüchlich werden
- ❌ Schwerer zu debuggen

---

### Warum AABB Collision Detection?

**Entscheidung**: Axis-Aligned Bounding Box mit Minimum Overlap

**Begründung**:
- Einfach zu implementieren
- Performant (keine Rotation-Checks)
- Ausreichend für Platformer
- Gut verständlich

**Alternative**: Pixel-Perfect Collision
- ❌ Zu langsam
- ❌ Unnötig präzise für dieses Spiel

**Alternative**: Circle Collision
- ❌ Passt nicht zu rechteckigen Sprites

---

## Gameplay-Entscheidungen

### Dash-Energie System

**Entscheidung**: Kontinuierlicher Drain statt One-Shot Cost

**Begründung**:
- Mehr Skill-basiert (Timing wichtig)
- Verhindert Spam
- Belohnt präzises Spielen

**Parameter**:
```python
max_dash_energy = 100.0
dash_drain_rate = 50.0  # 2 Sekunden max Dash
dash_regen_rate = 33.33 # 3 Sekunden bis voll
```

**Alternative**: Fixed Cost pro Dash
- ❌ Weniger interessant
- ❌ Binäres System (kann/kann nicht)

---

### Dash stoppt bei Wand/Cracked Block

**Entscheidung**: Dash endet sofort + Block zum Neustart

**Begründung**:
- Verhindert "Auto-Dash" durch gedrückte Taste
- Spieler muss bewusst neu dashen
- Mehr Kontrolle

**Implementation**:
```python
ram_blocked = False  # Flag

# Bei Kollision:
player.stop_ram()
player.ram_blocked = True

# Bei Shift-Release:
player.ram_blocked = False
```

**Alternative**: Dash geht automatisch weiter
- ❌ Unkontrollierbar
- ❌ Weniger präzise

---

### Respawn statt Game Over

**Entscheidung**: Bei Tod → Level neu laden (gleicher Level)

**Begründung**:
- Weniger frustrierend
- Ermutigt Experimentation
- Moderne Game-Design Practice

**Alternative**: Game Over → Menu
- ❌ Zu hart
- ❌ Bricht Flow

---

### Enemy Edge Detection

**Entscheidung**: Enemies drehen an Platform-Rändern um

**Begründung**:
- Verhindert Enemies die ins Nichts fallen
- Macht Levels vorhersagbarer
- Besseres Spielgefühl

**Implementation**:
```python
# Check one body width ahead
check_x = pos.x + width if moving_right else pos.x - width
check_y = pos.y + height + 5  # Below feet

if not has_ground_ahead:
    velocity.x = -velocity.x  # Turn around
```

---

### Invisible Boundary Walls

**Entscheidung**: Wände links, rechts, oben (unten = Tod)

**Begründung**:
- Verhindert aus-der-Welt-Bugs
- Klare Level-Grenzen
- Nur unten ist Abgrund (Gameplay-Mechanik)

**Implementation**:
```python
if pos.x < 0:
    pos.x = 0
    vel.x = 0

if pos.x + width > level_width:
    pos.x = level_width - width
    vel.x = 0
```

---

## Rendering-Entscheidungen

### Sprite-basiertes Rendering

**Entscheidung**: PNG Sprites statt farbige Rechtecke

**Begründung**:
- Besseres visuelles Feedback
- Professioneller Look
- Einfacher zu unterscheiden (Treppen vs Risse)

**Sprite Processing**:
```python
def remove_cyan_background(img):
    # Entfernt hellblauen Hintergrund
    # Macht transparent
```

**Trade-offs**:
- ✅ Schönere Grafik
- ❌ Mehr Arbeit (Sprite-Erstellung)
- ❌ Größere Assets

---

### Class-Level Sprite Loading (Blocks)

**Entscheidung**: Sprites in Block-Klasse, nicht pro Instanz

**Begründung**:
- Memory-Effizient (ein Sprite für alle Blöcke)
- Schnelleres Loading
- Pygame best practice

**Implementation**:
```python
class Block:
    _sprite_ground = None  # Class-level
    _sprite_cracked = None

    @classmethod
    def _load_sprites(cls):
        # Load once for all instances
```

**Alternative**: Pro-Instanz Loading
- ❌ 1000 Blöcke = 1000x gleiche Sprites im RAM

---

### Dash Energy Bar (Orange)

**Entscheidung**: Orange statt Blau/Grün

**Begründung**:
- Unterscheidet sich von Health (Rot)
- Signalisiert "Power/Energy"
- Gute Sichtbarkeit auf blauem Hintergrund

**Alternative Farben erwogen**:
- Blau: ❌ Zu ähnlich zum Himmel
- Gelb: ❌ Zu hell, schwer zu sehen
- Grün: ❌ Signalisiert "Health" nicht "Energy"

---

## Performance-Entscheidungen

### Spatial Queries für Collision Detection

**Entscheidung**: Nur Blöcke in Nähe prüfen

**Implementation**:
```python
search_area = pygame.Rect(
    player.x - 32,
    player.y - 32,
    player.width + 64,
    player.height + 64
)
nearby_blocks = level.get_blocks_in_range(search_area)
```

**Begründung**:
- 100 Blöcke breit × 20 hoch = 2000 Blöcke
- Ohne Spatial Query: 2000 Checks pro Frame
- Mit Spatial Query: ~10-20 Checks pro Frame
- **200x schneller!**

---

### Bounds Update Strategie

**Entscheidung**: Update bounds sofort nach jeder Kollisionsauflösung

**Begründung**:
- Verhindert "stuck in ground" Bug
- Jede Collision Resolution sieht korrekte Bounds
- Minimal Performance-Impact

**Ursprünglicher Fehler**:
```python
for block in blocks:
    resolve_collision(player, block)  # Ändert position
    # bounds noch nicht updated!
    # Nächste collision sieht alte bounds → Bug!
```

**Fix**:
```python
for block in blocks:
    resolve_collision(player, block)
    player.update_bounds()  # Sofort updaten!
```

---

### Debug Output Management

**Entscheidung**: Frame-Counter für reduzierte Ausgabe

**Begründung**:
- 60 FPS = 60 Prints pro Sekunde
- Terminal wird unleserlich
- Nur wichtige State-Changes printen

**Implementation**:
```python
if old_state != new_state:
    print(f"State changed: {old_state} -> {new_state}")
```

---

## Zukünftige Entscheidungen zu treffen

### Audio System
- [ ] Hintergrundmusik (boss.wav, ovrworld.wav vorhanden)
- [ ] Sound Effects (Jump, Dash, Block-Destroy)

### Level Design
- [ ] Level Editor vs Procedural Generation
- [ ] Difficulty Curve Tuning

### UI/UX
- [ ] Pause Menu
- [ ] Settings Screen
- [ ] Keyboard Remapping

### Features
- [ ] Checkpoints in Levels
- [ ] Power-Ups
- [ ] Multiple Lives Display
- [ ] High Score System

---

## Lessons Learned

1. **Collision Detection ist schwierig**
   - AABB mit overlap war richtige Wahl
   - Bounds-Update Timing ist kritisch

2. **State Management ist wichtig**
   - `ram_blocked` Flag verhindert Edge Cases
   - Klare State Machine > Boolean Soup

3. **Debug-Ausgaben sind essentiell**
   - Sprite Loading Logs halfen enorm
   - State Changes sichtbar machen

4. **Performance früh beachten**
   - Spatial Queries von Anfang an
   - Sprite Caching standard

5. **Testing im echten Gameplay**
   - "Stuck in ground" nur bei hohem Fall sichtbar
   - "Dash restart" nur bei schneller Eingabe problematisch
