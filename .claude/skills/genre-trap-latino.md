---
name: genre-trap-latino
description: Latin trap production reference — half-time drums, 808 glides, dark minor keys, hi-hat rolls. Use when the user asks for trap, Latin trap, dark beat, 808 beat, Bad Bunny / Anuel AA / Bryant Myers / Eladio Carrión / Myke Towers style productions.
---

# Latin Trap Production Reference

## Tempo

**130-150 BPM** written, **feels like 65-75 BPM** (half-time).
Common targets: 140 BPM (classic), 70 BPM (half-time written, same feel).

## Drum Patterns (1 bar = 4 beats at written tempo)

Half-time means the snare hits on beat 3 (not 2 and 4) — that's the genre's gravity.

### Kick (MIDI 36)

| Time | Velocity | Duration |
|------|----------|----------|
| 0.0  | 0.95     | 0.25     |
| 1.75 | 0.85     | 0.25     |
| 2.5  | 0.9      | 0.25     |

Variants: add ghost kick at 3.5 for trap-soul feel.

### Snare / Clap (MIDI 38 or 39) — half-time backbeat

| Time | Velocity | Duration |
|------|----------|----------|
| 2.0  | 0.9      | 0.5      |

That single hit on beat 3 (time=2.0) is the half-time snare. Layer with clap (MIDI 39) at same time, velocity 0.85, for thickness.

### Hi-Hat — 16th notes baseline (MIDI 42)

| Time | Velocity |
|------|----------|
| 0.0  | 0.55     |
| 0.25 | 0.45     |
| 0.5  | 0.6      |
| 0.75 | 0.45     |
| 1.0  | 0.55     |
| 1.25 | 0.45     |
| 1.5  | 0.6      |
| 1.75 | 0.45     |
| 2.0  | 0.55     |
| 2.25 | 0.45     |
| 2.5  | 0.6      |
| 2.75 | 0.45     |
| 3.0  | 0.55     |
| 3.25 | 0.45     |
| 3.5  | 0.6      |
| 3.75 | 0.45     |

Duration 0.125 for all hats.

### Hi-Hat Roll (signature trap element)

Triplet 16ths on beat 4 (time 3.0 onward):
| Time   | Velocity | Duration |
|--------|----------|----------|
| 3.0    | 0.5      | 0.0833   |
| 3.0833 | 0.55     | 0.0833   |
| 3.1667 | 0.6      | 0.0833   |
| 3.25   | 0.65     | 0.0833   |
| 3.3333 | 0.7      | 0.0833   |
| 3.4167 | 0.75     | 0.0833   |
| 3.5    | 0.8      | 0.0833   |
| 3.5833 | 0.85     | 0.0833   |
| 3.6667 | 0.9      | 0.0833   |
| 3.75   | 0.9      | 0.25     |

Or 32nd-note roll: 16 hits across beat 4, ascending velocity 0.4 → 0.95.

## 808 Bass — the engine of trap

MIDI range 24-36 (very low). Always sub. Use slides between notes.

For a 1-bar i (Am, root A1 = MIDI 33) loop:
| Time | MIDI | Duration | Velocity | Notes |
|------|------|----------|----------|-------|
| 0.0  | 33   | 1.75     | 0.95     | Hold  |
| 1.75 | 33   | 0.5      | 0.85     | Stab  |
| 2.5  | 33   | 1.5      | 0.9      | Hold  |

Melodic 808 (with glides over 2 bars, key A minor):
| Time | MIDI | Duration | Velocity |
|------|------|----------|----------|
| 0.0  | 33   | 1.5      | 0.95     |
| 1.5  | 36   | 0.5      | 0.85     |
| 2.0  | 33   | 1.5      | 0.9      |
| 3.5  | 31   | 0.5      | 0.8      |
| 4.0  | 29   | 2.0      | 0.95     |
| 6.0  | 33   | 2.0      | 0.9      |

For glides in FL: enable `slide` flag on the second note of a connected pair.

## Chord Progressions / Loops

Trap often uses 1-2 chord vamps or just a melodic loop with no full chords. When chords are present:

### i - VI (Am - F) — most common

| Bar | Chord | MIDI Notes (octave 4) |
|-----|-------|-----------------------|
| 1   | Am    | 57, 60, 64            |
| 2   | F     | 53, 57, 60            |

### i - iv (F#m - Bm) — Bad Bunny dark vibe (key F#m)

| Bar | Chord | MIDI Notes  |
|-----|-------|-------------|
| 1   | F#m   | 54, 57, 61  |
| 2   | Bm    | 59, 62, 66  |

### i - VII - VI - V (Am - G - F - E) — descending Andalusian, classic trap-soul

| Bar | Chord | MIDI Notes  |
|-----|-------|-------------|
| 1   | Am    | 57, 60, 64  |
| 2   | G     | 55, 59, 62  |
| 3   | F     | 53, 57, 60  |
| 4   | E     | 52, 56, 59  |

### Single sustained pad

Just a held minor chord (e.g. F#m: 54, 57, 61) for 4 bars, dark and atmospheric. Duration 16.0.

## Common Keys

F#m, Cm, Gm, Bbm, Em, Am. Dark minor, often with phrygian color (b2 leading tones).

## Scales

All from A4 (MIDI 69):
| Scale              | MIDI Notes                |
|--------------------|---------------------------|
| A natural minor    | 69, 71, 72, 74, 76, 77, 79|
| A harmonic minor   | 69, 71, 72, 74, 76, 77, 80|
| A phrygian         | 69, 70, 72, 74, 76, 77, 79|
| A phrygian dominant| 69, 70, 73, 74, 76, 77, 79|
| A minor pentatonic | 69, 72, 74, 76, 79         |

Phrygian dominant (Spanish gypsy scale) is the secret sauce for "dark Latin" melodies.

## Melodic Elements

Typical trap leads (octave 5-6, MIDI 72-95):
- Plucked synth (Serum / Sylenth pluck preset)
- Music box / glockenspiel
- Bell pluck
- Detuned saw lead
- Vocal chops (informational)
- Dark choir pad

Melodies are sparse — 4 to 8 notes per 2 bars, with rests. Less is more.

## Song Structure (shorter than reggaeton)

| Section    | Bars | Elements |
|------------|------|----------|
| Intro      | 4    | Melody only, no drums |
| Verse 1    | 16   | Drums + 808 + sparse melody |
| Hook/Chorus| 8    | Full energy, vocal-driven |
| Verse 2    | 16   | Variation |
| Hook       | 8    | Repeat |
| Outro      | 4    | Strip back |

Total ~2:30-3:00.

## Velocity Guide

| Element        | Range       |
|----------------|-------------|
| Kick           | 0.85-0.95   |
| Snare/clap     | 0.85-0.95   |
| Hi-hats baseline | 0.4-0.6   |
| Hi-hat rolls   | 0.4 → 0.95 ascending |
| 808 bass       | 0.85-0.95   |
| Melody         | 0.7-0.85    |
| Pads           | 0.5-0.65    |

## Quick Start Recipe

1. Set BPM to 140.
2. Send half-time drums (kick + snare on beat 3 + 16th hats) — 1 bar.
3. Add 808 on Am root with one slide note — 2 bars, loop.
4. Add dark plucked melody using A phrygian dominant — 2 bars.
5. Add hi-hat roll on every 4th bar.
6. Layer atmospheric pad (Am chord, sustained) underneath.

## When to WebSearch

- User names a specific producer/beatmaker not common knowledge (e.g. "Tainy", "Mvsis", "Subelo NEO style") → search current production techniques.
- User asks about plugin presets ("how does Bad Bunny get that 808?") → search "<artist> 808 settings tutorial".
- User asks about tempos/keys of a specific track → search "<track name> BPM key".
