from libqtile.config import Key, Click, Drag, Screen, Group, Match, Rule
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from themes import current_theme
import logging

log = logging.getLogger("qtile.screen")


class MultiScreenGroupBox(widget.GroupBox):
    def __init__(self, **config):
        widget.GroupBox.__init__(self, **config)
        self.namemap = config.get('namemap',{})

    def draw(self):
        self.drawer.clear(self.background or self.bar.background)

        offset = 0
        for i, g in enumerate(self.qtile.groups):
            gtext = g.name
            log.warn(gtext)
            if gtext in self.namemap:
                gtext = self.namemap[gtext]
            else:
                continue

            is_block = (self.highlight_method == 'block')

            bw = self.box_width([g])
            if g.screen:
                if self.bar.screen.group.name == g.name:
                    if self.qtile.currentScreen == self.bar.screen:
                        border = self.this_current_screen_border
                    else:
                        border = self.this_screen_border
                else:
                    border = self.other_screen_border
            elif self.group_has_urgent(g) and \
                    self.urgent_alert_method in ('border', 'block'):
                border = self.urgent_border
                if self.urgent_alert_method == 'block':
                    is_block = True
            else:
                border = self.background or self.bar.background

            if self.group_has_urgent(g) and self.urgent_alert_method == "text":
                text = self.urgent_text
            elif g.windows:
                text = self.active
            else:
                text = self.inactive

            self.drawbox(
                self.margin_x + offset,
                gtext,
                border,
                text,
                self.rounded,
                is_block,
                bw - self.margin_x * 2 - self.padding_x * 2
            )
            offset += bw
        self.drawer.draw(self.offset, self.width/2)

#GroupBox = widget.GroupBox
GroupBox = MultiScreenGroupBox


def get_screens(num_screens=1):
    screens = []
    default_params = dict(
        font=current_theme['font'],
        fontsize=10,
        padding=1,
        borderwidth=1,
    )

    groupbox_params = dict(
        urgent_alert_method='text',
        padding=1,
        borderwidth=1,
        rounded=False,
        highlight_method='block',
        this_current_screen_border=current_theme['border'])

    groupbox_params.update(default_params)
    prompt_params = default_params
    systray_params = default_params
    layout_textbox_params = dict(name="default", text="default config")
    layout_textbox_params.update(default_params)
    layout_textbox_params['padding'] = 2
    windowname_params = default_params
    systray_params = default_params
    clock_params = dict(fmt='%Y-%m-%d %a %I:%M %p')
    clock_params.update(default_params)
    pacman_params = default_params
    notify_params = default_params
    bitcointicker_params = default_params
    batteryicon_params = default_params

    gb1 = dict([(str(i), str(i)) for i in range(1,10)])
    gb1['right'] = "term"
    gb2 = dict([(str(i), str(i-10)) for i in range(11,20)])
    gb2['left'] = "term"
    screens.append(Screen(
        bar.Bar([
            GroupBox(namemap=gb1, **groupbox_params),
            widget.Sep(),
            widget.Prompt(**prompt_params),
            widget.WindowName(**windowname_params),
            widget.TextBox(**layout_textbox_params),
            widget.Sep(),
            widget.BitcoinTicker(**bitcointicker_params),
            widget.Sep(),
            widget.Pacman(**pacman_params),
            widget.Sep(),
            widget.Notify(**notify_params),
            widget.Sep(),
            widget.BatteryIcon(**batteryicon_params),
            widget.Sep(),
            widget.Systray(**systray_params),
            widget.Clock(**clock_params),

        ], 18)))
    if num_screens > 1:
        screens.append(Screen(
            bar.Bar([
                GroupBox(namemap=gb2, **groupbox_params),
                widget.Sep(),
                widget.WindowName(**windowname_params),
                widget.TextBox(**layout_textbox_params),
                widget.Sep(),
                widget.Clock(**clock_params),
            ], 18)))
    return screens
