import panel as pn
import panel.widgets as pnw
import smoltools

from common.widgets.pdb_input import (
    PDBInputWidget,
    PDBLoaderBase,
    ConformationInputWidget,
    SubunitInputWidget,
)


class NmrPDBLoader(PDBLoaderBase):
    def __init__(self, input_widget: PDBInputWidget, about: str, **params):
        super().__init__(input_widget=input_widget, about=about, **params)

        labeling_schemes = smoltools.albatrosy.LABELING_SCHEMES
        self._labeling_scheme = pnw.Select(
            name='Methyl labeling scheme',
            options=labeling_schemes,
            value=labeling_schemes[0],
        )

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
