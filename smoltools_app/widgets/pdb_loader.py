import asyncio
from typing import Protocol
import pandas as pd
import panel as pn
import panel.widgets as pnw

from smoltools.pdbtools import load, select
from smoltools import fret0

from Bio.PDB.Structure import Structure


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
        return load.read_pdb_from_bytes(self.structure_id, self.value)


def load_pdb_files(structure_a, chain_id_a, structure_b, chain_id_b) -> pd.DataFrame:
    # TODO: allow choosing model number
    chain_a = select.get_chain(structure_a, model=0, chain=chain_id_a)
    chain_b = select.get_chain(structure_b, model=0, chain=chain_id_b)

    distances_a = fret0.chain_to_distances(chain_a)
    distances_b = fret0.chain_to_distances(chain_b)

    return fret0.pairwise_distance_between_conformations(distances_a, distances_b)


def make_widget(dashboard: Dashboard) -> pn.Column:
    async def upload_files(event=None):
        # TODO: better error messages (more specific to conformation)
        try:
            # TODO: abstraction layer here
            structure_a = pdb_uploader_a.value_as_pdb
            chain_id_a = chain_input_a.value
            structure_b = pdb_uploader_b.value_as_pdb
            chain_id_b = chain_input_b.value

            # TODO: allow choosing model number
            chain_a = select.get_chain(structure_a, model=0, chain=chain_id_a)
            chain_b = select.get_chain(structure_b, model=0, chain=chain_id_b)

            dashboard.load_pdb_files(chain_a, chain_b)
            dashboard.load_analyses()

            upload_button.button_type = 'success'
            widget[-1] = ''
            await asyncio.sleep(2)
            upload_button.button_type = 'primary'

        except AttributeError:
            upload_button.button_type = 'warning'
            widget[-1] = 'Must select pdb files for both conformations'
        except KeyError as e:
            upload_button.button_type = 'warning'
            widget[-1] = f'Chain {e} not found'

    pdb_uploader_a = PDBFileInput(structure_id='conformation_a')
    pdb_uploader_b = PDBFileInput(structure_id='conformation_b')

    chain_input_a = pnw.TextInput(name='Chain', value='A')
    chain_input_b = pnw.TextInput(name='Chain', value='A')

    upload_button = upload_button = pnw.Button(name='Upload', button_type='primary')
    upload_button.on_click(upload_files)

    error_messages = ''

    widget = pn.Column(
        pn.Column(
            '#### Conformation A:',
            pdb_uploader_a,
            chain_input_a,
        ),
        pn.Column(
            '#### Conformation B:',
            pdb_uploader_b,
            chain_input_b,
        ),
        pn.Row(upload_button, align='center'),
        error_messages,
        sizing_mode='stretch_both',
    )
    return widget
