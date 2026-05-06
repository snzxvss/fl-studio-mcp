---
name: genre-champeta
description: Champeta production reference — Colombian Caribbean genre with African (soukous/makossa) DNA. Bright syncopated guitar (palanca/picao), heavy congas, walking bass. Use when the user asks for champeta, picó, costa caribe, champeta urbana, or Colombian Caribbean coast (Cartagena/Barranquilla) styles (Mr Black, Kevin Florez, Charles King, Young F).
---

# Champeta Production Reference

## Background (load this context before composing)

Champeta originated on Colombia's Caribbean coast (Cartagena, Barranquilla, San Basilio de Palenque) from African records — soukous (Congo), makossa (Cameroon), highlife (Ghana, Nigeria) — played on giant sound systems called **picós**. The genre split into two streams:

- **Champeta criolla / africana** (1980s-2000s): live band feel, prominent African guitar lines, Afro-Colombian percussion.
- **Champeta urbana** (2010s-present): merged with reggaeton/dembow, electronic drums, more polished production. Kevin Florez, Mr Black, Twister el Rey, Young F.

Knowing the user's target stream matters — ask if unclear.

## Tempo

- Champeta criolla: **95-110 BPM**
- Champeta urbana: **100-115 BPM** (overlap with reggaeton territory)

## Drum Patterns (1 bar = 4 beats)

### Champeta criolla — live percussion feel

Kick (MIDI 36): on beats 1 and 3.
| Time | Velocity |
|------|----------|
| 0.0  | 0.95     |
| 2.0  | 0.95     |

Snare (MIDI 38) — backbeat:
| Time | Velocity |
|------|----------|
| 1.0  | 0.85     |
| 3.0  | 0.85     |

Conga / Tumbadora (MIDI 63 = high conga, 64 = low conga) — 16th note tumbao:
| Time | MIDI | Velocity | Duration |
|------|------|----------|----------|
| 0.0  | 64   | 0.5      | 0.125    |
| 0.25 | 64   | 0.45     | 0.125    |
| 0.5  | 63   | 0.7      | 0.125    |
| 0.75 | 63   | 0.65     | 0.125    |
| 1.0  | 64   | 0.5      | 0.125    |
| 1.25 | 64   | 0.45     | 0.125    |
| 1.5  | 63   | 0.75     | 0.125    |
| 1.75 | 63   | 0.7      | 0.125    |
| 2.0  | 64   | 0.5      | 0.125    |
| 2.25 | 64   | 0.45     | 0.125    |
| 2.5  | 63   | 0.7      | 0.125    |
| 2.75 | 63   | 0.65     | 0.125    |
| 3.0  | 64   | 0.5      | 0.125    |
| 3.25 | 64   | 0.45     | 0.125    |
| 3.5  | 63   | 0.75     | 0.125    |
| 3.75 | 63   | 0.7      | 0.125    |

Cowbell (MIDI 56) — son clave (3-2):
| Time | Velocity |
|------|----------|
| 0.0  | 0.7      |
| 0.75 | 0.7      |
| 1.5  | 0.7      |
| 2.0  | 0.7      |
| 3.0  | 0.7      |

### Champeta urbana — hybrid with dembow

Use the reggaeton dembow drum kit (see `genre-reggaeton`) but layer the conga tumbao above and add a faster cowbell pattern.

## Distinctive Guitar — Palanca / Picao

This is the genre's signature. Bright, clean electric guitar arpeggio in syncopated 8th/16th notes.

### Pattern A — major key (C major), 2 bars

Notes are individual (not chords), MIDI octave 4-5:
| Time | MIDI | Note | Duration | Velocity |
|------|------|------|----------|----------|
| 0.0  | 64   | E4   | 0.25     | 0.75     |
| 0.5  | 67   | G4   | 0.25     | 0.7      |
| 0.75 | 72   | C5   | 0.25     | 0.8      |
| 1.0  | 67   | G4   | 0.25     | 0.7      |
| 1.5  | 64   | E4   | 0.25     | 0.7      |
| 2.0  | 65   | F4   | 0.25     | 0.75     |
| 2.5  | 69   | A4   | 0.25     | 0.7      |
| 2.75 | 72   | C5   | 0.25     | 0.8      |
| 3.0  | 69   | A4   | 0.25     | 0.7      |
| 3.5  | 65   | F4   | 0.25     | 0.7      |

Repeat over each chord, transposing to fit. The off-beat 0.75 / 2.75 hits give the soukous feel.

### Pattern B — minor key (Am), syncopated

| Time | MIDI | Note | Duration | Velocity |
|------|------|------|----------|----------|
| 0.0  | 60   | C5   | 0.25     | 0.75     |
| 0.5  | 64   | E5   | 0.25     | 0.7      |
| 0.75 | 69   | A5   | 0.25     | 0.8      |
| 1.5  | 67   | G5   | 0.25     | 0.7      |
| 2.0  | 65   | F5   | 0.25     | 0.75     |
| 2.5  | 69   | A5   | 0.25     | 0.7      |
| 2.75 | 72   | C6   | 0.25     | 0.8      |
| 3.5  | 67   | G5   | 0.25     | 0.7      |

## Bass — walking, follows guitar

Champeta bass is **melodic**, not just root notes. Walking patterns mirror the guitar.

For C major (root C2 = MIDI 36):
| Time | MIDI | Note | Duration | Velocity |
|------|------|------|----------|----------|
| 0.0  | 36   | C2   | 0.5      | 0.9      |
| 1.0  | 43   | G2   | 0.5      | 0.85     |
| 2.0  | 41   | F2   | 0.5      | 0.85     |
| 3.0  | 43   | G2   | 0.5      | 0.85     |

For Am: 45 (A2), 52 (E3), 50 (D3), 48 (C3) walking on beats 1, 1.5, 2.5, 3.5.

## Chord Progressions

Champeta favors **major keys** more than reggaeton/trap. Each chord = 1 bar. Velocity 0.6.

### I - V - vi - IV (C major) — pop champeta urbana

| Bar | Chord | MIDI Notes  |
|-----|-------|-------------|
| 1   | C     | 60, 64, 67  |
| 2   | G     | 55, 59, 62  |
| 3   | Am    | 57, 60, 64  |
| 4   | F     | 53, 57, 60  |

### I - IV - V (C - F - G) — classic criolla

| Bar | Chord | MIDI Notes  |
|-----|-------|-------------|
| 1   | C     | 60, 64, 67  |
| 2   | F     | 53, 57, 60  |
| 3   | G     | 55, 59, 62  |
| 4   | C     | 60, 64, 67  |

### ii - V - I (Dm - G - C)

For a more sophisticated soukous feel.

### Modal vamps (criolla africana)

Single major chord with mixolydian (b7) flavor — e.g. C major with Bb in melodies. 8-bar vamp.

## Common Keys

C, G, D, A, F (guitar-friendly major keys). Minor: Am, Em.

## Scales

All from C4 (MIDI 60):
| Scale              | MIDI Notes                |
|--------------------|---------------------------|
| C major (Ionian)   | 60, 62, 64, 65, 67, 69, 71|
| C Mixolydian       | 60, 62, 64, 65, 67, 69, 70|
| C major pentatonic | 60, 62, 64, 67, 69        |
| A natural minor    | 69, 71, 72, 74, 76, 77, 79|
| A Dorian           | 69, 71, 72, 74, 76, 78, 79|

Mixolydian and Dorian carry the African modal flavor.

## Song Structure

| Section      | Bars | Notes |
|--------------|------|-------|
| Intro        | 4-8  | Picó FX, sample shouts, guitar pickup |
| Verse 1      | 8-16 | Beat + bass + guitar palanca |
| Pre-chorus   | 4    | Build, percussion fill |
| Chorus       | 8    | Full energy, lead guitar / synth lead |
| Verse 2      | 8-16 | Variation |
| Sebadeo / break | 4-8 | Percussion-only break, signature MC shouts |
| Final chorus | 8-16 | Full ensemble |
| Outro        | 4    | Filtered fade or sound-system FX |

The "sebadeo" (percussion break) is iconic — strip everything except congas/cowbell for 4-8 bars.

## When to WebSearch

Champeta has limited English documentation — search aggressively when uncertain:
- Specific artist style: `"<artist>" champeta production technique`
- Sub-style: `champeta urbana 2024 BPM key`
- Sound design: `champeta lead guitar tone presets`
- Recent picó culture: `picó cartagena 2024 hits`

Reliable sources: Spanish-language music blogs (radio caracol, semana), YouTube tutorials in Spanish, Genius lyrics for production credits.

## Quick Start Recipe

1. Set BPM to 105.
2. Send champeta criolla drums (kick on 1 & 3, snare backbeat, conga tumbao, cowbell clave).
3. Add `I - V - vi - IV` progression in C major as 4-bar pad (low velocity 0.5).
4. Add walking bass (C-G-F-G) following root motion.
5. Add palanca guitar Pattern A — repeat 4x over the progression.
6. After 8 bars, drop a "sebadeo" break: only congas + cowbell for 4 bars.
7. Bring everything back for the chorus.
