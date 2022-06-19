import asyncio
from typing import Protocol
import panel as pn
import panel.widgets as pnw
from panel.viewable import Viewer
from pathlib import Path
import string

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


def make_widget(dashboard: Dashboard) -> pn.Column:
    async def upload_files(event=None):
        try:
            chain_a = conformation_a_widget.chain
            chain_b = conformation_b_widget.chain

            dashboard.load_pdb_files(chain_a, chain_b)
            dashboard.load_analyses()
        except (NoFileSelected, ChainNotFound) as e:
            upload_button.button_type = 'warning'
            status.value = f'Error: {e.args[0]}'
            # TODO: error handling for empty residue list?
        else:
            status.value = 'Success!'
            upload_button.button_type = 'success'
            await asyncio.sleep(1)
            dashboard.show_analyses()

    conformation_a_widget = PDBInputWidget('Conformation A')
    conformation_b_widget = PDBInputWidget('Conformation B')

    upload_button = upload_button = pnw.Button(
        name='Upload', button_type='primary', width=150
    )
    upload_button.on_click(upload_files)

    status = pnw.StaticText()

    return pn.Card(
        conformation_a_widget,
        pn.Spacer(height=10),
        conformation_b_widget,
        pn.Spacer(height=10),
        pn.Row(upload_button, align='center'),
        pn.Row(status, align='center'),
        collapsible=False,
        title='Upload Structures',
    )
