import os

import panel as pn

import fret0
import albatrosy
from utils import paths


def main() -> None:
    INDEX = str(paths.ROOT / 'index.html')

    APPS = {
        'fret0': fret0.app,
        'albaTROSY': albatrosy.app,
    }

    ON_HEROKU = os.environ.get('ON_HEROKU')
    if ON_HEROKU:
        PORT = int(os.environ.get('PORT'))
        server_config = {
            'address': '0.0.0.0',
            'websocket_origin': 'smoltools.herokuapp.com',
            'port': PORT,
            'index': INDEX,
        }
    else:
        PORT = 5006
        STATIC_DIRECTORIES = {'assets': paths.ASSETS}

        server_config = {
            'port': PORT,
            'index': INDEX,
            'static_dirs': STATIC_DIRECTORIES,
        }

    pn.serve(
        APPS,
        **server_config,
    )


if __name__ == '__main__':
    main()
