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
        layout.insert(2, '**Labeled Atoms**')
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
        self._ile = pnw.CheckBoxGroup(
            options=['CG2', 'CD'], inline=True, value=['CG2'], align='end'
        )
        self._leu = pnw.CheckBoxGroup(
            options=['CD1', 'CD2'], inline=True, value=['CD1', 'CD2'], align='end'
        )
        self._val = pnw.CheckBoxGroup(
            options=['CG1', 'CG2'], inline=True, value=['CG1', 'CG2'], align='end'
        )
        self._ala = pnw.CheckBoxGroup(options=['CB'], inline=True, align='end')
        self._met = pnw.CheckBoxGroup(options=['CE'], inline=True, align='end')
        self._thr = pnw.CheckBoxGroup(options=['CG2'], inline=True, align='end')

    def __panel__(self):
        return pn.Column(
            pn.Row('**Ile:**', pn.Spacer(), self._ile),
            pn.Row('**Leu:**', pn.Spacer(), self._leu),
            pn.Row('**Val:**', pn.Spacer(), self._val),
            pn.Row('**Ala:**', pn.Spacer(), self._ala),
            pn.Row('**Met:**', pn.Spacer(), self._met),
            pn.Row('**Thr:**', pn.Spacer(), self._thr),
        )

    @property
    def value(self):
        values = {
            'ILE': self._ile.value,
            'LEU': self._leu.value,
            'VAL': self._val.value,
            'ALA': self._ala.value,
            'MET': self._met.value,
            'THR': self._thr.value,
        }
        return {key: value for key, value in values.items() if value}
