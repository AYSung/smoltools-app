from typing import Callable
import panel as pn

from widgets.components.pdb_input import PDBLoader


class FretPDBLoader(PDBLoader):
    def __init__(self, upload_function: Callable[..., None], **params):
        super().__init__(upload_function=upload_function, **params)

    @property
    def use_sasa(self) -> bool:
        raise NotImplementedError

    @property
    def sasa_cutoff(self) -> float:
        raise NotImplementedError

    def __panel__(self) -> pn.panel:
        return pn.Card(
            self._pdb_input_a,
            pn.Spacer(height=10),
            self._pdb_input_b,
            pn.Spacer(height=10),
            pn.Row(self._button, align='center'),
            pn.Row(self._status, align='center'),
            collapsible=False,
            title='Upload Structures',
        )
