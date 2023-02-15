from typing import Callable

import panel as pn
import panel.widgets as pnw


# class NoFileSelected(Exception):
#     def __init__(self):
#         message = 'Please select Excel file'
#         super().__init__(message)


def excel_file_download(callback: Callable, filename: str) -> pnw.FileDownload:
    return pnw.FileDownload(
        auto=True,
        callback=callback,
        filename=filename,
        button_type='primary',
        label='Download analyzed data',
        name='download',
    )


def file_download_card() -> pn.Card:
    return pn.Card()


# class ExcelDownloader(Viewer):
#     def __init__(
#         self,
#         **params,
#     ):
#         super().__init__(**params)
#         self._download_widget = excel_file_download()

#         self._button = pnw.Button(name='Upload', button_type='primary', width=150)
#         self._status = pnw.StaticText()

#     def bind_button(self, function: Callable[..., None]) -> None:
#         self._button.on_click(function)

#     def show_error(self, error: Exception) -> None:
#         self._button.button_type = 'warning'
#         self._status.value = f'Error: {error.args[0]}'

#     def upload_success(self) -> None:
#         self._status.value = 'Success!'
#         self._button.button_type = 'success'
#         time.sleep(0.5)

#     @property
#     def input_value(self):
#         return self._input_widget.value

#     def __panel__(self) -> pn.panel:
#         return pn.Card(
#             self._input_widget,
#             pn.Row(self._button, align='center'),
#             pn.Row(self._status, align='center'),
#             collapsible=False,
#             title='Upload Plate Reader Data',
#         )
