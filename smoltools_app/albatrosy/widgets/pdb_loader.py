import panel as pn
import panel.widgets as pnw
from panel.viewable import Viewer

from common.widgets.pdb_loader import (
    PDBInputWidget,
    PDBLoader,
    ConformationInputWidget,
    SubunitInputWidget,
)


def _nmr_pdb_loader(input_widget: PDBInputWidget, about: str) -> PDBLoader:
    return PDBLoader(
        input_widget=input_widget, options_widget=LabeledAtomSelector(), about=about
    )


def nmr_conformation_loader() -> PDBLoader:
    about = """
        Upload structures for two conformations of the same protein to estimate changes in NOEs.
        """
    return _nmr_pdb_loader(input_widget=ConformationInputWidget(), about=about)


def nmr_subunit_loader() -> PDBLoader:
    about = """
        Upload a structure of a dimer to estimate the intra- and inter-subunit pairwise NOEs.
        """
    return _nmr_pdb_loader(input_widget=SubunitInputWidget(), about=about)


class LabeledAtomSelector(Viewer):
    def __init__(self, **params):
        super().__init__(**params)
        self._ile = atom_checkbox(options=['CD', 'CG2'], default=['CD'])
        self._leu = atom_checkbox(options=['CD1', 'CD2'], default=['CD1', 'CD2'])
        self._val = atom_checkbox(options=['CG1', 'CG2'], default=['CG1', 'CG2'])
        self._ala = atom_checkbox(options=['CB'])
        self._met = atom_checkbox(options=['CE'])
        self._thr = atom_checkbox(options=['CG2'])

    def __panel__(self):
        return pn.Column(
            pn.Row('**Labeled atoms:**', height=30),
            checkbox_row('Ile:', self._ile),
            checkbox_row('Leu:', self._leu),
            checkbox_row('Val:', self._val),
            checkbox_row('Ala:', self._ala),
            checkbox_row('Met:', self._met),
            checkbox_row('Thr:', self._thr),
        )

    @property
    def value(self):
        ile_atoms = (
            self._ile.value + ['CD1'] if 'CD' in self._ile.value else self._ile.value
        )

        values = {
            'ILE': ile_atoms,
            'LEU': self._leu.value,
            'VAL': self._val.value,
            'ALA': self._ala.value,
            'MET': self._met.value,
            'THR': self._thr.value,
        }
        return {key: value for key, value in values.items() if value}


def atom_checkbox(options: list[str], default: list[str] = None) -> pnw.CheckBoxGroup:
    if default is None:
        default = []

    return pnw.CheckBoxGroup(
        options=options,
        inline=True,
        value=default,
        align='start',
        margin=(7, 0, 0, 5),
    )


def checkbox_row(title: str, checkbox_group: pnw.CheckBoxGroup) -> pn.Row:
    return pn.Row(title, checkbox_group, height=25)
