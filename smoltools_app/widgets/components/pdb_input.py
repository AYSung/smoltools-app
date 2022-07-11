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
    def __panel__(self) -> pn.Column():
        ...

    def chain_a(self) -> Chain:
        ...

    def chain_b(self) -> Chain:
        ...


class ConformationInputWidget(PDBInputWidget):
    def __init__(self, **params):
        super().__init__(**params)
        self._pdb_file_input_a = pdb_file_input()
        self._model_input_a = model_input()
        self._chain_input_a = chain_input()

        self._pdb_file_input_b = pdb_file_input()
        self._model_input_b = model_input()
        self._chain_input_b = chain_input()

    def __panel__(self) -> pn.Column:
        return pn.Column(
            '**Conformation A:**',
            self._pdb_file_input_a,
            pn.Row(
                self._model_input_a,
                self._chain_input_a,
            ),
            pn.Spacer(height=10),
            '**Conformation B:**',
            self._pdb_file_input_b,
            pn.Row(
                self._model_input_b,
                self._chain_input_b,
            ),
        )

    @property
    def chain_a(self) -> Chain:
        return load_pdb_file(
            widget_id='Conformation A',
            filename=self._pdb_file_input_a.filename,
            byte_file=self._pdb_file_input_a.value,
            model=self._model_input_a.value,
            chain=self._chain_input_a.value,
        )

    @property
    def chain_b(self) -> Chain:
        return load_pdb_file(
            widget_id='Conformation B',
            filename=self._pdb_file_input_b.filename,
            byte_file=self._pdb_file_input_b.value,
            model=self._model_input_b.value,
            chain=self._chain_input_b.value,
        )


class SubunitInputWidget(PDBInputWidget):
    def __init__(self, **params):
        super().__init__(**params)
        self._pdb_file_input = pdb_file_input()
        self._model_input_a = model_input()
        self._chain_input_a = chain_input(default='A')

        self._model_input_b = model_input()
        self._chain_input_b = chain_input(default='B')

    def __panel__(self) -> pn.Column:
        return pn.Column(
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

    @property
    def chain_a(self) -> Chain:
        return load_pdb_file(
            widget_id='the structure',
            filename=self._pdb_file_input.filename,
            byte_file=self._pdb_file_input.value,
            model=self._model_input_a.value,
            chain=self._chain_input_a.value,
        )

    @property
    def chain_b(self) -> Chain:
        return load_pdb_file(
            widget_id='the structure',
            filename=self._pdb_file_input.filename,
            byte_file=self._pdb_file_input.value,
            model=self._model_input_b.value,
            chain=self._chain_input_b.value,
        )


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
    def __init__(
        self,
        input_widget: PDBInputWidget,
        upload_function: Callable[..., None],
        about: str,
        **params,
    ):
        super().__init__(**params)
        self._about = about
        self._input_widget = input_widget

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
        return self._input_widget.chain_a

    @property
    def chain_b(self) -> Chain:
        return self._input_widget.chain_b

    def __panel__(self) -> pn.panel:
        return pn.Card(
            self._about,
            self._input_widget,
            pn.Row(self._button, align='center'),
            pn.Row(self._status, align='center'),
            collapsible=False,
            title='Upload Structures',
        )
