from typing import Callable

import panel as pn
import panel.widgets as pnw
from panel.viewable import Viewer
from pathlib import Path
import string
import time

from Bio.PDB.Structure import Structure
from Bio.PDB.Chain import Chain

from smoltools.pdbtools import load, select
from smoltools.pdbtools.exceptions import ChainNotFound


class NoFileSelected(Exception):
    def __init__(self, input_id: str):
        message = f'Please select pdb file for {input_id}'
        super().__init__(message)


class PDBInputWidget(Viewer):
    def __init__(self, widget_id: str, **params):
        self.widget_id = widget_id
        super().__init__(**params)
        self._pdb_file_input = pnw.FileInput(accept='.pdb')
        self._model_input = pnw.IntInput(name='Model', value=0, width=60)
        self._chain_input = pnw.Select(
            name='Chain',
            options=[char for char in string.ascii_uppercase[:26]],
            value='A',
            width=60,
        )
        self._layout = pn.Column(
            f'**{self.widget_id}:**',
            self._pdb_file_input,
            pn.Row(
                self._model_input,
                self._chain_input,
            ),
        )

    def __panel__(self):
        return self._layout

    @property
    def pdb_structure(self) -> Structure:
        try:
            return load.read_pdb_from_bytes(
                self._pdb_file_input.filename, self._pdb_file_input.value
            )
        except AttributeError:
            raise NoFileSelected(self.widget_id)

    @property
    def chain(self) -> Chain:
        structure = self.pdb_structure

        model = self._model_input.value
        chain_id = self._chain_input.value

        try:
            return select.get_chain(structure, model, chain_id)
        except KeyError:
            structure_id = Path(self._pdb_file_input.filename).stem
            raise ChainNotFound(structure_id, model, chain_id)


class PDBLoaderBase(Viewer):
    def __init__(self, upload_function: Callable[..., None], **params):
        super().__init__(**params)
        self._pdb_input_a = PDBInputWidget('Structure A')
        self._pdb_input_b = PDBInputWidget('Structure B')

        self._button = pnw.Button(name='Upload', button_type='primary', width=150)
        self._button.on_click(upload_function)

        self._status = pnw.StaticText()

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

    def __panel__(self) -> pn.panel:
        return pn.Card(
            self._pdb_input_a,
            pn.Spacer(height=10),
            self._pdb_input_b,
            pn.Spacer(height=10),
            pn.Row(self._button, align='center'),
            pn.Row(self._status, align='center'),
            collapsible=False,
            title='Upload Structures',
        )
