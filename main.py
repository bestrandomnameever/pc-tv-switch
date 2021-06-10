from pulse import PulseRepresentative
from xrandr import XRandr
from windows import Windows
# from pulsectl.pulsectl import Pulse
from nightlight import NightLight
# import gi
# from pulsectl.pulsectl import Pulse
# gi.require_version('Wnck', '3.0')
# from gi.repository import Wnck as wnck

import re
import subprocess
import time
import signal

TV_RESOLUTION = "3840x2160"
TV_XRANDR_COMMAND = "xrandr --output DVI-D-0 --off --output HDMI-0 --primary --mode 3840x2160 --pos 0x0 --rotate normal --output DP-0 --off --output DP-1 --off --output DP-2 --off --output DP-3 --off --output DP-4 --off --output DP-5 --off"
COMPUTER_RESOLUTION = "3440x1440"
COMPUTER_XRANDR_COMMAND = "xrandr --output HDMI-0 --off --output DP-0 --primary --mode 3440x1440 --pos 0x0 --rotate normal"
COMPUTER_SINK_NAME = r"OriGen G2  Digital Stereo \(IEC958\)"
TV_SINK_NAME = r"GP104 High Definition Audio Controller Digital Stereo"

nightlight: NightLight
pulse: PulseRepresentative
windows: Windows
xrandr: XRandr

def cleanup():
    pulse.clean_up()
    xrandr.clean_up()
    nightlight.clean_up()
    windows.clean_up()

def elegant_shutoff():
    # Kill the running 
    cleanup()

# The actual process

# Temporarily ignore SIGINTs
signal.signal(signal.SIGINT, cleanup)

# Minimize all currently open windows 
windows = Windows()
current_windows = windows.get_windows_and_current_states()
windows.minimize_all_open_windows(current_windows)

# Nightlight generates a green overlay on the tv so switch off while in tv-mode
nightlight = NightLight()
if nightlight.current_state == True:
    nightlight.set_night_switch(False)

# Switch dispay to tv with xrandr
xrandr = XRandr(COMPUTER_XRANDR_COMMAND, COMPUTER_RESOLUTION)
xrandr.rerun_xrandr_till_it_sticks(TV_XRANDR_COMMAND, TV_RESOLUTION)

pulse = PulseRepresentative(COMPUTER_SINK_NAME)
pulse.set_mute_sink_input_idxs(pulse.get_currently_active_sink_inputs(), True)
pulse.change_default_sink_to(pulse.get_sink_with_description_like(TV_SINK_NAME))

# Start pegasus in "background"
process = subprocess.Popen(["pegasus-fe", "--disable-menu-reboot", "--disable-menu-shutdown"])

# Monitor if pegasus has exited yet 
while process.poll() is None:
    time.sleep(0.5)
    # Check if something has managed to fuck up xrandr (ge. game going fullscreen)
    # And try to restore xrandr
    xrandr.rerun_xrandr_till_it_sticks(TV_XRANDR_COMMAND, TV_RESOLUTION)

cleanup()