---
name: music-theory
description: Music theory knowledge for chord building, scale generation, and MIDI note mapping
---

# Music Theory Reference

## Chord Formulas (semitones from root)

- Major: 0, 4, 7
- Minor: 0, 3, 7
- Diminished: 0, 3, 6
- Augmented: 0, 4, 8
- Maj7: 0, 4, 7, 11
- min7: 0, 3, 7, 10
- dom7: 0, 4, 7, 10
- dim7: 0, 3, 6, 9
- half-dim7: 0, 3, 6, 10
- sus2: 0, 2, 7
- sus4: 0, 5, 7
- add9: 0, 4, 7, 14
- 9th: 0, 4, 7, 10, 14
- 11th: 0, 4, 7, 10, 14, 17
- 13th: 0, 4, 7, 10, 14, 17, 21

## Scale Formulas (semitones)

- Major (Ionian): 0, 2, 4, 5, 7, 9, 11
- Natural Minor (Aeolian): 0, 2, 3, 5, 7, 8, 10
- Harmonic Minor: 0, 2, 3, 5, 7, 8, 11
- Melodic Minor (asc): 0, 2, 3, 5, 7, 9, 11
- Dorian: 0, 2, 3, 5, 7, 9, 10
- Phrygian: 0, 1, 3, 5, 7, 8, 10
- Lydian: 0, 2, 4, 6, 7, 9, 11
- Mixolydian: 0, 2, 4, 5, 7, 9, 10
- Locrian: 0, 1, 3, 5, 6, 8, 10
- Pentatonic Major: 0, 2, 4, 7, 9
- Pentatonic Minor: 0, 3, 5, 7, 10
- Blues: 0, 3, 5, 6, 7, 10
- Whole Tone: 0, 2, 4, 6, 8, 10
- Chromatic: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11

## Note-to-MIDI Mapping

Root notes (octave 4): C=60, C#=61, D=62, D#=63, E=64, F=65, F#=66, G=67, G#=68, A=69, A#=70, B=71

To get any octave: MIDI = root + (octave - 4) * 12

## Common Progressions (Roman Numerals)

- Pop: I-V-vi-IV
- Sad pop: vi-IV-I-V
- Jazz ii-V-I: ii7-V7-Imaj7
- 12-bar blues: I-I-I-I-IV-IV-I-I-V-IV-I-V
- Canon: I-V-vi-iii-IV-I-IV-V
- Andalusian: i-VII-VI-V

## Voice Leading Tips

- Move each voice to the nearest chord tone
- Keep common tones in the same voice
- Avoid parallel fifths and octaves
- Bass notes typically in octave 2-3 (MIDI 36-59)
- Chords typically in octave 3-5 (MIDI 48-83)
- Melody typically in octave 4-5 (MIDI 60-83)
