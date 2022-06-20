from typing import Protocol
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


class Dashboard(Protocol):
    def load_pdb_files(self, chain_a, chain_b) -> None:
        ...

    def load_analyses(self) -> None:
        ...

    def show_analyses(self) -> None:
        ...


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


class PDBLoader(Viewer):
    def __init__(self, dashboard: Dashboard, **params):
        super().__init__(**params)
        self._pdb_input_a = PDBInputWidget('Conformation A')
        self._pbd_input_b = PDBInputWidget('Conformation B')

        self._button = pnw.Button(name='Upload', button_type='primary', width=150)
        self._button.on_click(self.upload_files)
        self._status = pnw.StaticText()

        self._dashboard = dashboard
        self._layout = pn.Card(
            self._pdb_input_a,
            pn.Spacer(height=10),
            self._pbd_input_b,
            pn.Spacer(height=10),
            pn.Row(self._button, align='center'),
            pn.Row(self._status, align='center'),
            collapsible=False,
            title='Upload Structures',
        )

    def upload_files(self, event=None):
        try:
            chain_a = self._pdb_input_a.chain
            chain_b = self._pbd_input_b.chain

            self._dashboard.load_pdb_files(chain_a, chain_b)
            self._dashboard.load_analyses()
        except (NoFileSelected, ChainNotFound) as e:
            self._button.button_type = 'warning'
            self._status.value = f'Error: {e.args[0]}'
            # TODO: error handling for empty residue list?
        else:
            self._status.value = 'Success!'
            self._button.button_type = 'success'
            time.sleep(0.5)
            self._dashboard.show_analyses()

    def __panel__(self) -> pn.panel:
        return self._layout
