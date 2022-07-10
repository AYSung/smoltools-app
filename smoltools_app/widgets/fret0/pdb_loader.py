from typing import Callable
import panel as pn
import panel.widgets as pnw

from widgets.components.pdb_input import PDBLoaderBase


class FretPDBLoader(PDBLoaderBase):
    def __init__(self, upload_function: Callable[..., None], **params):
        super().__init__(upload_function=upload_function, **params)
        self._use_sasa = pnw.Checkbox(name='SASA loaded as b-factor?')

    @property
    def use_sasa(self) -> bool:
        return self._use_sasa.value

    def __panel__(self) -> pn.panel:
        layout = super().__panel__()
        layout.insert(4, self._use_sasa)
        return layout
