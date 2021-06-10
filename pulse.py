import re
from typing import Any, List
from pulsectl.pulsectl import Pulse

class PulseRepresentative:
    pulse: Pulse
    active_sink_input_idxs_at_start: List[Any]
    restore_sink_name: str

    def __init__(self, restore_sink_name) -> None:
        self.pulse = Pulse("sink-switch")
        self.active_sink_input_idxs_at_start = self.get_currently_active_sink_inputs()
        self.restore_sink_name = restore_sink_name

    def get_currently_active_sink_inputs(self):
        return [sink_input.index for sink_input in self.pulse.sink_input_list()]

    def set_mute_sink_input_idxs(self, idxs: List[Any], mute_state: bool):
        for input_idx in idxs:
            self.pulse.sink_input_mute(input_idx, mute_state)

    def change_default_sink_to(self, sink):
        self.pulse.default_set(sink)

    def get_sink_with_description_like(self, sink_name_pattern_regex):
        sinks = self.pulse.sink_list()
        sink_names = [sink.description for sink in sinks]
        matches = [True if re.match(sink_name_pattern_regex, sink_name) else False for sink_name in sink_names]
        idx = matches.index(True)
        return sinks[idx]

    def clean_up(self):
        # Restore original default sink
        restore_sink = self.get_sink_with_description_like(self.restore_sink_name)
        self.change_default_sink_to(restore_sink)
        # Unmute all muted programs
        self.set_mute_sink_input_idxs(self.active_sink_input_idxs_at_start, False)
        self.pulse.close()