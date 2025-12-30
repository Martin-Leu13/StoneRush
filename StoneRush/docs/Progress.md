# StoneRush - Development Progress

## 2025-12-30 - Session 1: Bug Fixes & Block Sprites

### Session Ziele
Behebung von 4 kritischen Bugs und Integration neuer Block-Sprites aus Screenshots.

### Probleme beim Start
1. **Spieler steckt im Boden fest** - Bei Fall aus großer Höhe
2. **Spieler klebt an Wand beim Dashen** - Dash stoppt nicht richtig
3. **Block-Texturen nicht geladen** - Neue Sprites aus import-Ordner nicht verwendet
4. **Dash stoppt nicht bei rissigem Block** - Dash geht automatisch weiter

---

### 1. Block-Sprites Integration

**Problem**: Die neuen Block-Sprites aus dem `import/` Ordner wurden nicht geladen.

**Ursprüngliche Sprites**: Graue Rechtecke
**Ziel**: Texturen mit Treppen-Muster (normal) und Risse (cracked)

**Fehler bei der Umsetzung**:
- Erster Versuch: Falsche Screenshots verwendet (143005.png, 143430.png)
- Diese zeigten zu große, undeutliche Blöcke
- Zweiter Versuch: **Korrekte Screenshots** verwendet (161631.png, 161708.png)

**Lösung**:
```python
# Screenshot Verarbeitung
1. Load: Screenshot 2025-12-30 161631.png (Treppen-Block)
2. Load: Screenshot 2025-12-30 161708.png (Rissiger Block)
3. Remove cyan background (RGB 140-165, 200-235, 220-245)
4. Crop to bounding box
5. Resize to 32x32 with LANCZOS
6. Save as block_ground.png, block_cracked.png
```

**Code-Änderungen**:
- `sprite_manager.py`: Block-Sprites laden mit Debug-Ausgaben
- `entities/block.py`: Class-level Sprite Loading
- Erstellt: `extract_blocks.py` für Sprite-Verarbeitung

**Dateien**:
- ✅ `assets/block_ground.png` (32×32, Treppen-Muster)
- ✅ `assets/block_cracked.png` (32×32, Risse)

**Debug-Ausgabe**:
```
[SPRITE MANAGER] Lade Block-Sprites...
[OK] block_ground.png geladen: (32, 32)
[OK] block_cracked.png geladen: (32, 32)
[BLOCK] Ground-Sprite gefunden, skaliere auf (32, 32)
[BLOCK] Cracked-Sprite gefunden, skaliere auf (32, 32)
```

---

### 2. Spieler steckt im Boden - BEHOBEN

**Problem**: Bei Fall aus großer Höhe bleibt der Spieler teilweise im Boden stecken.

**Root Cause**:
- Bounds wurden nicht sofort nach Kollisionsauflösung aktualisiert
- Mehrere Kollisionen pro Frame verwendeten veraltete Bounds
- Position wurde geändert, aber bounds.y blieb alt

**Lösung**:
```python
# collision_system.py:127, 133, 138, 151
if min_overlap == overlap_top and vel.y >= 0:
    pos.y = b_bounds.y - p_bounds.height
    vel.y = 0
    player.set_grounded(True)
    player.update_bounds()  # ✅ SOFORT updaten!
```

**Vorher**:
```python
for block in blocks:
    resolve_collision(player, block)  # Ändert position
    # bounds noch veraltet!
# update_bounds() erst am Ende
```

**Nachher**:
```python
for block in blocks:
    resolve_collision(player, block)
    player.update_bounds()  # Sofort nach jeder Resolution
```

**Getestet**: Falle von 10+ Blöcken Höhe → Keine Stuck-Bugs mehr

---

### 3. Dash stoppt bei Wand - BEHOBEN

**Problem**: Beim Dashen in eine Wand bleibt der Spieler "kleben" oder der Dash startet sofort neu.

**Root Cause**:
- `InputSystem` ruft jedes Frame `start_ram()` auf wenn Shift gedrückt
- Nach `stop_ram()` (bei Wand-Kollision) startet Dash sofort neu
- Keine Sperre gegen sofortigen Neustart

**Lösung**: `ram_blocked` Flag eingeführt

```python
# player.py:67
self.ram_blocked = False

# player.py:201 - start_ram()
if self.state != PlayerState.RAMMING and self.dash_energy > 0 and not self.ram_blocked:
    self.state = PlayerState.RAMMING
    # ...

# player.py:230 - stop_ram() (called by collision)
def stop_ram(self):
    self._stop_ramming()
    self.ram_blocked = True  # ✅ Blockiere Neustart

# player.py:219 - stop_ram_if_active() (called by input)
def stop_ram_if_active(self):
    if self.state == PlayerState.RAMMING:
        self._stop_ramming()
    self.ram_blocked = False  # ✅ Entsperre bei Shift-Release
```

**Flow**:
1. Spieler dasht in Wand
2. Kollision → `stop_ram()` → `ram_blocked = True`
3. Input-System versucht `start_ram()` → blockiert durch Flag
4. Spieler lässt Shift los → `ram_blocked = False`
5. Spieler kann wieder neu dashen

**Getestet**: Dash in Wand → Stopp → Shift loslassen → Shift drücken → Neuer Dash ✅

---

### 4. Dash stoppt bei rissigem Block - BEHOBEN

**Problem**: Beim Rammen eines rissigen Blocks geht der Dash weiter statt zu stoppen.

**Gewünschtes Verhalten**: Dash soll sofort enden, Shift muss neu gedrückt werden.

**Lösung**:
```python
# collision_system.py:141-145
if player.is_ramming():
    if block.get_type() == BlockType.CRACKED:
        block.destroy()
    # Stop dash immediately when hitting any block while dashing
    player.stop_ram()  # ✅ Ruft stop_ram() + setzt ram_blocked
```

**Vorher**: Block wurde zerstört, Dash ging weiter
**Nachher**: Block wird zerstört, Dash endet, Shift muss neu gedrückt werden

---

### Code-Statistik

**Geänderte Dateien**:
1. `entities/player.py`
   - Zeilen geändert: ~15
   - Neu: `ram_blocked` Flag, `stop_ram()` Methode

2. `systems/collision_system.py`
   - Zeilen geändert: ~30
   - Fix: Bounds-Updates nach jeder Resolution
   - Fix: Dash-Stopp bei allen Block-Kollisionen

3. `sprite_manager.py`
   - Zeilen geändert: ~10
   - Neu: Block-Sprite Loading mit Debug

4. `entities/block.py`
   - Zeilen geändert: ~20
   - Neu: Class-level Sprite Loading mit Debug

5. `extract_blocks.py`
   - Neu erstellt: ~80 Zeilen
   - Sprite-Verarbeitung Automation

**Neue Dateien**:
- `docs/Architecture.md`
- `docs/Decision.md`
- `docs/Progress.md`
- `extract_blocks.py`

---

### Testing & Validation

**Manuelle Tests durchgeführt**:
- ✅ Fall aus großer Höhe (10+ Blöcke)
- ✅ Dash in Wand (links & rechts)
- ✅ Dash in rissigen Block
- ✅ Block-Sprites sichtbar
- ✅ Dash-Energy Bar funktioniert
- ✅ Respawn System
- ✅ Enemy Edge Detection
- ✅ Boundary Walls

**Debug-Ausgaben**:
```
[SPRITE MANAGER] Lade Block-Sprites...
[OK] block_ground.png geladen: (32, 32)
[OK] block_cracked.png geladen: (32, 32)
[BLOCK] Lade Block-Sprites vom SpriteManager...
[BLOCK] Ground-Sprite gefunden, skaliere auf (32, 32)
[BLOCK] Cracked-Sprite gefunden, skaliere auf (32, 32)
```

**Keine Crashes, keine Fehler**

---

### Lessons Learned

1. **Bounds-Update Timing ist kritisch**
   - Sofort nach Position-Änderung updaten
   - Nicht bis zum Ende warten

2. **Input-Blocking wichtig für Gameplay**
   - `ram_blocked` Flag verhindert ungewolltes Verhalten
   - Spieler braucht Kontrolle über Dash-Neustart

3. **Sprite-Verarbeitung braucht Iteration**
   - Erste Screenshots waren falsch
   - Debug-Ausgaben halfen schnell zu identifizieren
   - Vorschau-Bilder (128×128) gut zum Verifizieren

4. **Debug-Ausgaben sind Gold wert**
   - Sprite-Loading Logs zeigten sofort Erfolg
   - State-Change Logs helfen bei Debugging

---

### Nächste Session - Geplante Tasks

**Features**:
- [ ] Audio Integration (boss.wav, ovrworld.wav)
- [ ] Sound Effects (Jump, Dash, Destroy)
- [ ] Pause Menu
- [ ] Level Select Screen

**Bugs/Polish**:
- [ ] Enemy Sprite Animation
- [ ] Player Death Animation
- [ ] Block Destroy Animation/Particles
- [ ] Dash Cooldown Visual Feedback

**Optimierung**:
- [ ] Profiling durchführen
- [ ] FPS Counter implementieren
- [ ] Memory Usage optimieren

**Documentation**:
- [ ] README.md erstellen
- [ ] Controls dokumentieren
- [ ] Installation Guide

---

### Zeitaufwand

**Session-Dauer**: ~2-3 Stunden

**Aufschlüsselung**:
- Bug-Analyse: 30 min
- Block-Sprites (Fehler + Fix): 45 min
- Kollisions-Fixes: 30 min
- Dash-System Fixes: 20 min
- Testing: 15 min
- Documentation: 30 min

---

### Git Commit

```bash
# Alle Änderungen committed
git add .
git commit -m "Bug fixes: Ground collision, dash blocking, block sprites

- Fix: Player stuck in ground when falling from height
- Fix: Dash stops immediately at walls/cracked blocks
- Fix: Dash requires shift release before restarting
- Add: Block sprites from screenshots (stairs & cracks)
- Add: Debug output for sprite loading
- Add: Documentation (Architecture, Decision, Progress)

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Session Summary

**Status**: ✅ Alle 4 Bugs behoben, Block-Sprites integriert

**Ergebnis**: Spiel ist jetzt spielbar ohne kritische Bugs. Visuals deutlich verbessert durch echte Block-Texturen.

**Nächster Fokus**: Audio-Integration und UI/UX Verbesserungen
