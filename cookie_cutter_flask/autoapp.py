# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from cookie_cutter_flask.app import create_app
from cookie_cutter_flask.settings import DevConfig, ProdConfig

CONFIG = DevConfig# if get_debug_flag() else ProdConfig

app = create_app(CONFIG)

if __name__ == "__main__":
    app.run()