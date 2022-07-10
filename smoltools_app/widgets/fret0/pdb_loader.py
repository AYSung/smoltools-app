from typing import Callable
import panel as pn
import panel.widgets as pnw
from panel.viewable import Viewer
import time

from Bio.PDB.Chain import Chain

from widgets.components.pdb_input import PDBInputWidget


class PDBLoader(Viewer):
    def __init__(self, upload_function: Callable[..., None], **params):
        super().__init__(**params)
        self._pdb_input_a = PDBInputWidget('Conformation A')
        self._pdb_input_b = PDBInputWidget('Conformation B')

        self._button = pnw.Button(name='Upload', button_type='primary', width=150)
        self._button.on_click(upload_function)  # link to function in dashboard.
        self._status = pnw.StaticText()

        self._layout = pn.Card(
            self._pdb_input_a,
            pn.Spacer(height=10),
            self._pdb_input_b,
            pn.Spacer(height=10),
            pn.Row(self._button, align='center'),
            pn.Row(self._status, align='center'),
            collapsible=False,
            title='Upload Structures',
        )

    def __panel__(self) -> pn.panel:
        return self._layout

    def show_error(self, error: Exception) -> None:
        self._button.button_type = 'warning'
        self._status.value = f'Error: {error.args[0]}'

    def upload_success(self) -> None:
        self._status.value = 'Success!'
        self._button.button_type = 'success'
        time.sleep(0.5)

    @property
    def chain_a(self) -> Chain:
        return self._pdb_input_a.chain

    @property
    def chain_b(self) -> Chain:
        return self._pdb_input_b.chain

    @property
    def use_sasa(self) -> bool:
        raise NotImplementedError
