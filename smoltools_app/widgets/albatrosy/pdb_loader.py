from typing import Callable
import panel as pn
import panel.widgets as pnw
import smoltools

from widgets.components.pdb_input import PDBLoaderBase


class NmrPDBLoader(PDBLoaderBase):
    def __init__(self, upload_function: Callable[..., None], **params):
        super().__init__(upload_function=upload_function, **params)
        labelling_schemes = smoltools.albatrosy.LABELLING_SCHEMES
        self._labelling_scheme = pnw.Select(
            name='Methyl labeling scheme',
            options=labelling_schemes,
            value=labelling_schemes[0],
        )
        self._calculate_interchain_noes = pnw.Checkbox(
            name='Calculate interchain NOEs?'
        )

    @property
    def interchain_noe(self) -> bool:
        return self._calculate_interchain_noes.value

    @property
    def labelling_scheme(self) -> str:
        return self._labelling_scheme.value

    def __panel__(self) -> pn.panel:
        layout = super().__panel__()
        layout.insert(4, self._labelling_scheme)
        layout.insert(5, self._calculate_interchain_noes)
        return layout
