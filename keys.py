from libqtile.config import Key, Click, Drag, Screen, Group, Match, Rule
from libqtile.command import lazy
from libqtile import layout, bar, widget
from extra import (SwitchToWindowGroup, check_restart,
                   terminal, MoveToOtherScreenGroup, SwitchGroup)
from screens import PRIMARY_SCREEN, SECONDARY_SCREEN
from system import get_hostconfig


def get_keys(mod, groups):
    is_laptop = get_hostconfig('laptop')
    left_termkey = get_hostconfig('left_termkey')
    right_termkey = get_hostconfig('right_termkey')
    left_remote_termkey = get_hostconfig('left_remote_termkey')
    right_remote_termkey = get_hostconfig('right_remote_termkey')
    monitor_key = get_hostconfig('monitor_key')
    keys = [
        # Switch between windows in current stack pane
        ([mod], "k",
         lazy.layout.up(),
         lazy.layout.previous().when('monadtall')),
        ([mod], "j", 
         lazy.layout.down(),
         lazy.layout.next().when('monadtall')),

        # Move windows up or down in current stack
        ([mod, "shift"], "k", lazy.layout.shuffle_up()),
        ([mod, "shift"], "j", lazy.layout.shuffle_down()),

        ([mod], "h", 
         lazy.layout.up().when('monadtall'),
         lazy.layout.previous()),
        ([mod], "l", 
         lazy.layout.down().when('monadtall'),
         lazy.layout.next()),

        ([mod, "shift"], "l", 
         lazy.layout.client_to_next().when('stack'),
         lazy.layout.increase_ratio().when('tile')),
        ([mod, "shift"], "h", 
         lazy.layout.client_to_previous().when('stack'),
         lazy.layout.decrease_ratio().when('tile')),

        ([mod, "shift"], "space", lazy.layout.flip().when('monadtall'),
         lazy.layout.rotate().when('tile')),

        # Swap panes of split stack
        # toggle between windows just like in unity with 'alt+tab'
        (["mod1", "shift"], "Tab", lazy.layout.down()),
        (["mod1"], "Tab", lazy.layout.up()),
        ([mod, "shift"], "comma",
         lazy.function(MoveToOtherScreenGroup(prev=True))),
        ([mod, "shift"], "period",
         lazy.function(MoveToOtherScreenGroup(prev=False))),
        # Toggle between split and unsplit sides of stack.
        # Split = all windows displayed
        # Unsplit = 1 window displayed, like Max layout, but still with
        # multiple stack panes
        ([mod, "shift"], "Return", lazy.layout.toggle_split()),
        (["shift", mod], "q", lazy.shutdown()),
        # Toggle between different layouts as defined below
        ([mod], "space",    lazy.nextlayout()),
        ([mod], "q",      lazy.window.kill()),
        # Key([mod, "control"], "r", lazy.restart()),
        ([mod, "control"], "r", lazy.function(check_restart)),
        ([mod], "Right", lazy.screen.nextgroup()),
        ([mod], "Left", lazy.screen.prevgroup()),
        ([], "F6",      lazy.function(SwitchGroup("6", PRIMARY_SCREEN))),

        ([mod], "m", lazy.group.setlayout('max')),
        ([mod], "t", lazy.group.setlayout('tile')),
        ([mod], "s", lazy.group.setlayout('stack')),
        ([mod], "x", lazy.group.setlayout('monadtall')),
        ([mod], "f", lazy.window.toggle_floating()),
        #([mod], "t", lazy.group.setlayout('xmonad-tall')),

        # APP LAUNCHERS
        #([mod], "r", lazy.spawncmd()),
        ([mod], "F2", lazy.spawn("dmenu_run -f -l 20")),
        ([mod], "r", lazy.spawncmd()),
        ([mod], "Return", lazy.spawn("st")),
        ([mod, "shift"], "b", lazy.spawn("conkeror")),
        ([mod, "shift"], "g", lazy.spawn("google-chrome-stable")),
        ([mod, "control"], "l", lazy.spawn("xscreensaver-command -lock")),
        #([], "3270_PrintScreen", lazy.spawn("ksnapshot")),
        ([mod, "shift"], "s", lazy.spawn("ksnapshot")),
        ([mod, "control"], "Escape", lazy.spawn("xkill")),
        ([], "F1",      lazy.function(SwitchGroup("1"))),
        ([], "F2",      lazy.function(SwitchGroup("2"))),
        ([], "F10",      lazy.function(SwitchGroup("4", 0))),
        ([], "F9", lazy.function(SwitchGroup("3", 0))),

        ([], left_termkey, lazy.function(
            SwitchToWindowGroup(
                groups, "left", title=[".*left.*"], cmd=terminal("left"),
                wm_class=["InputOutput"], screen=PRIMARY_SCREEN))),

        ([], right_termkey, lazy.function(
            SwitchToWindowGroup(
                groups, "right", cmd=terminal("right"), title=[".*right.*"],
                wm_class=["InputOutput"], screen=SECONDARY_SCREEN))),

        ([mod], left_remote_termkey, lazy.function(
            SwitchToWindowGroup(
                groups, "remote_left", cmd="st -t remote_left ",
                screen=PRIMARY_SCREEN, title=[".*remote_left.*"],
                wm_class=["InputOutput"]))),

        ([mod], right_remote_termkey, lazy.function(
            SwitchToWindowGroup(
                groups, "remote_right", cmd="st -t remote_right ",
                screen=SECONDARY_SCREEN, title=[".*remote_right.*"],
                wm_class=["InputOutput"]))),

        ([], monitor_key, lazy.function(
            SwitchToWindowGroup(
                groups, "monitor", cmd=terminal("monitor"),
                title=[".*monitor.*"], SECONDARY_SCREEN,
                wm_class=["InputOutput"]))),
    ]
    laptop_keys = [
        # laptop keys
        ([], "XF86MonBrightnessUp", lazy.spawn("sudo samctl.py -s up")),
        ([], "XF86MonBrightnessDown", lazy.spawn(
            "sudo samctl.py -s down")),
        ([], "XF86KbdBrightnessUp", lazy.spawn("sudo samctl.py -k up")),
        ([], "XF86KbdBrightnessDown", lazy.spawn(
            "sudo samctl.py -k down")),
        ([], "XF86AudioLowerVolume", lazy.spawn("sudo samctl.py -k up")),
        ([], "XF86AudioRaiseVolume", lazy.spawn(
            "sudo samctl.py -v down")),
        ([], "XF86WLAN", lazy.spawn(
            "nmcli con up id Xperia\ Z1\ Network --nowait")),
    ]
    if is_laptop:
        keys.extend(laptop_keys)
    return [Key(*k) for k in keys]
