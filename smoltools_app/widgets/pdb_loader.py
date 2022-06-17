from typing import Protocol
import panel as pn
import panel.widgets as pnw

from utils import colors
import fret0
from Bio.PDB.Structure import Structure


class Dashboard(Protocol):
    def load_pdb_files(self, structure_a, chain_a, structure_b, chain_b) -> None:
        ...


class PDBFileInput(pnw.FileInput):
    def __init__(self, structure_id: str, **params):
        super().__init__(accept='.pdb', **params)
        self.structure_id = structure_id

    @property
    def value_as_pdb(self) -> Structure:
        return fret0.read_pdb_from_bytes(self.structure_id, self.value)


def make_widget(dashboard: Dashboard) -> pn.Column:
    def upload_files(event=None):
        if pdb_uploader_a.value is None or pdb_uploader_b.value is None:
            upload_button.button_type = 'warning'
            return

        dashboard.load_pdb_files(
            pdb_uploader_a.value_as_pdb,
            chain_input_a.value,
            pdb_uploader_b.value_as_pdb,
            chain_input_b.value,
        )

        upload_button.button_type = 'success'
        widget.collapsed = True
        widget.header_background = colors.GREEN

    pdb_uploader_a = PDBFileInput(structure_id='conformation_a')
    pdb_uploader_b = PDBFileInput(structure_id='conformation_b')

    chain_input_a = pnw.TextInput(name='Chain', value='A')
    chain_input_b = pnw.TextInput(name='Chain', value='A')

    upload_button = upload_button = pnw.Button(name='Upload', button_type='primary')
    upload_button.on_click(upload_files)

    widget = pn.Column(
        pn.Column(
            pn.pane.Markdown('#### Conformation A:'),
            pdb_uploader_a,
            chain_input_a,
        ),
        pn.Column(
            pn.pane.Markdown('#### Conformation B:'),
            pdb_uploader_b,
            chain_input_b,
        ),
        pn.Row(upload_button, align='center'),
        sizing_mode='stretch_both',
    )
    return widget
