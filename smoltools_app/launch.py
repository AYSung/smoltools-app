import panel as pn

import fret0
import albatrosy


def main() -> None:
    APPS = {
        'fret0': fret0.app,
        'albaTROSY': albatrosy.app,
    }

    PORT = 5006
    # TODO: index page
    # INDEX = str(paths.ROOT / 'index.html')
    # STATIC_DIRECTORIES = {'assets': paths.ASSETS}

    pn.serve(
        APPS,
        port=PORT,
        # index=INDEX,
        # static_dirs=STATIC_DIRECTORIES,
    )


if __name__ == '__main__':
    main()
