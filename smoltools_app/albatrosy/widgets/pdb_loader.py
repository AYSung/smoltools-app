import panel as pn
import panel.widgets as pnw
from panel.viewable import Viewer

from common.widgets.pdb_input import (
    PDBInputWidget,
    PDBLoaderBase,
    ConformationInputWidget,
    SubunitInputWidget,
)


class NmrPDBLoader(PDBLoaderBase):
    def __init__(self, input_widget: PDBInputWidget, about: str, **params):
        super().__init__(input_widget=input_widget, about=about, **params)
        self._labeling_scheme = LabeledAtomSelector()

    @property
    def labeling_scheme(self) -> str:
        return self._labeling_scheme.value

    def __panel__(self) -> pn.panel:
        layout = super().__panel__()
        layout.insert(2, self._labeling_scheme)
        return layout


def nmr_conformation_loader() -> NmrPDBLoader:
    about = """
        Upload structures for two conformations of the same protein to estimate changes in NOEs.
        """
    return NmrPDBLoader(input_widget=ConformationInputWidget(), about=about)


def nmr_subunit_loader() -> NmrPDBLoader:
    about = """
        Upload a structure of a dimer to estimate the intra- and inter-subunit pairwise NOEs.
        """
    return NmrPDBLoader(input_widget=SubunitInputWidget(), about=about)


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
            pn.Row('Ile:', self._ile, height=25),
            pn.Row('Leu:', self._leu, height=25),
            pn.Row('Val:', self._val, height=25),
            pn.Row('Ala:', self._ala, height=25),
            pn.Row('Met:', self._met, height=25),
            pn.Row('Thr:', self._thr, height=25),
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


def atom_checkbox(options: list[str], default: list[str] = None):
    if default is None:
        default = []

    return pnw.CheckBoxGroup(
        options=options,
        inline=True,
        value=default,
        align='start',
        margin=(7, 0, 0, 5),
    )
