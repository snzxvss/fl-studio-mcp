"""Genre-aware music generators for urban/Latin/Caribbean styles.

These tools produce note lists ready to be sent to FL Studio's piano roll
via fl_send_notes. They never write to FL Studio directly — the caller
inspects/edits the output and sends it explicitly. This keeps the
generators pure, composable, and testable without FL Studio open.

Knowledge sources:
- .claude/skills/genre-reggaeton.md  — dembow pattern, perreo variant
- .claude/skills/genre-trap-latino.md — half-time drums, 808 glides
- .claude/skills/genre-dancehall.md   — riddims (one-drop, steppers, syncopated)
- .claude/skills/genre-champeta.md    — Caribbean drums + palanca guitar
- .claude/skills/genre-dembow.md      — Dominican fast dembow + Pow Pow

All times are in quarter notes (1 bar = 4 in 4/4). All velocities are 0.0-1.0.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from music21 import key as m21key
from music21 import roman as m21roman

if TYPE_CHECKING:
    from fastmcp import FastMCP


# ---------------------------------------------------------------------------
# Drum kit MIDI map (General MIDI standard)
# ---------------------------------------------------------------------------

DRUM_MIDI = {
    "kick": 36,
    "rim": 37,
    "snare": 38,
    "clap": 39,
    "hihat_closed": 42,
    "hihat_open": 46,
    "tom_low": 43,
    "tom_mid": 47,
    "tom_high": 50,
    "cowbell": 56,
    "conga_high": 63,
    "conga_low": 64,
}


# Each entry is (time_in_bar, velocity, duration). Times are quarter notes.
# Patterns are 1 bar (4 beats) unless documented otherwise — repeated by `bars`.

# Reused dancehall skanking 8th-note hi-hat pattern (offbeat emphasis).
_DH_SKANK_HATS: list[tuple[float, float, float]] = [
    (0.5, 0.65, 0.25), (1.5, 0.7, 0.25), (2.5, 0.65, 0.25), (3.5, 0.7, 0.25),
]

DRUM_PATTERNS: dict[str, dict[str, dict[str, list[tuple[float, float, float]]]]] = {
    "reggaeton": {
        "default": {
            "kick": [(0.0, 0.9, 0.25), (1.0, 0.85, 0.25), (2.0, 0.9, 0.25), (3.0, 0.85, 0.25)],
            "snare": [(0.75, 0.8, 0.25), (1.5, 0.75, 0.25), (2.75, 0.8, 0.25), (3.5, 0.75, 0.25)],
            "hihat_closed": [(t, 0.6, 0.25) for t in (0.0, 1.0, 2.0, 3.0)],
            "hihat_open": [(0.5, 0.5, 0.25), (2.5, 0.5, 0.25)],
        },
        "perreo": {
            "kick": [(0.0, 0.9, 0.25), (1.0, 0.85, 0.25), (2.0, 0.9, 0.25), (3.0, 0.85, 0.25)],
            "snare": [(0.75, 0.8, 0.25), (1.75, 0.75, 0.25), (2.75, 0.8, 0.25), (3.75, 0.75, 0.25)],
            "hihat_closed": [
                (t, 0.5 if i % 2 == 0 else 0.7, 0.125)
                for i, t in enumerate(i * 0.25 for i in range(16))
            ],
        },
    },
    "trap_latino": {
        "default": {
            # half-time: snare on beat 3 only
            "kick": [(0.0, 0.95, 0.25), (1.75, 0.85, 0.25), (2.5, 0.9, 0.25)],
            "snare": [(2.0, 0.9, 0.5)],
            "clap": [(2.0, 0.85, 0.5)],
            "hihat_closed": [
                (i * 0.25, 0.55 if i % 2 == 0 else 0.45, 0.125) for i in range(16)
            ],
        },
    },
    "dancehall": {
        "one_drop": {
            "kick": [(2.0, 0.95, 0.25)],
            "rim": [(1.0, 0.8, 0.25), (3.0, 0.8, 0.25)],
            "hihat_closed": _DH_SKANK_HATS,
        },
        "steppers": {
            "kick": [(0.0, 0.95, 0.25), (1.0, 0.85, 0.25), (2.0, 0.95, 0.25), (3.0, 0.85, 0.25)],
            "clap": [(1.0, 0.85, 0.25), (3.0, 0.85, 0.25)],
            "hihat_closed": _DH_SKANK_HATS,
            "hihat_open": [(1.0, 0.5, 0.25), (3.0, 0.5, 0.25)],
        },
        "syncopated": {
            "kick": [(0.0, 0.95, 0.25), (1.5, 0.85, 0.25), (2.0, 0.9, 0.25), (3.5, 0.8, 0.25)],
            "snare": [(1.0, 0.8, 0.25), (3.0, 0.8, 0.25)],
            "hihat_closed": _DH_SKANK_HATS,
        },
    },
    "champeta": {
        "criolla": {
            "kick": [(0.0, 0.95, 0.25), (2.0, 0.95, 0.25)],
            "snare": [(1.0, 0.85, 0.25), (3.0, 0.85, 0.25)],
            "conga_high": [
                (t, v, 0.125)
                for t, v in [
                    (0.5, 0.7), (0.75, 0.65),
                    (1.5, 0.75), (1.75, 0.7),
                    (2.5, 0.7), (2.75, 0.65),
                    (3.5, 0.75), (3.75, 0.7),
                ]
            ],
            "conga_low": [
                (t, v, 0.125)
                for t, v in [
                    (0.0, 0.5), (0.25, 0.45),
                    (1.0, 0.5), (1.25, 0.45),
                    (2.0, 0.5), (2.25, 0.45),
                    (3.0, 0.5), (3.25, 0.45),
                ]
            ],
            "cowbell": [(t, 0.7, 0.25) for t in (0.0, 0.75, 1.5, 2.0, 3.0)],
        },
        "urbana": {
            # hybrid with reggaeton dembow + champeta congas
            "kick": [(0.0, 0.9, 0.25), (1.0, 0.85, 0.25), (2.0, 0.9, 0.25), (3.0, 0.85, 0.25)],
            "snare": [(0.75, 0.8, 0.25), (1.5, 0.75, 0.25), (2.75, 0.8, 0.25), (3.5, 0.75, 0.25)],
            "conga_high": [(t, 0.7, 0.125) for t in (0.5, 1.5, 2.5, 3.5)],
            "cowbell": [(t, 0.6, 0.25) for t in (0.0, 0.75, 2.0, 2.75)],
        },
    },
    "dembow": {
        # Dominican dembow — fast, aggressive, Pow-Pow stab on offbeats
        "default": {
            "kick": [(0.0, 0.95, 0.25), (0.75, 0.85, 0.25), (2.0, 0.95, 0.25), (2.75, 0.85, 0.25)],
            "snare": [
                (0.5, 0.85, 0.25), (1.0, 0.8, 0.25), (1.5, 0.85, 0.25),
                (2.5, 0.85, 0.25), (3.0, 0.8, 0.25), (3.5, 0.85, 0.25),
            ],
            "hihat_closed": [(i * 0.25, 0.55, 0.125) for i in range(16)],
            "hihat_open": [(0.5, 0.6, 0.25), (2.5, 0.6, 0.25)],
        },
    },
}


# Pow-Pow stab sample for Dominican dembow — pitched percussion as melody.
# Returned as a separate generator since it lives outside the GM drum kit.
DEMBOW_POWPOW_PATTERN = [
    (0.5, 65, 0.9, 0.25),  # (time, midi, velocity, duration)
    (1.5, 65, 0.9, 0.25),
    (2.5, 65, 0.9, 0.25),
    (3.5, 67, 0.9, 0.25),  # pitch up on beat 4 for tension
]


# ---------------------------------------------------------------------------
# Chord progressions — Roman numerals, transposed at runtime via music21
# ---------------------------------------------------------------------------

CHORD_PROGRESSIONS: dict[str, dict[str, list[str]]] = {
    "reggaeton": {
        "bad_bunny": ["i", "iv", "VII", "III"],
        "j_balvin": ["i", "VI", "III", "VII"],
        "karol_g":  ["iv", "i", "VI", "V"],
    },
    "trap_latino": {
        "i_VI": ["i", "VI"],
        "i_iv": ["i", "iv"],
        "i_VII_VI_V": ["i", "VII", "VI", "V"],
        "single_minor": ["i"],
    },
    "dancehall": {
        "vamp_minor": ["i"],
        "i_VII": ["i", "VII"],
        "i_iv_VII_i": ["i", "iv", "VII", "i"],
        "pop_major": ["I", "V", "vi", "IV"],
    },
    "champeta": {
        "I_V_vi_IV": ["I", "V", "vi", "IV"],
        "I_IV_V": ["I", "IV", "V", "I"],
        "ii_V_I": ["ii", "V", "I", "I"],
    },
    "dembow": {
        "vamp_minor": ["i"],
        "i_VI": ["i", "VI"],
        "i_v": ["i", "v"],  # darker variant
    },
}


# Default key suggestions per genre (used when caller omits `key`)
DEFAULT_KEYS: dict[str, str] = {
    "reggaeton": "A minor",
    "trap_latino": "F# minor",
    "dancehall": "A minor",
    "champeta": "C major",
    "dembow": "A minor",
}


# Default BPM per genre (informational — pyscript bridge does NOT set BPM,
# but the LLM uses this to advise the user / set tempo via fl_set_tempo).
DEFAULT_BPM: dict[str, tuple[int, int]] = {
    "reggaeton": (90, 100),
    "trap_latino": (130, 145),
    "dancehall": (95, 110),
    "champeta": (100, 110),
    "dembow": (118, 125),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _drum_pattern_to_notes(
    pattern: dict[str, list[tuple[float, float, float]]],
    bars: int,
) -> list[dict[str, Any]]:
    """Expand a 1-bar drum pattern into a multi-bar note list."""
    notes: list[dict[str, Any]] = []
    for instrument, hits in pattern.items():
        midi = DRUM_MIDI.get(instrument)
        if midi is None:
            continue
        for bar in range(bars):
            base = bar * 4.0
            for time_in_bar, vel, dur in hits:
                notes.append(
                    {
                        "midi": midi,
                        "time": round(base + time_in_bar, 4),
                        "duration": dur,
                        "velocity": vel,
                    }
                )
    return notes


def _resolve_progression(
    genre: str,
    progression_id: str | None,
) -> tuple[str, list[str]]:
    """Pick the chord progression, return (id, romans)."""
    progressions = CHORD_PROGRESSIONS.get(genre)
    if not progressions:
        raise ValueError(f"Unknown genre '{genre}'. Known: {sorted(CHORD_PROGRESSIONS)}")
    if progression_id is None:
        progression_id = next(iter(progressions))  # first listed = default
    if progression_id not in progressions:
        raise ValueError(
            f"Unknown progression '{progression_id}' for genre '{genre}'. "
            f"Available: {sorted(progressions)}"
        )
    return progression_id, progressions[progression_id]


def _key_from_string(key_str: str) -> m21key.Key:
    """Parse 'A minor', 'F# minor', 'C major', etc."""
    parts = key_str.strip().split()
    if len(parts) == 1:
        # default to major if mode omitted
        return m21key.Key(parts[0], "major")
    tonic = parts[0]
    mode = parts[1].lower()
    if mode not in ("major", "minor"):
        raise ValueError(f"Unsupported mode '{mode}' (use 'major' or 'minor')")
    return m21key.Key(tonic, mode)


def _voice_chord_in_octave(pitch_classes: list[Any], target_midi_low: int = 53) -> list[int]:
    """Lay out chord pitches in a comfortable octave for piano roll display.

    pitch_classes: music21 Pitch objects (octave usually 4 by default)
    target_midi_low: lowest MIDI for the chord root area (default ~53 = F3)
    """
    if not pitch_classes:
        return []
    # Bring root close to target_midi_low; voice the rest above
    base_pc = pitch_classes[0].pitchClass
    root_midi = target_midi_low + ((base_pc - target_midi_low) % 12)
    midis = [root_midi]
    prev = root_midi
    for p in pitch_classes[1:]:
        candidate = prev + ((p.pitchClass - prev) % 12)
        if candidate == prev:
            candidate += 12
        midis.append(candidate)
        prev = candidate
    return midis


def _chord_progression_to_notes(
    romans: list[str],
    key: m21key.Key,
    bars_per_chord: int,
    chord_octave_low: int,
    velocity: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Build chord notes + extracted root info for bass generation.

    Returns (chord_notes, chord_meta) where chord_meta is a list of
    {"time": float, "duration": float, "root_midi": int, "label": str, "midi_notes": [...]}
    used by bass generators.
    """
    chord_notes: list[dict[str, Any]] = []
    chord_meta: list[dict[str, Any]] = []
    for i, rn_str in enumerate(romans):
        try:
            rn = m21roman.RomanNumeral(rn_str, key)
        except Exception as e:
            raise ValueError(f"Invalid Roman numeral '{rn_str}' in key {key}: {e}") from e
        midis = _voice_chord_in_octave(list(rn.pitches), target_midi_low=chord_octave_low)
        time = i * bars_per_chord * 4.0
        duration = bars_per_chord * 4.0 - 0.5  # slight gap so chords don't run together
        for midi in midis:
            chord_notes.append(
                {
                    "midi": int(midi),
                    "time": round(time, 4),
                    "duration": round(duration, 4),
                    "velocity": velocity,
                }
            )
        chord_meta.append(
            {
                "time": round(time, 4),
                "duration": round(bars_per_chord * 4.0, 4),
                "root_midi": int(midis[0]),
                "label": str(rn.figure),
                "midi_notes": [int(m) for m in midis],
            }
        )
    return chord_notes, chord_meta


# ---------------------------------------------------------------------------
# Bass generators per genre
# ---------------------------------------------------------------------------


def _n(midi: int, time: float, duration: float, velocity: float) -> dict[str, Any]:
    """Build a note dict (compact helper to keep bass templates readable)."""
    return {
        "midi": midi,
        "time": round(time, 4),
        "duration": duration,
        "velocity": velocity,
    }


# Bass templates per genre. Each entry: (offset_in_bar, duration, velocity, semis_from_root)
# semis_from_root is 0 for plain root, 7 for fifth, etc.
_BASS_TEMPLATES: dict[str, list[tuple[float, float, float, int]]] = {
    "reggaeton":   [(0.0, 1.5, 0.9, 0), (2.0, 1.0, 0.85, 0), (3.0, 0.5, 0.7, 0)],
    "trap_latino": [(0.0, 1.75, 0.95, 0), (1.75, 0.5, 0.85, 0), (2.5, 1.5, 0.9, 0)],
    "dembow":      [
        (0.0, 0.5, 0.95, 0), (1.0, 0.25, 0.85, 0), (2.0, 0.5, 0.95, 0),
        (3.0, 0.25, 0.85, 0), (3.5, 0.25, 0.85, 0),
    ],
    "dancehall":   [
        (0.0, 0.5, 0.95, 0), (1.5, 0.5, 0.85, 0),
        (2.0, 0.5, 0.95, 0), (3.5, 0.5, 0.85, 0),
    ],
    "champeta":    [
        (0.0, 0.5, 0.9, 0), (1.0, 0.5, 0.85, 7),
        (2.0, 0.5, 0.85, 0), (3.0, 0.5, 0.85, 7),
    ],
}


def _bass_for_chord(
    genre: str,
    root_midi: int,
    bar_offset: float,
    bars: int,
) -> list[dict[str, Any]]:
    """Generate bass notes for a single chord block in the given genre's style."""
    template = _BASS_TEMPLATES.get(genre)
    notes: list[dict[str, Any]] = []
    if template is None:
        # Fallback: root on beat 1, full bar
        for b in range(bars):
            notes.append(_n(root_midi, bar_offset + b * 4.0, 4.0, 0.9))
        return notes
    for b in range(bars):
        base = bar_offset + b * 4.0
        for t, dur, vel, semis in template:
            notes.append(_n(root_midi + semis, base + t, dur, vel))
    return notes


def _bass_octave_for_genre(genre: str) -> int:
    """Recommended bass octave (returns the MIDI value for the lowest A in that octave)."""
    return {
        "trap_latino": 33,    # A1 — very low 808
        "dembow": 33,          # A1
        "reggaeton": 45,       # A2
        "dancehall": 45,       # A2
        "champeta": 36,        # C2 area
    }.get(genre, 45)


def _force_to_bass_octave(midi: int, genre: str) -> int:
    """Drop a chord root to the genre's preferred bass octave."""
    target_low = _bass_octave_for_genre(genre)
    pc = midi % 12
    target_pc = target_low % 12
    base = target_low - target_pc + pc
    while base < target_low - 6:
        base += 12
    while base > target_low + 6:
        base -= 12
    return base


# ---------------------------------------------------------------------------
# Champeta palanca guitar — explicit MIDI patterns from the skill
# ---------------------------------------------------------------------------

# Pattern A — major key (transcribed for C major in skill); we transpose to caller's key.
# Format: (time_in_2bars, semitones_from_root, duration, velocity)
PALANCA_PATTERN_A_MAJOR = [
    (0.0, 4, 0.25, 0.75),   # E
    (0.5, 7, 0.25, 0.7),    # G
    (0.75, 12, 0.25, 0.8),  # C (oct up)
    (1.0, 7, 0.25, 0.7),    # G
    (1.5, 4, 0.25, 0.7),    # E
    (2.0, 5, 0.25, 0.75),   # F
    (2.5, 9, 0.25, 0.7),    # A
    (2.75, 12, 0.25, 0.8),  # C
    (3.0, 9, 0.25, 0.7),    # A
    (3.5, 5, 0.25, 0.7),    # F
]

# Pattern B — minor key (transcribed Am, octave 5)
PALANCA_PATTERN_B_MINOR = [
    (0.0, 3, 0.25, 0.75),   # C
    (0.5, 7, 0.25, 0.7),    # E
    (0.75, 12, 0.25, 0.8),  # A
    (1.5, 10, 0.25, 0.7),   # G
    (2.0, 8, 0.25, 0.75),   # F
    (2.5, 12, 0.25, 0.7),   # A
    (2.75, 15, 0.25, 0.8),  # C (oct up)
    (3.5, 10, 0.25, 0.7),   # G
]


# ---------------------------------------------------------------------------
# FastMCP registration
# ---------------------------------------------------------------------------


def register_generator_tools(mcp: FastMCP) -> None:
    """Register genre-aware generator tools."""

    @mcp.tool()
    def fl_list_genre_templates(genre: str | None = None) -> dict[str, Any]:
        """List available drum patterns and chord progressions for each genre.

        Use this before calling generators so you know which `variant` and
        `progression_id` values are valid.

        Args:
            genre: Optional filter: "reggaeton" | "trap_latino" | "dancehall"
                | "champeta" | "dembow". Omit to list all genres.

        Returns:
            {
              "<genre>": {
                "drum_variants": [...],
                "progressions": {"<id>": ["I", "V", ...]},
                "default_key": "A minor",
                "bpm_range": [90, 100]
              }, ...
            }
        """
        out: dict[str, Any] = {}
        genres = [genre] if genre else list(CHORD_PROGRESSIONS)
        for g in genres:
            if g not in CHORD_PROGRESSIONS:
                continue
            out[g] = {
                "drum_variants": list(DRUM_PATTERNS.get(g, {}).keys()),
                "progressions": CHORD_PROGRESSIONS[g],
                "default_key": DEFAULT_KEYS.get(g),
                "bpm_range": list(DEFAULT_BPM.get(g, (120, 120))),
            }
        return out

    @mcp.tool()
    def fl_generate_drum_pattern(
        genre: str,
        bars: int = 4,
        variant: str | None = None,
    ) -> dict[str, Any]:
        """Generate a genre-specific drum pattern (kick + snare + hats + percussion).

        Returns notes ready for fl_send_notes. Drum MIDI numbers follow the
        General MIDI standard (kick=36, snare=38, clap=39, closed_hat=42,
        open_hat=46, conga_high=63, conga_low=64, cowbell=56, etc.).

        Args:
            genre: "reggaeton" | "trap_latino" | "dancehall" | "champeta" | "dembow"
            bars: Number of bars to generate (default 4).
            variant: Pattern variant. If omitted, uses the genre's default.
                Reggaeton: "default" | "perreo"
                Dancehall: "one_drop" | "steppers" | "syncopated"
                Champeta: "criolla" | "urbana"
                Dembow / Trap Latino: only "default"
                Use fl_list_genre_templates to discover variants.

        Returns:
            {
              "notes": [...],          # ready for fl_send_notes
              "metadata": {
                "genre": ..., "variant": ..., "bars": ...,
                "instruments": [...], "bpm_range": [...], "note_count": ...
              }
            }
        """
        if genre not in DRUM_PATTERNS:
            return {"error": f"Unknown genre '{genre}'. Known: {sorted(DRUM_PATTERNS)}"}
        variants = DRUM_PATTERNS[genre]
        if variant is None:
            variant = next(iter(variants))
        if variant not in variants:
            return {
                "error": f"Unknown variant '{variant}' for {genre}. Available: {sorted(variants)}"
            }
        pattern = variants[variant]
        notes = _drum_pattern_to_notes(pattern, bars)
        return {
            "notes": notes,
            "metadata": {
                "genre": genre,
                "variant": variant,
                "bars": bars,
                "instruments": list(pattern.keys()),
                "bpm_range": list(DEFAULT_BPM.get(genre, (120, 120))),
                "note_count": len(notes),
            },
        }

    @mcp.tool()
    def fl_generate_chord_progression(
        genre: str,
        key: str | None = None,
        progression_id: str | None = None,
        bars_per_chord: int = 1,
        repeats: int = 1,
        chord_octave_low: int = 53,
        velocity: float = 0.65,
    ) -> dict[str, Any]:
        """Generate a chord progression in the requested key, styled for the genre.

        Roman-numeral templates from the genre skills are transposed to the
        requested key via music21. Each chord is voiced as a 3-note triad
        starting around `chord_octave_low` (default F3).

        Args:
            genre: "reggaeton" | "trap_latino" | "dancehall" | "champeta" | "dembow"
            key: e.g. "A minor", "F# minor", "C major". Defaults to the
                genre's typical key (A minor for most urban genres,
                C major for champeta).
            progression_id: e.g. "bad_bunny", "j_balvin" for reggaeton;
                "i_VI" for trap; "I_V_vi_IV" for champeta.
                Use fl_list_genre_templates to see options.
            bars_per_chord: Bars each chord lasts (default 1).
            repeats: Number of times to repeat the full progression (default 1).
            chord_octave_low: Lowest MIDI note for chord voicing (default 53 = F3).
            velocity: Note velocity 0.0-1.0 (default 0.65, soft pad-like).

        Returns:
            {
              "notes": [...],
              "metadata": {
                "genre": ..., "key": "A minor", "progression_id": ...,
                "romans": ["i", "iv", "VII", "III"],
                "chord_meta": [{"time", "duration", "root_midi", "label", "midi_notes"}, ...],
                "total_bars": int
              }
            }
        """
        if genre not in CHORD_PROGRESSIONS:
            return {"error": f"Unknown genre '{genre}'. Known: {sorted(CHORD_PROGRESSIONS)}"}
        try:
            prog_id, romans = _resolve_progression(genre, progression_id)
        except ValueError as e:
            return {"error": str(e)}

        key_str = key or DEFAULT_KEYS.get(genre, "A minor")
        try:
            k = _key_from_string(key_str)
        except ValueError as e:
            return {"error": str(e)}

        all_notes: list[dict[str, Any]] = []
        all_meta: list[dict[str, Any]] = []
        for r in range(repeats):
            chord_notes, chord_meta = _chord_progression_to_notes(
                romans, k, bars_per_chord, chord_octave_low, velocity
            )
            offset = r * len(romans) * bars_per_chord * 4.0
            for n in chord_notes:
                n["time"] = round(n["time"] + offset, 4)
            for m in chord_meta:
                m["time"] = round(m["time"] + offset, 4)
            all_notes.extend(chord_notes)
            all_meta.extend(chord_meta)

        return {
            "notes": all_notes,
            "metadata": {
                "genre": genre,
                "key": f"{k.tonic.name} {k.mode}",
                "progression_id": prog_id,
                "romans": romans,
                "chord_meta": all_meta,
                "total_bars": len(romans) * bars_per_chord * repeats,
            },
        }

    @mcp.tool()
    def fl_generate_bassline_from_chords(
        chords: list[dict[str, Any]],
        genre: str,
        force_bass_octave: bool = True,
    ) -> dict[str, Any]:
        """Generate a genre-styled bass line that follows a list of chord blocks.

        Pass the `chord_meta` you got from fl_generate_chord_progression, OR
        any list of dicts with at least {"time": float, "duration": float,
        "root_midi": int}. Genre dictates the rhythmic style:
        - reggaeton: 808 sub stabs at beats 1, 3, end of bar
        - trap_latino: long held 808, then stab, then hold (low octave)
        - dembow: punchy short stabs (quintuplet feel)
        - dancehall: syncopated, mirrors kick
        - champeta: walking root-fifth-root-fifth

        Args:
            chords: List of chord blocks (use chord_meta from
                fl_generate_chord_progression). Each block needs
                {"time", "duration", "root_midi"}.
            genre: One of the supported genres.
            force_bass_octave: If True (default), drops each root to the
                genre's preferred bass octave (e.g. octave 1 for trap, octave
                2 for reggaeton).

        Returns:
            {"notes": [...], "metadata": {"genre", "chord_count", "note_count"}}
        """
        if not chords:
            return {"error": "Empty 'chords' list."}
        if genre not in DEFAULT_KEYS:
            return {"error": f"Unknown genre '{genre}'. Known: {sorted(DEFAULT_KEYS)}"}

        notes: list[dict[str, Any]] = []
        for block in chords:
            try:
                time = float(block["time"])
                duration = float(block["duration"])
                root = int(block["root_midi"])
            except (KeyError, TypeError, ValueError) as e:
                return {"error": f"Invalid chord block {block!r}: {e}"}
            bars = max(1, int(round(duration / 4.0)))
            if force_bass_octave:
                root = _force_to_bass_octave(root, genre)
            notes.extend(_bass_for_chord(genre, root, time, bars))

        return {
            "notes": notes,
            "metadata": {
                "genre": genre,
                "chord_count": len(chords),
                "note_count": len(notes),
                "bass_octave_anchor": _bass_octave_for_genre(genre),
            },
        }

    @mcp.tool()
    def fl_generate_palanca_guitar(
        key: str = "C major",
        bars: int = 4,
        pattern: str = "auto",
        octave: int = 4,
    ) -> dict[str, Any]:
        """Generate a champeta-style palanca/picao guitar line.

        The palanca is the bright syncopated electric-guitar arpeggio that
        defines champeta. Pattern A targets major keys, Pattern B targets
        minor keys (auto-selected from `key` unless `pattern` is set).

        Args:
            key: e.g. "C major", "G major", "A minor". Defaults to "C major".
            bars: Total bars (the underlying patterns are 4 beats; we repeat
                them every bar). Default 4.
            pattern: "A" (major-key pattern), "B" (minor-key pattern),
                or "auto" (default — picks based on the mode of `key`).
            octave: MIDI octave for the tonic anchor (standard MIDI: octave 4
                puts middle C at 60). Default 4 — bright guitar register that
                matches the skill reference (MIDI 60-72 area). Increase to 5
                for a brighter/higher voicing.

        Returns:
            {"notes": [...], "metadata": {"key", "pattern_used", "bars", "note_count"}}
        """
        try:
            k = _key_from_string(key)
        except ValueError as e:
            return {"error": str(e)}

        if pattern == "auto":
            pattern_used = "A" if k.mode == "major" else "B"
        elif pattern in ("A", "B"):
            pattern_used = pattern
        else:
            return {"error": "pattern must be 'A', 'B', or 'auto'"}

        # Anchor: tonic at octave-12 starting reference
        tonic_midi = (octave + 1) * 12 + k.tonic.pitchClass  # MIDI midi=(octave+1)*12 + pc

        template = PALANCA_PATTERN_A_MAJOR if pattern_used == "A" else PALANCA_PATTERN_B_MINOR
        notes: list[dict[str, Any]] = []
        for bar in range(bars):
            base_time = bar * 4.0
            for time_in_bar, semis, dur, vel in template:
                notes.append(
                    {
                        "midi": int(tonic_midi + semis),
                        "time": round(base_time + time_in_bar, 4),
                        "duration": dur,
                        "velocity": vel,
                    }
                )
        return {
            "notes": notes,
            "metadata": {
                "key": f"{k.tonic.name} {k.mode}",
                "pattern_used": pattern_used,
                "bars": bars,
                "octave": octave,
                "note_count": len(notes),
            },
        }

    @mcp.tool()
    def fl_generate_dembow_powpow(bars: int = 4, midi_low: int = 65) -> dict[str, Any]:
        """Generate the signature 'Pow Pow' stab pattern for Dominican dembow.

        Pow Pow = pitched percussion blast (synth or pitched drum) on the
        offbeats. Pitched up on beat 4 for tension. Place this on a
        dedicated channel (a synth blast or tuned 'pow' sample).

        Args:
            bars: Number of bars (default 4).
            midi_low: MIDI note for the main stab (default 65 = F4).
                Beat-4 hit is +2 semitones (G4 by default).

        Returns:
            {"notes": [...], "metadata": {"bars", "note_count", "midi_low"}}
        """
        notes: list[dict[str, Any]] = []
        for bar in range(bars):
            base = bar * 4.0
            for time_in_bar, midi_pitch, vel, dur in DEMBOW_POWPOW_PATTERN:
                # Replace the 65/67 with caller's chosen base + offset
                offset = midi_pitch - 65
                notes.append(
                    {
                        "midi": midi_low + offset,
                        "time": round(base + time_in_bar, 4),
                        "duration": dur,
                        "velocity": vel,
                    }
                )
        return {
            "notes": notes,
            "metadata": {"bars": bars, "midi_low": midi_low, "note_count": len(notes)},
        }
