import logging
import os
import sys

from sliderepl import Deck

banner_top = (
    "!!{letstalk} ░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒█████████████"
    "!!{logo1} SQL!!{logo2}Alchemy !!{logo3}2.0"
    "!!{letstalkul} - Let's Talk "
    "!!{letstalk}█████████████▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░\n"
)



class SADeck(Deck):
    style_lookup = {
        "box": ("blue",),
        "slidenum": ("blue",),
        "titletext": ("magenta", None, ["bold"]),
        "intro_line": ("dark_grey", None, ["dark"]),
        "bullet": ("dark_grey",),
        "boldbullet": ("dark_grey", None, ["bold"]),
        "red": ("red",),
        "yellow": ("yellow",),
        "letstalk": ("blue", None, []),
        "plain": (),

        "logo1": ("dark_grey", "on_light_grey", ["bold"]),
        "logo2": ("red", "on_light_grey", ["bold"]),
        "logo3": ("yellow", "on_light_grey", ["bold"]),
        "letstalkul": ("blue", "on_light_grey", ["bold"]),

    }

    expose = Deck.expose + ("echo",)

    def __init__(self, path=None, echo_on=True, **options):
        Deck.__init__(self, path, **options)
        self.start_with_echo = echo_on
        self.banner_top = self._color(banner_top, "plain")

    def start(self):
        logging_config = {
            "format": "[SQL]: %(message)s",
            "stream": self.highlight_stdout("sql"),
        }
        logging.basicConfig(**logging_config)

        sys.path.insert(0, os.path.dirname(self.path))

        self._set_echo(self.start_with_echo and "on" or "off")

    def echo(self):
        """Toggle SQL echo on or off."""
        self._set_echo(not self._echo)

    def _set_echo(self, value):
        self._echo = value
        log = logging.getLogger("sqlalchemy.engine")
        if self._echo:
            log.setLevel(logging.INFO)
        else:
            log.setLevel(logging.WARN)
        print("%% SQL echo is now %s" % (self._echo and "ON" or "OFF"))


deck = SADeck
