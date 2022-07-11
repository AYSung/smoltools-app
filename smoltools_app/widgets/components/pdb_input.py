from typing import Callable

import panel as pn
import panel.widgets as pnw
from panel.viewable import Viewer
from pathlib import Path
import string
import time

from Bio.PDB.Chain import Chain
from smoltools.pdbtools import load, select
from smoltools.pdbtools.exceptions import ChainNotFound


class NoFileSelected(Exception):
    def __init__(self, input_id: str):
        message = f'Please select pdb file for {input_id}'
        super().__init__(message)


def pdb_file_input() -> pnw.FileInput:
    return pnw.FileInput(accept='.pdb')


def model_input() -> pnw.IntInput:
    return pnw.IntInput(name='Model', value=0, start=0, step=1, width=60)


def chain_input(default: str = 'A') -> pnw.Select:
    return pnw.Select(
        name='Chain',
        options=[char for char in string.ascii_uppercase[:26]],
        value=default,
        width=60,
    )


class PDBInputWidget(Viewer):
    def __init__(self, widget_id: str, **params):
        super().__init__(**params)
        self.widget_id = widget_id
        self._pdb_file_input = pdb_file_input()
        self._model_input = model_input()
        self._chain_input = chain_input()

    def __panel__(self):
        return pn.Column(
            f'**{self.widget_id}:**',
            self._pdb_file_input,
            pn.Row(
                self._model_input,
                self._chain_input,
            ),
        )

    @property
    def values(self) -> dict:
        return {
            'widget_id': self.widget_id,
            'filename': self._pdb_file_input.filename,
            'byte_file': self._pdb_file_input.value,
            'model': self._model_input.value,
            'chain': self._chain_input.value,
        }


def load_pdb_file(
    widget_id: str, filename: str, byte_file: bytes, model: int, chain: str
) -> Chain:
    try:
        structure = load.read_pdb_from_bytes(filename, byte_file)
        return select.get_chain(structure, model, chain)
    except AttributeError:
        raise NoFileSelected(widget_id)
    except KeyError:
        structure_id = Path(filename).stem
        raise ChainNotFound(structure_id, model, chain)


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
        return load_pdb_file(**self._pdb_input_a.values)

    @property
    def chain_b(self) -> Chain:
        return load_pdb_file(**self._pdb_input_b.values)

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


class PDBLoaderBase2(Viewer):
    def __init__(self, upload_function: Callable[..., None], **params):
        super().__init__(**params)
        self._pdb_file_input = pdb_file_input()

        self._model_input_a = model_input()
        self._chain_input_a = chain_input()

        self._model_input_b = model_input()
        self._chain_input_b = chain_input(default='B')

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
        return load_pdb_file(
            widget_id='Structure A',
            filename=self._pdb_file_input.filename,
            byte_file=self._pdb_file_input.value,
            model=self._model_input_a.value,
            chain=self._chain_input_a.value,
        )

    @property
    def chain_b(self) -> Chain:
        return load_pdb_file(
            widget_id='Structure B',
            filename=self._pdb_file_input.filename,
            byte_file=self._pdb_file_input.value,
            model=self._model_input_b.value,
            chain=self._chain_input_b.value,
        )

    def __panel__(self) -> pn.panel:
        pdb_input_widget = pn.Column(
            '**Structure:**',
            self._pdb_file_input,
            pn.Spacer(height=10),
            pn.Row(
                'Subunit 1:',
                self._model_input_a,
                self._chain_input_a,
            ),
            pn.Row(
                'Subunit 2:',
                self._model_input_b,
                self._chain_input_b,
            ),
        )
        return pn.Card(
            pdb_input_widget,
            # pn.Spacer(height=10),
            pn.Row(self._button, align='center'),
            pn.Row(self._status, align='center'),
            collapsible=False,
            title='Upload Structures',
        )
