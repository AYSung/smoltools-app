import os

import panel as pn

import fret0
import albatrosy_monomer
import albatrosy_dimer
from utils import paths


def main() -> None:
    INDEX = str(paths.SOURCE / 'index.html')

    APPS = {
        'Fret0': fret0.app,
        'AlbaTROSY_monomer': albatrosy_monomer.app,
        'AlbaTROSY_dimer': albatrosy_dimer.app,
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
