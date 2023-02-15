from typing import Callable

import panel as pn
from panel.viewable import Viewer
import panel.widgets as pnw
import time


class NoFileSelected(Exception):
    def __init__(self):
        message = 'Please select Excel file'
        super().__init__(message)


def excel_file_input() -> pnw.FileInput:
    return pnw.FileInput(accept='.xls,.xlsx')


class ExcelLoader(Viewer):
    def __init__(
        self,
        **params,
    ):
        super().__init__(**params)
        self._input_widget = excel_file_input()

        self._button = pnw.Button(name='Upload', button_type='primary', width=150)
        self._status = pnw.StaticText()

    def bind_button(self, function: Callable[..., None]) -> None:
        self._button.on_click(function)

    def show_error(self, error: Exception) -> None:
        self._button.button_type = 'warning'
        self._status.value = f'Error: {error.args[0]}'

    def upload_success(self) -> None:
        self._status.value = 'Success!'
        self._button.button_type = 'success'
        time.sleep(0.5)

    @property
    def input_value(self):
        return self._input_widget.value

    def __panel__(self) -> pn.panel:
        return pn.Card(
            self._input_widget,
            pn.Row(self._button, align='center'),
            pn.Row(self._status, align='center'),
            collapsible=False,
            title='Upload Plate Reader Data',
        )
