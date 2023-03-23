import logging
from libqtile.bar import Bar as QBar
from libqtile import bar, hook, pangocffi
from taqtile.themes import current_theme, default_params

logger = logging.getLogger("taqtile")


class Bar(QBar):
    default_background = None
    defaults = [
        ("focused_background", "#000000", "Background colour."),
    ]

    def __init__(self, widgets, **config):
        bar_height = config.pop("bar_height", 8) or 8
        super().__init__(widgets, int(bar_height), **config)
        self.add_defaults(Bar.defaults)
        self.default_background = self.background
        self.default_foreground = self.foreground
        hook.subscribe.current_screen_change(self._hook_current_screen_change)

    def _hook_current_screen_change(self, *args):
        if not self.qtile:
            return
        logger.debug(
            f"current_screen_change current_screen: {self.qtile.current_screen.index} self.screen:{self.screen.index}"
        )

        if self.screen == self.qtile.current_screen:
            self.background = self.focused_background
        else:
            self.background = self.default_background
        self._configure(self.qtile, self.screen, reconfigure=True)
        self.draw()
