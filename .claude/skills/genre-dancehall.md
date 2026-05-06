---
name: genre-dancehall
description: Jamaican dancehall production reference — riddims, one-drop and steppers patterns, minor-key vamps, syncopated bass. Use when the user asks for dancehall, riddim, Jamaican beats, or Patois/toasting style productions (Vybz Kartel, Sean Paul, Popcaan, Shenseea).
---

# Dancehall Production Reference

## Tempo

**90-110 BPM** (classic 95-100). Modern dancehall pop pushes 105-110 BPM.
Origin of the reggaeton "dembow" rhythm (Shabba Ranks - "Dem Bow", 1990).

## Drum Patterns (1 bar = 4 beats)

### Pattern A — One-Drop (classic, sparse)

Kick (MIDI 36):
| Time | Velocity | Duration |
|------|----------|----------|
| 2.0  | 0.95     | 0.25     |

Snare/Rim (MIDI 38 or 37):
| Time | Velocity | Duration |
|------|----------|----------|
| 1.0  | 0.8      | 0.25     |
| 3.0  | 0.8      | 0.25     |

### Pattern B — Steppers (modern dancehall, four-on-floor)

Kick (MIDI 36):
| Time | Velocity | Duration |
|------|----------|----------|
| 0.0  | 0.95     | 0.25     |
| 1.0  | 0.85     | 0.25     |
| 2.0  | 0.95     | 0.25     |
| 3.0  | 0.85     | 0.25     |

Clap/Snare (MIDI 39 / 38):
| Time | Velocity | Duration |
|------|----------|----------|
| 1.0  | 0.85     | 0.25     |
| 3.0  | 0.85     | 0.25     |

### Pattern C — Syncopated dancehall (Diwali / Sleng Teng feel)

Kick:
| Time | Velocity |
|------|----------|
| 0.0  | 0.95     |
| 1.5  | 0.85     |
| 2.0  | 0.9      |
| 3.5  | 0.8      |

Snare/Rim on 1.0 and 3.0 (velocity 0.8, duration 0.25).

### Hi-Hats — Skanking 8ths (MIDI 42)

| Time | Velocity |
|------|----------|
| 0.5  | 0.65     |
| 1.5  | 0.7      |
| 2.5  | 0.65     |
| 3.5  | 0.7      |

Open hat (MIDI 46) on 1.0 and 3.0 for "skank" emphasis.

### Timbale / Tom Fill (MIDI 41, 43, 45) — 4-bar fills

End-of-phrase tumble: 16th notes on beat 4, ascending toms.

## Riddim References (study these for authenticity)

| Riddim       | Year | Key       | Style                     |
|--------------|------|-----------|---------------------------|
| Sleng Teng   | 1985 | A minor   | First digital riddim      |
| Dem Bow      | 1990 | A minor   | Origin of reggaeton groove|
| Diwali       | 2002 | A minor   | Steel drum / clap pattern |
| Filthy       | 2009 | F# minor  | Hard-hitting modern       |
| Unfinished Business | 2014 | C minor | Modern bashment      |

If user requests a specific riddim not listed, WebSearch: `"<riddim name>" dancehall riddim BPM key drum pattern`.

## Chord Progressions

Each chord = 1 bar. Velocity 0.65. Duration 3.5.
Dancehall is heavily minor-key and often uses only 1-2 chords looped.

### Single-chord vamp (very common)

| Bar | Chord | MIDI Notes  |
|-----|-------|-------------|
| 1-4 | Am    | 57, 60, 64  |

### i - VII (Am - G)

| Bar | Chord | MIDI Notes  |
|-----|-------|-------------|
| 1   | Am    | 57, 60, 64  |
| 2   | G     | 55, 59, 62  |
| 3   | Am    | 57, 60, 64  |
| 4   | G     | 55, 59, 62  |

### i - iv - VII - i (Am - Dm - G - Am)

| Bar | Chord | MIDI Notes  |
|-----|-------|-------------|
| 1   | Am    | 57, 60, 64  |
| 2   | Dm    | 62, 65, 69  |
| 3   | G     | 55, 59, 62  |
| 4   | Am    | 57, 60, 64  |

### Major-key dancehall pop (Sean Paul-style)

I - V - vi - IV (C major):
| Bar | Chord | MIDI Notes  |
|-----|-------|-------------|
| 1   | C     | 60, 64, 67  |
| 2   | G     | 55, 59, 62  |
| 3   | Am    | 57, 60, 64  |
| 4   | F     | 53, 57, 60  |

## Bass

Sub-bass, syncopated, often follows the kick rhythm rather than the chord changes.

For Am one-bar (root A2 = MIDI 45):
| Time | MIDI | Duration | Velocity |
|------|------|----------|----------|
| 0.0  | 45   | 0.5      | 0.95     |
| 1.5  | 45   | 0.5      | 0.85     |
| 2.0  | 45   | 0.5      | 0.95     |
| 3.5  | 45   | 0.5      | 0.85     |

Walking variant — root, fifth, octave, fifth (A-E-A-E).

## Scales for Melodies / Toasting Lines

All from A4 (MIDI 69):
| Scale            | MIDI Notes                  |
|------------------|------------------------------|
| A natural minor  | 69, 71, 72, 74, 76, 77, 79  |
| A Dorian         | 69, 71, 72, 74, 76, 78, 79  |
| A minor pentatonic | 69, 72, 74, 76, 79        |
| A blues          | 69, 72, 74, 75, 76, 79      |

Melodic motifs: short repeating 2-bar hooks, often steel drum, marimba, or pluck synth.

## Song Structure

| Section      | Bars | Notes |
|--------------|------|-------|
| Intro        | 4-8  | Riddim only, vocal sample |
| Verse 1      | 8-16 | Beat + bass, sparse melody |
| Pre/Build    | 4    | Drum fill, hat roll |
| Chorus       | 8    | Full riddim, hook melody |
| Verse 2      | 8-16 | Variation |
| Bridge/Break | 4-8  | Drop drums, vocal-led |
| Chorus       | 8    | Final |
| Outro        | 4    | Filtered fadeout |

## Quick Start Recipe

1. Set BPM to 100.
2. Send Pattern B drums (steppers) — 1 bar, loop 4x.
3. Add `i - VII` chord vamp (Am - G) — 4 bars.
4. Add syncopated bass on Am root.
5. Add steel-drum or marimba melody using A minor pentatonic.
6. Layer rim shot ghost notes for swing.
