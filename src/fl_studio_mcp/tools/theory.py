"""Music theory analysis tools for FL Studio MCP.

Reads piano-roll state and exposes high-level analysis: key detection
(Krumhansl-Schmuckler via music21), chord-progression analysis with
Roman-numeral function, and a project summary that combines transport
state with the theory analysis.

These tools never write to FL Studio — they are purely read + analyze.
They accept either piano roll state from disk OR explicit notes provided
by the caller (useful for testing without FL Studio).
"""

from __future__ import annotations

import json
import platform
from pathlib import Path
from typing import TYPE_CHECKING, Any

from music21 import chord as m21chord
from music21 import key as m21key
from music21 import note as m21note
from music21 import roman as m21roman
from music21 import stream as m21stream

if TYPE_CHECKING:
    from fastmcp import FastMCP


# ---------------------------------------------------------------------------
# Path resolution: be resilient to OneDrive-redirected Documents on Windows
# ---------------------------------------------------------------------------


def _candidate_state_paths() -> list[Path]:
    """All plausible locations of piano_roll_state.json on this machine.

    Windows users frequently have their Documents folder redirected into
    OneDrive ("Documents" or "Documentos" depending on locale). Try the
    standard path first, then OneDrive variants.
    """
    home = Path.home()
    relative = (
        Path("Image-Line") / "FL Studio" / "Settings" / "Piano roll scripts"
    ) / "piano_roll_state.json"
    bases: list[Path] = []
    system = platform.system()
    if system in ("Darwin", "Windows"):
        bases.append(home / "Documents")
        bases.append(home / "OneDrive" / "Documents")
        bases.append(home / "OneDrive" / "Documentos")
    else:
        bases.append(home / ".fl-studio" / "Settings")
    return [b / relative for b in bases]


def _read_piano_roll_state() -> dict[str, Any]:
    """Read the latest piano_roll_state.json. Returns {} if not found."""
    for candidate in _candidate_state_paths():
        if candidate.exists():
            try:
                with open(candidate, encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    return data
            except (json.JSONDecodeError, OSError):
                continue
    return {}


# ---------------------------------------------------------------------------
# music21 helpers
# ---------------------------------------------------------------------------


def _notes_to_stream(notes: list[dict[str, Any]], ppq: int = 96) -> m21stream.Stream:
    """Convert FL piano roll note dicts into a music21 Stream.

    Each note dict supports either:
      - {"midi"|"number": int, "time": float (quarter notes), "duration": float}
      - {"midi"|"number": int, "time": int (ticks), "length": int (ticks)}

    PPQ is used to convert ticks to quarter notes when ticks are present.
    """
    s = m21stream.Stream()
    for n in notes:
        midi = n.get("midi", n.get("number"))
        if midi is None:
            continue

        # Two input flavors:
        #   (a) caller-style:  {"duration": qn, "time": qn}        - already in quarter notes
        #   (b) state-export:  {"length": ticks, "time": ticks}    - in ticks, divide by ppq
        in_quarter_notes = "duration" in n
        if in_quarter_notes:
            duration_ql = float(n["duration"])
            offset_ql = float(n.get("time", 0.0))
        else:
            length_ticks = float(n.get("length", ppq))
            duration_ql = length_ticks / ppq if ppq else 1.0
            time_ticks = float(n.get("time", 0))
            offset_ql = time_ticks / ppq if ppq else 0.0

        velocity = n.get("velocity", 0.8)
        m21n = m21note.Note(midi=int(midi), quarterLength=max(duration_ql, 0.0625))
        if isinstance(velocity, float) and 0.0 <= velocity <= 1.0:
            m21n.volume.velocity = int(round(velocity * 127))
        else:
            m21n.volume.velocity = int(velocity)
        s.insert(offset_ql, m21n)
    return s


def _resolve_notes(
    notes: list[dict[str, Any]] | None,
) -> tuple[list[dict[str, Any]], int, str]:
    """Pick notes from explicit arg or piano roll state.

    Returns: (notes, ppq, source_label)
    """
    if notes is not None and len(notes) > 0:
        return notes, 96, "argument"

    state = _read_piano_roll_state()
    pr_notes = state.get("notes", [])
    ppq = int(state.get("ppq", 96)) or 96
    return pr_notes, ppq, "piano_roll_state.json"


def _chord_label(c: m21chord.Chord) -> str:
    """Return a compact human-readable chord label, e.g. 'Am', 'Cmaj7', 'F#°'."""
    try:
        root = c.root().name
        quality = c.quality  # 'major' | 'minor' | 'diminished' | 'augmented' | 'other'
        is_seventh = c.isSeventh()
        if quality == "minor":
            base = f"{root}m"
        elif quality == "diminished":
            base = f"{root}°"
        elif quality == "augmented":
            base = f"{root}+"
        else:
            base = root  # major or other
        if is_seventh and quality == "major":
            base += "maj7"
        elif is_seventh and quality == "minor":
            base += "m7"
        elif is_seventh and quality == "diminished":
            base = f"{root}°7"
        elif is_seventh:
            base += "7"
        return base
    except Exception:
        return c.pitchedCommonName or c.commonName or "?"


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------


def _detect_key(notes: list[dict[str, Any]], ppq: int) -> dict[str, Any]:
    """Run Krumhansl-Schmuckler key detection on a note list."""
    s = _notes_to_stream(notes, ppq=ppq)
    if len(s.flatten().notes) == 0:
        return {
            "key": None,
            "tonic": None,
            "mode": None,
            "confidence": 0.0,
            "alternates": [],
            "note_count": 0,
        }
    k: m21key.Key = s.analyze("key")
    alternates = []
    for alt in getattr(k, "alternateInterpretations", []) or []:
        alternates.append(
            {
                "key": f"{alt.tonic.name} {alt.mode}",
                "correlation": round(float(alt.correlationCoefficient), 4),
            }
        )
    return {
        "key": f"{k.tonic.name} {k.mode}",
        "tonic": k.tonic.name,
        "mode": k.mode,
        "confidence": round(float(k.correlationCoefficient), 4),
        "alternates": alternates[:5],
        "note_count": len(s.flatten().notes),
    }


def _analyze_chords(
    notes: list[dict[str, Any]],
    ppq: int,
    detected_key: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Segment piano-roll notes into chords and label each with a Roman numeral."""
    s = _notes_to_stream(notes, ppq=ppq)
    if len(s.flatten().notes) == 0:
        return {"chords": [], "key": None}

    if detected_key is None:
        detected_key = _detect_key(notes, ppq)

    if detected_key.get("key"):
        try:
            tonic_str = detected_key["tonic"]
            mode_str = detected_key["mode"]
            k = m21key.Key(tonic_str, mode_str)
        except Exception:
            k = None
    else:
        k = None

    chordified = s.chordify()
    chords_out: list[dict[str, Any]] = []
    for el in chordified.recurse().getElementsByClass(m21chord.Chord):
        if len(el.pitches) < 2:
            continue
        offset_ql = round(float(el.offset), 4)
        duration_ql = round(float(el.quarterLength), 4)
        label = _chord_label(el)
        roman_str = None
        function = None
        if k is not None:
            try:
                rn = m21roman.romanNumeralFromChord(el, k)
                roman_str = rn.romanNumeralAlone + (rn.figuresWritten or "")
                if not roman_str:
                    roman_str = rn.figure
                function = rn.functionalityScore
            except Exception:
                roman_str = None
        chords_out.append(
            {
                "time": offset_ql,
                "duration": duration_ql,
                "midi_notes": sorted(int(p.midi) for p in el.pitches),
                "label": label,
                "roman": roman_str,
                "function_score": function,
            }
        )
    return {"chords": chords_out, "key": detected_key.get("key")}


# ---------------------------------------------------------------------------
# FastMCP registration
# ---------------------------------------------------------------------------


def register_theory_tools(mcp: FastMCP) -> None:
    """Register music-theory analysis tools."""

    @mcp.tool()
    def fl_detect_key_and_scale(
        notes: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Detect the musical key and mode of the piano roll content.

        Uses the Krumhansl-Schmuckler algorithm (via music21) to estimate
        the most likely key from pitch-class distribution.

        Args:
            notes: Optional list of note dicts ({"midi", "time", "duration",
                "velocity"}). If omitted, reads piano_roll_state.json.

        Returns:
            {
              "key": "C major" | "A minor" | ...,
              "tonic": "C",
              "mode": "major" | "minor",
              "confidence": float (Pearson correlation, 0..1),
              "alternates": [{"key": "...", "correlation": float}, ...],
              "note_count": int,
              "source": "argument" | "piano_roll_state.json"
            }
        """
        resolved, ppq, source = _resolve_notes(notes)
        result = _detect_key(resolved, ppq)
        result["source"] = source
        return result

    @mcp.tool()
    def fl_analyze_chord_progression(
        notes: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Analyze the chord progression in the piano roll.

        Segments the notes into chords (vertical sonorities), labels each
        chord (e.g. "Am", "F#°7", "Cmaj7") and computes Roman-numeral
        function relative to the detected key (e.g. "i", "V7", "vi").

        Args:
            notes: Optional list of note dicts. If omitted, reads piano roll
                state from disk.

        Returns:
            {
              "key": "C major" | None,
              "chords": [
                  {"time": float, "duration": float, "midi_notes": [..],
                   "label": "Am", "roman": "vi", "function_score": float|None},
                  ...
              ],
              "source": "argument" | "piano_roll_state.json"
            }
        """
        resolved, ppq, source = _resolve_notes(notes)
        result = _analyze_chords(resolved, ppq)
        result["source"] = source
        return result

    @mcp.tool()
    def fl_get_project_summary() -> dict[str, Any]:
        """High-level snapshot: piano-roll content, detected key, chords, and
        suggested genres based on the analysis.

        Combines piano-roll analysis with simple genre suggestions derived
        from key/mode (no transport read here — that lives in fl_get_transport_status).

        Returns:
            {
              "note_count": int,
              "duration_quarter_notes": float,
              "duration_bars": float,
              "key": "...",
              "tonic": "C",
              "mode": "major"|"minor",
              "key_confidence": float,
              "chord_count": int,
              "unique_chords": ["Am", "F", ...],
              "progression_roman": ["vi", "IV", "I", "V"],
              "genre_suggestions": ["reggaeton (minor key fits)", ...],
              "source": "piano_roll_state.json"
            }
        """
        notes, ppq, source = _resolve_notes(None)
        if not notes:
            return {
                "note_count": 0,
                "message": "No notes found in piano roll state. "
                "Run fl_get_piano_roll_state in FL Studio first to refresh state.",
                "source": source,
            }

        key_info = _detect_key(notes, ppq)
        chord_info = _analyze_chords(notes, ppq, detected_key=key_info)

        s = _notes_to_stream(notes, ppq=ppq)
        flat = s.flatten().notes
        max_end = 0.0
        for n in flat:
            end = float(n.offset) + float(n.quarterLength)
            if end > max_end:
                max_end = end

        unique_chord_labels: list[str] = []
        roman_seq: list[str] = []
        for c in chord_info["chords"]:
            if c["label"] and c["label"] not in unique_chord_labels:
                unique_chord_labels.append(c["label"])
            if c.get("roman"):
                roman_seq.append(c["roman"])

        suggestions: list[str] = []
        mode = key_info.get("mode")
        if mode == "minor":
            suggestions.extend(
                [
                    "reggaeton (minor key, dembow groove fits)",
                    "trap latino (dark minor, 808s)",
                    "dembow dominicano (minor vamp + Pow Pow)",
                    "dancehall (minor riddim)",
                ]
            )
        elif mode == "major":
            suggestions.extend(
                [
                    "champeta (major key, palanca guitar)",
                    "pop dancehall (major-key Sean Paul style)",
                ]
            )

        return {
            "note_count": len(notes),
            "duration_quarter_notes": round(max_end, 3),
            "duration_bars": round(max_end / 4.0, 3),
            "key": key_info.get("key"),
            "tonic": key_info.get("tonic"),
            "mode": key_info.get("mode"),
            "key_confidence": key_info.get("confidence"),
            "chord_count": len(chord_info["chords"]),
            "unique_chords": unique_chord_labels,
            "progression_roman": roman_seq,
            "genre_suggestions": suggestions,
            "source": source,
        }
