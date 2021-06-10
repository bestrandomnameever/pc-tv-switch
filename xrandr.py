import re
import subprocess

# class XRandrConfig:

# TODO expand if neccesary, all pretty hardcoded atm
class XRandr:
    restore_xrandr_cmd: str
    restore_resolution: str

    def __init__(self, restore_xrandr_cmd, restore_resolution) -> None:
        self.restore_xrandr_cmd = restore_xrandr_cmd
        self.restore_resolution = restore_resolution

    # def __get_current_connected_monitors_and_options(self):
    #     status_proc = subprocess.run(["xrandr", "-q"], stdout=subprocess.PIPE)
    #     output = status_proc.stdout.decode('utf-8')

    # def get_current_dimensions(self):
    #     pass

    def query_xdpyinfo(self) -> str:
        status_proc = subprocess.run(["xdpyinfo"], stdout=subprocess.PIPE)
        output = status_proc.stdout.decode('utf-8')

        return output

    def check_if_current_monitor_matches(self, resolution: str):
        xdpyinfo_query_output = self.query_xdpyinfo()
        return len(re.findall(f"dimensions:\s*{resolution} pixels", xdpyinfo_query_output)) == 1

    def run_xrandr(self, xrandr_command):
        subprocess.run(xrandr_command.split(" "))

    def rerun_xrandr_till_it_sticks(self, xrandr_command: str, expected_resolution: str):
        if not self.check_if_current_monitor_matches(expected_resolution):
            self.run_xrandr(xrandr_command)
            self.rerun_xrandr_till_it_sticks(xrandr_command, expected_resolution)
    
    def clean_up(self):
        # Return to inital display configuration with xrandr
        self.rerun_xrandr_till_it_sticks(self.restore_xrandr_cmd, self.restore_resolution)