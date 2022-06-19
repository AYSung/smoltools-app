import sys

import panel as pn

import fret0
import albatrosy


def main() -> None:
    APPS = {
        'fret0': fret0.app,
        'albaTROSY': albatrosy.app,
    }

    PORT = int(sys.argv[1])

    # INDEX = str(paths.ROOT / 'index.html')
    # STATIC_DIRECTORIES = {'assets': paths.ASSETS}

    pn.serve(
        APPS,
        address='0.0.0.0',
        websocket_origin='smoltools.herokuapp.com',
        port=PORT,
        # index=INDEX,
        # static_dirs=STATIC_DIRECTORIES,
    )


if __name__ == '__main__':
    main()
