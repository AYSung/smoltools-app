from typing import Callable
import panel as pn

from widgets.components.pdb_input import PDBLoaderBase


class FretPDBLoader(PDBLoaderBase):
    def __init__(self, upload_function: Callable[..., None], **params):
        super().__init__(upload_function=upload_function, **params)

    @property
    def use_sasa(self) -> bool:
        raise NotImplementedError

    @property
    def sasa_cutoff(self) -> float:
        raise NotImplementedError

    def __panel__(self) -> pn.panel:
        layout = super().__panel__()
        # layout.insert(4, self._calculate_interchain_noes)
        return layout
