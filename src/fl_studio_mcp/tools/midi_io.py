"""MIDI file import/export tools.

Read a list of notes from a `.mid` file (`fl_import_midi`) and write a list
of notes to a `.mid` file (`fl_export_midi`). Format matches what
fl_send_notes expects: midi/time(quarter notes)/duration(quarter notes)/velocity(0-1).

Uses `mido` (already a project dependency).
"""

from __future__ import annotations

import json
import platform
from pathlib import Path
from typing import TYPE_CHECKING, Any

import mido

if TYPE_CHECKING:
    from fastmcp import FastMCP


# ---------------------------------------------------------------------------
# Path helpers (reused from theory module pattern)
# ---------------------------------------------------------------------------


def _candidate_state_paths() -> list[Path]:
    home = Path.home()
    relative = (
        Path("Image-Line") / "FL Studio" / "Settings" / "Piano roll scripts"
    ) / "piano_roll_state.json"
    bases: list[Path] = []
    if platform.system() in ("Darwin", "Windows"):
        bases.append(home / "Documents")
        bases.append(home / "OneDrive" / "Documents")
        bases.append(home / "OneDrive" / "Documentos")
    else:
        bases.append(home / ".fl-studio" / "Settings")
    return [b / relative for b in bases]


def _read_piano_roll_state() -> dict[str, Any]:
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
# MIDI conversions
# ---------------------------------------------------------------------------


def _notes_to_mido(
    notes: list[dict[str, Any]],
    ppq: int,
    bpm: float,
    channel: int,
) -> mido.MidiFile:
    """Build a single-track MidiFile from a notes list."""
    mid = mido.MidiFile(ticks_per_beat=ppq, type=1)
    track = mido.MidiTrack()
    mid.tracks.append(track)
    track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm), time=0))
    track.append(mido.MetaMessage("time_signature", numerator=4, denominator=4, time=0))

    # Build event list (note_on, note_off) in absolute ticks then sort.
    events: list[tuple[int, int, mido.Message]] = []  # (abs_ticks, priority, msg)
    for n in notes:
        midi = int(n.get("midi", n.get("number", 60)))
        time_qn = float(n.get("time", 0.0))
        duration_qn = float(n.get("duration", 1.0))
        velocity = n.get("velocity", 0.8)
        if isinstance(velocity, float) and 0.0 <= velocity <= 1.0:
            v_int = int(round(velocity * 127))
        else:
            v_int = int(velocity)
        v_int = max(1, min(127, v_int))
        on_tick = int(round(time_qn * ppq))
        off_tick = on_tick + int(round(duration_qn * ppq))
        # priority: 0 = note_off must come before simultaneous note_on
        on_msg = mido.Message("note_on", note=midi, velocity=v_int, channel=channel)
        off_msg = mido.Message("note_off", note=midi, velocity=0, channel=channel)
        events.append((on_tick, 1, on_msg))
        events.append((off_tick, 0, off_msg))

    events.sort(key=lambda e: (e[0], e[1]))
    last_tick = 0
    for abs_tick, _, msg in events:
        delta = abs_tick - last_tick
        msg.time = max(0, delta)
        track.append(msg)
        last_tick = abs_tick
    track.append(mido.MetaMessage("end_of_track", time=0))
    return mid


def _mido_to_notes(mid: mido.MidiFile) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Convert a MidiFile into a flat note list in quarter-note timing.

    Returns (notes, metadata). Notes are merged across all tracks.
    """
    ppq = mid.ticks_per_beat
    notes_out: list[dict[str, Any]] = []
    bpm: float | None = None
    time_sig: tuple[int, int] | None = None

    for track in mid.tracks:
        abs_tick = 0
        # Track open notes per (channel, midi)
        open_notes: dict[tuple[int, int], tuple[int, int]] = {}  # → (start_tick, velocity)
        for msg in track:
            abs_tick += msg.time
            if msg.is_meta:
                if msg.type == "set_tempo" and bpm is None:
                    bpm = round(mido.tempo2bpm(msg.tempo), 3)
                elif msg.type == "time_signature" and time_sig is None:
                    time_sig = (msg.numerator, msg.denominator)
                continue
            if msg.type == "note_on" and msg.velocity > 0:
                open_notes[(msg.channel, msg.note)] = (abs_tick, msg.velocity)
            elif msg.type in ("note_off", "note_on"):
                # note_on with velocity 0 is also note_off
                key = (msg.channel, msg.note)
                if key in open_notes:
                    start_tick, vel = open_notes.pop(key)
                    duration_ticks = abs_tick - start_tick
                    notes_out.append(
                        {
                            "midi": int(msg.note),
                            "time": round(start_tick / ppq if ppq else 0.0, 4),
                            "duration": round(duration_ticks / ppq if ppq else 0.0, 4),
                            "velocity": round(vel / 127.0, 4),
                            "channel": int(msg.channel),
                        }
                    )

    notes_out.sort(key=lambda n: (n["time"], n["midi"]))
    end_qn = max((n["time"] + n["duration"] for n in notes_out), default=0.0)
    metadata = {
        "ppq": ppq,
        "bpm": bpm,
        "time_signature": list(time_sig) if time_sig else [4, 4],
        "track_count": len(mid.tracks),
        "note_count": len(notes_out),
        "length_quarter_notes": round(end_qn, 4),
    }
    return notes_out, metadata


# ---------------------------------------------------------------------------
# FastMCP registration
# ---------------------------------------------------------------------------


def register_midi_io_tools(mcp: FastMCP) -> None:
    """Register MIDI I/O tools."""

    @mcp.tool()
    def fl_export_midi(
        file_path: str,
        notes: list[dict[str, Any]] | None = None,
        ppq: int = 96,
        bpm: float = 120.0,
        channel: int = 0,
    ) -> dict[str, Any]:
        """Export a list of notes to a Standard MIDI File (.mid).

        Notes use the standard fl_send_notes format (quarter-note timing).
        If `notes` is omitted, reads the current piano_roll_state.json
        (i.e. exports whatever is currently in FL Studio's piano roll —
        you must call fl_get_piano_roll_state first to refresh state).

        Args:
            file_path: Output path (absolute, ending in .mid). Directory
                must exist.
            notes: Optional list of note dicts. If omitted, reads piano roll state.
            ppq: Pulses per quarter note (default 96).
            bpm: Tempo to embed in the file (default 120).
            channel: MIDI channel 0-15 (default 0).

        Returns:
            {"file_path": ..., "metadata": {"note_count", "ppq", "bpm"}}
            or {"error": "..."} on failure.
        """
        if notes is None:
            state = _read_piano_roll_state()
            state_notes = state.get("notes", [])
            if not state_notes:
                return {
                    "error": "No notes provided and piano_roll_state.json is empty. "
                    "Pass `notes` explicitly or run fl_get_piano_roll_state in FL Studio.",
                }
            # State file uses ticks; we need to convert to quarter notes for _notes_to_mido
            state_ppq = int(state.get("ppq", 96)) or 96
            converted: list[dict[str, Any]] = []
            for n in state_notes:
                converted.append(
                    {
                        "midi": int(n.get("midi", n.get("number", 60))),
                        "time": float(n.get("time", 0.0))
                        if "duration" in n
                        else float(n.get("time_ticks", 0)) / state_ppq,
                        "duration": float(n.get("duration", 0.0))
                        if "duration" in n
                        else float(n.get("length_ticks", 0)) / state_ppq,
                        "velocity": float(n.get("velocity", 0.8)),
                    }
                )
            notes = converted

        out_path = Path(file_path)
        if not out_path.parent.exists():
            return {"error": f"Output directory does not exist: {out_path.parent}"}
        if out_path.suffix.lower() != ".mid":
            return {"error": "file_path must end in .mid"}

        try:
            mid = _notes_to_mido(notes, ppq=ppq, bpm=bpm, channel=channel)
            mid.save(str(out_path))
        except Exception as e:
            return {"error": f"Failed to write MIDI file: {e}"}

        ends = (float(n.get("time", 0)) + float(n.get("duration", 0)) for n in notes)
        end_qn = max(ends, default=0.0)
        return {
            "file_path": str(out_path),
            "metadata": {
                "note_count": len(notes),
                "ppq": ppq,
                "bpm": bpm,
                "channel": channel,
                "length_quarter_notes": round(end_qn, 4),
            },
        }

    @mcp.tool()
    def fl_import_midi(file_path: str) -> dict[str, Any]:
        """Read a Standard MIDI File (.mid) and return its notes in
        fl_send_notes format.

        All tracks are merged into one flat note list. Channel info is
        preserved per note (`"channel": int`). Time/duration are in
        quarter notes.

        Args:
            file_path: Input path to a .mid file.

        Returns:
            {
              "notes": [{"midi", "time", "duration", "velocity", "channel"}, ...],
              "metadata": {"ppq", "bpm", "time_signature", "track_count",
                           "note_count", "length_quarter_notes"}
            }
            or {"error": "..."} on failure.
        """
        in_path = Path(file_path)
        if not in_path.exists():
            return {"error": f"File not found: {in_path}"}
        if in_path.suffix.lower() != ".mid":
            return {"error": "file_path must end in .mid"}

        try:
            mid = mido.MidiFile(str(in_path))
        except Exception as e:
            return {"error": f"Failed to parse MIDI file: {e}"}

        notes, metadata = _mido_to_notes(mid)
        return {"notes": notes, "metadata": metadata}
