import panel as pn

import fret0
from utils import config


def main() -> None:
    config.configure_panel_extensions()
    config.configure_plotting_libraries()

    APPS = {
        'fret0': fret0.app,
    }

    PORT = 5006
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
