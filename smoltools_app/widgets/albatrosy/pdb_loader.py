from typing import Callable
import panel as pn
import panel.widgets as pnw
import smoltools

from widgets.components.pdb_input import PDBLoaderBase, PDBLoaderBase2


class NmrPDBLoader(PDBLoaderBase):
    def __init__(self, upload_function: Callable[..., None], **params):
        super().__init__(upload_function=upload_function, **params)
        labeling_schemes = smoltools.albatrosy.LABELING_SCHEMES
        self._labeling_scheme = pnw.Select(
            name='Methyl labeling scheme',
            options=labeling_schemes,
            value=labeling_schemes[0],
        )
        self._calculate_interchain_noes = pnw.Checkbox(name='Calculate interchain NOEs')

    @property
    def interchain_noe(self) -> bool:
        return self._calculate_interchain_noes.value

    @property
    def labeling_scheme(self) -> str:
        return self._labeling_scheme.value

    def __panel__(self) -> pn.panel:
        layout = super().__panel__()
        layout.insert(4, self._labeling_scheme)
        return layout


class NmrPDBLoader2(PDBLoaderBase2):
    def __init__(self, upload_function: Callable[..., None], **params):
        super().__init__(upload_function=upload_function, **params)
        labeling_schemes = smoltools.albatrosy.LABELING_SCHEMES
        self._labeling_scheme = pnw.Select(
            name='Methyl labeling scheme',
            options=labeling_schemes,
            value=labeling_schemes[0],
        )
        self._calculate_interchain_noes = pnw.Checkbox(name='Calculate interchain NOEs')

    @property
    def interchain_noe(self) -> bool:
        return self._calculate_interchain_noes.value

    @property
    def labeling_scheme(self) -> str:
        return self._labeling_scheme.value

    def __panel__(self) -> pn.panel:
        layout = super().__panel__()
        layout.insert(1, self._labeling_scheme)
        return layout
