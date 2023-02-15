from typing import Callable

import panel.widgets as pnw


def excel_file_download(callback: Callable, filename: str) -> pnw.FileDownload:
    return pnw.FileDownload(
        auto=True,
        callback=callback,
        filename=filename,
        button_type='primary',
        label='Download analyzed data',
    )
