"""MIDI note transformations: transpose, quantize, humanize, voice-lead, arpeggiate.

These tools accept a list of note dicts (the same format used by fl_send_notes)
and return a transformed list. They never write to FL Studio directly — pipe
the output into fl_send_notes when ready.

All tools preserve any extra note properties (pan, color, fcut, fres, etc.)
that aren't directly transformed.
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Any

from music21 import chord as m21chord
from music21 import key as m21key
from music21 import note as m21note
from music21 import roman as m21roman

if TYPE_CHECKING:
    from fastmcp import FastMCP


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _clone(note: dict[str, Any]) -> dict[str, Any]:
    """Shallow-copy a note dict; preserve all custom fields."""
    return dict(note)


def _clamp_midi(value: int) -> int:
    return max(0, min(127, value))


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


# ---------------------------------------------------------------------------
# Transformations
# ---------------------------------------------------------------------------


def _transpose(notes: list[dict[str, Any]], semitones: int) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for n in notes:
        nn = _clone(n)
        nn["midi"] = _clamp_midi(int(n.get("midi", n.get("number", 60))) + semitones)
        out.append(nn)
    return out


def _quantize(
    notes: list[dict[str, Any]],
    grid: float,
    strength: float,
) -> list[dict[str, Any]]:
    """Snap each note's start time toward the nearest grid line.

    grid=0.25 = 16th-note grid. strength=1.0 = full snap; 0.5 = halfway.
    """
    if grid <= 0:
        return [_clone(n) for n in notes]
    out: list[dict[str, Any]] = []
    s = _clamp01(strength)
    for n in notes:
        nn = _clone(n)
        t = float(n.get("time", 0.0))
        snapped = round(t / grid) * grid
        nn["time"] = round(t + (snapped - t) * s, 4)
        out.append(nn)
    return out


def _humanize(
    notes: list[dict[str, Any]],
    time_amount: float,
    velocity_amount: float,
    seed: int | None,
) -> list[dict[str, Any]]:
    """Add small random jitter to time and velocity.

    time_amount: max time deviation in quarter notes (e.g. 0.02 = ~5 ms at 120 BPM)
    velocity_amount: max velocity deviation 0.0-1.0
    """
    rng = random.Random(seed)
    out: list[dict[str, Any]] = []
    for n in notes:
        nn = _clone(n)
        if time_amount > 0:
            t = float(n.get("time", 0.0))
            nn["time"] = round(max(0.0, t + rng.uniform(-time_amount, time_amount)), 4)
        if velocity_amount > 0:
            v = float(n.get("velocity", 0.8))
            nn["velocity"] = round(_clamp01(v + rng.uniform(-velocity_amount, velocity_amount)), 4)
        out.append(nn)
    return out


def _voice_lead(
    chord_blocks: list[dict[str, Any]],
    key_str: str | None,
    octave_anchor_low: int = 53,
) -> list[dict[str, Any]]:
    """Re-voice a chord progression so consecutive chords share common tones
    and minimize voice movement.

    Each chord block must contain {"time", "duration", "midi_notes" or "label"}.
    Returns chord blocks with updated `midi_notes` and a flat `notes` list
    suitable for fl_send_notes.
    """
    if not chord_blocks:
        return []

    # Resolve a key if provided (for nicer roman handling); not strictly required.
    k = None
    if key_str:
        try:
            parts = key_str.strip().split()
            tonic = parts[0]
            mode = parts[1].lower() if len(parts) > 1 else "major"
            k = m21key.Key(tonic, mode)
        except Exception:
            k = None

    out_blocks: list[dict[str, Any]] = []
    prev_voicing: list[int] = []
    for block in chord_blocks:
        # Get chord pitches (pitch classes) from either midi_notes or label
        pcs: list[int] = []
        if "midi_notes" in block and block["midi_notes"]:
            pcs = sorted({int(m) % 12 for m in block["midi_notes"]})
        elif "label" in block:
            try:
                if k is not None and any(c in block["label"] for c in "iIvVx"):
                    rn = m21roman.RomanNumeral(block["label"], k)
                    pcs = [int(p.pitchClass) for p in rn.pitches]
                else:
                    c = m21chord.Chord(block["label"])
                    pcs = [int(p.pitchClass) for p in c.pitches]
            except Exception:
                pcs = []
        if not pcs:
            out_blocks.append(_clone(block))
            continue

        # Choose voicing: each pitch class is placed near the corresponding voice
        # in the previous chord (greedy nearest-neighbor)
        if not prev_voicing:
            # First chord: anchor near octave_anchor_low
            new_voicing = []
            target = octave_anchor_low
            for pc in pcs:
                candidate = target + ((pc - target) % 12)
                if new_voicing and candidate <= new_voicing[-1]:
                    candidate += 12
                new_voicing.append(candidate)
        else:
            # Match each prev voice to the closest available pitch class
            new_voicing = []
            available_pcs = list(pcs)
            for prev_midi in prev_voicing:
                best_pc = None
                best_dist = 999
                for pc in available_pcs:
                    candidate = prev_midi + ((pc - prev_midi + 6) % 12) - 6
                    dist = abs(candidate - prev_midi)
                    if dist < best_dist:
                        best_dist = dist
                        best_pc = (pc, candidate)
                if best_pc is None:
                    break
                new_voicing.append(best_pc[1])
                available_pcs.remove(best_pc[0])
            # Append any remaining pitch classes above
            for pc in available_pcs:
                last = new_voicing[-1] if new_voicing else octave_anchor_low
                candidate = last + ((pc - last) % 12)
                if candidate == last:
                    candidate += 12
                new_voicing.append(candidate)

        new_voicing = sorted({_clamp_midi(m) for m in new_voicing})
        prev_voicing = new_voicing
        nb = _clone(block)
        nb["midi_notes"] = new_voicing
        out_blocks.append(nb)

    return out_blocks


def _arpeggiate(
    midi_notes: list[int],
    time_start: float,
    pattern: str,
    rate: float,
    total_duration: float,
    velocity: float,
) -> list[dict[str, Any]]:
    """Turn a chord into an arpeggio.

    pattern: "up" | "down" | "up_down" | "down_up" | "random"
    rate: duration of each arp note in quarter notes (e.g. 0.25 = 16th notes)
    total_duration: total length of the arpeggio in quarter notes
    """
    if not midi_notes or rate <= 0 or total_duration <= 0:
        return []
    sorted_notes = sorted(midi_notes)
    if pattern == "up":
        sequence = sorted_notes
    elif pattern == "down":
        sequence = list(reversed(sorted_notes))
    elif pattern == "up_down":
        sequence = sorted_notes + list(reversed(sorted_notes[1:-1]))
        if not sequence:
            sequence = sorted_notes
    elif pattern == "down_up":
        rev = list(reversed(sorted_notes))
        sequence = rev + sorted_notes[1:-1]
        if not sequence:
            sequence = rev
    elif pattern == "random":
        sequence = list(sorted_notes)
        random.shuffle(sequence)
    else:
        sequence = sorted_notes

    out: list[dict[str, Any]] = []
    n_steps = int(round(total_duration / rate))
    for i in range(n_steps):
        midi = sequence[i % len(sequence)]
        out.append(
            {
                "midi": int(midi),
                "time": round(time_start + i * rate, 4),
                "duration": rate,
                "velocity": velocity,
            }
        )
    return out


# ---------------------------------------------------------------------------
# FastMCP registration
# ---------------------------------------------------------------------------


def register_transform_tools(mcp: FastMCP) -> None:
    """Register MIDI transformation tools."""

    @mcp.tool()
    def fl_transpose_notes(
        notes: list[dict[str, Any]],
        semitones: int,
    ) -> dict[str, Any]:
        """Shift every note up/down by N semitones.

        Args:
            notes: List of note dicts (midi/time/duration/velocity).
            semitones: Positive = up, negative = down. Notes are clamped 0-127.

        Returns:
            {"notes": [transformed], "metadata": {"semitones", "input_count"}}
        """
        if not notes:
            return {"notes": [], "metadata": {"semitones": semitones, "input_count": 0}}
        out = _transpose(notes, semitones)
        return {
            "notes": out,
            "metadata": {"semitones": semitones, "input_count": len(notes)},
        }

    @mcp.tool()
    def fl_quantize_notes(
        notes: list[dict[str, Any]],
        grid: float = 0.25,
        strength: float = 1.0,
    ) -> dict[str, Any]:
        """Snap note start times to a rhythmic grid.

        Args:
            notes: List of note dicts.
            grid: Grid resolution in quarter notes. 1.0=quarter, 0.5=8th,
                0.25=16th (default), 0.125=32nd, 0.333=8th triplet.
            strength: 0.0-1.0. 1.0 = full snap, 0.5 = halfway, 0.0 = no snap.

        Returns:
            {"notes": [...], "metadata": {"grid", "strength"}}
        """
        out = _quantize(notes, grid, strength)
        return {
            "notes": out,
            "metadata": {"grid": grid, "strength": strength, "count": len(out)},
        }

    @mcp.tool()
    def fl_humanize_notes(
        notes: list[dict[str, Any]],
        time_amount: float = 0.02,
        velocity_amount: float = 0.08,
        seed: int | None = None,
    ) -> dict[str, Any]:
        """Add small random offsets to time and velocity for a more human feel.

        Args:
            notes: List of note dicts.
            time_amount: Max time deviation in quarter notes (default 0.02 ~
                5ms at 120 BPM). Use sparingly: 0.01-0.04 typical.
            velocity_amount: Max velocity deviation 0.0-1.0 (default 0.08).
            seed: Optional integer for reproducible randomization.

        Returns:
            {"notes": [...], "metadata": {"time_amount", "velocity_amount", "seed"}}
        """
        out = _humanize(notes, time_amount, velocity_amount, seed)
        return {
            "notes": out,
            "metadata": {
                "time_amount": time_amount,
                "velocity_amount": velocity_amount,
                "seed": seed,
                "count": len(out),
            },
        }

    @mcp.tool()
    def fl_voice_lead_chords(
        chord_blocks: list[dict[str, Any]],
        key: str | None = None,
        octave_anchor_low: int = 53,
        velocity: float = 0.65,
    ) -> dict[str, Any]:
        """Re-voice a chord progression for smooth voice leading.

        Each chord block needs at least one of:
          - "midi_notes": list of MIDI numbers (from a previous chord generator)
          - "label": chord symbol like "Am", "F#°7" OR Roman numeral like "vi"
            (Roman numerals require the `key` argument)
        And `time` + `duration` for placement.

        The algorithm uses greedy nearest-neighbor: each voice in the new
        chord moves to the closest pitch class in the next chord, minimizing
        total voice movement.

        Args:
            chord_blocks: list of dicts, each with at least
                {"time", "duration", "midi_notes" or "label"}.
            key: e.g. "A minor". Required if blocks use Roman numerals.
            octave_anchor_low: Lowest MIDI for the FIRST chord (default 53 = F3).
            velocity: Velocity for output notes (default 0.65).

        Returns:
            {
              "notes": [...],  # flat note list for fl_send_notes
              "chord_blocks": [...],  # blocks with updated midi_notes
              "metadata": {"input_count", "output_count"}
            }
        """
        out_blocks = _voice_lead(chord_blocks, key, octave_anchor_low)
        notes: list[dict[str, Any]] = []
        for block in out_blocks:
            if "midi_notes" not in block or not block["midi_notes"]:
                continue
            t = float(block.get("time", 0.0))
            d = float(block.get("duration", 4.0))
            for midi in block["midi_notes"]:
                notes.append(
                    {
                        "midi": int(midi),
                        "time": round(t, 4),
                        "duration": round(max(0.25, d - 0.5), 4),
                        "velocity": velocity,
                    }
                )
        return {
            "notes": notes,
            "chord_blocks": out_blocks,
            "metadata": {
                "input_count": len(chord_blocks),
                "output_count": len(out_blocks),
                "note_count": len(notes),
            },
        }

    @mcp.tool()
    def fl_arpeggiate_chord(
        midi_notes: list[int],
        time_start: float = 0.0,
        pattern: str = "up",
        rate: float = 0.25,
        total_duration: float = 4.0,
        velocity: float = 0.75,
    ) -> dict[str, Any]:
        """Convert a held chord into an arpeggio.

        Args:
            midi_notes: List of MIDI note numbers forming the chord
                (e.g. [60, 64, 67] for C major).
            time_start: Where the arp begins, in quarter notes (default 0).
            pattern: "up" | "down" | "up_down" | "down_up" | "random".
            rate: Duration of each step in quarter notes
                (default 0.25 = 16th notes).
            total_duration: Total length of the arpeggio in quarter notes
                (default 4.0 = one bar).
            velocity: Velocity 0.0-1.0 (default 0.75).

        Returns:
            {"notes": [...], "metadata": {"pattern", "rate", "step_count"}}
        """
        if not midi_notes:
            return {"error": "midi_notes is empty"}
        out = _arpeggiate(midi_notes, time_start, pattern, rate, total_duration, velocity)
        return {
            "notes": out,
            "metadata": {
                "pattern": pattern,
                "rate": rate,
                "step_count": len(out),
                "total_duration": total_duration,
            },
        }


# Suppress unused-import warning at import time (m21note used for type stubs awareness)
_ = m21note
