---
name: genre-dembow
description: Dominican dembow production reference — fast aggressive percussion, "pow pow" stabs, minimal harmony, repetitive vocal-driven hooks. Use whenever the user says "dembow" (this is the default meaning — the Dominican genre), or names artists like El Alfa, Rochy RD, Tokischa, Yomel El Meloso, Bulin 47, Chimbala, Chael Producing, Nico Clinico.
---

# Dembow (Dominican) Production Reference

## Context

**"Dembow" = the Dominican Republic genre.** That's the default meaning — do not ask the user to clarify. Faster (115-130 BPM), aggressive, percussion-forward, often built on the "Pow Pow" sample. Exploded internationally with El Alfa.

The phrase **"dembow rhythm"** or **"dembow pattern"** (rhythm/pattern, not the bare word "dembow") refers to the older snare/kick groove inherited from Shabba Ranks' "Dem Bow" (1990) used inside reggaeton (`genre-reggaeton`, 85-100 BPM). Only switch to that meaning when the user explicitly says "dembow rhythm/pattern/groove" or is already working on a reggaeton track.

## Tempo

**115-130 BPM** (sweet spot 120-125). Some modern tracks push to 130-135.

## Drum Patterns (1 bar = 4 beats)

### Pattern A — Classic dembow dominicano

Kick (MIDI 36):
| Time | Velocity |
|------|----------|
| 0.0  | 0.95     |
| 0.75 | 0.85     |
| 2.0  | 0.95     |
| 2.75 | 0.85     |

Snare (MIDI 38) — tresillo with offbeat extension:
| Time | Velocity |
|------|----------|
| 0.5  | 0.85     |
| 1.0  | 0.8      |
| 1.5  | 0.85     |
| 2.5  | 0.85     |
| 3.0  | 0.8      |
| 3.5  | 0.85     |

Hi-hat (MIDI 42) — 16ths, all velocity 0.55, duration 0.125:
times 0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75.

Open hat (MIDI 46) on 0.5 and 2.5, velocity 0.6, duration 0.25.

### "Pow Pow" stab — the genre signature

Tuned percussion blast (synth or pitched drum sample). Usually MIDI 60-72 range. Fires on the offbeats:
| Time | MIDI | Velocity | Duration |
|------|------|----------|----------|
| 0.5  | 65   | 0.9      | 0.25     |
| 1.5  | 65   | 0.9      | 0.25     |
| 2.5  | 65   | 0.9      | 0.25     |
| 3.5  | 65   | 0.9      | 0.25     |

Variants: pitch up on beat 4 (MIDI 67 instead of 65) for tension; double-hit ("pow-pow") with MIDI 65 then 67 on time 3.5.

### Hi-Hat Roll Fills (every 4 bars)

32nd-note ramp on beat 4 (time 3.0 → 3.875), velocity 0.4 → 0.95. See `genre-reggaeton` table format.

## Bass — short, punchy 808 stabs

Less sustained than reggaeton. More like rapid repeated hits.

For Am (root A1 = MIDI 33):
| Time | MIDI | Duration | Velocity |
|------|------|----------|----------|
| 0.0  | 33   | 0.5      | 0.95     |
| 1.0  | 33   | 0.25     | 0.85     |
| 2.0  | 33   | 0.5      | 0.95     |
| 3.0  | 33   | 0.25     | 0.85     |
| 3.5  | 33   | 0.25     | 0.85     |

Some modern dembow uses a single sustained 808 instead — full bar at velocity 0.95.

## Chord Progressions / Harmony

Dembow is **harmonically minimal** — many tracks have NO chord layer at all, just bass + percussion + Pow Pow + vocal. When chords exist:

### Single-chord vamp (most common)

| Bar | Chord | MIDI Notes  |
|-----|-------|-------------|
| 1-4 | Am    | 57, 60, 64  |

Velocity 0.5, duration 16 (sustained).

### i - VI (Am - F)

| Bar | Chord | MIDI Notes  |
|-----|-------|-------------|
| 1-2 | Am    | 57, 60, 64  |
| 3-4 | F     | 53, 57, 60  |

### i - v (Am - Em) — darker

| Bar | Chord | MIDI Notes  |
|-----|-------|-------------|
| 1-2 | Am    | 57, 60, 64  |
| 3-4 | Em    | 52, 55, 59  |

## Common Keys

Am, Em, F#m, Dm. Almost always minor.

## Scales

All from A4 (MIDI 69):
| Scale              | MIDI Notes                |
|--------------------|---------------------------|
| A natural minor    | 69, 71, 72, 74, 76, 77, 79|
| A minor pentatonic | 69, 72, 74, 76, 79         |
| A phrygian         | 69, 70, 72, 74, 76, 77, 79|

Melodies are usually short 2-3 note motifs, not full melodic lines.

## Distinctive Production Elements

- **Pitched percussion as melody**: tuned cowbells, drum hits used as harmonic content.
- **Vocal stutters / chops**: rapid repetitions ("ra-ra-ra-ra"). Informational.
- **Sample chops**: short 1-bar samples looped aggressively.
- **Dale dale / shoutouts**: producer tags as percussion. Informational.
- **Aggressive transients**: heavy clipping, distortion on drums.
- **Filter sweeps**: opening/closing on the loop every 8 bars.

## Song Structure (short, repetitive)

| Section    | Bars | Notes |
|------------|------|-------|
| Intro      | 4    | Pow Pow + bass only |
| Verse 1    | 8    | Full beat + vocal |
| Hook       | 8    | Same beat, hook melody/chant |
| Verse 2    | 8    | Variation, often shorter |
| Hook       | 8    | Repeat |
| Outro      | 4    | Strip back to Pow Pow |

Total length ~2:00-2:30. Dembow tracks are intentionally short and repetitive.

## Velocity Guide

| Element        | Range       |
|----------------|-------------|
| Kick           | 0.85-0.95   |
| Snare          | 0.8-0.9     |
| Hi-hats        | 0.45-0.6    |
| Pow Pow stab   | 0.85-0.95   |
| Bass 808       | 0.85-0.95   |
| Pad/chord      | 0.4-0.55 (if used) |

## When to WebSearch

- Specific producer: `"Chael Producing" dembow drums` / `"Nico Clinico" dembow`
- Recent hits / current BPM trends: `dembow dominicano 2024 hits`
- Sample packs: `dembow Pow Pow sample pack`
- Sub-styles: `dembow tiraera vs dembow comercial`

## Quick Start Recipe

1. Set BPM to 122.
2. Send Pattern A drums (kick + snare + 16th hats).
3. Add Pow Pow stab on offbeats (MIDI 65, times 0.5/1.5/2.5/3.5).
4. Add Am 808 bass — short stabs pattern above.
5. (Optional) Add sustained Am pad at velocity 0.5 for atmosphere.
6. Loop 8 bars. Add hi-hat roll on bar 4.
7. Layer pitch-up Pow Pow (MIDI 67) on every 4th bar for variation.
