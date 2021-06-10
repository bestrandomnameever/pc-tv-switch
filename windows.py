import time
import gi
gi.require_version('Wnck', '3.0')
from typing import Any, List
from gi.repository import Wnck as wnck

class Windows():
    screen: Any
    initial_windows_and_states: List[Any]

    def __init__(self) -> None:
        self.screen = wnck.Screen.get_default()
        self.screen.force_update()
        self.initial_windows_and_states = self.get_windows_and_current_states()

    def get_windows_and_current_states(self):
        # self.scrn.force_update()
        windows = self.screen.get_windows_stacked()

        windows = [{
            "pid": window.get_pid(),
            "name": window.get_name(),
            "workspace": window.get_workspace(),
            "active": window.is_active,
            "geometry": window.get_geometry(),
            "maximized": window.is_maximized(),
            "minimized": window.is_minimized(),
            "window": window

        } for window in windows]

        return windows

    def filter_windows_on_minimized_state(self, windows, minimized_state: bool):
        return [window_obj["window"] for window_obj in windows if window_obj['minimized'] == minimized_state] 

    def minimize_all_open_windows(self, windows):
        for window in self.filter_windows_on_minimized_state(windows, False):
            window.minimize()
    
    def unminimize_all_windows(self, windows):
        for window in windows:
            window.unminimize(int(time.time()))

    def clean_up(self):
        # Reset windows to orginal state on initial display configuration
        originally_unminimized_windows = self.filter_windows_on_minimized_state(self.initial_windows_and_states, False)
        self.unminimize_all_windows(originally_unminimized_windows)