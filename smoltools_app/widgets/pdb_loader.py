import asyncio
from typing import Protocol
import panel as pn
import panel.widgets as pnw
from panel.viewable import Viewer
import string

from smoltools.pdbtools import load, select

from Bio.PDB.Structure import Structure
from Bio.PDB.Chain import Chain


class NoFileSelected(Exception):
    def __init__(self, input_id: str):
        self.input_id = input_id


class ChainNotFound(Exception):
    def __init__(self, input_id, model_id, chain_id):
        self.input_id = input_id
        self.model_id = model_id
        self.chain_id = chain_id


class Dashboard(Protocol):
    def load_pdb_files(self, chain_a, chain_b) -> None:
        ...

    def load_analyses(self) -> None:
        ...


class PDBFileInput(pnw.FileInput):
    def __init__(self, structure_id: str, **params):
        super().__init__(accept='.pdb', **params)
        self.structure_id = structure_id

    @property
    def value_as_pdb(self) -> Structure:
        if self.value is None:
            raise NoFileSelected(self.structure_id)
        else:
            return load.read_pdb_from_bytes(self.structure_id, self.value)


class PDBInputWidget(Viewer):
    def __init__(self, structure_id: str, **params):
        self.structure_id = structure_id
        super().__init__(**params)
        self._pdb_file_input = PDBFileInput(structure_id)
        self._model_input = pnw.IntInput(name='Model', value=0, width=60)
        self._chain_input = pnw.Select(
            name='Chain',
            options=[char for char in string.ascii_uppercase[:26]],
            value='A',
            width=60,
        )
        self._layout = pn.Column(
            f'#### {self.structure_id}:',
            self._pdb_file_input,
            pn.Row(
                self._model_input,
                self._chain_input,
            ),
        )

    def __panel__(self):
        return self._layout

    @property
    def chain(self) -> Chain:
        structure = self._pdb_file_input.value_as_pdb

        model = self._model_input.value
        chain_id = self._chain_input.value

        try:
            return select.get_chain(structure, model, chain_id)
        except KeyError:
            raise ChainNotFound(self.structure_id, model, chain_id)


def make_widget(dashboard: Dashboard) -> pn.Column:
    async def upload_files(event=None):
        try:
            chain_a = conformation_a_widget.chain
            chain_b = conformation_b_widget.chain

            dashboard.load_pdb_files(chain_a, chain_b)
            dashboard.load_analyses()
        except ChainNotFound as e:
            upload_button.button_type = 'warning'
            status.value = f'Chain {e.model_id}/{e.chain_id} not found for {e.input_id}'
        except NoFileSelected as e:
            upload_button.button_type = 'warning'
            status.value = f'Must select pdb file for {e.input_id}'
        else:
            status.value = 'Success!'
            upload_button.button_type = 'success'
            await asyncio.sleep(3)
            status.value = ''
            upload_button.button_type = 'primary'

    conformation_a_widget = PDBInputWidget('Conformation A')
    conformation_b_widget = PDBInputWidget('Conformation B')

    upload_button = upload_button = pnw.Button(
        name='Upload', button_type='primary', width=150
    )
    upload_button.on_click(upload_files)

    status = pnw.StaticText(value='')

    widget = pn.Column(
        conformation_a_widget,
        pn.Spacer(height=10),
        conformation_b_widget,
        pn.Spacer(height=30),
        upload_button,
        status,
        loading_indicator=True,
    )
    return widget
