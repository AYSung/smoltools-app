import panel as pn
import panel.widgets as pnw

from widgets.components.pdb_input import PDBLoaderBase, ConformationInputWidget


class FretPDBLoader(PDBLoaderBase):
    def __init__(self, about: str, **params):
        super().__init__(input_widget=ConformationInputWidget(), about=about, **params)
        self._use_sasa = pnw.Checkbox(name='SASA loaded as b-factor')

    @property
    def use_sasa(self) -> bool:
        return self._use_sasa.value

    def __panel__(self) -> pn.panel:
        layout = super().__panel__()
        layout.insert(2, self._use_sasa)
        return layout


def fret_pdb_loader() -> FretPDBLoader:
    about = """
        Upload structures for two conformations of the same protein to estimate changes in FRET efficiency.
        """
    return FretPDBLoader(about=about)
