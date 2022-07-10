from typing import Callable
import panel as pn
import panel.widgets as pnw

from widgets.components.pdb_input import PDBLoader


class PDBLoader(PDBLoader):
    def __init__(self, upload_function: Callable[..., None], **params):
        super().__init__(upload_function=upload_function, **params)
        self._calculate_interchain_noes = pnw.Checkbox(
            name='Calculate interchain NOEs?'
        )

    @property
    def interchain_noe(self) -> bool:
        return self._calculate_interchain_noes.value

    def __panel__(self) -> pn.panel:
        layout = super().__panel__()
        layout.insert(4, self._calculate_interchain_noes)
        return layout
