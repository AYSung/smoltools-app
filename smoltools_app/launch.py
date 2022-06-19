import os

import panel as pn

import fret0
import albatrosy
from smoltools_app.utils import paths


def main() -> None:
    APPS = {
        'fret0': fret0.app,
        'albaTROSY': albatrosy.app,
    }

    # INDEX = str(paths.ROOT / 'index.html')
    STATIC_DIRECTORIES = {'assets': paths.ASSETS}

    ON_HEROKU = os.environ.get('ON_HEROKU')
    if ON_HEROKU:
        PORT = int(os.environ.get('PORT'))
        server_config = {
            'address': '0.0.0.0',
            'websocket_origin': 'smoltools.herokuapp.com',
            'port': PORT,
        }
    else:
        PORT = 5006
        server_config = {'port': PORT}

    pn.serve(
        APPS,
        # index=INDEX,
        static_dirs=STATIC_DIRECTORIES,
        **server_config,
    )


if __name__ == '__main__':
    main()
