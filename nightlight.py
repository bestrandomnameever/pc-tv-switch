import subprocess
import re

class NightLight:
    original_state: bool
    current_state: bool

    def __init__(self) -> None:
        self.current_state = self.is_night_switch_on()
        self.original_state = self.current_state

    def is_night_switch_on(self) -> bool:
        dconf_night_light_query = subprocess.check_output("dconf read /org/gnome/settings-daemon/plugins/color/night-light-enabled".split(" "))
        dconf_night_light_query_str = dconf_night_light_query.decode("utf8")
        return False if re.match(r"true", dconf_night_light_query_str) is None else True

    def set_night_switch(self, desired_state: bool):
        state_string = "true" if desired_state else "false"
        subprocess.run(f"dconf write /org/gnome/settings-daemon/plugins/color/night-light-enabled {state_string}".split(" "))
        self.current_state = desired_state

    def clean_up(self):
        if self.original_state != self.current_state:
            self.set_night_switch(self.original_state)