import os

import panel as pn

from apps import fret0, albatrosy
from utils import paths


def main() -> None:
    INDEX = str(paths.SOURCE / 'index.html')

    APPS = {
        'Fret0': fret0.app,
        'AlbaTROSY': albatrosy.app,
    }

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
        STATIC_DIRECTORIES = {'assets': paths.ASSETS}

        server_config = {
            'port': PORT,
            'static_dirs': STATIC_DIRECTORIES,
        }

    pn.serve(
        APPS,
        index=INDEX,
        **server_config,
    )


if __name__ == '__main__':
    main()
