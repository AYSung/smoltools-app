import os

import panel as pn

from albatrosy.app import app as albatrosy_app
from fret0.app import app as fret0_app
from utils import paths


def main() -> None:
    INDEX = str(paths.SOURCE / 'index.html')

    APPS = {
        'Fret0': fret0_app,
        'AlbaTROSY': albatrosy_app,
    }

    ON_HEROKU = os.environ.get('ON_HEROKU')
    if ON_HEROKU:
        APP_NAME = os.environ.get('HEROKU_APP_NAME', 'smoltools')
        PORT = int(os.environ.get('PORT'))
        server_config = {
            'address': '0.0.0.0',
            'websocket_origin': f'{APP_NAME}.herokuapp.com',
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
