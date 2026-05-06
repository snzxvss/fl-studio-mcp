---
name: fl-studio-api
description: FL Studio scripting API reference for both Piano Roll and MIDI Controller environments
---

# FL Studio API Reference

## Two Scripting Environments

FL Studio has two separate Python contexts. They cannot access each other.

### 1. Piano Roll Scripts (`flpianoroll` module)

Used by: `ComposeWithLLM.pyscript`

```python
import flpianoroll as flp

# Read
flp.score.noteCount          # Total notes
flp.score.getNote(index)     # Get note object
flp.score.PPQ                # Pulses per quarter note

# Write
note = flp.Note()
note.number = 60             # MIDI number
note.time = 0                # Ticks
note.length = 96             # Ticks
note.velocity = 0.8          # 0.0-1.0
flp.score.addNote(note)

# Delete (iterate backward!)
flp.score.deleteNote(index)
```

Note properties: number, time, length, velocity, pan, color, fcut, fres, slide, porta

### 2. MIDI Controller Scripts

Separate modules — NOT available in piano roll scripts:

```python
import channels    # Channel rack
import mixer       # Mixer
import transport   # Play/stop/record
import plugins     # Plugin parameters
import device      # MIDI device I/O
import ui          # Window navigation
```

Key functions:
- `plugins.setParamValue(value, paramIndex, channelIndex, slotIndex)`
- `plugins.getParamName(paramIndex, channelIndex, slotIndex)`
- `plugins.nextPreset(channelIndex, slotIndex)`
- `mixer.setTrackVolume(trackIndex, volume)`
- `mixer.setTrackPan(trackIndex, pan)`
- `channels.selectChannel(index)`
- `transport.start()` / `transport.stop()` / `transport.record()`

Full API reference: https://il-group.github.io/FL-Studio-API-Stubs/midi_controller_scripting/
