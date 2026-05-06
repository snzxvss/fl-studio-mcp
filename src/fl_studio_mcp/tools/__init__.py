"""FL Studio MCP tools."""

from fl_studio_mcp.tools.channels import register_channel_tools
from fl_studio_mcp.tools.generators import register_generator_tools
from fl_studio_mcp.tools.midi_io import register_midi_io_tools
from fl_studio_mcp.tools.mixer import register_mixer_tools
from fl_studio_mcp.tools.piano_roll import register_piano_roll_tools
from fl_studio_mcp.tools.plugins import register_plugin_tools
from fl_studio_mcp.tools.theory import register_theory_tools
from fl_studio_mcp.tools.transforms import register_transform_tools
from fl_studio_mcp.tools.transport import register_transport_tools

__all__ = [
    "register_transport_tools",
    "register_mixer_tools",
    "register_channel_tools",
    "register_plugin_tools",
    "register_piano_roll_tools",
    "register_theory_tools",
    "register_generator_tools",
    "register_transform_tools",
    "register_midi_io_tools",
]
