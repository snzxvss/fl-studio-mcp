# FL Studio MCP Server (Python)

Python MCP server that lets AI assistants control FL Studio — transport, mixer, channels, plugins, and piano roll. Hybrid architecture: MIDI Controller bridge (real-time DAW state) + Piano Roll script bridge (note composition). Windows + macOS.

Specialized for urban music production (reggaeton, dembow, dancehall, trap latino, champeta) with music-theory-aware tools and genre-aware generators.

## Project Context

- **MCP tools** are in `src/fl_studio_mcp/tools/` — registered in `src/fl_studio_mcp/server.py`
- **Utils** are in `src/fl_studio_mcp/utils/` — MIDI bridge, file bridge, keystroke trigger
- **MIDI Controller bridge:** `fl_controller/device_FLStudioMCP.py` — installed inside FL Studio, listens on loopMIDI/IAC port, dispatches commands to `channels`/`mixer`/`transport`/`plugins`/`patterns`
- **Piano Roll bridge:** `scripts/ComposeWithLLM.pyscript` — installed inside FL Studio's Piano Roll scripts dir, processes JSON requests, exports state
- **Agent skills** are in `.claude/skills/` — read these for genre conventions (`genre-*.md`) and theory (`music-theory.md`); the `urban-producer.md` skill is the coordinator
- **JSON contracts** between MCP server and FL Studio bridges must stay stable — both pyscripts depend on them

## Architecture (one MCP, two bridges)

```
Claude ──► MCP Server (Python) ──┬──► loopMIDI/IAC ──► device_FLStudioMCP.py ──► FL Studio API
                                  │                     (transport/mixer/channels/plugins)
                                  │
                                  └──► JSON files + Ctrl+Alt+Y ──► ComposeWithLLM.pyscript ──► Piano Roll API
                                       (mcp_request.json,           (notes: add/delete/clear/state)
                                        piano_roll_state.json)
```

## Key Constraints

- All new code must lint clean: `uv run ruff check .`
- The two bridges run in **isolated Python interpreters** inside FL Studio — they cannot share state. Always pick the right channel:
  - Piano roll operations → file bridge + keystroke trigger
  - Everything else (channels, mixer, transport, plugins, patterns) → MIDI bridge
- Time values in piano roll tools are in **quarter notes** (the bridge converts to ticks)
- Time values in transport tools are typically in **ticks** (FL native)
- Velocity in piano roll: 0.0–1.0. Velocity in real-time channel triggering: 0–127

## Before Modifying the Piano Roll

Always call `fl_get_piano_roll_state` first. Use `mode="add"` by default; only `mode="replace"` when the user explicitly asks to start fresh.

## MIDI Quick Reference

- C4 (middle C) = MIDI 60. Each semitone = +1
- FL Studio displays one octave higher: MIDI 60 shows as C5
- Piano roll durations: 0.25=16th, 0.5=8th, 1=quarter, 2=half, 4=whole
- Piano roll time: `time=0` is beat 1, `time=4` is measure 2 (in 4/4)

## Connection Setup (required before any tool call)

1. FL Studio must be running with the project file loaded
2. **MIDI Controller script** must be active: FL Studio → Options → MIDI Settings → enable the loopMIDI/IAC input → assign `FLStudioMCP` controller
3. **Piano Roll script** must be loaded once per session: open Piano Roll → Tools → Scripting → ComposeWithLLM
4. Server connects via `fl_connect()` — verify with `fl_connection_status()`

## Tool Catalog (57 tools across 7 subsystems)

- **Transport (7):** `fl_play`, `fl_stop`, `fl_record`, `fl_get_transport_status`, `fl_set_song_position`, `fl_get_song_length`, `fl_set_loop_mode`, `fl_set_playback_speed`
- **Mixer (11):** `fl_get_mixer_track_count`, `fl_get_mixer_track_info`, `fl_get_all_mixer_tracks`, `fl_set_track_volume`, `fl_set_track_pan`, `fl_mute_track`, `fl_solo_track`, `fl_arm_track`, `fl_set_track_name`, `fl_set_track_color`, `fl_set_stereo_separation`
- **Channels (15+):** info, volume, pan, mute, solo, select, color, route_to_mixer, real-time `fl_trigger_note`, step sequencer (`fl_get_grid_bit`, `fl_set_grid_bit`, `fl_get_step_sequence`, `fl_set_step_sequence`)
- **Plugins (10):** valid, name, params (get/set/list), preset navigation, color
- **Piano Roll (8):** `fl_send_notes`, `fl_send_chord`, `fl_delete_notes`, `fl_clear_piano_roll`, `fl_get_piano_roll_state`, `fl_trigger_script`, `fl_get_piano_roll_info`, `fl_clear_request_queue`
- **Connection (2):** `fl_connect`, `fl_connection_status`

For exact signatures see `src/fl_studio_mcp/tools/*.py`.

## Note Properties (Piano Roll)

The state export already exposes all FL note properties: `number, time, length, velocity, pan, color, fcut, fres, slide, porta, pitchofs, selected, muted`. The current `fl_send_notes` accepts only `midi/duration/time/velocity` — extending it to write the rest is a planned task (see Roadmap, F1).

## Roadmap (where new work goes)

| Phase | Scope | Status |
|-------|-------|--------|
| F0    | Fork karlo, validate, register | Done |
| F1    | Music theory analysis tools (`fl_analyze_chord_progression`, `fl_detect_key_and_scale`, `fl_get_project_summary`) using `music21` | Done |
| F2    | Genre-aware generators (`fl_generate_drum_pattern`, `fl_generate_chord_progression`, `fl_generate_bassline_from_chords`, `fl_generate_palanca_guitar`, `fl_generate_dembow_powpow`, `fl_list_genre_templates`) | Done |
| F3    | MIDI transformations (`fl_transpose_notes`, `fl_quantize_notes`, `fl_humanize_notes`, `fl_voice_lead_chords`, `fl_arpeggiate_chord`) | Done |
| F4    | MIDI I/O (`fl_export_midi`, `fl_import_midi`) using `mido` | Done |
| F5    | Extended note properties in `fl_send_notes` (pan, color, fcut, fres, slide, porta, pitchofs, muted) — accepted by both MCP and pyscript bridge | Done |
| F6    | `fl_send_notes_to_channel` — selects channel + focuses its piano roll automatically before triggering, eliminating manual clicks for multi-channel composition. Adds `channels.selectAndShowPianoRoll` to the MIDI controller bridge. | Done |

Total tool count after F0–F6: **74 tools** across 9 modules (transport, mixer, channels, plugins, piano_roll, theory, generators, transforms, midi_io).

## Where to Find Things

- Skills (genre conventions + theory + coordinator) → `.claude/skills/`
- Tool source → `src/fl_studio_mcp/tools/`
- Bridge protocol (MIDI side) → `fl_controller/device_FLStudioMCP.py`
- Bridge protocol (piano roll side) → `scripts/ComposeWithLLM.pyscript`
- Setup scripts → `scripts/setup.sh`, `scripts/install_mcp_for_claude.sh`
- FL Studio Python API stubs → installed as dev dep `fl-studio-api-stubs`
